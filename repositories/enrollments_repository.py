from db import get_db

def get_students_for_course(course_id):
    db = get_db()
    return db.execute("""
        SELECT users.id, users.first_name, users.last_name, active
        FROM enrollments
        JOIN users ON enrollments.student_id = users.id
        WHERE enrollments.course_id = ?
    """, (course_id,)).fetchall()


def enroll_student(course_id, student_id):
    db = get_db()
    db.execute("""
        INSERT OR IGNORE INTO enrollments (course_id, student_id)
        VALUES (?, ?)
    """, (course_id, student_id))
    db.commit()


def unenroll_student(course_id, student_id):
    db = get_db()
    db.execute("""
        DELETE FROM enrollments
        WHERE course_id = ? AND student_id = ?
    """, (course_id, student_id))
    db.commit()
