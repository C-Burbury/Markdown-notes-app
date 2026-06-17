def test_register_success(client):
    response = client.post("/auth/register", json = {
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["email"] == "test@example.com"
    assert "password_hash" not in body

def test_duplicate_email(client):
    client.post("/auth/register", json = {
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/auth/register", json = {
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 409

def test_login_success(client):
    client.post("/auth/register", json = {
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json = {
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_bad_password(client):
    client.post("/auth/register", json = {
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json = {
        "email": "test@example.com",
        "password": "password1234"
    })
    assert response.status_code == 401