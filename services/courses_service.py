from repositories.courses_repository import (
    fetch_all_courses_for_admin,
    fetch_courses_for_teacher,
    fetch_courses_for_student,
    insert_course
)


def get_courses_for_user(role: str, user_id: int):
    if role == "admin":
        return fetch_all_courses_for_admin()

    if role == "teacher":
        return fetch_courses_for_teacher(user_id)

    return fetch_courses_for_student(user_id)


def add_course(name: str):
    success, error = insert_course(name)

    if not success:
        return None, error

    return "Course added", None