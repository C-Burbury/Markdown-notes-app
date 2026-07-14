from sqlalchemy import select
from app.models.tag import note_tags

def test_attach_tag(client, register_and_login):
    headers = register_and_login("attach@test.com")
    note = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()
    
    response = client.post(f"/notes/{note['id']}/tags", json={"name": "python"}, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "python"
    assert "id" in body

def test_reattach_tag(client, register_and_login):
    headers = register_and_login("reattach@test.com")
    note = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()
    
    response = client.post(f"/notes/{note['id']}/tags", json={"name": "python"}, headers=headers)
    assert response.status_code == 201

    response = client.post(f"/notes/{note['id']}/tags", json={"name": "python"}, headers=headers)
    assert response.status_code == 201
    body = response.json()
    tags = client.get(f"/notes/{note['id']}/tags", headers=headers).json()
    assert len(tags) == 1
    assert body["name"] == "python"
    assert "id" in body

def test_find_or_create_tag(client, register_and_login):
    headers = register_and_login("find_or_create@test.com")
    note = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()
    note2 = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()

    response = client.post(f"/notes/{note['id']}/tags", json={"name": "python"}, headers=headers)
    assert response.status_code == 201

    response = client.post(f"/notes/{note2['id']}/tags", json={"name": "python"}, headers=headers)
    assert response.status_code == 201

    all_tags = client.get("/tags", headers=headers).json()
    assert len(all_tags) == 1
    assert all_tags[0]["name"] == "python"

def test_get_tag_owner(client, register_and_login):
    headers_a = register_and_login("owner1@test.com")
    headers_b = register_and_login("owner2@test.com")
    note_a = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers_a).json()
    note_b = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers_b).json()

    client.post(f"/notes/{note_a['id']}/tags", json={"name": "python"}, headers=headers_a)
    client.post(f"/notes/{note_b['id']}/tags", json={"name": "education"}, headers=headers_b)

    a_tags = client.get("/tags", headers=headers_a).json()
    b_tags = client.get("/tags", headers=headers_b).json()
    
    assert len(a_tags) == 1
    assert a_tags[0]["name"] == "python"

    assert len(b_tags) == 1
    assert b_tags[0]["name"] == "education"

def test_get_notes_tags(client, register_and_login):
    headers = register_and_login("multi_tags@test.com")
    note_a = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()
    note_b = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()

    client.post(f"/notes/{note_a['id']}/tags", json={"name": "python"}, headers=headers)
    client.post(f"/notes/{note_b['id']}/tags", json={"name": "education"}, headers=headers)

    a_tags = client.get(f"/notes/{note_a['id']}/tags", headers=headers).json()
    b_tags = client.get(f"/notes/{note_b['id']}/tags", headers=headers).json()

    assert len(a_tags) == 1
    assert a_tags[0]["name"] == "python"

    assert len(b_tags) == 1
    assert b_tags[0]["name"] == "education"

def test_detach_tag(client, register_and_login):
    headers = register_and_login("detach@test.com")
    note = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()

    tag = client.post(f"/notes/{note['id']}/tags", json={"name": "python"}, headers=headers).json()

    response = client.delete(f"/notes/{note['id']}/tags/{tag['id']}", headers=headers)
    assert response.status_code == 204

    tags = client.get(f"/notes/{note['id']}/tags", headers=headers).json()

    assert len(tags) == 0

def test_detach_not_attached(client, register_and_login):
    headers = register_and_login("detach_none@test.com")
    note = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()

    response = client.delete(f"/notes/{note['id']}/tags/9999", headers=headers)
    assert response.status_code == 204

def test_cross_user_delete(client, register_and_login):
    headers_a = register_and_login("cross_deletea@test.com")
    headers_b = register_and_login("cross_deleteb@test.com")

    note_a = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers_a).json()
    tag = client.post(f"/notes/{note_a['id']}/tags", json={"name": "python"}, headers=headers_a).json()

    response = client.delete(f"/notes/{note_a['id']}/tags/{tag['id']}", headers=headers_b)
    assert response.status_code == 404

def test_cross_user_attach(client, register_and_login):
    headers_a = register_and_login("cross_attacha@test.com")
    headers_b = register_and_login("cross_attachb@test.com")

    note_a = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers_a).json()

    response = client.post(f"/notes/{note_a['id']}/tags", json={"name": "python"}, headers=headers_b)
    assert response.status_code == 404

def test_cross_user_get(client, register_and_login):
    headers_a = register_and_login("cross_geta@test.com")
    headers_b = register_and_login("cross_getb@test.com")

    note_a = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers_a).json()

    response = client.get(f"/notes/{note_a['id']}/tags", headers=headers_b)
    assert response.status_code == 404

def test_note_delete_cascades(client, register_and_login, db_session):
    headers = register_and_login("cascade@test.com")
    note = client.post("/notes/", json={"title": "Note", "body": ""}, headers=headers).json()
    client.post(f"/notes/{note['id']}/tags", json={"name": "python"}, headers=headers)

    client.delete(f"/notes/{note['id']}", headers=headers)

    rows = db_session.execute(
        select(note_tags).where(note_tags.c.note_id == note["id"])
    ).all()
    assert rows == []