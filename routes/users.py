import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_db
from routes.auth import login_required

users_bp = Blueprint("users", __name__)

# Users page
@users_bp.route("/users")
@login_required
def manage_users():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()

    return render_template("users.html", users=users)



# Add a user page
@users_bp.route("/users/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()

    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"].lower().strip()
        password = request.form["password"]
        role = request.form["role"]

        try:
            db.execute("""
                INSERT INTO users (firstName, lastName, email, password, role, active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (firstName, lastName, email, password, role))

            db.commit()
            return redirect(url_for("users.manage_users"))

        except sqlite3.IntegrityError:
            return render_template(
                "users/add_user.html",
                error="Email already exists",
                firstName=firstName,
                lastName=lastName,
                email=email,
                role=role
            )

    return render_template("users/add_user.html")
