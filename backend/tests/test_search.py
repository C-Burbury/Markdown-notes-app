def test_no_match(client, register_and_login):
    headers = register_and_login("nomatch@test.com")
    client.post("/notes/", json={"title": "A note", "body": "hello"}, headers=headers)

    response = client.get("/search/", params={"q": "hippo"}, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["next_cursor"] is None

def test_title_outranks_body(client, register_and_login):
    headers = register_and_login("title_vs_body@test.com")
    body_note = client.post("/notes/", json={"title": "No", "body": "Hippo"}, headers=headers).json()
    title_note = client.post("/notes/", json={"title": "Hippo", "body": "no"}, headers=headers).json()

    response = client.get("/search/", params={"q": "hippo"}, headers=headers)
    assert response.status_code == 200
    body = response.json()

    assert body["items"][0]["id"] == title_note["id"]
    assert body["items"][1]["id"] == body_note["id"]
    assert body["items"][0]["rank"] > body["items"][1]["rank"]

def test_multi_word(client, register_and_login):
    headers = register_and_login("multi_word@test.com")
    note_a = client.post("/notes/", json={"title": "Yes", "body": "Hippo Slugs Hippo Hawks"}, headers=headers).json()
    note_b = client.post("/notes/", json={"title": "Yes", "body": "Hippo Slugs Hippo Slugs"}, headers=headers).json()

    response = client.get("/search/", params={"q": "hippo slugs"}, headers=headers)
    assert response.status_code == 200
    body = response.json()

    assert body["items"][0]["id"] == note_b["id"]
    assert body["items"][1]["id"] == note_a["id"]
    assert body["items"][0]["rank"] > body["items"][1]["rank"]

def test_special_chars(client, register_and_login):
    headers = register_and_login("special@test.com")
    response = client.get("/search/", params={"q": "hippo & ! \"quotes\""}, headers=headers)
    assert response.status_code == 200

def test_owner_scoping(client, register_and_login):
    headers_a = register_and_login("owner_a@test.com")
    headers_b = register_and_login("owner_b@test.com")
    client.post("/notes/", json={"title": "Hippo", "body": ""}, headers=headers_a)

    response = client.get("/search/", params={"q": "hippo"}, headers=headers_b)
    assert response.status_code == 200
    assert response.json()["items"] == []

def test_headline_marks(client, register_and_login):
    headers = register_and_login("headline@test.com")
    client.post("/notes/", json={"title": "No", "body": "Hippo here"}, headers=headers)

    response = client.get("/search/", params={"q": "hippo"}, headers=headers)
    body = response.json()
    assert "<mark>" in body["items"][0]["headline"]

def test_cursor_pagination(client, register_and_login):
    headers = register_and_login("cursor_search@test.com")

    for i in range(5):
        client.post("/notes/", json={"title": "Hippo", "body": f"note {i}"}, headers=headers)
    cursor = None
    all_items = []

    while True:
        params = {"q": "hippo", "page_limit": 2}
        if cursor:
            params["cursor"] = cursor
        body = client.get("/search/", headers=headers, params=params).json()
        all_items.extend(body["items"])
        cursor = body["next_cursor"]
        if cursor is None:
            break

    assert len(all_items) == 5
    ids = [i["id"] for i in all_items]
    assert len(ids) == len(set(ids))
    ranks = [i["rank"] for i in all_items]
    assert ranks == sorted(ranks, reverse=True)