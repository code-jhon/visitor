"""VIS-2: auth/RBAC tables and seed (roles, permissions, admin user).

Revision ID: 0001_auth_rbac
Revises:
Create Date: 2026-06-18

Creates users, roles, permissions, the user_roles / role_permissions join
tables and user_profiles, then seeds the PRD §4 roles, a baseline permission
set, the role→permission matrix and an initial admin account.
"""
from __future__ import annotations

import uuid

import sqlalchemy as sa
from alembic import op

from app.core.config import settings
from app.core.security import hash_password

revision = "0001_auth_rbac"
down_revision = None
branch_labels = None
depends_on = None


# PRD §4 roles.
ROLES = [
    ("admin", "Full system administration"),
    ("empresa", "Company/organization administrator"),
    ("empleado", "Employee performing visits"),
    ("proveedor", "Provider / coordinator"),
    ("cliente", "Client / patient"),
    ("soporte", "Support staff"),
]

# Baseline permission codes (extended by later tickets).
PERMISSIONS = [
    ("users:read", "View users"),
    ("users:write", "Create/update/deactivate users"),
    ("roles:assign", "Assign roles to users"),
    ("visits:read", "View visits"),
    ("visits:write", "Create/update visits"),
    ("reports:read", "View reports"),
]

# Role → permission matrix.
ROLE_PERMISSIONS = {
    "admin": [p[0] for p in PERMISSIONS],
    "empresa": ["users:read", "users:write", "roles:assign", "visits:read", "visits:write", "reports:read"],
    "proveedor": ["visits:read", "visits:write", "reports:read", "users:read"],
    "empleado": ["visits:read", "visits:write"],
    "soporte": ["users:read", "visits:read"],
    "cliente": ["visits:read"],
}


def _uid() -> str:
    return uuid.uuid4().hex


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "roles",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False, server_default=""),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "permissions",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False, server_default=""),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.String(length=32), nullable=False),
        sa.Column("role_id", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )

    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.String(length=32), nullable=False),
        sa.Column("permission_id", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )

    op.create_table(
        "user_profiles",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.String(length=32), nullable=False),
        sa.Column("profile_type", sa.String(length=50), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("extra", sa.Text(), nullable=False, server_default=""),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", name="uq_user_profiles_user_id"),
    )

    _seed()


def _seed() -> None:
    bind = op.get_bind()

    role_ids: dict[str, str] = {}
    for name, desc in ROLES:
        rid = _uid()
        role_ids[name] = rid
        bind.execute(
            sa.text("INSERT INTO roles (id, name, description) VALUES (:id, :name, :description)"),
            {"id": rid, "name": name, "description": desc},
        )

    perm_ids: dict[str, str] = {}
    for code, desc in PERMISSIONS:
        pid = _uid()
        perm_ids[code] = pid
        bind.execute(
            sa.text("INSERT INTO permissions (id, code, description) VALUES (:id, :code, :description)"),
            {"id": pid, "code": code, "description": desc},
        )

    for role_name, codes in ROLE_PERMISSIONS.items():
        for code in codes:
            bind.execute(
                sa.text("INSERT INTO role_permissions (role_id, permission_id) VALUES (:r, :p)"),
                {"r": role_ids[role_name], "p": perm_ids[code]},
            )

    # Initial admin account.
    admin_id = _uid()
    bind.execute(
        sa.text(
            "INSERT INTO users (id, email, hashed_password, full_name, is_active) "
            "VALUES (:id, :email, :pw, :name, true)"
        ),
        {
            "id": admin_id,
            "email": settings.seed_admin_email,
            "pw": hash_password(settings.seed_admin_password),
            "name": "Administrator",
        },
    )
    bind.execute(
        sa.text("INSERT INTO user_roles (user_id, role_id) VALUES (:u, :r)"),
        {"u": admin_id, "r": role_ids["admin"]},
    )


def downgrade() -> None:
    op.drop_table("user_profiles")
    op.drop_table("role_permissions")
    op.drop_table("user_roles")
    op.drop_table("permissions")
    op.drop_table("roles")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
