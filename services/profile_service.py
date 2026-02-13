from db import get_db


def update_email(user_id: int, new_email: str):
    """
    Returns:
    - (None, "error text") if error
    - ("Email updated", None) if success
    """

    db = get_db()

    # Check that the email address is not occupied by another user.
    existing = db.execute(
        "SELECT id FROM users WHERE LOWER(email)=LOWER(?) AND id != ?",
        (new_email, user_id)
    ).fetchone()

    if existing:
        return None, "This email is already in use"

    # Updating email
    db.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    db.commit()

    return "Email updated", None



def change_password(user, old_password: str, new_password: str, repeat_password: str):
    """
    Returns:
    - (None, "error text") if error
    - ("Password successfully changed", None) if success
    """

    if old_password != user["password"]:
        return None, "The old password is incorrect"

    if new_password != repeat_password:
        return None, "The new passwords do not match."

    if not new_password:
        return None, "The password cannot be empty"

    db = get_db()
    db.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (new_password, user["id"])
    )
    db.commit()

    return "Password successfully changed", None
