import PyPDF2
import re
from datetime import datetime

class ResumeParser:
    def __init__(self):
        # Common skill variations and synonyms
        self.skill_synonyms = {
            'python': ['python', 'py', 'python3'],
            'javascript': ['javascript', 'js', 'node.js', 'nodejs', 'react', 'vue', 'angular'],
            'java': ['java', 'j2ee', 'spring', 'hibernate'],
            'sql': ['sql', 'mysql', 'postgresql', 'oracle', 'database', 'db'],
            'machine learning': ['machine learning', 'ml', 'deep learning', 'neural network', 'ai', 'artificial intelligence'],
            'project management': ['project management', 'agile', 'scrum', 'kanban', 'pmp'],
            'leadership': ['leadership', 'team lead', 'manager', 'supervisor', 'director'],
            'communication': ['communication', 'presentation', 'public speaking', 'collaboration'],
        }
        
        # Action verbs that indicate strong experience
        self.strong_action_verbs = [
            'achieved', 'improved', 'increased', 'decreased', 'reduced', 'optimized',
            'developed', 'created', 'built', 'designed', 'implemented', 'launched',
            'led', 'managed', 'directed', 'spearheaded', 'coordinated',
            'analyzed', 'researched', 'evaluated', 'assessed',
            'automated', 'streamlined', 'enhanced', 'transformed'
        ]
        
        # Quantifiable achievement indicators
        self.quantifiers = [
            r'\d+%', r'\$\d+', r'\d+[kmb]', r'\d+x', r'\d+ percent',
            r'increased by \d+', r'reduced by \d+', r'saved \d+',
            r'\d+ projects', r'\d+ team', r'\d+ clients', r'\d+ users'
        ]
    
    def extract_text(self, pdf_path):
        """Extract text from PDF resume"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def extract_sections(self, resume_text):
        """Identify and extract resume sections"""
        text_lower = resume_text.lower()
        sections = {
            'education': False,
            'experience': False,
            'skills': False,
            'projects': False,
            'certifications': False
        }
        
        # Check for standard section headers
        if any(header in text_lower for header in ['education', 'academic', 'degree']):
            sections['education'] = True
        if any(header in text_lower for header in ['experience', 'employment', 'work history']):
            sections['experience'] = True
        if any(header in text_lower for header in ['skills', 'technical skills', 'competencies']):
            sections['skills'] = True
        if any(header in text_lower for header in ['projects', 'portfolio']):
            sections['projects'] = True
        if any(header in text_lower for header in ['certification', 'licenses', 'accreditation']):
            sections['certifications'] = True
        
        return sections
    
    def extract_contact_info(self, resume_text):
        """Extract and validate contact information"""
        score = 0
        
        # Email detection (stricter pattern)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, resume_text)
        if emails:
            score += 3
        
        # Phone detection (various formats)
        phone_patterns = [
            r'\b\d{10}\b',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
            r'\+\d{1,3}[-.\s]?\d{10,14}\b'
        ]
        has_phone = any(re.search(pattern, resume_text) for pattern in phone_patterns)
        if has_phone:
            score += 2
        
        # LinkedIn profile
        if 'linkedin.com' in resume_text.lower():
            score += 2
        
        # Location/Address
        if any(indicator in resume_text.lower() for indicator in [', india', ', usa', ', uk', 'city,', 'state']):
            score += 1
        
        return min(score, 8)  # Max 8 points
    
    def analyze_experience_quality(self, resume_text):
        """Analyze quality and depth of experience descriptions"""
        text_lower = resume_text.lower()
        score = 0
        
        # Count strong action verbs
        action_verb_count = sum(1 for verb in self.strong_action_verbs if verb in text_lower)
        score += min(action_verb_count * 2, 12)  # Max 12 points
        
        # Check for quantifiable achievements
        quantifiable_count = sum(1 for pattern in self.quantifiers 
                                if re.search(pattern, text_lower))
        score += min(quantifiable_count * 3, 15)  # Max 15 points
        
        # Check for years of experience mentioned
        year_patterns = [r'\d+ years?', r'\d+\+ years?', r'\d{4}\s*-\s*\d{4}', r'\d{4}\s*-\s*present']
        if any(re.search(pattern, text_lower) for pattern in year_patterns):
            score += 5
        
        return min(score, 32)  # Max 32 points for experience quality
    
    def match_qualification(self, resume_text, required_qualification):
        """Advanced qualification matching with context"""
        text_lower = resume_text.lower()
        qual_lower = required_qualification.lower()
        score = 0
        
        # Direct match
        if qual_lower in text_lower:
            score = 15
        else:
            # Check for partial matches and related terms
            qual_words = qual_lower.split()
            significant_words = [w for w in qual_words if len(w) > 3 and w not in ['and', 'the', 'with', 'from']]
            
            matches = sum(1 for word in significant_words if word in text_lower)
            if significant_words:
                match_percentage = matches / len(significant_words)
                score = int(match_percentage * 15)
            
            # Bonus for degree-related keywords
            degree_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma', 'certification']
            if any(keyword in text_lower for keyword in degree_keywords):
                score += 3
        
        return min(score, 18)  # Max 18 points
    
    def match_skills_advanced(self, resume_text, requirements):
        """Advanced skill matching with synonyms and context"""
        text_lower = resume_text.lower()
        
        if not requirements:
            return 15  # Default if no requirements specified
        
        required_skills = [req.strip().lower() for req in requirements.split(',')]
        matched_skills = 0
        total_weight = 0
        
        for skill in required_skills:
            # Get synonyms for this skill
            synonyms = [skill]
            for key, syn_list in self.skill_synonyms.items():
                if skill in syn_list or skill == key:
                    synonyms = syn_list
                    break
            
            # Check if any synonym is found
            skill_found = any(syn in text_lower for syn in synonyms)
            
            # Weight skills based on specificity (longer = more specific = higher weight)
            weight = len(skill.split())
            total_weight += weight
            
            if skill_found:
                matched_skills += weight
        
        if total_weight > 0:
            match_score = (matched_skills / total_weight) * 30
        else:
            match_score = 15
        
        return min(int(match_score), 30)  # Max 30 points
    
    def analyze_formatting_quality(self, resume_text):
        """Analyze resume formatting and structure"""
        score = 0
        
        # Check for proper sections
        sections = self.extract_sections(resume_text)
        section_count = sum(sections.values())
        score += min(section_count * 2, 8)  # Max 8 points
        
        # Check resume length (not too short, not too long)
        word_count = len(resume_text.split())
        if 300 <= word_count <= 1000:
            score += 4
        elif 200 <= word_count <= 1500:
            score += 2
        
        return score  # Max 12 points
    
    def calculate_score(self, resume_text, job):
        """
        Calculate comprehensive resume score based on multiple factors
        Total: 100 points
        """
        text_lower = resume_text.lower()
        
        if not text_lower or len(text_lower) < 50:
            return 0
        
        score = 0
        
        # 1. Qualification Match (18 points)
        qual_score = self.match_qualification(resume_text, job.get('qualification', ''))
        score += qual_score
        
        # 2. Skills & Requirements Match (30 points)
        skills_score = self.match_skills_advanced(resume_text, job.get('requirements', ''))
        score += skills_score
        
        # 3. Experience Quality & Achievements (32 points)
        exp_score = self.analyze_experience_quality(resume_text)
        score += exp_score
        
        # 4. Contact Information (8 points)
        contact_score = self.extract_contact_info(resume_text)
        score += contact_score
        
        # 5. Formatting & Structure (12 points)
        format_score = self.analyze_formatting_quality(resume_text)
        score += format_score
        
        # Apply penalty for keyword stuffing (repetition of same skill >5 times)
        if job.get('requirements'):
            for skill in job['requirements'].split(',')[:3]:  # Check top 3 skills
                skill = skill.strip().lower()
                count = text_lower.count(skill)
                if count > 8:
                    score -= 5  # Penalty for obvious keyword stuffing
        
        return max(0, min(score, 100))  # Ensure score is between 0-100