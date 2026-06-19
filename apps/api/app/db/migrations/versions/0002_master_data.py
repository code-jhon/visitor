"""VIS-3: master-data domain tables and RBAC permission seed.

Revision ID: 0002_master_data
Revises: 0001_auth_rbac
Create Date: 2026-06-18

Creates the catalog, people, visit-lifecycle and operational tables and seeds
the per-group read/write permissions plus the role→permission grants that the
CRUD routers enforce. Targets PostgreSQL (tests build schema from ORM metadata).
"""
from __future__ import annotations

import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0002_master_data"
down_revision = "0001_auth_rbac"
branch_labels = None
depends_on = None


# New permission codes (read/write per API group). visits:* and reports:read
# already exist from 0001_auth_rbac.
NEW_PERMISSIONS = [
    ("services:read", "View services/subservices"),
    ("services:write", "Manage services/subservices"),
    ("tariffs:read", "View tariffs"),
    ("tariffs:write", "Manage tariffs"),
    ("certificates:read", "View certificate requirements"),
    ("certificates:write", "Manage certificate requirements"),
    ("employees:read", "View employees"),
    ("employees:write", "Manage employees"),
    ("providers:read", "View providers"),
    ("providers:write", "Manage providers"),
    ("clients:read", "View clients"),
    ("clients:write", "Manage clients"),
    ("patients:read", "View patients"),
    ("patients:write", "Manage patients"),
    ("service-requests:read", "View service requests"),
    ("service-requests:write", "Manage service requests"),
    ("evaluations:read", "View evaluations"),
    ("evaluations:write", "Manage evaluations"),
    ("notifications:read", "View notifications"),
    ("notifications:write", "Manage notifications"),
    ("financial:read", "View financial liquidations"),
    ("financial:write", "Manage financial liquidations"),
    ("support:read", "View support tickets"),
    ("support:write", "Manage support tickets"),
]

_ALL = [c for c, _ in NEW_PERMISSIONS]

ROLE_GRANTS = {
    "admin": _ALL,
    "empresa": _ALL,
    "proveedor": [
        "services:read", "tariffs:read", "certificates:read", "employees:read",
        "providers:read", "clients:read", "patients:read",
        "service-requests:read", "service-requests:write",
        "evaluations:read", "notifications:read",
    ],
    "empleado": [
        "services:read", "clients:read", "patients:read",
        "service-requests:read", "evaluations:read", "evaluations:write",
        "notifications:read",
    ],
    "soporte": [
        "support:read", "support:write", "notifications:read",
        "clients:read", "patients:read", "service-requests:read",
    ],
    "cliente": [
        "service-requests:read", "service-requests:write",
        "evaluations:read", "evaluations:write", "notifications:read",
    ],
}

VISIT_STATUS = postgresql.ENUM(
    "scheduled", "en_route", "in_progress", "completed", "cancelled", "no_show",
    name="visit_status", create_type=False,
)


def _uid() -> str:
    return uuid.uuid4().hex


def _ts(*extra: sa.Column) -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        *extra,
    ]


