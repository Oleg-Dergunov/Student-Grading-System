from flask import Blueprint, render_template, request, redirect, url_for, session
from routes.auth import login_required
from services.users_service import get_all_users, create_user

users_bp = Blueprint("users", __name__)


@users_bp.route("/users")
@login_required
def manage_users():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    users = get_all_users()

    return render_template("users.html", users=users)


@users_bp.route("/users/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"].lower().strip()
        password = request.form["password"]
        role = request.form["role"]

        success, error = create_user(firstName, lastName, email, password, role)

        if error:
            return render_template(
                "users/add_user.html",
                error=error,
                firstName=firstName,
                lastName=lastName,
                email=email,
                role=role
            )

        return redirect(url_for("users.manage_users"))

    return render_template("users/add_user.html")