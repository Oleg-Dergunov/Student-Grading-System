import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_db
from routes.auth import login_required

courses_bp = Blueprint("courses", __name__)

# Initial page
@courses_bp.route("/")
@login_required
def index():
    return redirect(url_for("courses.courses"))


# Courses page
@courses_bp.route("/courses")
@login_required
def courses():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    role = session["role"]
    user_id = session["user_id"]

    db = get_db()

    if role == "admin": # The admin can see all courses
        courses = db.execute("""
            SELECT 
                courses.id,
                courses.name,
                users.firstName AS teacherFirstName,
                users.lastName AS teacherLastName,
                (
                    SELECT COUNT(*) 
                    FROM enrollments 
                    WHERE enrollments.course_id = courses.id
                ) AS studentCount
            FROM courses
            LEFT JOIN users ON courses.teacher_id = users.id
        """).fetchall()

    elif role == "teacher": # Teacher sees the courses they teach
        courses = db.execute("""
            SELECT 
                courses.id,
                courses.name,
                users.firstName AS teacherFirstName,
                users.lastName AS teacherLastName,
                (
                    SELECT COUNT(*) 
                    FROM enrollments 
                    WHERE enrollments.course_id = courses.id
                ) AS studentCount
            FROM courses
            LEFT JOIN users ON courses.teacher_id = users.id
            WHERE courses.teacher_id = ?
        """, (user_id,)).fetchall()

    else: # Student sees the courses they are enrolled in
        courses = db.execute("""
            SELECT 
                courses.id,
                courses.name,
                users.firstName AS teacherFirstName,
                users.lastName AS teacherLastName,
                (
                    SELECT COUNT(*) 
                    FROM enrollments 
                    WHERE enrollments.course_id = courses.id
                ) AS studentCount
            FROM enrollments
            JOIN courses ON enrollments.course_id = courses.id
            LEFT JOIN users ON courses.teacher_id = users.id
            WHERE enrollments.student_id = ?
        """, (user_id,)).fetchall()

    return render_template("courses.html", courses=courses)


# Add a course page
@courses_bp.route("/courses/add_course", methods=["GET", "POST"])
@login_required
def add_course():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()

    if request.method == "POST":
        name = request.form["name"]


        try:
            db.execute("INSERT INTO courses (name, teacher_id) VALUES (?, NULL)", (name,))
            db.commit()
        except sqlite3.IntegrityError:
            return render_template(
                "courses/add_course.html",
                error="A course with this name already exists",
                name=name
            )


        return redirect(url_for("courses.courses"))

    return render_template("courses/add_course.html")