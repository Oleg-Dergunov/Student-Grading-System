from flask import Blueprint, render_template, request, redirect, url_for
from routes.auth import login_required, admin_required
from services.users_service import (
    get_all_users,
    create_user,
    get_user_by_id,
    admin_update_user
)

users_bp = Blueprint("users", __name__)


# Users page (admin only)
@users_bp.route("/users")
@login_required
@admin_required
def manage_users():
    users = get_all_users()
    return render_template("users.html", users=users)


# Add a user page (admin only)
@users_bp.route("/users/add_user", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():
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


# Edit user page (admin only)
@users_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return "User not found", 404

    error = None
    success = None

    if request.method == "POST":
        first = request.form["firstName"].strip()
        last = request.form["lastName"].strip()
        email = request.form["email"].lower().strip()
        role = request.form["role"]
        active = int(request.form["status"])
        new_password = request.form.get("new_password", "").strip()

        success, error = admin_update_user(
            user_id,
            first,
            last,
            email,
            role,
            active,
            new_password
        )

        if success:
            user = get_user_by_id(user_id)

    return render_template(
        "users/edit_user.html",
        user=user,
        error=error,
        success=success
    )