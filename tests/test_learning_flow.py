QUIZ = {
    "questions": [
        {"text": "2+2?", "options": ["3", "4"], "correct": [1]},
        {"text": "Cell powerhouse?", "options": ["Nucleus", "Mitochondria"], "correct": [1]},
    ],
    "pass_score": 100,
}


async def _setup(client, admin_headers):
    s = await client.post("/api/v1/admin/subjects", json={"title": "Biology"}, headers=admin_headers)
    sid = s.json()["id"]
    mods = {}
    for key, type_, content in [
        ("theory", "theoretical", {"body": "# Cells"}),
        ("quiz", "quiz", QUIZ),
        ("practice", "practical", {"instructions": "Lab", "steps": [{"text": "a"}, {"text": "b", "required": False}]}),
    ]:
        r = await client.post(
            "/api/v1/admin/modules",
            json={"subject_id": sid, "type": type_, "title": key, "content": content},
            headers=admin_headers,
        )
        assert r.status_code == 201, r.text
        mods[key] = r.json()["id"]
    return sid, mods


async def test_admin_only(client, user_headers):
    r = await client.post("/api/v1/admin/subjects", json={"title": "X"}, headers=user_headers)
    assert r.status_code == 403


async def test_invalid_content_rejected(client, admin_headers):
    sid = (await client.post("/api/v1/admin/subjects", json={"title": "B"}, headers=admin_headers)).json()["id"]
    bad = {"questions": [{"text": "q", "options": ["a", "b"], "correct": [5]}]}
    r = await client.post(
        "/api/v1/admin/modules",
        json={"subject_id": sid, "type": "quiz", "title": "q", "content": bad},
        headers=admin_headers,
    )
    assert r.status_code == 422


async def test_quiz_hides_answers(client, admin_headers, user_headers):
    sid, mods = await _setup(client, admin_headers)
    r = await client.get(f"/api/v1/modules/{mods['quiz']}", headers=user_headers)
    assert all("correct" not in q for q in r.json()["content"]["questions"])


async def test_submit_and_progress(client, admin_headers, user_headers):
    sid, mods = await _setup(client, admin_headers)

    r = await client.post(f"/api/v1/modules/{mods['quiz']}/submit", json={"answers": [[1], [0]]}, headers=user_headers)
    assert r.json() == {"score": 50.0, "passed": False, "feedback": "1/2 correct"}
    r = await client.post(f"/api/v1/modules/{mods['quiz']}/submit", json={"answers": [[1], [1]]}, headers=user_headers)
    assert r.json()["passed"] is True

    r = await client.post(f"/api/v1/modules/{mods['theory']}/submit", json={}, headers=user_headers)
    assert r.json()["passed"] is True

    r = await client.post(
        f"/api/v1/modules/{mods['practice']}/submit", json={"completed_steps": [1]}, headers=user_headers
    )
    assert r.json()["passed"] is False

    prog = {p["module_id"]: p for p in (await client.get("/api/v1/progress", headers=user_headers)).json()}
    assert prog[mods["quiz"]]["attempts"] == 2 and prog[mods["quiz"]]["score"] == 100.0

    summary = (await client.get(f"/api/v1/progress/subjects/{sid}", headers=user_headers)).json()
    assert summary["total_modules"] == 3 and summary["completed_modules"] == 2


async def test_bad_submission(client, admin_headers, user_headers):
    _, mods = await _setup(client, admin_headers)
    r = await client.post(f"/api/v1/modules/{mods['quiz']}/submit", json={"answers": [[1]]}, headers=user_headers)
    assert r.status_code == 422
