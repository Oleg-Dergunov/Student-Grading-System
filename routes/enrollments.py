from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required, admin_required
from services.courses_service import get_course_by_id
from services.enrollments_service import (
    enroll_student,
    unenroll_student,
    load_enrollment_data
)

enrollments_bp = Blueprint("enrollments", __name__)


@enrollments_bp.route("/courses/<int:course_id>/edit/enrollments", methods=["GET", "POST"])
@login_required
@admin_required
def edit_course_enrollments(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404

    # POST: add/remove students
    if request.method == "POST":
        action = request.form.get("action")
        student_id = request.form.get("student_id")

        if action == "enroll":
            success, error = enroll_student(course_id, student_id)
        elif action == "unenroll":
            success, error = unenroll_student(course_id, student_id)

        students, enrolled_ids, _ = load_enrollment_data(course_id)

        return render_template(
            "courses/enrollments.html",
            course=course,
            students=students,
            enrolled_ids=enrolled_ids,
            success=success,
            error=error
        )


    # GET: load data for page
    students, enrolled_ids, error = load_enrollment_data(course_id)

    return render_template(
        "courses/enrollments.html",
        course=course,
        students=students,
        enrolled_ids=enrolled_ids
    )
