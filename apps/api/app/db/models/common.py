"""Shared model helpers and mixins for the domain model (VIS-3).

Every domain table uses a 32-char UUID string primary key (consistent with the
auth tables from VIS-2) and carries ``created_at`` / ``updated_at`` timestamps.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


def uuid_hex() -> str:
    return uuid.uuid4().hex


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PKMixin:
    """32-char UUID string primary key."""

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uuid_hex)


class TimestampMixin:
    """Creation and last-update timestamps maintained by the ORM."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )
