from repositories.users_repository import (
    find_user_with_email,
    update_user_email,
    update_user_password,
    get_user_by_id
)


def update_email(user_id: int, new_email: str):
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found"

    if user["email"] == new_email:
        return None, None

    existing = find_user_with_email(new_email, user_id)
    if existing:
        return None, "This email is already in use"

    update_user_email(user_id, new_email)
    return "Email updated", None



def change_password(user, old_password: str, new_password: str, repeat_password: str):
   
    if old_password != user["password"]:
        return None, "The old password is incorrect"

    if new_password == user["password"]:
        return None, "Entered new password matches the old one"

    if new_password != repeat_password:
        return None, "The new passwords do not match."

    if not new_password:
        return None, "The password cannot be empty"

    update_user_password(user["id"], new_password)
    return "Password successfully changed", None
