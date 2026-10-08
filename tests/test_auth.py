async def test_register_login_me(client):
    r = await client.post("/api/v1/auth/register", json={"email": "x@example.com", "password": "password123"})
    assert r.status_code == 201
    dup = await client.post("/api/v1/auth/register", json={"email": "x@example.com", "password": "password123"})
    assert dup.status_code == 409

    bad = await client.post("/api/v1/auth/login", data={"username": "x@example.com", "password": "nope"})
    assert bad.status_code == 401

    token = (
        await client.post("/api/v1/auth/login", data={"username": "x@example.com", "password": "password123"})
    ).json()["access_token"]
    me = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["email"] == "x@example.com"
    assert me.json()["is_admin"] is False


async def test_protected_requires_token(client):
    assert (await client.get("/api/v1/subjects")).status_code == 401
