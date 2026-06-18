"""People master data: employees, providers, clients and patients (VIS-3).

Each record may optionally link to a ``users`` row (VIS-2) when the person has
login access; the master record exists independently so non-authenticating
people (e.g. a patient cared for by a relative) can still be modeled.
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.common import PKMixin, TimestampMixin
from app.db.session import Base


class Employee(PKMixin, TimestampMixin, Base):
    __tablename__ = "employees"

    user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    document_id: Mapped[str] = mapped_column(String(60), default="", index=True)
    email: Mapped[str] = mapped_column(String(255), default="")
    phone: Mapped[str] = mapped_column(String(50), default="")
    address: Mapped[str] = mapped_column(String(255), default="")
    position: Mapped[str] = mapped_column(String(120), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Provider(PKMixin, TimestampMixin, Base):
    """Provider / coordinator (a partner organization or coordinating person)."""

    __tablename__ = "providers"

    user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(150), default="")
    email: Mapped[str] = mapped_column(String(255), default="")
    phone: Mapped[str] = mapped_column(String(50), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Client(PKMixin, TimestampMixin, Base):
    """Client: the contracting party that requests services."""

    __tablename__ = "clients"

    user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    document_id: Mapped[str] = mapped_column(String(60), default="", index=True)
    email: Mapped[str] = mapped_column(String(255), default="")
    phone: Mapped[str] = mapped_column(String(50), default="")
    address: Mapped[str] = mapped_column(String(255), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    patients: Mapped[list["Patient"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )


class Patient(PKMixin, TimestampMixin, Base):
    """Patient receiving care; linked to the client responsible for them.

    Sensitive health data is intentionally minimal here — visibility is enforced
    by RBAC (VIS-2) and hardened by VIS-4.
    """

    __tablename__ = "patients"

    client_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    document_id: Mapped[str] = mapped_column(String(60), default="", index=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    address: Mapped[str] = mapped_column(String(255), default="")
    medical_notes: Mapped[str] = mapped_column(Text, default="")

    client: Mapped[Client | None] = relationship(back_populates="patients")
