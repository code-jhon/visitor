"""Auth and RBAC tests (VIS-2 acceptance criteria)."""
from __future__ import annotations

from app.core.config import settings
from tests.conftest import ADMIN_EMAIL, ADMIN_PASSWORD, auth_header, login


def test_login_success_returns_tokens(client):
    tokens = login(client)
    assert tokens["token_type"] == "bearer"
    assert tokens["access_token"] and tokens["refresh_token"]


def test_login_invalid_password_rejected(client):
    resp = client.post(
        "/auth/login", data={"username": ADMIN_EMAIL, "password": "wrong"}
    )
    assert resp.status_code == 401


def test_protected_endpoint_requires_token(client):
    assert client.get("/users").status_code == 401


def test_admin_can_list_users(client):
    resp = client.get("/users", headers=auth_header(client))
    assert resp.status_code == 200
    assert any(u["email"] == ADMIN_EMAIL for u in resp.json())


def test_refresh_issues_new_access_token(client):
    tokens = login(client)
    resp = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert resp.status_code == 200
    assert resp.json()["access_token"]


def test_refresh_rejects_access_token(client):
    tokens = login(client)
    resp = client.post("/auth/refresh", json={"refresh_token": tokens["access_token"]})
    assert resp.status_code == 401


def test_expired_access_token_rejected(client, monkeypatch):
    # Force an already-expired access token.
    monkeypatch.setattr(settings, "access_token_expire_minutes", -1)
    tokens = login(client)
    resp = client.get(
        "/users", headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert resp.status_code == 401


def test_rbac_denies_insufficient_role(client):
    # Create a cliente (only visits:read) and ensure it cannot list users.
    admin = auth_header(client)
    created = client.post(
        "/users",
        headers=admin,
        json={
            "email": "patient@visitor.app",
            "password": "patient-pass-1",
            "full_name": "Pat Patient",
            "roles": ["cliente"],
        },
    )
    assert created.status_code == 201, created.text

    patient = auth_header(client, "patient@visitor.app", "patient-pass-1")
    assert client.get("/users", headers=patient).status_code == 403
    # But may read its own profile.
    assert client.get("/users/me", headers=patient).status_code == 200


def test_deactivated_user_cannot_login(client):
    admin = auth_header(client)
    created = client.post(
        "/users",
        headers=admin,
        json={
            "email": "emp@visitor.app",
            "password": "emp-pass-123",
            "full_name": "Emp",
            "roles": ["empleado"],
        },
    ).json()

    deact = client.post(f"/users/{created['id']}/deactivate", headers=admin)
    assert deact.status_code == 200
    assert deact.json()["is_active"] is False

    resp = client.post(
        "/auth/login", data={"username": "emp@visitor.app", "password": "emp-pass-123"}
    )
    assert resp.status_code == 403


def test_role_assignment(client):
    admin = auth_header(client)
    user = client.post(
        "/users",
        headers=admin,
        json={
            "email": "coord@visitor.app",
            "password": "coord-pass-1",
            "full_name": "Coord",
            "roles": ["empleado"],
        },
    ).json()

    resp = client.put(
        f"/users/{user['id']}/roles", headers=admin, json={"roles": ["proveedor"]}
    )
    assert resp.status_code == 200
    assert [r["name"] for r in resp.json()["roles"]] == ["proveedor"]


def test_password_reset_flow(client):
    admin = auth_header(client)
    client.post(
        "/users",
        headers=admin,
        json={
            "email": "reset@visitor.app",
            "password": "old-pass-123",
            "full_name": "Reset",
            "roles": ["empleado"],
        },
    )
    req = client.post(
        "/auth/password-reset/request", json={"email": "reset@visitor.app"}
    )
    assert req.status_code == 202
    token = req.json()["reset_token"]

    confirm = client.post(
        "/auth/password-reset/confirm",
        json={"token": token, "new_password": "new-pass-456"},
    )
    assert confirm.status_code == 200

    # Old password fails, new one works.
    assert (
        client.post(
            "/auth/login",
            data={"username": "reset@visitor.app", "password": "old-pass-123"},
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/auth/login",
            data={"username": "reset@visitor.app", "password": "new-pass-456"},
        ).status_code
        == 200
    )


def test_unknown_role_rejected(client):
    admin = auth_header(client)
    resp = client.post(
        "/users",
        headers=admin,
        json={
            "email": "bad@visitor.app",
            "password": "bad-pass-123",
            "full_name": "Bad",
            "roles": ["wizard"],
        },
    )
    assert resp.status_code == 400
