"""VIS-9: flexible tariff modalities and effective-date range.

Adds the pricing ``modality`` (per service / provider / hour / km), an optional
``provider_id`` (for per-provider tariffs) and a ``valid_from`` / ``valid_to``
effective range so price changes never rewrite historical liquidations.
Targets PostgreSQL (tests build the schema from the ORM metadata).

Revision ID: 0003_tariff_modality
Revises: 0002_master_data
Create Date: 2026-06-18
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0003_tariff_modality"
down_revision = "0002_master_data"
branch_labels = None
depends_on = None

TARIFF_MODALITY = postgresql.ENUM(
    "per_service", "per_provider", "per_hour", "per_km", name="tariff_modality"
)


def upgrade() -> None:
    bind = op.get_bind()
    TARIFF_MODALITY.create(bind, checkfirst=True)
    op.add_column(
        "tariffs",
        sa.Column(
            "modality",
            TARIFF_MODALITY,
            nullable=False,
            server_default="per_service",
        ),
    )
    op.add_column("tariffs", sa.Column("provider_id", sa.String(length=32), nullable=True))
    op.add_column("tariffs", sa.Column("valid_from", sa.Date(), nullable=True))
    op.add_column("tariffs", sa.Column("valid_to", sa.Date(), nullable=True))
    op.create_index("ix_tariffs_modality", "tariffs", ["modality"])
    op.create_index("ix_tariffs_provider_id", "tariffs", ["provider_id"])
    op.create_foreign_key(
        "fk_tariffs_provider_id",
        "tariffs",
        "providers",
        ["provider_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    bind = op.get_bind()
    op.drop_constraint("fk_tariffs_provider_id", "tariffs", type_="foreignkey")
    op.drop_index("ix_tariffs_provider_id", table_name="tariffs")
    op.drop_index("ix_tariffs_modality", table_name="tariffs")
    op.drop_column("tariffs", "valid_to")
    op.drop_column("tariffs", "valid_from")
    op.drop_column("tariffs", "provider_id")
    op.drop_column("tariffs", "modality")
    TARIFF_MODALITY.drop(bind, checkfirst=True)
