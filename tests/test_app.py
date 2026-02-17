# Test 1: App Loads
def test_home_redirects_to_login(client):
    response = client.get("/")
    assert response.status_code == 302

# Test 2: Login Page Loads
def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200

# Test 3: 
def test_invalid_page_returns_404(client):
    response = client.get("/thispagedoesnotexist")
    assert response.status_code == 404
