import sqlite3
from db import get_db


def get_courses_for_user(role: str, user_id: int):
    db = get_db()

    if role == "admin":
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

    if role == "teacher":
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



def add_course(name: str):
    db = get_db()

    try:
        db.execute(
            "INSERT INTO courses (name, teacher_id) VALUES (?, NULL)",
            (name,)
        )
        db.commit()
        return "Course added", None

    except sqlite3.IntegrityError:
        return None, "A course with this name already exists"