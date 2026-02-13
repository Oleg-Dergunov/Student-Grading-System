from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from db import get_db

auth_bp = Blueprint("auth", __name__)

# Decorator @login_required
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", 
            (session["user_id"],)
        ).fetchone()

        if not user or user["active"] == 0:
            session.clear()
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)
    return wrapper


# Global context processor automatically passing current_user to all templates
@auth_bp.app_context_processor
def inject_user():
    user = None
    if "user_id" in session:
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", 
            (session["user_id"],)
        ).fetchone()
    return dict(current_user=user)


# Login page
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form["identifier"]
        password = request.form["password"]

        db = get_db()

        # If the user entered a number → search by ID
        if identifier.isdigit():
            user = db.execute(
                "SELECT * FROM users WHERE id = ? AND password = ?",
                (int(identifier), password)
            ).fetchone()
        else:
            # Otherwise we consider it an email
            user = db.execute(
                "SELECT * FROM users WHERE LOWER(email) = LOWER(?) AND password = ?",
                (identifier, password)
            ).fetchone()

        # User not found or wrong password
        if not user:
            return render_template("login.html", error="Invalid credentials")

        # User found but inactive
        if user["active"] == 0:
            return render_template("login.html", error="User is inactive")

        # User is active → login
        session["user_id"] = user["id"] 
        session["role"] = user["role"]

        return redirect(url_for("courses.courses"))

    return render_template("login.html")


# Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
