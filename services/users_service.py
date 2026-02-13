from repositories.users_repository import fetch_all_users, insert_user


def get_all_users():
    return fetch_all_users()


def create_user(firstName: str, lastName: str, email: str, password: str, role: str):
    success, error = insert_user(firstName, lastName, email, password, role)

    if not success:
        return None, error

    return "User created", None