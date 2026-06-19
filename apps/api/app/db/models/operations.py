"""Operational and cross-cutting master tables (VIS-3).

Service requests, evaluations, notifications, messages, report requests,
financial liquidations, the audit log and support tickets. The relational
structure lives here; each module's business logic is implemented by its own
ticket (financial calc → VIS-16, audit hardening → VIS-4, etc.).
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.common import PKMixin, TimestampMixin, utcnow
from app.db.session import Base


class ServiceRequest(PKMixin, TimestampMixin, Base):
    __tablename__ = "service_requests"

    client_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    service_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("services.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(40), default="pending", nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    requested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Evaluation(PKMixin, TimestampMixin, Base):
    __tablename__ = "evaluations"

    visit_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("visits.id", ondelete="SET NULL"), nullable=True, index=True
    )
    client_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comments: Mapped[str] = mapped_column(Text, default="")


class Notification(PKMixin, TimestampMixin, Base):
    __tablename__ = "notifications"

    user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, default="")
    channel: Mapped[str] = mapped_column(String(30), default="in_app", nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Message(PKMixin, TimestampMixin, Base):
    __tablename__ = "messages"

    sender_user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    recipient_user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    body: Mapped[str] = mapped_column(Text, default="")
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ReportRequest(PKMixin, TimestampMixin, Base):
    __tablename__ = "report_requests"

    requested_by_user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    report_type: Mapped[str] = mapped_column(String(80), nullable=False)
    params: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="pending", nullable=False)


class FinancialLiquidation(PKMixin, TimestampMixin, Base):
    """Payroll/settlement record. Exact formulas are computed by VIS-16."""

    __tablename__ = "financial_liquidations"

    employee_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    provider_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("providers.id", ondelete="SET NULL"), nullable=True
    )
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    gross_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    deductions: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    net_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="draft", nullable=False)


class AuditLog(PKMixin, Base):
    """Audit trail. Populated systematically by VIS-4; table defined here."""

    __tablename__ = "audit_logs"

    actor_user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(64), default="")
    before: Mapped[str] = mapped_column(Text, default="")
    after: Mapped[str] = mapped_column(Text, default="")
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow
    )


class SupportTicket(PKMixin, TimestampMixin, Base):
    __tablename__ = "support_tickets"

    requester_user_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="open", nullable=False, index=True)
    priority: Mapped[str] = mapped_column(String(30), default="normal", nullable=False)
