"""VIS-9 — Configuration: tariff modalities and validity (acceptance criteria)."""
from __future__ import annotations

from tests.conftest import auth_header


def _service(client, admin):
    return client.post("/services", headers=admin, json={"name": "Nursing"}).json()


def test_tariff_modalities_supported(client):
    admin = auth_header(client)
    svc = _service(client, admin)
    for modality in ("per_service", "per_hour", "per_km"):
        resp = client.post(
            "/tariffs",
            headers=admin,
            json={
                "service_id": svc["id"],
                "name": f"T-{modality}",
                "modality": modality,
                "amount": "20.00",
            },
        )
        assert resp.status_code == 201, resp.text
        assert resp.json()["modality"] == modality


def test_per_provider_requires_provider(client):
    admin = auth_header(client)
    svc = _service(client, admin)
    bad = client.post(
        "/tariffs",
        headers=admin,
        json={"service_id": svc["id"], "name": "P", "modality": "per_provider", "amount": "10"},
    )
    assert bad.status_code == 422

    prov = client.post("/providers", headers=admin, json={"name": "Acme"}).json()
    ok = client.post(
        "/tariffs",
        headers=admin,
        json={
            "service_id": svc["id"],
            "name": "P",
            "modality": "per_provider",
            "provider_id": prov["id"],
            "amount": "10",
        },
    )
    assert ok.status_code == 201, ok.text
    assert ok.json()["provider_id"] == prov["id"]


def test_validity_range_validation(client):
    admin = auth_header(client)
    svc = _service(client, admin)
    bad = client.post(
        "/tariffs",
        headers=admin,
        json={
            "service_id": svc["id"],
            "name": "V",
            "amount": "10",
            "valid_from": "2026-06-30",
            "valid_to": "2026-06-01",
        },
    )
    assert bad.status_code == 422


def test_config_write_requires_permission(client):
    """A cliente role cannot modify configuration."""
    admin = auth_header(client)
    svc = _service(client, admin)
    client.post(
        "/users",
        headers=admin,
        json={"email": "cli@visitor.app", "password": "pass-1234",
              "full_name": "Cli", "roles": ["cliente"]},
    )
    cli = auth_header(client, "cli@visitor.app", "pass-1234")
    resp = client.post(
        "/tariffs", headers=cli,
        json={"service_id": svc["id"], "name": "X", "amount": "1"},
    )
    assert resp.status_code == 403
