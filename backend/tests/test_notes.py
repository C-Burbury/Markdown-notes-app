def test_post_creates(client, register_and_login):
    headers = register_and_login("a@test.com")
    response = client.post("/notes/", json={"title": "A note", "body": "hello"}, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["title"] == "A note"
    assert body["user_id"] is not None

def test_get_own_note(client, register_and_login):
    headers_a = register_and_login("a@test.com")
    note = client.post("/notes/", json={"title": "A note", "body": ""}, headers=headers_a).json()

    response = client.get(f"/notes/{note['id']}", headers=headers_a)
    assert response.status_code == 200

def test_patch_own_note(client, register_and_login):
    headers_a = register_and_login("a@test.com")
    note = client.post("/notes/", json={"title": "A note", "body": ""}, headers=headers_a).json()

    response = client.patch(f"/notes/{note['id']}", json={"title": "Updated"}, headers=headers_a)
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated"
    assert body["body"] == ""

def test_delete_own_note(client, register_and_login):
    headers_a = register_and_login("a@test.com")
    note = client.post("/notes/", json={"title": "A note", "body": ""}, headers=headers_a).json()

    response = client.delete(f"/notes/{note['id']}", headers=headers_a)
    assert response.status_code == 204

    response = client.get(f"/notes/{note['id']}", headers=headers_a)
    assert response.status_code == 404

def test_cross_user_get(client, register_and_login):
    headers_a = register_and_login("a@test.com")
    headers_b = register_and_login("b@test.com")

    note = client.post("/notes/", json={"title": "A note", "body": ""}, headers=headers_a).json()

    response = client.get(f"/notes/{note['id']}", headers=headers_b)
    assert response.status_code == 404

def test_cross_user_patch(client, register_and_login):
    headers_a = register_and_login("a@test.com")
    headers_b = register_and_login("b@test.com")

    note = client.post("/notes/", json={"title": "A note", "body": ""}, headers=headers_a).json()

    response = client.patch(f"/notes/{note['id']}", json={"title": "Updated"}, headers=headers_b)
    assert response.status_code == 404

def test_cross_user_delete(client, register_and_login):
    headers_a = register_and_login("a@test.com")
    headers_b = register_and_login("b@test.com")

    note = client.post("/notes/", json={"title": "A note", "body": ""}, headers=headers_a).json()

    response = client.delete(f"/notes/{note['id']}", headers=headers_b)
    assert response.status_code == 404

def test_no_token(client):
    response = client.post("/notes/", json={"title": "A note", "body": ""})
    assert response.status_code == 401

    response = client.get("/notes/1")
    assert response.status_code == 401   