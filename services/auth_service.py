from db import get_db


def authenticate_user(identifier: str, password: str):
    """
    Возвращает:
    - (user, None) если всё ок
    - (None, "текст ошибки") если ошибка
    """

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

    if not user:
        return None, "Invalid credentials"

    if user["active"] == 0:
        return None, "User is inactive"

    return user, None