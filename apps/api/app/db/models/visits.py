"""Visit lifecycle tables (VIS-3 schema; business logic lands in VIS-10).

This ticket defines the relational structure — visits, assignments, the
append-only status-event log and incidents/novelties — with geolocation and
timestamp fields. The state machine and transition rules belong to VIS-10.
"""
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.common import PKMixin, TimestampMixin
from app.db.session import Base


class VisitStatus(str, enum.Enum):
    """Visit states (aligned with VIS-10)."""

    scheduled = "scheduled"
    en_route = "en_route"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


class Visit(PKMixin, TimestampMixin, Base):
    __tablename__ = "visits"

    client_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    patient_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("patients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    service_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("services.id", ondelete="SET NULL"), nullable=True
    )
    subservice_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("subservices.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[VisitStatus] = mapped_column(
        Enum(VisitStatus, name="visit_status"),
        default=VisitStatus.scheduled,
        nullable=False,
        index=True,
    )
    scheduled_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scheduled_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    address: Mapped[str] = mapped_column(String(255), default="")
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")

    assignments: Mapped[list["VisitAssignment"]] = relationship(
        back_populates="visit", cascade="all, delete-orphan"
    )
    status_events: Mapped[list["VisitStatusEvent"]] = relationship(
        back_populates="visit", cascade="all, delete-orphan"
    )
    incidents: Mapped[list["VisitIncident"]] = relationship(
        back_populates="visit", cascade="all, delete-orphan"
    )


class VisitAssignment(PKMixin, TimestampMixin, Base):
    __tablename__ = "visit_assignments"

    visit_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("visits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    employee_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    provider_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("providers.id", ondelete="SET NULL"), nullable=True
    )
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    visit: Mapped[Visit] = relationship(back_populates="assignments")


class VisitStatusEvent(PKMixin, Base):
    """Append-only log of visit state transitions with geo/timestamp."""

    __tablename__ = "visit_status_events"

    visit_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("visits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[VisitStatus] = mapped_column(
        Enum(VisitStatus, name="visit_status"), nullable=False
    )
    event_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actor_user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    note: Mapped[str] = mapped_column(Text, default="")

    visit: Mapped[Visit] = relationship(back_populates="status_events")


class VisitIncident(PKMixin, TimestampMixin, Base):
    """Incident / novelty reported during a visit."""

    __tablename__ = "visit_incidents"

    visit_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("visits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[str] = mapped_column(String(80), default="general", nullable=False)
    severity: Mapped[str] = mapped_column(String(30), default="low", nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    reported_by_user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    visit: Mapped[Visit] = relationship(back_populates="incidents")
