from repositories.users_repository import (
    fetch_all_users, 
    insert_user,
    find_user_by_email_excluding,
    update_user_admin,
    update_user_password,
    get_user_by_id as repo_get_user_by_id
)


def get_user_by_id(user_id):
    return repo_get_user_by_id(user_id)


def get_all_users():
    return fetch_all_users()


def create_user(first_name: str, last_name: str, email: str, password: str, role: str):
    success, error = insert_user(first_name, last_name, email, password, role)

    if not success:
        return None, error

    return "User created", None


def admin_update_user(user_id, first_name, last_name, email, role, status, new_password):
    # Load current user
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found"

    # Check email uniqueness
    existing = find_user_by_email_excluding(email, user_id)
    if existing:
        return None, "This email is already in use"

    # Check if anything changed
    no_changes = (
        user["first_name"] == first_name and
        user["last_name"] == last_name and
        user["email"] == email and
        user["role"] == role and
        user["active"] == status and
        not new_password
    )

    if no_changes:
        return None, None

    # Update main fields
    update_user_admin(user_id, first_name, last_name, email, role, status)

    # Update password if provided
    if new_password:
        update_user_password(user_id, new_password)

    return "User updated successfully", None
