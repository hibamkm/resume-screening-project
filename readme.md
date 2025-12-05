# 🎯 AI-Powered Resume Screening System

A comprehensive Flask-based web application that automates resume screening using machine learning to predict candidate personality traits and match them with job requirements.

## ✨ Features

- **Multi-User System**: Separate portals for Admin, Companies, and Job Seekers
- **AI-Powered Screening**: Machine learning model for personality prediction from resumes
- **Job Management**: Companies can post jobs and review applications
- **Resume Analysis**: Automatic extraction and analysis of PDF resumes
- **Application Tracking**: Real-time status updates for job applications
- **Complaint System**: Built-in feedback mechanism for users

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **ML Libraries**: scikit-learn, pandas, numpy
- **PDF Processing**: PyMuPDF (fitz)
- **Others**: joblib for model persistence

## 📋 Prerequisites

- Python 3.7+
- MySQL Server (5.7+)
- pip package manager

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-screening-system.git
cd resume-screening-system
```

### 2. Install Dependencies

```bash
pip install flask pymysql PyMuPDF scikit-learn pandas numpy joblib
```

### 3. Database Setup

#### Check Your MySQL Port

First, verify your MySQL port (usually 3306 or 3307). Update `database.py`:

```python
user="root"
password=""  # Add your MySQL password if you have one
database="resume_screening"
port=3306  # Change to 3307 if needed
```

#### Create Database and Tables

Run the following SQL commands in your MySQL client:

```sql
CREATE DATABASE IF NOT EXISTS resume_screening;
USE resume_screening;

-- Login table
CREATE TABLE IF NOT EXISTS login (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100),
    usertype VARCHAR(50)
);

-- Company table
CREATE TABLE IF NOT EXISTS company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    login_id INT,
    company_name VARCHAR(100),
    place VARCHAR(100),
    phone VARCHAR(100),
    email VARCHAR(100),
    est_year VARCHAR(500)
);

-- User table
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

-- Jobs table
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

-- Application table
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

-- Complaints table
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    user_type VARCHAR(100),
    complaint_des TEXT,
    reply TEXT,
    date DATE
);

-- Insert default admin account
INSERT INTO login (username, password, usertype) 
VALUES ('admin', 'admin123', 'admin');
```

### 4. Create Required Directories

```bash
mkdir -p static/resume
mkdir -p static/models
```

### 5. Train the ML Model

Create a file `train_model.py`:

```python
from ml_model import MLModel
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
    'personality': [
        'Analytical', 
        'Leadership', 
        'Creative', 
        'Detail-oriented', 
        'Outgoing'
    ]
}

df = pd.DataFrame(data)

# Train and save model
ml = MLModel()
ml.train_model(df)
print("✅ Model trained and saved successfully!")
```

Run the training script (only needed once):

```bash
python train_model.py
```

## 🎮 Running the Application

Start the Flask server:

```bash
python main.py
```

The application will be available at: `http://localhost:5005`

## 👥 User Roles & Default Credentials

| Role | Username | Password | Notes |
|------|----------|----------|-------|
| Admin | `admin` | `admin123` | Pre-configured |
| Company | - | - | Register via `/company_reg` |
| Job Seeker | - | - | Register via `/user_reg` |

## 📖 Usage Guide

### For Administrators

1. Login at `/login` with admin credentials
2. Manage companies and users
3. Review and respond to complaints
4. Monitor system activity

### For Companies

1. Register at `/company_reg`
2. Login with your credentials
3. Post job openings via "Upload Jobs"
4. Review applications and candidate profiles
5. Update application status

### For Job Seekers

1. Register at `/user_reg`
2. Login and complete your profile
3. Upload your resume (PDF format)
4. Browse available jobs
5. Apply for positions
6. Track application status

## 🧪 Testing

### Test Database Connection

```python
# test_db.py
from database import select

result = select("SELECT * FROM login WHERE username='admin'")
print(result)
```

### Test ML Model

```python
# test_ml.py
from ml_model import MLModel

ml = MLModel()
result = ml.predict_personality("python developer with 5 years experience")
print(result)
```

## 🔧 Configuration

### Change Application Port

In `main.py`:

```python
app.run(debug=True, port=5000, host="0.0.0.0")  # Change port as needed
```

### Update Database Credentials

In `database.py`:

```python
user="root"
password="your_mysql_password"
database="resume_screening"
port=3306
```

## ⚠️ Troubleshooting

### Module Not Found Errors

```bash
# PyMuPDF/fitz error
pip install PyMuPDF

# Other missing packages
pip install flask pymysql scikit-learn pandas numpy joblib
```

### Database Connection Issues

- Verify MySQL is running: `sudo systemctl status mysql`
- Check port in `database.py` (3306 or 3307)
- Confirm credentials are correct

### Table Does Not Exist

Run the SQL script provided in Database Setup section

### Model Not Found Error

```bash
python train_model.py
```

### 404 Errors

Ensure all blueprints are registered in `main.py`:

```python
app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(compny)
app.register_blueprint(user)
app.register_blueprint(api)
```

### File/Directory Errors

```bash
mkdir -p static/resume
mkdir -p static/models
```

## 📁 Project Structure

```
resume-screening-system/
├── main.py                 # Application entry point
├── database.py            # Database connection handler
├── ml_model.py            # ML model for personality prediction
├── train_model.py         # Model training script
├── public.py              # Public routes (login, register)
├── admin.py               # Admin panel routes
├── compny.py              # Company portal routes
├── user.py                # Job seeker portal routes
├── api.py                 # API endpoints
├── static/
│   ├── resume/           # Uploaded resumes
│   └── models/           # Trained ML models
└── templates/            # HTML templates
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Known Issues

- PDF extraction may fail for scanned/image-based resumes
- Model accuracy depends on training data quality
- Large resume files may cause timeout issues

