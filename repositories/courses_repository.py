import sqlite3
from db import get_db


def fetch_all_courses_for_admin():
    db = get_db()
    query = """
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
    """
    return db.execute(query).fetchall()


def fetch_courses_for_teacher(user_id: int):
    db = get_db()
    query = """
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
    """
    return db.execute(query, (user_id,)).fetchall()


def fetch_courses_for_student(user_id: int):
    db = get_db()
    query = """
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
    """
    return db.execute(query, (user_id,)).fetchall()


def insert_course(name: str):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO courses (name, teacher_id) VALUES (?, NULL)",
            (name,)
        )
        db.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "A course with this name already exists"
