import sqlite3
from db import get_db


def get_all_users():
    db = get_db()
    return db.execute("SELECT * FROM users").fetchall()


def create_user(firstName: str, lastName: str, email: str, password: str, role: str):
    db = get_db()

    try:
        db.execute("""
            INSERT INTO users (firstName, lastName, email, password, role, active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (firstName, lastName, email, password, role))

        db.commit()
        return "User created", None

    except sqlite3.IntegrityError:
        return None, "Email already exists"
