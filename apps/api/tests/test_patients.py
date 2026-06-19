"""VIS-7 — Clients/Patients: search, calendar and sensitive-field masking."""
from __future__ import annotations

from tests.conftest import auth_header


def _patient(client, admin, first, last, notes=""):
    r = client.post("/patients", headers=admin,
                    json={"first_name": first, "last_name": last, "medical_notes": notes})
    assert r.status_code == 201, r.text
    return r.json()


def test_patient_search(client):
    admin = auth_header(client)
    _patient(client, admin, "Dora", "Sol")
    _patient(client, admin, "Edu", "Mar")
    res = client.get("/patients/search", headers=admin, params={"q": "dora"})
    assert res.status_code == 200
    assert [p["first_name"] for p in res.json()] == ["Dora"]


def test_sensitive_notes_masked_by_role(client):
    admin = auth_header(client)
    p = _patient(client, admin, "Fina", "Paz", notes="diabetic")

    # admin (sensitive) sees notes
    res = client.get("/patients/search", headers=admin, params={"q": "fina"})
    assert res.json()[0]["medical_notes"] == "diabetic"

    # proveedor has patients:read but is not a sensitive role -> notes masked
    client.post("/users", headers=admin,
                json={"email": "pv@visitor.app", "password": "pass-1234",
                      "full_name": "Pv", "roles": ["proveedor"]})
    prov = auth_header(client, "pv@visitor.app", "pass-1234")
    res2 = client.get("/patients/search", headers=prov, params={"q": "fina"})
    assert res2.status_code == 200
    assert res2.json()[0]["medical_notes"] == ""


def test_patient_calendar_reflects_visits(client):
    admin = auth_header(client)
    p = _patient(client, admin, "Gus", "Rio")
    client.post("/visits", headers=admin,
                json={"patient_id": p["id"], "address": "9 Ave", "status": "scheduled",
                      "scheduled_start": "2026-08-01T08:00:00Z"})
    cal = client.get(f"/patients/{p['id']}/calendar", headers=admin)
    assert cal.status_code == 200
    assert len(cal.json()["visits"]) == 1
    assert cal.json()["visits"][0]["status"] == "scheduled"


def test_calendar_404_and_rbac(client):
    admin = auth_header(client)
    assert client.get("/patients/none/calendar", headers=admin).status_code == 404
