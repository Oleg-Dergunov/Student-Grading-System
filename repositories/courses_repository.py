import sqlite3
from db import get_db


def fetch_all_courses_for_admin():
    db = get_db()
    query = """
        SELECT 
            courses.id,
            courses.name,
            users.first_name AS teacher_first_name,
            users.last_name AS teacher_last_name,
            (
                SELECT COUNT(*) 
                FROM enrollments 
                WHERE enrollments.course_id = courses.id
            ) AS student_count
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
            users.first_name AS teacher_first_name,
            users.last_name AS teacher_last_name,
            (
                SELECT COUNT(*) 
                FROM enrollments 
                WHERE enrollments.course_id = courses.id
            ) AS student_count
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
            users.first_name AS teacher_first_name,
            users.last_name AS teacher_last_name,
            (
                SELECT COUNT(*) 
                FROM enrollments 
                WHERE enrollments.course_id = courses.id
            ) AS student_count
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


def get_course_by_id(course_id: int):
    db = get_db()
    query = """
        SELECT 
            courses.id,
            courses.name,
            courses.teacher_id,
            users.first_name AS teacher_first_name,
            users.last_name AS teacher_last_name
        FROM courses
        LEFT JOIN users ON courses.teacher_id = users.id
        WHERE courses.id = ?
    """
    return db.execute(query, (course_id,)).fetchone()


def update_course(course_id: int, name: str, teacher_id: int | None):
    db = get_db()
    db.execute("""
        UPDATE courses
        SET name = ?, teacher_id = ?
        WHERE id = ?
    """, (name, teacher_id, course_id))
    db.commit()
