"""merge heads

Revision ID: 2e657ac5f463
Revises: 0003_audit_permissions, 0003_tariff_modality
Create Date: 2026-06-18 23:56:40.028388
"""
from alembic import op
import sqlalchemy as sa


revision = '2e657ac5f463'
down_revision = ('0003_audit_permissions', '0003_tariff_modality')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
