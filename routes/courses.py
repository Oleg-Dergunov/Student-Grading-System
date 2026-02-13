from flask import Blueprint, render_template, request, redirect, url_for, session
from routes.auth import login_required
from services.courses_service import get_courses_for_user, add_course

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/")
@login_required
def index():
    return redirect(url_for("courses.courses"))


@courses_bp.route("/courses")
@login_required
def courses():
    role = session["role"]
    user_id = session["user_id"]

    courses = get_courses_for_user(role, user_id)

    return render_template("courses.html", courses=courses)


@courses_bp.route("/courses/add_course", methods=["GET", "POST"])
@login_required
def add_course_route():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form["name"]

        success, error = add_course(name)

        if error:
            return render_template(
                "courses/add_course.html",
                error=error,
                name=name
            )

        return redirect(url_for("courses.courses"))

    return render_template("courses/add_course.html")