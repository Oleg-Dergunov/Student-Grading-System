from repositories.courses_repository import (
    fetch_all_courses_for_admin,
    fetch_courses_for_teacher,
    fetch_courses_for_student,
    insert_course,
    get_course_by_id,
    update_course
)
from repositories.users_repository import get_user_by_id, get_all_teachers


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


def load_course_for_edit(course_id: int):
    return get_course_by_id(course_id)


def load_teachers_for_course_edit():
    teachers = get_all_teachers()
    return [t for t in teachers if t["active"]
]


def process_course_edit(course_id: int, form):
    name = form["name"].strip()

    # Normalize teacher_id
    teacher_id_raw = form.get("teacher_id")
    if teacher_id_raw == "" or teacher_id_raw is None:
        teacher_id = None
    else:
        teacher_id = int(teacher_id_raw)

    # Load current course
    current = get_course_by_id(course_id)
    if not current:
        raise ValueError("Course not found")

    # Check teacher activity
    if teacher_id is not None:
        teacher = get_user_by_id(teacher_id)

        if not teacher:
            raise ValueError("Teacher does not exist")

        if not teacher["active"]:
            raise ValueError("Cannot assign an inactive teacher")

    # Check if data changed
    no_changes = (
        current["name"] == name and
        current["teacher_id"] == teacher_id
    )

    if no_changes:
        return current, False

    # Apply update
    update_course(course_id, name, teacher_id)

    updated = get_course_by_id(course_id)
    return updated, True