def upgrade() -> None:
    bind = op.get_bind()
    VISIT_STATUS.create(bind, checkfirst=True)

    # --- Catalog -----------------------------------------------------------
    op.create_table(
        "services",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("name", sa.String(150), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "subservices",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("service_id", sa.String(32), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_subservices_service_id", "subservices", ["service_id"])
    op.create_table(
        "tariffs",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("service_id", sa.String(32), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subservice_id", sa.String(32), sa.ForeignKey("subservices.id", ondelete="SET NULL"), nullable=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False, server_default="USD"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_tariffs_service_id", "tariffs", ["service_id"])
    op.create_table(
        "certificate_requirements",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("applies_to", sa.String(50), nullable=False, server_default="empleado"),
        sa.Column("is_mandatory", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # --- People ------------------------------------------------------------
    op.create_table(
        "employees",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("first_name", sa.String(120), nullable=False),
        sa.Column("last_name", sa.String(120), nullable=False),
        sa.Column("document_id", sa.String(60), nullable=False, server_default=""),
        sa.Column("email", sa.String(255), nullable=False, server_default=""),
        sa.Column("phone", sa.String(50), nullable=False, server_default=""),
        sa.Column("address", sa.String(255), nullable=False, server_default=""),
        sa.Column("position", sa.String(120), nullable=False, server_default=""),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_employees_document_id", "employees", ["document_id"])
    op.create_table(
        "providers",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("contact_name", sa.String(150), nullable=False, server_default=""),
        sa.Column("email", sa.String(255), nullable=False, server_default=""),
        sa.Column("phone", sa.String(50), nullable=False, server_default=""),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "clients",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("first_name", sa.String(120), nullable=False),
        sa.Column("last_name", sa.String(120), nullable=False),
        sa.Column("document_id", sa.String(60), nullable=False, server_default=""),
        sa.Column("email", sa.String(255), nullable=False, server_default=""),
        sa.Column("phone", sa.String(50), nullable=False, server_default=""),
        sa.Column("address", sa.String(255), nullable=False, server_default=""),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_clients_document_id", "clients", ["document_id"])
    op.create_table(
        "patients",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("client_id", sa.String(32), sa.ForeignKey("clients.id", ondelete="SET NULL"), nullable=True),
        sa.Column("first_name", sa.String(120), nullable=False),
        sa.Column("last_name", sa.String(120), nullable=False),
        sa.Column("document_id", sa.String(60), nullable=False, server_default=""),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("address", sa.String(255), nullable=False, server_default=""),
        sa.Column("medical_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_patients_client_id", "patients", ["client_id"])
    op.create_index("ix_patients_document_id", "patients", ["document_id"])

    # --- Visits ------------------------------------------------------------
    op.create_table(
        "visits",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("client_id", sa.String(32), sa.ForeignKey("clients.id", ondelete="SET NULL"), nullable=True),
        sa.Column("patient_id", sa.String(32), sa.ForeignKey("patients.id", ondelete="SET NULL"), nullable=True),
        sa.Column("service_id", sa.String(32), sa.ForeignKey("services.id", ondelete="SET NULL"), nullable=True),
        sa.Column("subservice_id", sa.String(32), sa.ForeignKey("subservices.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", VISIT_STATUS, nullable=False, server_default="scheduled"),
        sa.Column("scheduled_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduled_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("address", sa.String(255), nullable=False, server_default=""),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_visits_client_id", "visits", ["client_id"])
    op.create_index("ix_visits_patient_id", "visits", ["patient_id"])
    op.create_index("ix_visits_status", "visits", ["status"])
    op.create_table(
        "visit_assignments",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("visit_id", sa.String(32), sa.ForeignKey("visits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("employee_id", sa.String(32), sa.ForeignKey("employees.id", ondelete="SET NULL"), nullable=True),
        sa.Column("provider_id", sa.String(32), sa.ForeignKey("providers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_visit_assignments_visit_id", "visit_assignments", ["visit_id"])
    op.create_table(
        "visit_status_events",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("visit_id", sa.String(32), sa.ForeignKey("visits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", VISIT_STATUS, nullable=False),
        sa.Column("event_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actor_user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("note", sa.Text(), nullable=False, server_default=""),
    )
    op.create_index("ix_visit_status_events_visit_id", "visit_status_events", ["visit_id"])
    op.create_table(
        "visit_incidents",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("visit_id", sa.String(32), sa.ForeignKey("visits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(80), nullable=False, server_default="general"),
        sa.Column("severity", sa.String(30), nullable=False, server_default="low"),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("reported_by_user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_visit_incidents_visit_id", "visit_incidents", ["visit_id"])

    # --- Operations --------------------------------------------------------
    op.create_table(
        "service_requests",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("client_id", sa.String(32), sa.ForeignKey("clients.id", ondelete="SET NULL"), nullable=True),
        sa.Column("service_id", sa.String(32), sa.ForeignKey("services.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", sa.String(40), nullable=False, server_default="pending"),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_service_requests_client_id", "service_requests", ["client_id"])
    op.create_index("ix_service_requests_status", "service_requests", ["status"])
    op.create_table(
        "evaluations",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("visit_id", sa.String(32), sa.ForeignKey("visits.id", ondelete="SET NULL"), nullable=True),
        sa.Column("client_id", sa.String(32), sa.ForeignKey("clients.id", ondelete="SET NULL"), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("comments", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_evaluations_visit_id", "evaluations", ["visit_id"])
    op.create_table(
        "notifications",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("channel", sa.String(30), nullable=False, server_default="in_app"),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_table(
        "messages",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("sender_user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("recipient_user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_messages_recipient_user_id", "messages", ["recipient_user_id"])
    op.create_table(
        "report_requests",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("requested_by_user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("report_type", sa.String(80), nullable=False),
        sa.Column("params", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(40), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "financial_liquidations",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("employee_id", sa.String(32), sa.ForeignKey("employees.id", ondelete="SET NULL"), nullable=True),
        sa.Column("provider_id", sa.String(32), sa.ForeignKey("providers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("period_start", sa.Date(), nullable=True),
        sa.Column("period_end", sa.Date(), nullable=True),
        sa.Column("gross_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("deductions", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("net_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(3), nullable=False, server_default="USD"),
        sa.Column("status", sa.String(40), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("actor_user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.String(80), nullable=False),
        sa.Column("entity_type", sa.String(80), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=False, server_default=""),
        sa.Column("before", sa.Text(), nullable=False, server_default=""),
        sa.Column("after", sa.Text(), nullable=False, server_default=""),
        sa.Column("latitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("longitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_logs_actor_user_id", "audit_logs", ["actor_user_id"])
    op.create_index("ix_audit_logs_entity_type", "audit_logs", ["entity_type"])
    op.create_table(
        "support_tickets",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("requester_user_id", sa.String(32), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("subject", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(40), nullable=False, server_default="open"),
        sa.Column("priority", sa.String(30), nullable=False, server_default="normal"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_support_tickets_requester_user_id", "support_tickets", ["requester_user_id"])
    op.create_index("ix_support_tickets_status", "support_tickets", ["status"])

    _seed_permissions()


def _seed_permissions() -> None:
    bind = op.get_bind()

    # Insert new permissions, capturing ids.
    perm_ids: dict[str, str] = {}
    for code, desc in NEW_PERMISSIONS:
        pid = _uid()
        perm_ids[code] = pid
        bind.execute(
            sa.text("INSERT INTO permissions (id, code, description) VALUES (:id, :code, :description)"),
            {"id": pid, "code": code, "description": desc},
        )

    # Resolve role ids by name.
    role_rows = bind.execute(sa.text("SELECT id, name FROM roles")).fetchall()
    role_ids = {name: rid for rid, name in role_rows}

    for role_name, codes in ROLE_GRANTS.items():
        rid = role_ids.get(role_name)
        if rid is None:
            continue
        for code in codes:
            bind.execute(
                sa.text("INSERT INTO role_permissions (role_id, permission_id) VALUES (:r, :p)"),
                {"r": rid, "p": perm_ids[code]},
            )


def downgrade() -> None:
    bind = op.get_bind()

    # Remove seeded grants/permissions first.
    codes = tuple(c for c, _ in NEW_PERMISSIONS)
    bind.execute(
        sa.text(
            "DELETE FROM role_permissions WHERE permission_id IN "
            "(SELECT id FROM permissions WHERE code IN :codes)"
        ).bindparams(sa.bindparam("codes", expanding=True)),
        {"codes": list(codes)},
    )
    bind.execute(
        sa.text("DELETE FROM permissions WHERE code IN :codes").bindparams(
            sa.bindparam("codes", expanding=True)
        ),
        {"codes": list(codes)},
    )

    for table in [
        "support_tickets",
        "audit_logs",
        "financial_liquidations",
        "report_requests",
        "messages",
        "notifications",
        "evaluations",
        "service_requests",
        "visit_incidents",
        "visit_status_events",
        "visit_assignments",
        "visits",
        "patients",
        "clients",
        "providers",
        "employees",
        "certificate_requirements",
        "tariffs",
        "subservices",
        "services",
    ]:
        op.drop_table(table)

    VISIT_STATUS.drop(bind, checkfirst=True)
