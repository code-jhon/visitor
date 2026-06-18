"""Auth / RBAC models: User, Role, Permission and per-role profile (VIS-2).

Design notes
------------
* Many-to-many ``user_roles`` and ``role_permissions`` keep the role→permission
  matrix data-driven (the PRD §4 roles are seeded by the first migration).
* ``UserProfile`` holds role-specific attributes (employee, client/patient,
  provider/coordinator, support). It is intentionally thin here; VIS-3 fleshes
  out domain fields. A 1:1 link to ``User`` keeps auth concerns separate.
* Primary keys are UUID strings so tokens can carry the subject without
  exposing sequential ids.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _uuid() -> str:
    return uuid.uuid4().hex


def _now() -> datetime:
    return datetime.now(timezone.utc)


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String(32), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", String(32), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String(32), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", String(32), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="")

    roles: Mapped[list["Role"]] = relationship(
        secondary=role_permissions, back_populates="permissions"
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="")

    permissions: Mapped[list[Permission]] = relationship(
        secondary=role_permissions, back_populates="roles", lazy="selectin"
    )
    users: Mapped[list["User"]] = relationship(
        secondary=user_roles, back_populates="roles"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )

    roles: Mapped[list[Role]] = relationship(
        secondary=user_roles, back_populates="users", lazy="selectin"
    )
    profile: Mapped["UserProfile | None"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class UserProfile(Base):
    """Role-specific profile data, one row per user.

    ``profile_type`` mirrors the user's primary role (employee, client,
    provider, support). Domain-specific columns are added by VIS-3; ``extra``
    is a free-form text blob for the interim.
    """

    __tablename__ = "user_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_profiles_user_id"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    profile_type: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), default="")
    extra: Mapped[str] = mapped_column(Text, default="")

    user: Mapped[User] = relationship(back_populates="profile")
