from flask import *
from database import *
import fitz  # PyMuPDF
import uuid
import os

user=Blueprint("user",__name__)

@user.route("/userhome")
def userhome():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    data = {}
    q = "SELECT * FROM user WHERE login_id='%s'" % (session['login_id'])
    res = select(q)
    if res:
        data['user'] = res[0]
    
    # Get user's applications
    q = "SELECT * FROM application WHERE user_id='%s'" % (res[0]['user_id'])
    apps = select(q)
    if apps:
        data['applications'] = apps
    
    return render_template("userhome.html", data=data)

@user.route("/user_profile_view", methods=['GET', 'POST'])
def user_profile_view():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    data = {}
    q = "SELECT * FROM user WHERE login_id='%s'" % (session['login_id'])
    data['view'] = select(q)
    
    if 'submit' in request.form:
        pdf = request.files['file']
        if pdf:
            # Create upload folder if not exists
            if not os.path.exists('static/resume'):
                os.makedirs('static/resume')
            
            path1 = 'static/resume/' + str(uuid.uuid4()) + pdf.filename
            pdf.save(path1)
            
            # Extract text from PDF
            with open(path1, 'rb') as pdf_file:
                pdf_reader = fitz.open(pdf_file)
                text = ''
                for page_num in range(pdf_reader.page_count):
                    page = pdf_reader.load_page(page_num)
                    text += page.get_text()
            
            # Clean text
            resume_text = text.replace("'", "''")
            
            q = "UPDATE user SET cv_file='%s', cv_des='%s' WHERE login_id='%s'" % (path1, resume_text, session['login_id'])
            update(q)
            flash('CV uploaded successfully!')
            return redirect(url_for('user.user_profile_view'))
    
    return render_template('user_profile_view.html', data=data)

@user.route("/usersendcomplaints", methods=['GET', 'POST'])
def usersendcomplaints():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    data = {}
    # Get user_id
    q = "SELECT user_id FROM user WHERE login_id='%s'" % (session['login_id'])
    res = select(q)
    user_id = res[0]['user_id'] if res else None
    
    if 'submit' in request.form:
        comp = request.form['comp'].replace("'", "''")
        q = "INSERT INTO complaints(user_id, user_type, complaint_des, reply, date) VALUES ('%s', 'user', '%s', 'pending', CURDATE())" % (user_id, comp)
        insert(q)
        flash('Complaint submitted successfully!')
        return redirect(url_for('user.usersendcomplaints'))
    
    q = "SELECT * FROM complaints WHERE user_id='%s' AND user_type='user'" % (user_id)
    data['complaint'] = select(q)
    
    return render_template("usersendcomplaint.html", data=data)

@user.route("/viewjobs")
def viewjobs():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    data = {}
    q = "SELECT * FROM jobs WHERE status='approved'"
    data['jobs'] = select(q)
    
    return render_template("viewjobs_user.html", data=data)

@user.route("/applyjob", methods=['GET', 'POST'])
def applyjob():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    job_id = request.args.get('id')
    
    # Get user details
    q = "SELECT * FROM user WHERE login_id='%s'" % (session['login_id'])
    user_data = select(q)
    
    if request.method == 'POST':
        if not user_data[0]['cv_file']:
            flash('Please upload your CV first!')
            return redirect(url_for('user.user_profile_view'))
        
        # Insert application
        q = "INSERT INTO application(user_id, job_id, date, resume_path, status) VALUES ('%s', '%s', CURDATE(), '%s', 'pending')" % (user_data[0]['user_id'], job_id, user_data[0]['cv_file'])
        insert(q)
        flash('Application submitted successfully!')
        return redirect(url_for('user.viewjobs'))
    
    return redirect(url_for('user.viewjobs'))