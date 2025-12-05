🚀 Pre-Run Checklist
1. Install Required Packages
bashpip install flask pymysql PyMuPDF scikit-learn pandas numpy joblib
2. Database Setup (CRITICAL)
First, check your MySQL port:
python# In database.py, verify this matches YOUR MySQL:
port=3307  # Change to 3306 if that's your MySQL port
Run this SQL to create/fix tables:
sqlCREATE DATABASE IF NOT EXISTS resume_screening;
USE resume_screening;

-- Create login table
CREATE TABLE IF NOT EXISTS login (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100),
    usertype VARCHAR(50)
);

-- Create company table
CREATE TABLE IF NOT EXISTS company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    login_id INT,
    company_name VARCHAR(100),
    place VARCHAR(100),
    phone VARCHAR(100),
    email VARCHAR(100),
    est_year VARCHAR(500)
);

-- Create user table
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    login_id INT,
    fname VARCHAR(100),
    lname VARCHAR(100),
    place VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(100),
    cv_file VARCHAR(500),
    cv_des TEXT
);

-- Create jobs table
CREATE TABLE IF NOT EXISTS jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    title VARCHAR(100),
    qualification VARCHAR(100),
    details TEXT,
    last_date VARCHAR(100),
    requirements TEXT,
    date_posted DATE,
    status VARCHAR(50) DEFAULT 'pending'
);

-- Create application table
CREATE TABLE IF NOT EXISTS application (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    job_id INT,
    date DATE,
    resume_path VARCHAR(500),
    personality VARCHAR(100),
    mark VARCHAR(50),
    status VARCHAR(100) DEFAULT 'pending'
);

-- Create complaints table
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    user_type VARCHAR(100),
    complaint_des TEXT,
    reply TEXT,
    date DATE
);

-- Insert default admin
INSERT INTO login (username, password, usertype) VALUES ('admin', 'admin123', 'admin');



5. Train the ML Model (FIRST TIME ONLY)
Create a file train_model.py:
pythonfrom ml_model import MLModel
import pandas as pd

# Create sample training data
data = {
    'text': [
        'python java sql data analysis machine learning',
        'leadership team management project management communication',
        'creative design photoshop illustrator ui ux',
        'accounting finance excel budget analysis',
        'sales marketing customer service communication'
    ],
    'personality': ['Analytical', 'Leadership', 'Creative', 'Detail-oriented', 'Outgoing']
}

df = pd.DataFrame(data)

# Train model
ml = MLModel()
ml.train_model(df)
print("Model trained and saved!")
Run it once:
bashpython train_model.py
6. Run the Application
Start Flask:
bashpython main.py
```

You should see:
```
 * Running on http://0.0.0.0:5005
 * Restarting with stat
7. Testing Flow (IN THIS ORDER)
Step 1: Login as Admin

URL: http://localhost:5005/login
Username: admin
Password: admin123

Step 2: Register a Company

URL: http://localhost:5005/company_reg
Fill all details
Then login with company credentials

Step 3: Company Posts Job

Login as company
Go to "Upload Jobs"
Add job details

Step 4: Register as User

URL: http://localhost:5005/user_reg
Fill registration form

Step 5: User Uploads CV

Login as user
Go to profile
Upload a PDF resume

Step 6: User Applies for Job

Browse jobs
Click apply


⚠️ Common Errors & Fixes
Error 1: "No module named 'fitz'"
bashpip install PyMuPDF
Error 2: "Can't connect to MySQL server"
Check database.py:
pythonport=3306  # or 3307 - check your MySQL port
Error 3: "Table doesn't exist"
Run the SQL script above in your MySQL
Error 4: "Personality model not found"
bashpython train_model.py
Error 5: "404 Not Found"
Make sure all blueprints are registered in main.py:
pythonapp.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(compny)
app.register_blueprint(user)  # Don't forget this!
app.register_blueprint(api)
Error 6: "FileNotFoundError: static/resume"
bashmkdir -p static/resume
mkdir -p static/models

🔧 Important Configuration Changes
In database.py - Match your MySQL setup:
pythonuser="root"
password=""  # Add your MySQL password if you have one
database="resume_screening"
port=3306  # Change to 3307 if needed
In main.py - Change port if 5005 is busy:
pythonapp.run(debug=True, port=5000, host="0.0.0.0")  # Change 5005 to 5000

✅ Quick Test Commands
Test database connection:
python# test_db.py
from database import select
result = select("SELECT * FROM login WHERE username='admin'")
print(result)
Test ML model:
python# test_ml.py
from ml_model import MLModel
ml = MLModel()
result = ml.predict_personality("python developer with 5 years experience")
print(result)

📝 Default Login Credentials
RoleUsernamePasswordAdminadminadmin123Company(register first)(your choice)User(register first)(your choice)

🎯 Quick Start Commands
bash# 1. Install packages
pip install flask pymysql PyMuPDF scikit-learn pandas numpy joblib

# 2. Create folders
mkdir static/resume static/models

# 3. Run SQL script (in MySQL)
# Copy the CREATE TABLE commands above

# 4. Train ML model (first time only)
python train_model.py

# 5. Start application
python main.py

# 6. Open browser
# Go to: http://localhost:5005

What's the status of your MySQL? Is it running on port 3306 or 3307? Let me know if you hit any errors and I'll help you fix them immediately! 🚀Hokay fix 