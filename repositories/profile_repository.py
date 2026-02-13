from db import get_db


def find_user_with_email(email: str, exclude_user_id: int):
    db = get_db()
    return db.execute(
        "SELECT id FROM users WHERE LOWER(email)=LOWER(?) AND id != ?",
        (email, exclude_user_id)
    ).fetchone()


def update_user_email(user_id: int, new_email: str):
    db = get_db()
    db.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    db.commit()


def update_user_password(user_id: int, new_password: str):
    db = get_db()
    db.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (new_password, user_id)
    )
    db.commit()