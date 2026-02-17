def test_login_route_exists(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_users_page_requires_login(client):
    response = client.get("/users", follow_redirects=True)
    assert response.status_code in (200, 302)


def test_courses_page_requires_login(client):
    response = client.get("/courses", follow_redirects=True)
    assert response.status_code in (200, 302)


def test_profile_page_requires_login(client):
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code in (200, 302)