# AWS Cloud-Based Employee Management System (EMS)

## Overview

The AWS Cloud-Based Employee Management System (EMS) is a web-based application developed using Python Flask, MySQL, HTML, CSS, and JavaScript. The system is deployed on Amazon Web Services (AWS) and provides an efficient platform for managing employee information, departments, reports, and workforce analytics.

The application enables administrators and HR personnel to perform employee management operations such as adding, updating, deleting, and viewing employee records while maintaining a user-friendly and responsive interface.

---

## Features

### Authentication & Security

* Administrator Login System
* HR Registration Module
* Secure Database Connectivity using MySQL

### Employee Management

* Add New Employees
* View Employee Records
* Update Employee Information
* Delete Employee Records
* Search Employees

### Department Management

* Department-wise Employee Distribution
* Employee Count by Department
* Department Dashboard Analytics

### Workforce Classification

* Employee Type Management

  * Full Time
  * Contract

* Competency Level Tracking

  * T1
  * T2
  * T3

* Work Mode Management

  * Office
  * Remote

### Reporting

* Employee Reports
* Excel Export Functionality
* PDF Report Generation

### Dashboard

* Employee Statistics
* Department Statistics
* Salary Analytics
* Interactive Employee Insights

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask Framework

### Database

* MySQL

### Cloud Platform

* Amazon Web Services (AWS EC2)

### Additional Libraries

* PyMySQL
* Pandas
* OpenPyXL
* ReportLab
* Gunicorn

---

## Database Schema

### Department Table

| Column    | Type    |
| --------- | ------- |
| dept_id   | INT     |
| dept_name | VARCHAR |

### Employee Table

| Column           | Type    |
| ---------------- | ------- |
| emp_id           | INT     |
| emp_name         | VARCHAR |
| email            | VARCHAR |
| phone            | VARCHAR |
| dept_id          | INT     |
| designation      | VARCHAR |
| salary           | DECIMAL |
| joining_date     | DATE    |
| employee_type    | VARCHAR |
| competency_level | VARCHAR |
| work_mode        | VARCHAR |

### Admin Table

| Column   | Type    |
| -------- | ------- |
| admin_id | INT     |
| username | VARCHAR |
| password | VARCHAR |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Vishnu3118-MB/AWS_Cloud-Based-Emp-mgmt-sys.git
cd AWS_Cloud-Based-Emp-mgmt-sys
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure MySQL Database

Create a database:

```sql
CREATE DATABASE employee_db;
```

Update database credentials in:

```python
app.py
```

```python
db = pymysql.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="employee_db"
)
```

### Run Application

```bash
python app.py
```

Application will run on:

```text
http://localhost:5000
```

---

## AWS Deployment

This project is deployed on Amazon EC2.

### Services Used

* Amazon EC2
* Security Groups
* Ubuntu Server
* MySQL Server

### Deployment Steps

1. Launch EC2 Instance
2. Configure Security Groups
3. Install Python & MySQL
4. Clone GitHub Repository
5. Configure Database
6. Run Flask Application
7. Deploy using Gunicorn

---

## Project Screenshots

* Login Page
* Dashboard
* Employee Management
* Department Analytics
* Employee Type Summary
* Competency Level Summary
* Work Mode Summary
* Reports Module

---

## Future Enhancements

* Role-Based Access Control (RBAC)
* Employee Attendance Tracking
* Payroll Management
* Leave Management System
* Email Notifications
* AWS RDS Integration
* Docker Deployment
* CI/CD Pipeline Integration

---

## Author

**Vishnu M B**

Final Year Computer Science Engineering Student

C Byre Gowda Institute of Technology, Kolar

---

## License

This project is developed for educational and learning purposes.
