from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from database import Database
from resume_parser import ResumeParser

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads/resumes'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = Database()
resume_parser = ResumeParser()

# ==================== HOME & AUTH ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        place = request.form['place']
        email = request.form['email']
        phone = request.form['phone']
        
        # Check if username exists
        if db.check_username_exists(username):
            flash('Username already exists', 'error')
            return redirect(url_for('register_user'))
        
        # Create login entry
        login_id = db.create_login(username, password, 'user')
        
        # Create user entry
        db.create_user(login_id, first_name, last_name, place, email, phone)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register_user.html')

@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        company_name = request.form['company_name']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        est_year = request.form['est_year']
        
        # Check if username exists
        if db.check_username_exists(username):
            flash('Username already exists', 'error')
            return redirect(url_for('register_company'))
        
        # Create login entry
        login_id = db.create_login(username, password, 'company')
        
        # Create company entry
        db.create_company(login_id, company_name, place, phone, email, est_year)
        
        flash('Company registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register_company.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_data = db.verify_login(username, password)
        
        if user_data:
            session['login_id'] = user_data['login_id']
            session['username'] = user_data['username']
            session['usertype'] = user_data['usertype']
            
            if user_data['usertype'] == 'admin':
                return redirect(url_for('admin_home'))
            elif user_data['usertype'] == 'company':
                company = db.get_company_by_login_id(user_data['login_id'])
                session['company_id'] = company['company_id']
                session['company_name'] = company['company_name']
                return redirect(url_for('company_home'))
            elif user_data['usertype'] == 'user':
                user = db.get_user_by_login_id(user_data['login_id'])
                session['user_id'] = user['user_id']
                session['user_name'] = f"{user['first_name']} {user['last_name']}"
                return redirect(url_for('user_home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# ==================== COMPANY ROUTES ====================

@app.route('/company_home')
def company_home():
    if 'usertype' not in session or session['usertype'] != 'company':
        return redirect(url_for('login'))
    return render_template('company/company_home.html')

@app.route('/upload_job', methods=['GET', 'POST'])
def upload_job():
    if 'usertype' not in session or session['usertype'] != 'company':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        qualification = request.form['qualification']
        details = request.form['details']
        last_date = request.form['last_date']
        requirements = request.form['requirements']
        
        db.create_job(session['company_id'], title, qualification, 
                     details, last_date, requirements)
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('upload_job'))
    
    return render_template('company/upload_job.html')

@app.route('/view_application')
def view_application():
    if 'usertype' not in session or session['usertype'] != 'company':
        return redirect(url_for('login'))
    
    sorted_applications = db.get_company_applications(session['company_id'])
    sorted_applications = sorted(sorted_applications, key=lambda x: x['mark'], reverse=True)

    # now group by job_id
    grouped_applications = {}
    for app in sorted_applications:
        job_id = app['job_id'] 
        if job_id not in grouped_applications:
            grouped_applications[job_id] = []
        grouped_applications[job_id].append(app)

    return render_template('company/view_application.html', grouped_applications=grouped_applications)

# ==================== USER ROUTES ====================

@app.route('/user_home')
def user_home():
    if 'usertype' not in session or session['usertype'] != 'user':
        return redirect(url_for('login'))
    return render_template('user/user_home.html')

@app.route('/view_companies')
def view_companies():
    if 'usertype' not in session or session['usertype'] != 'user':
        return redirect(url_for('login'))
    
    companies = db.get_all_companies()
    return render_template('user/view_companies.html', companies=companies)

@app.route('/view_jobs/<int:company_id>')
def view_jobs(company_id):
    if 'usertype' not in session or session['usertype'] != 'user':
        return redirect(url_for('login'))
    
    jobs = db.get_company_jobs(company_id)
    company = db.get_company_by_id(company_id)
    return render_template('user/view_jobs.html', jobs=jobs, company=company)

@app.route('/apply_job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'usertype' not in session or session['usertype'] != 'user':
        return redirect(url_for('login'))
    
    if 'resume' not in request.files:
        flash('No resume uploaded', 'error')
        return redirect(request.referrer)
    
    if db.check_user_applied(session['user_id'], job_id):
        flash('You have already applied for this job', 'error')
        return redirect(request.referrer)
    
    file = request.files['resume']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.referrer)
    
    if file and file.filename.endswith('.pdf'):
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        filename = secure_filename(f"{session['user_id']}_{job_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Store relative path for database
        relative_path = f"uploads/resumes/{filename}"
        
        # Parse resume and calculate score
        resume_text = resume_parser.extract_text(filepath)
        job = db.get_job_by_id(job_id)
        score = resume_parser.calculate_score(resume_text, job)
        
        # Create application with relative path
        db.create_application(session['user_id'], job_id, relative_path, score)
        
        flash(f'Application submitted successfully!, 'success')
        return redirect(url_for('view_my_applications'))
    else:
        flash('Only PDF files are allowed', 'error')
        return redirect(request.referrer)

@app.route('/view_my_applications')
def view_my_applications():
    if 'usertype' not in session or session['usertype'] != 'user':
        return redirect(url_for('login'))
    
    applications = db.get_user_applications(session['user_id'])
    return render_template('user/view_my_applications.html', applications=applications)

@app.route('/send_complaint', methods=['GET', 'POST'])
def send_complaint():
    if 'usertype' not in session or session['usertype'] != 'user':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        complaint_text = request.form['complaint']
        db.create_complaint(session['user_id'], complaint_text)
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('send_complaint'))
    
    return render_template('user/send_complaint.html')

@app.route('/view_replies')
def view_replies():
    if 'usertype' not in session or session['usertype'] != 'user':
        return redirect(url_for('login'))
    
    complaints = db.get_user_complaints(session['user_id'])
    return render_template('user/view_replies.html', complaints=complaints)

# ==================== ADMIN ROUTES ====================

@app.route('/admin_home')
def admin_home():
    if 'usertype' not in session or session['usertype'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin/admin_home.html')

@app.route('/admin_view_companies')
def admin_view_companies():
    if 'usertype' not in session or session['usertype'] != 'admin':
        return redirect(url_for('login'))
    
    companies = db.get_all_companies()
    return render_template('admin/view_companies.html', companies=companies)

@app.route('/admin_view_applications')
def admin_view_applications():
    if 'usertype' not in session or session['usertype'] != 'admin':
        return redirect(url_for('login'))
    
    # Get applications grouped by company and job
    applications_hierarchy = db.get_applications_grouped_by_company_job()
    return render_template('admin/view_applications.html', applications=applications_hierarchy)

@app.route('/admin_view_complaints')
def admin_view_complaints():
    if 'usertype' not in session or session['usertype'] != 'admin':
        return redirect(url_for('login'))
    
    complaints = db.get_all_complaints()
    return render_template('admin/view_complaints.html', complaints=complaints)

@app.route('/reply_complaint/<int:complaint_id>', methods=['POST'])
def reply_complaint(complaint_id):
    if 'usertype' not in session or session['usertype'] != 'admin':
        return redirect(url_for('login'))
    
    reply = request.form['reply']
    db.update_complaint_reply(complaint_id, reply)
    flash('Reply sent successfully!', 'success')
    return redirect(url_for('admin_view_complaints'))

if __name__ == '__main__':
    app.run(debug=True)