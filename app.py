import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "supersecretkey"  


# Connecting to db
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("db.sqlite")
        g.db.row_factory = sqlite3.Row
    return g.db


# Connection closure after query
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Decorator @login_required
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", 
            (session["user_id"],)
        ).fetchone()

        if not user or user["active"] == 0:
            session.clear()
            return redirect(url_for("login"))

        return f(*args, **kwargs)
    return wrapper


# Global context processor automatically passing current_user to all templates
@app.context_processor
def inject_user():
    user = None
    if "user_id" in session:
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return dict(current_user=user)


# Initial page
@app.route("/")
@login_required
def index():
    return redirect(url_for("courses"))



# Login page
@app.route("/login", methods=["GET", "POST"])
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

        return redirect(url_for("courses"))

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Courses page
@app.route("/courses")
@login_required
def courses():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session["role"]
    user_id = session["user_id"]

    db = get_db()

    if role == "admin": # The admin can see all courses
        courses = db.execute("""
            SELECT 
                courses.id,
                courses.name,
                users.firstName AS teacherFirstName,
                users.lastName AS teacherLastName,
                (
                    SELECT COUNT(*) 
                    FROM enrollments 
                    WHERE enrollments.course_id = courses.id
                ) AS studentCount
            FROM courses
            LEFT JOIN users ON courses.teacher_id = users.id
        """).fetchall()

    elif role == "teacher": # Teacher sees the courses they teach
        courses = db.execute("""
            SELECT 
                courses.id,
                courses.name,
                users.firstName AS teacherFirstName,
                users.lastName AS teacherLastName,
                (
                    SELECT COUNT(*) 
                    FROM enrollments 
                    WHERE enrollments.course_id = courses.id
                ) AS studentCount
            FROM courses
            LEFT JOIN users ON courses.teacher_id = users.id
            WHERE courses.teacher_id = ?
        """, (user_id,)).fetchall()

    else: # Student sees the courses they are enrolled in
        courses = db.execute("""
            SELECT 
                courses.id,
                courses.name,
                users.firstName AS teacherFirstName,
                users.lastName AS teacherLastName,
                (
                    SELECT COUNT(*) 
                    FROM enrollments 
                    WHERE enrollments.course_id = courses.id
                ) AS studentCount
            FROM enrollments
            JOIN courses ON enrollments.course_id = courses.id
            LEFT JOIN users ON courses.teacher_id = users.id
            WHERE enrollments.student_id = ?
        """, (user_id,)).fetchall()

    return render_template("courses.html", courses=courses)



# Profile page
@app.route("/profile", methods=["GET", "POST"])
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



# Add a course page
@app.route("/courses/add_course", methods=["GET", "POST"])
@login_required
def add_course():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db()

    if request.method == "POST":
        name = request.form["name"]


        try:
            db.execute("INSERT INTO courses (name, teacher_id) VALUES (?, NULL)", (name,))
            db.commit()
        except sqlite3.IntegrityError:
            return render_template(
                "courses/add_course.html",
                error="A course with this name already exists",
                name=name
            )


        return redirect(url_for("courses"))

    return render_template("courses/add_course.html")


# Users page
@app.route("/users")
@login_required
def manage_users():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()

    return render_template("users.html", users=users)



# Add a user page
@app.route("/users/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

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
            return redirect(url_for("manage_users"))

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




# Open browser with localhost
import webbrowser
import threading

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")



if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
