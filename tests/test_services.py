import services.auth_service as auth_service
import services.users_service as users_service
import services.courses_service as courses_service


def test_auth_service_module_loads():
    assert auth_service is not None


def test_users_service_module_loads():
    assert users_service is not None


def test_courses_service_module_loads():
    assert courses_service is not None
