"""Master-data CRUD and RBAC tests (VIS-3 acceptance criteria)."""
from __future__ import annotations

from tests.conftest import auth_header


def _make_user(client, admin, email, role):
    resp = client.post(
        "/users",
        headers=admin,
        json={"email": email, "password": "pass-1234", "full_name": email, "roles": [role]},
    )
    assert resp.status_code == 201, resp.text
    return auth_header(client, email, "pass-1234")


# --- CRUD ------------------------------------------------------------------
def test_service_crud_roundtrip(client):
    admin = auth_header(client)

    created = client.post("/services", headers=admin, json={"name": "Nursing"})
    assert created.status_code == 201, created.text
    svc = created.json()
    assert svc["name"] == "Nursing" and svc["is_active"] is True

    listed = client.get("/services", headers=admin)
    assert listed.status_code == 200
    assert any(s["id"] == svc["id"] for s in listed.json())

    got = client.get(f"/services/{svc['id']}", headers=admin)
    assert got.status_code == 200

    patched = client.patch(
        f"/services/{svc['id']}", headers=admin, json={"description": "Home nursing"}
    )
    assert patched.status_code == 200
    assert patched.json()["description"] == "Home nursing"

    deleted = client.delete(f"/services/{svc['id']}", headers=admin)
    assert deleted.status_code == 204
    assert client.get(f"/services/{svc['id']}", headers=admin).status_code == 404


def test_subservice_links_to_service(client):
    admin = auth_header(client)
    svc = client.post("/services", headers=admin, json={"name": "Therapy"}).json()
    sub = client.post(
        "/subservices",
        headers=admin,
        json={"service_id": svc["id"], "name": "Physio"},
    )
    assert sub.status_code == 201, sub.text
    assert sub.json()["service_id"] == svc["id"]


def test_tariff_amount_and_validation(client):
    admin = auth_header(client)
    svc = client.post("/services", headers=admin, json={"name": "Care"}).json()
    ok = client.post(
        "/tariffs",
        headers=admin,
        json={"service_id": svc["id"], "name": "Std", "amount": "49.90"},
    )
    assert ok.status_code == 201, ok.text
    assert str(ok.json()["amount"]) in ("49.9", "49.90")

    bad = client.post(
        "/tariffs",
        headers=admin,
        json={"service_id": svc["id"], "name": "Neg", "amount": "-5"},
    )
    assert bad.status_code == 422  # amount ge=0


def test_required_field_validation(client):
    admin = auth_header(client)
    # Employee requires first_name/last_name.
    resp = client.post("/employees", headers=admin, json={"first_name": "Ana"})
    assert resp.status_code == 422


def test_visit_uses_status_enum(client):
    admin = auth_header(client)
    cli = client.post(
        "/clients", headers=admin, json={"first_name": "Bob", "last_name": "Lee"}
    ).json()
    visit = client.post(
        "/visits",
        headers=admin,
        json={"client_id": cli["id"], "address": "1 Main St", "status": "scheduled"},
    )
    assert visit.status_code == 201, visit.text
    assert visit.json()["status"] == "scheduled"

    bad = client.post("/visits", headers=admin, json={"status": "teleported"})
    assert bad.status_code == 422


def test_status_event_is_append_only(client):
    admin = auth_header(client)
    visit = client.post("/visits", headers=admin, json={"address": "x"}).json()
    ev = client.post(
        "/visit-status-events",
        headers=admin,
        json={"visit_id": visit["id"], "status": "en_route"},
    )
    assert ev.status_code == 201, ev.text
    # No update/delete routes are registered for the append-only log.
    assert client.patch(
        f"/visit-status-events/{ev.json()['id']}", headers=admin, json={"note": "x"}
    ).status_code == 405
    assert client.delete(
        f"/visit-status-events/{ev.json()['id']}", headers=admin
    ).status_code == 405


# --- RBAC ------------------------------------------------------------------
def test_rbac_read_requires_permission(client):
    # cliente role does not hold services:read.
    patient = _make_user(client, auth_header(client), "c1@visitor.app", "cliente")
    assert client.get("/services", headers=patient).status_code == 403


def test_rbac_write_denied_for_read_only_role(client):
    # empleado holds clients:read but not clients:write.
    emp = _make_user(client, auth_header(client), "e1@visitor.app", "empleado")
    assert client.get("/clients", headers=emp).status_code == 200
    denied = client.post(
        "/clients", headers=emp, json={"first_name": "No", "last_name": "Way"}
    )
    assert denied.status_code == 403


def test_protected_endpoints_require_auth(client):
    assert client.get("/services").status_code == 401
    assert client.get("/visits").status_code == 401
