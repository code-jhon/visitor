"""VIS-4 — Audit trail and sensitive-field protection (acceptance criteria)."""
from __future__ import annotations

from app.services.audit import mask_fields
from tests.conftest import auth_header


def test_record_and_query_audit(client, db_session):
    from app.services.audit import record_audit

    admin = auth_header(client)
    record_audit(db_session, action="visit.start", entity_type="visit",
                 entity_id="v1", before={"status": "scheduled"},
                 after={"status": "in_progress"}, latitude=4.6, longitude=-74.1)

    res = client.get("/audit-logs", headers=admin, params={"entity_type": "visit"})
    assert res.status_code == 200
    rows = res.json()
    assert len(rows) == 1
    assert rows[0]["action"] == "visit.start"
    assert "in_progress" in rows[0]["after"]


def test_audit_log_is_append_only(client):
    """No write routes exist on the audit-log resource."""
    admin = auth_header(client)
    assert client.post("/audit-logs", headers=admin, json={}).status_code in (404, 405)
    assert client.delete("/audit-logs/anything", headers=admin).status_code in (404, 405)


def test_audit_read_requires_permission(client):
    admin = auth_header(client)
    # empresa role does NOT have audit:read
    client.post("/users", headers=admin,
                json={"email": "emp@visitor.app", "password": "pass-1234",
                      "full_name": "E", "roles": ["empresa"]})
    emp = auth_header(client, "emp@visitor.app", "pass-1234")
    assert client.get("/audit-logs", headers=emp).status_code == 403
    # soporte does have it
    client.post("/users", headers=admin,
                json={"email": "sop@visitor.app", "password": "pass-1234",
                      "full_name": "S", "roles": ["soporte"]})
    sop = auth_header(client, "sop@visitor.app", "pass-1234")
    assert client.get("/audit-logs", headers=sop).status_code == 200


def test_mask_fields_helper():
    data = {"first_name": "Ana", "medical_notes": "sensitive"}
    masked = mask_fields(data, sensitive=["medical_notes"], allowed=False)
    assert masked["medical_notes"] == ""
    assert masked["first_name"] == "Ana"
    full = mask_fields(data, sensitive=["medical_notes"], allowed=True)
    assert full["medical_notes"] == "sensitive"
