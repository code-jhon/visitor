"""VIS-4: audit:read permission for the immutable audit-log query endpoint.

Adds the ``audit:read`` permission and grants it to Admin and Soporte. The
``audit_logs`` table itself is created by 0002 (VIS-3); this migration only seeds
the access-control needed to read it. Append-only semantics are enforced at the
API layer (no create/update/delete route).

Revision ID: 0003_audit_permissions
Revises: 0002_master_data
Create Date: 2026-06-18
"""
from __future__ import annotations

import uuid

import sqlalchemy as sa
from alembic import op

revision = "0003_audit_permissions"
down_revision = "0002_master_data"
branch_labels = None
depends_on = None

PERM = ("audit:read", "View the audit log")
GRANT_ROLES = ("admin", "soporte")


def upgrade() -> None:
    bind = op.get_bind()
    pid = uuid.uuid4().hex
    bind.execute(
        sa.text("INSERT INTO permissions (id, code, description) VALUES (:id, :code, :desc)"),
        {"id": pid, "code": PERM[0], "desc": PERM[1]},
    )
    role_rows = bind.execute(sa.text("SELECT id, name FROM roles")).fetchall()
    role_ids = {name: rid for rid, name in role_rows}
    for role in GRANT_ROLES:
        rid = role_ids.get(role)
        if rid is not None:
            bind.execute(
                sa.text("INSERT INTO role_permissions (role_id, permission_id) VALUES (:r, :p)"),
                {"r": rid, "p": pid},
            )


def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text(
            "DELETE FROM role_permissions WHERE permission_id IN "
            "(SELECT id FROM permissions WHERE code = :code)"
        ),
        {"code": PERM[0]},
    )
    bind.execute(sa.text("DELETE FROM permissions WHERE code = :code"), {"code": PERM[0]})
