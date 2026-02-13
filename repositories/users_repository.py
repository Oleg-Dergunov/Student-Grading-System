import sqlite3
from db import get_db


def fetch_all_users():
    db = get_db()
    return db.execute("SELECT * FROM users").fetchall()


def insert_user(firstName: str, lastName: str, email: str, password: str, role: str):
    db = get_db()

    try:
        db.execute("""
            INSERT INTO users (firstName, lastName, email, password, role, active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (firstName, lastName, email, password, role))

        db.commit()
        return True, None

    except sqlite3.IntegrityError:
        return False, "Email already exists"
    

def get_user_by_id(user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

def find_user_by_email_excluding(email, user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE email = ? AND id != ?",
        (email, user_id)
    ).fetchone()

def update_user_admin(user_id, first, last, email, role, active):
    db = get_db()
    db.execute(
        """
        UPDATE users
        SET firstName = ?, lastName = ?, email = ?, role = ?, active = ?
        WHERE id = ?
        """,
        (first, last, email, role, active, user_id)
    )
    db.commit()

def update_user_password(user_id, new_password):
    db = get_db()
    db.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (new_password, user_id)
    )
    db.commit()
