"""Test fixtures: in-memory SQLite app with seeded RBAC data (VIS-2).

Tables are created from the ORM metadata (the Alembic migration targets
PostgreSQL); roles, permissions and an admin user mirror the migration seed so
the API behaves identically under test.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.db.models import Permission, Role, User
from app.db.session import Base, get_db
from app.main import app

# Mirror of the migration seed (app/db/migrations/versions/0001_auth_rbac.py).
ROLES = ["admin", "empresa", "empleado", "proveedor", "cliente", "soporte"]
PERMISSIONS = [
    "users:read",
    "users:write",
    "roles:assign",
    "visits:read",
    "visits:write",
    "reports:read",
]
ROLE_PERMISSIONS = {
    "admin": PERMISSIONS,
    "empresa": ["users:read", "users:write", "roles:assign", "visits:read", "visits:write", "reports:read"],
    "proveedor": ["visits:read", "visits:write", "reports:read", "users:read"],
    "empleado": ["visits:read", "visits:write"],
    "soporte": ["users:read", "visits:read"],
    "cliente": ["visits:read"],
}

ADMIN_EMAIL = "admin@visitor.app"
ADMIN_PASSWORD = "admin-pass-123"


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSession()

    perms = {code: Permission(code=code, description=code) for code in PERMISSIONS}
    roles = {}
    for name in ROLES:
        roles[name] = Role(
            name=name,
            description=name,
            permissions=[perms[c] for c in ROLE_PERMISSIONS[name]],
        )
    admin = User(
        email=ADMIN_EMAIL,
        hashed_password=hash_password(ADMIN_PASSWORD),
        full_name="Administrator",
        is_active=True,
        roles=[roles["admin"]],
    )
    session.add_all([*perms.values(), *roles.values(), admin])
    session.commit()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def login(client, email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
    resp = client.post("/auth/login", data={"username": email, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()


def auth_header(client, email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
    tokens = login(client, email, password)
    return {"Authorization": f"Bearer {tokens['access_token']}"}
