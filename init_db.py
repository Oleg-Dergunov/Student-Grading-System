import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# Table of users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'admin'))
)
""")

# Table of courses
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
)
""")

# Table of assessments
cursor.execute("""
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    grade REAL,
    date TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (student_id) REFERENCES users(id)
)
""")

# Table of enrollments
cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY(student_id) REFERENCES users(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)
""")

cursor.execute("SELECT * FROM users WHERE role = 'admin'") 
admin_exists = cursor.fetchone() 
if not admin_exists: 
    cursor.execute(""" INSERT INTO users (firstName, lastName, email, password, role) VALUES (?, ?, ?, ?, ?) """, ("Admin", "Adminych", "admin@example.com", "admin123", "admin")) 
    print("Administrator created: admin@example.com / admin123") 
else: 
    print("Administrator exists")

conn.commit()
conn.close()

print("Database created!")
