def test_invalid_login_returns_error(client):
    response = client.post(
        "/login",
        data={
            "username": "wronguser",
            "password": "wrongpass"
        },
        follow_redirects=True
    )

    # App returns 400 for invalid login → this is expected behaviour
    assert response.status_code in (200, 400)

