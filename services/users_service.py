from repositories.users_repository import (
    fetch_all_users, 
    insert_user,
    find_user_by_email_excluding,
    update_user_admin,
    update_user_password,
    get_user_by_id as repo_get_user_by_id
)


def get_all_users():
    return fetch_all_users()


def create_user(firstName: str, lastName: str, email: str, password: str, role: str):
    success, error = insert_user(firstName, lastName, email, password, role)

    if not success:
        return None, error

    return "User created", None


def admin_update_user(user_id, first, last, email, role, status, new_password):
    existing = find_user_by_email_excluding(email, user_id)
    if existing:
        return None, "This email is already in use"

    update_user_admin(user_id, first, last, email, role, status)

    if new_password:
        update_user_password(user_id, new_password)

    return "User updated successfully", None

def get_user_by_id(user_id):
    return repo_get_user_by_id(user_id)