# Talent Screen 360 - Recruitment Management System

A comprehensive Flask-based web application for managing job recruitment processes with user, company, and admin roles.

## Features

### For Users
- Register and login
- Browse companies and view job postings
- Apply for jobs by uploading resumes (PDF)
- Automatic resume scoring based on job requirements
- Track application status
- Submit complaints and view admin replies

### For Companies
- Register and login
- Post job openings with requirements
- View all applications received
- See candidate scores and contact information
- Access applicant resumes

### For Admin
- View all registered companies
- View application rankings sorted by score
- Manage user complaints and send replies
- Monitor platform activity

## Project Structure

```
talent_screen360/
│
├── app.py                          # Main Flask application
├── database.py                     # Database operations module
├── resume_parser.py                # Resume parsing and scoring module
├── requirements.txt                # Python dependencies
├── init_database.sql               # Database initialization script
│
├── templates/
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── login.html                  # Login page
│   ├── register_user.html          # User registration
│   ├── register_company.html       # Company registration
│   │
│   ├── company/
│   │   ├── company_home.html       # Company dashboard
│   │   ├── upload_job.html         # Post job form
│   │   └── view_application.html   # View applications
│   │
│   ├── user/
│   │   ├── user_home.html          # User dashboard
│   │   ├── view_companies.html     # Browse companies
│   │   ├── view_jobs.html          # View job listings
│   │   ├── view_my_applications.html  # User's applications
│   │   ├── send_complaint.html     # Submit complaint
│   │   └── view_replies.html       # View complaint replies
│   │
│   └── admin/
│       ├── admin_home.html         # Admin dashboard
│       ├── view_companies.html     # All companies
│       ├── view_applications.html  # Ranked applications
│       └── view_complaints.html    # Manage complaints
│
└── static/
    ├── uploads/
    │   └── resumes/                # Uploaded resume storage
    └── assets/                     # CSS, JS, images (from GP template)
```

## Installation and Setup

### 1. Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher
- Pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database

1. Open MySQL and run the initialization script:

```bash
mysql -u root -p < init_database.sql
```

Or manually execute the SQL commands in `init_database.sql`

2. Update database credentials in `database.py`:

```python
self.config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',  # Change this
    'database': 'talent_screen360'
}
```

### 4. Setup Static Files

Download the GP template from [BootstrapMade](https://bootstrapmade.com/gp-free-multipurpose-html-bootstrap-template/) and place the assets folder in the `static/` directory:

```
static/
├── assets/
│   ├── css/
│   ├── js/
│   ├── img/
│   └── vendor/
└── uploads/
    └── resumes/
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/`

## Default Admin Credentials

- **Username:** admin
- **Password:** admin123

## Usage Guide

### User Workflow
1. Register as a user from the home page
2. Login with your credentials
3. Browse companies and view their job postings
4. Upload your resume (PDF only) to apply for jobs
5. View your applications and scores
6. Submit complaints if needed

### Company Workflow
1. Register as a company from the home page
2. Login with your credentials
3. Post job openings with requirements
4. View applications received with candidate scores
5. Download and review resumes

### Admin Workflow
1. Login with admin credentials
2. Monitor all companies and applications
3. View application rankings
4. Respond to user complaints

## Resume Scoring System

The system automatically scores resumes based on:

- **Qualification Match (30 points):** Checks if required qualifications are mentioned
- **Requirements Match (40 points):** Matches skills and requirements
- **Experience Indicators (15 points):** Presence of work experience keywords
- **Education Indicators (10 points):** Educational background mentions
- **Contact Information (5 points):** Email and phone presence

**Total Score:** 100 points

## Key Features

### Security
- Session-based authentication
- Role-based access control
- Secure file uploads with validation

### User Experience
- Responsive design using Bootstrap
- Flash messages for user feedback
- Clean and modern UI using GP template
- Intuitive navigation

### Data Management
- MySQL database with proper relationships
- Automatic date tracking
- Application status management

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL server is running
   - Verify database credentials in `database.py`
   - Ensure database is initialized

2. **File Upload Error**
   - Check `static/uploads/resumes/` folder exists
   - Verify folder permissions
   - Ensure only PDF files are uploaded

3. **Template Not Found**
   - Verify all template files are in correct folders
   - Check file names match route definitions

4. **Static Assets Not Loading**
   - Ensure GP template assets are in `static/assets/`
   - Check file paths in templates

## Future Enhancements

- Email notifications for applications
- Advanced resume parsing with NLP
- Interview scheduling system
- Company ratings and reviews
- Application tracking timeline
- Export reports (PDF/Excel)
- Password encryption (currently using plain text)

## License

This project uses the GP template from BootstrapMade. Please refer to their [license](https://bootstrapmade.com/license/) for template usage.

## Support

For issues or questions, submit a complaint through the user interface or contact the admin.