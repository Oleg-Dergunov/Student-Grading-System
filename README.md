# Student Grading System

### Overview
A Flask web application for managing users, courses, and student records. Supports administrator, teacher, and student roles, as well as an active/inactive user system.

### 🚀 Features  
  
✅ Authorization by email or ID  
✅ User activity check  
✅ login_required decorator for protecting routes  
✅ Role-based navigation  
✅ Roles:    
- Administrator — Manage users and courses
- Teacher — View and manage your courses
- Student — View courses you're enrolled in
  

### 📂 Project Structure

The project is organized into layers:

Student-Grading-System/  
│  
├── app.py # Entry Point  
├── db.py # Database Connection and Teardown  
├── db.sqlite # Database  
│  
├── routes/ # HTTP Routes (Blueprints)  
├── services/ # Business Logic  
├── repositories/ # SQL queries  
├── templates/ # Jinja2 templates  
└── static/ # CSS, images  

### 🛠 Technologies Used  
- Python 3.x
- Flask
- SQLite
- Jinja2 templates

### 🔧 Installation & Usage  
Python 3 is required.

Run the application:

```bash
git clone https://github.com/Oleg-Dergunov/Student-Grading-System.git  
cd Student-Grading-System 
python app.py
```

🔐 Test login

You can use an existing administrator account to log in:

ID: 1

Password: admin123
