"""VIS-6 — Employees: search, availability and RBAC (acceptance criteria)."""
from __future__ import annotations

from tests.conftest import auth_header


def _emp(client, admin, first, last, **extra):
    body = {"first_name": first, "last_name": last, **extra}
    r = client.post("/employees", headers=admin, json=body)
    assert r.status_code == 201, r.text
    return r.json()


def test_employee_search_by_name_and_filters(client):
    admin = auth_header(client)
    _emp(client, admin, "Ana", "Gomez", position="Nurse", document_id="A1")
    _emp(client, admin, "Beto", "Ruiz", position="Driver", document_id="B2", is_active=False)

    by_name = client.get("/employees/search", headers=admin, params={"q": "ana"})
    assert by_name.status_code == 200
    assert [e["first_name"] for e in by_name.json()] == ["Ana"]

    by_doc = client.get("/employees/search", headers=admin, params={"document_id": "B2"})
    assert [e["last_name"] for e in by_doc.json()] == ["Ruiz"]

    actives = client.get("/employees/search", headers=admin, params={"is_active": "true"})
    assert all(e["is_active"] for e in actives.json())


def test_employee_availability_reflects_visits(client):
    admin = auth_header(client)
    emp = _emp(client, admin, "Carl", "Diaz")

    avail = client.get(f"/employees/{emp['id']}/availability", headers=admin)
    assert avail.status_code == 200
    assert avail.json()["available"] is True
    assert avail.json()["busy_slots"] == []

    visit = client.post(
        "/visits", headers=admin,
        json={"address": "1 St", "status": "scheduled",
              "scheduled_start": "2026-07-01T09:00:00Z",
              "scheduled_end": "2026-07-01T11:00:00Z"},
    ).json()
    client.post(
        "/visit-assignments", headers=admin,
        json={"visit_id": visit["id"], "employee_id": emp["id"]},
    )
    busy = client.get(f"/employees/{emp['id']}/availability", headers=admin)
    assert busy.json()["available"] is False
    assert len(busy.json()["busy_slots"]) == 1
    assert busy.json()["busy_slots"][0]["visit_id"] == visit["id"]


def test_employee_availability_404(client):
    admin = auth_header(client)
    assert client.get("/employees/none/availability", headers=admin).status_code == 404


def test_employee_search_requires_permission(client):
    admin = auth_header(client)
    client.post(
        "/users", headers=admin,
        json={"email": "c2@visitor.app", "password": "pass-1234",
              "full_name": "C", "roles": ["cliente"]},
    )
    cli = auth_header(client, "c2@visitor.app", "pass-1234")
    assert client.get("/employees/search", headers=cli).status_code == 403
