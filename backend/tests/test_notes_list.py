from datetime import datetime
from app.models.note import Note

def test_list_empty(client, register_and_login):
    headers = register_and_login("empty@test.com")

    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["next_cursor"] is None

def test_single_page(client, register_and_login):
    headers = register_and_login("single@test.com")

    for i in range(2):
        client.post("/notes/", json={"title": f"Note {i}", "body": ""}, headers=headers)

    response = client.get("/notes/", headers=headers, params={"page_limit": 3})
    body = response.json()
    assert len(body["items"]) == 2
    assert body["next_cursor"] is None

def test_multi_page_traversal(client, register_and_login):
    headers = register_and_login("multi@test.com")

    for i in range(25):
        client.post("/notes/", json={"title": f"Note {i}", "body": ""}, headers=headers)
    cursor = None
    all_notes = []

    while True:
        params = {"page_limit": 2}
        if cursor:
            params["cursor"] = cursor
        response = client.get("/notes/", headers=headers, params=params)
        body = response.json()
        all_notes.extend(body["items"])
        cursor = body["next_cursor"]
        if cursor is None:
            break
    assert len(all_notes) == 25
    ids = [n["id"] for n in all_notes]
    assert len(ids) == len(set(ids))

    timestamps = [n["created_at"] for n in all_notes]
    assert timestamps == sorted(timestamps, reverse=True)

def test_owner_scoping(client, register_and_login):
    headers_a = register_and_login("a@test.com")
    headers_b = register_and_login("b@test.com")

    for i in range(2):
        client.post("/notes/", json={"title": f"Note {i}", "body": ""}, headers=headers_a)

    response = client.get("/notes/", headers=headers_b, params={"page_limit": 3})
    body = response.json()
    assert body["items"] == []
    assert body["next_cursor"] is None

def test_tiebreaker_ordering(client, register_and_login, db_session):
    headers = register_and_login("tie@test.com")
    user_id = client.get("/user/me", headers=headers).json()["id"]
    fixed_ts = datetime(2025, 1, 1, 12, 0, 0)

    for i in range(3):
        note = Note(title=f"Note {i}", body="", user_id=user_id, created_at=fixed_ts)
        db_session.add(note)
    db_session.commit()

    cursor = None
    all_notes = []
    while True:
        params = {"page_limit": 2}
        if cursor:
            params["cursor"] = cursor
        response = client.get("/notes/", headers=headers, params=params)
        body = response.json()
        all_notes.extend(body["items"])
        cursor = body["next_cursor"]
        if cursor is None:
            break

    assert len(all_notes) == 3
    ids = [n["id"] for n in all_notes]
    assert len(ids) == len(set(ids))
    assert ids == sorted(ids, reverse=True)

def test_created_after(client, register_and_login, db_session):
    headers = register_and_login("created_after@test.com")
    user_id = client.get("/user/me", headers=headers).json()["id"]
    old_ts = datetime(2024, 1, 1, 12, 0, 0)
    new_ts = datetime(2025, 1, 1, 12, 0, 0)
    db_session.add(Note(title="Old", body="", user_id=user_id, created_at=old_ts))
    db_session.add(Note(title="New", body="", user_id=user_id, created_at=new_ts))
    db_session.commit()

    response = client.get("/notes/", headers=headers, params={"created_after": "2024-06-01T00:00:00"})
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["title"] == "New"

def test_created_before(client, register_and_login, db_session):
    headers = register_and_login("created_before@test.com")
    user_id = client.get("/user/me", headers=headers).json()["id"]
    old_ts = datetime(2024, 1, 1, 12, 0, 0)
    new_ts = datetime(2025, 1, 1, 12, 0, 0)
    db_session.add(Note(title="Old", body="", user_id=user_id, created_at=old_ts))
    db_session.add(Note(title="New", body="", user_id=user_id, created_at=new_ts))
    db_session.commit()

    response = client.get("/notes/", headers=headers, params={"created_before": "2024-06-01T00:00:00"})
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["title"] == "Old"

def test_date_range_filter(client, register_and_login, db_session):
    headers = register_and_login("range@test.com")
    user_id = client.get("/user/me", headers=headers).json()["id"]
    db_session.add(Note(title="Too Old", body="", user_id=user_id, created_at=datetime(2023, 1, 1)))
    db_session.add(Note(title="In Range", body="", user_id=user_id, created_at=datetime(2024, 6, 1)))
    db_session.add(Note(title="Too New", body="", user_id=user_id, created_at=datetime(2026, 1, 1)))
    db_session.commit()

    response = client.get("/notes/", headers=headers, params={
        "created_after": "2024-01-01T00:00:00",
        "created_before": "2025-01-01T00:00:00"
    })
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["title"] == "In Range"

def test_ascending_order(client, register_and_login, db_session):
    headers = register_and_login("asc@test.com")
    user_id = client.get("/user/me", headers=headers).json()["id"]

    for i in range(5):
        db_session.add(Note(title=f"Note {i}", body="", user_id=user_id, created_at=datetime(2025, 1, i + 1)))
    db_session.commit()

    cursor = None
    all_notes = []
    while True:
        params = {"page_limit": 2, "sort": "asc"}
        if cursor:
            params["cursor"] = cursor
        response = client.get("/notes/", headers=headers, params=params)
        body = response.json()
        all_notes.extend(body["items"])
        cursor = body["next_cursor"]
        if cursor is None:
            break

    assert len(all_notes) == 5
    ids = [n["id"] for n in all_notes]
    assert len(ids) == len(set(ids))
    timestamps = [n["created_at"] for n in all_notes]
    assert timestamps == sorted(timestamps)

def test_tag_filter(client, register_and_login):
    headers = register_and_login("tagfilter@test.com")

    note_a = client.post("/notes/", json={"title": "Tagged", "body": ""}, headers=headers).json()
    note_b = client.post("/notes/", json={"title": "Untagged", "body": ""}, headers=headers).json()

    client.post(f"/notes/{note_a['id']}/tags", json={"name": "python"}, headers=headers)

    response = client.get("/notes/", headers=headers, params={"tag": "python"})
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 1
    assert items[0]["id"] == note_a["id"]
    assert all(item["id"] != note_b["id"] for item in items)

