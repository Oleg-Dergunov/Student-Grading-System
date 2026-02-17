import repositories.users_repository as users_repository
import repositories.courses_repository as courses_repository


def test_users_repository_module_loads():
    assert users_repository is not None


def test_courses_repository_module_loads():
    assert courses_repository is not None

