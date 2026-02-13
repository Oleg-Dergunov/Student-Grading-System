from db import get_db


def find_user_by_id_and_password(user_id: int, password: str):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ? AND password = ?",
        (user_id, password)
    ).fetchone()


def find_user_by_email_and_password(email: str, password: str):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE LOWER(email) = LOWER(?) AND password = ?",
        (email, password)
    ).fetchone()
