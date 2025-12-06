-- Create database
CREATE DATABASE IF NOT EXISTS talent_screen360;
USE talent_screen360;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS application_request;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS login;

-- Create login table
CREATE TABLE login (
    login_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100),
    usertype VARCHAR(50)
);

-- Create user table
CREATE TABLE user (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    login_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    place VARCHAR(150),
    email VARCHAR(100),
    phone VARCHAR(20),
    FOREIGN KEY (login_id) REFERENCES login(login_id) ON DELETE CASCADE
);

-- Create company table
CREATE TABLE company (
    company_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    login_id INT,
    company_name VARCHAR(200),
    place VARCHAR(150),
    phone VARCHAR(20),
    email VARCHAR(100),
    est_year VARCHAR(10),
    FOREIGN KEY (login_id) REFERENCES login(login_id) ON DELETE CASCADE
);

-- Create jobs table
CREATE TABLE jobs (
    job_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    title VARCHAR(200),
    qualification VARCHAR(200),
    details TEXT,
    last_date DATE,
    requirements VARCHAR(200),
    FOREIGN KEY (company_id) REFERENCES company(company_id) ON DELETE CASCADE
);

-- Create applications table
CREATE TABLE applications (
    application_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    job_id INT,
    date DATE,
    resume_path VARCHAR(500),
    mark VARCHAR(50),
    status VARCHAR(100) DEFAULT 'pending'
);

-- Create application_request table (optional, for future use)
CREATE TABLE application_request (
    app_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    job_id INT,
    apply_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

-- Create complaints table
CREATE TABLE complaints (
    complaint_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    complaint TEXT,
    date DATE,
    reply TEXT,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

-- Insert admin user (username: admin, password: admin123)
INSERT INTO login (username, password, usertype) VALUES ('admin', 'admin123', 'admin');

-- Display success message
SELECT 'Database initialized successfully!' AS message;
SELECT 'Admin credentials - Username: admin, Password: admin123' AS info;