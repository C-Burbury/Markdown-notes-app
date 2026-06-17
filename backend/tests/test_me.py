def test_me_no_token(client):
    response = client.get("/user/me")
    assert response.status_code == 401

def test_me_bad_token(client):
    response = client.get("/user/me", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401

def test_me_valid_token(client):
    client.post("/auth/register", json={"email": "me@example.com", "password": "password123"})
    login = client.post("/auth/login", json={"email": "me@example.com", "password": "password123"})
    token = login.json()["access_token"]

    response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "me@example.com"
    assert "id" in body
    assert "password_hash" not in body