"""VIS-5 — Operational dashboard summary (acceptance criteria)."""
from __future__ import annotations

from tests.conftest import auth_header


def test_summary_requires_auth(client):
    assert client.get("/dashboard/summary").status_code == 401


def test_summary_counts_match_visits(client):
    admin = auth_header(client)
    for _ in range(3):
        client.post("/visits", headers=admin, json={"address": "x", "status": "scheduled"})
    client.post("/visits", headers=admin, json={"address": "y", "status": "completed"})

    s = client.get("/dashboard/summary", headers=admin)
    assert s.status_code == 200
    data = s.json()
    assert data["total_visits"] == 4
    assert data["by_status"]["scheduled"] == 3
    assert data["by_status"]["completed"] == 1
    assert data["unassigned"] == 3  # 3 active scheduled, none assigned


def test_summary_rbac(client):
    admin = auth_header(client)
    client.post("/users", headers=admin,
                json={"email": "n@visitor.app", "password": "pass-1234",
                      "full_name": "N", "roles": ["cliente"]})
    # cliente has visits:read -> allowed
    cli = auth_header(client, "n@visitor.app", "pass-1234")
    assert client.get("/dashboard/summary", headers=cli).status_code == 200
