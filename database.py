import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'YOUR_MYSQL_PASSWORD',  # Change this
            'database': 'talent_screen360',
            'buffered': True
        }
    
    def get_connection(self):
        return mysql.connector.connect(**self.config)
    
    # ==================== LOGIN OPERATIONS ====================
    
    def check_username_exists(self, username):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    
    def create_login(self, username, password, usertype):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO login (username, password, usertype) VALUES (%s, %s, %s)",
            (username, password, usertype)
        )
        conn.commit()
        login_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return login_id
    
    def verify_login(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM login WHERE username = %s AND password = %s",
            (username, password)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, login_id, first_name, last_name, place, email, phone):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO user (login_id, first_name, last_name, place, email, phone) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (login_id, first_name, last_name, place, email, phone)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_user_by_login_id(self, login_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE login_id = %s", (login_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    def check_user_applied(self, user_id, job_id):
        """Check if user has already applied for this job"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM applications WHERE user_id = %s AND job_id = %s",
            (user_id, job_id)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    
    # ==================== COMPANY OPERATIONS ====================
    
    def create_company(self, login_id, company_name, place, phone, email, est_year):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO company (login_id, company_name, place, phone, email, est_year) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (login_id, company_name, place, phone, email, est_year)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_company_by_login_id(self, login_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM company WHERE login_id = %s", (login_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    def get_company_by_id(self, company_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM company WHERE company_id = %s", (company_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    def get_all_companies(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM company")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    # ==================== JOB OPERATIONS ====================
    
    def create_job(self, company_id, title, qualification, details, last_date, requirements):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO jobs (company_id, title, qualification, details, last_date, requirements) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (company_id, title, qualification, details, last_date, requirements)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_company_jobs(self, company_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs WHERE company_id = %s ORDER BY job_id DESC", (company_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def get_job_by_id(self, job_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    # ==================== APPLICATION OPERATIONS ====================
    
    def create_application(self, user_id, job_id, resume_path, mark):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO applications (user_id, job_id, date, resume_path, mark, status) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, job_id, datetime.now().date(), resume_path, str(mark), 'pending')
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_user_applications(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT a.*, j.title, j.qualification, c.company_name 
               FROM applications a 
               JOIN jobs j ON a.job_id = j.job_id 
               JOIN company c ON j.company_id = c.company_id 
               WHERE a.user_id = %s 
               ORDER BY a.application_id DESC""",
            (user_id,)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def get_company_applications(self, company_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT a.*, j.title, u.first_name, u.last_name, u.email, u.phone 
               FROM applications a 
               JOIN jobs j ON a.job_id = j.job_id 
               JOIN user u ON a.user_id = u.user_id 
               WHERE j.company_id = %s 
               ORDER BY a.application_id DESC""",
            (company_id,)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def get_all_applications_sorted(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT a.*, j.title, u.first_name, u.last_name, u.email, c.company_name 
               FROM applications a 
               JOIN jobs j ON a.job_id = j.job_id 
               JOIN user u ON a.user_id = u.user_id 
               JOIN company c ON j.company_id = c.company_id 
               ORDER BY CAST(a.mark AS UNSIGNED) DESC"""
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def get_applications_grouped_by_company_job(self):
        """
        Returns a 3-level nested structure:
        {
            'Company A': {
                'Job Title 1': [app1, app2, app3],  # sorted by mark
                'Job Title 2': [app4, app5]
            },
            'Company B': {
                'Job Title 3': [app6, app7]
            }
        }
        """
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT 
                   a.*, 
                   j.title as job_title, 
                   j.company_id,
                   u.first_name, 
                   u.last_name, 
                   u.email, 
                   u.phone,
                   c.company_name 
               FROM applications a 
               JOIN jobs j ON a.job_id = j.job_id 
               JOIN user u ON a.user_id = u.user_id 
               JOIN company c ON j.company_id = c.company_id 
               ORDER BY c.company_name, j.title, CAST(a.mark AS UNSIGNED) DESC"""
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Build the 3-level nested structure
        grouped = {}
        for app in results:
            company_name = app['company_name']
            job_title = app['job_title']
            
            # Create company level if doesn't exist
            if company_name not in grouped:
                grouped[company_name] = {}
            
            # Create job level if doesn't exist
            if job_title not in grouped[company_name]:
                grouped[company_name][job_title] = []
            
            # Add application to the list
            grouped[company_name][job_title].append(app)
        
        return grouped
    
    # ==================== COMPLAINT OPERATIONS ====================
    
    def create_complaint(self, user_id, complaint):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO complaints (user_id, complaint, date) 
               VALUES (%s, %s, %s)""",
            (user_id, complaint, datetime.now().date())
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_user_complaints(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM complaints WHERE user_id = %s ORDER BY complaint_id DESC",
            (user_id,)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def get_all_complaints(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT c.*, u.first_name, u.last_name, u.email 
               FROM complaints c 
               JOIN user u ON c.user_id = u.user_id 
               ORDER BY c.complaint_id DESC"""
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def update_complaint_reply(self, complaint_id, reply):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE complaints SET reply = %s WHERE complaint_id = %s",
            (reply, complaint_id)
        )
        conn.commit()
        cursor.close()
        conn.close()