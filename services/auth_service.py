from repositories.auth_repository import (
    find_user_by_id_and_password,
    find_user_by_email_and_password
)


def authenticate_user(identifier: str, password: str):
    """
    Returns:
    - (user, None) if success
    - (None, "error text") if failure
    """

    # If the user entered a number → search by ID
    if identifier.isdigit():
        user = find_user_by_id_and_password(int(identifier), password)
    else:
        user = find_user_by_email_and_password(identifier, password)

    if not user:
        return None, "Invalid credentials"

    if user["active"] == 0:
        return None, "User is inactive"

    return user, None
