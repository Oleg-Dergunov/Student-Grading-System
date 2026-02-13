from flask import Blueprint, render_template, request, session
from db import get_db
from routes.auth import login_required

profile_bp = Blueprint("profile", __name__)

# Profile page
@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    db = get_db()
    user_id = session["user_id"]

    user = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    error = None
    success = None
    show_email_form = False
    show_password_form = False

    # 1. Show email change form
    if request.method == "POST" and "show_email_form" in request.form:
        show_email_form = True

    # 2. Show password change form
    if request.method == "POST" and "show_password_form" in request.form:
        show_password_form = True

    # 3. Email update
    if request.method == "POST" and "update_email" in request.form:
        show_email_form = True  # leave the form open on error

        new_email = request.form["email"].lower().strip()

        existing = db.execute(
            "SELECT id FROM users WHERE LOWER(email)=LOWER(?) AND id != ?",
            (new_email, user_id)
        ).fetchone()

        if existing:
            error = "This email is already in use"
        else:
            db.execute(
                "UPDATE users SET email = ? WHERE id = ?",
                (new_email, user_id)
            )
            db.commit()
            success = "Email updated"
            show_email_form = False  # hide form after success

            user = db.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()

    # 4. Change password
    if request.method == "POST" and "change_password" in request.form:
        show_password_form = True

        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        repeat_password = request.form["repeat_password"]

        if old_password != user["password"]:
            error = "The old password is incorrect"
        elif new_password != repeat_password:
            error = "The new passwords do not match."
        elif not new_password:
            error = "The password cannot be empty"
        else:
            db.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (new_password, user_id)
            )
            db.commit()
            success = "Password successfully changed"
            show_password_form = False

    return render_template(
        "profile.html",
        error=error,
        success=success,
        show_password_form=show_password_form,
        show_email_form=show_email_form
    )
