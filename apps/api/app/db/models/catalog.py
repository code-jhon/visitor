"""Service catalog and tariff master data (VIS-3, extended by VIS-9).

``Service`` → ``Subservice`` is a one-to-many tree; ``Tariff`` prices a service
or a specific subservice. VIS-9 makes the tariff model flexible: it supports the
four pricing modalities required by the PRD (per service, per provider, per hour
and per kilometre / mileage allowance) plus an effective-date range so historical
liquidations are never broken by a price change. ``CertificateRequirement``
captures the document requirements that apply to employees/providers before they
can perform visits.
"""
from __future__ import annotations

import enum
from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.common import PKMixin, TimestampMixin
from app.db.session import Base


class Service(PKMixin, TimestampMixin, Base):
    __tablename__ = "services"

    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    subservices: Mapped[list["Subservice"]] = relationship(
        back_populates="service", cascade="all, delete-orphan"
    )
    tariffs: Mapped[list["Tariff"]] = relationship(
        back_populates="service", cascade="all, delete-orphan"
    )


class Subservice(PKMixin, TimestampMixin, Base):
    __tablename__ = "subservices"

    service_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    service: Mapped[Service] = relationship(back_populates="subservices")


class TariffModality(str, enum.Enum):
    """Pricing modality of a tariff (PRD §8.3, VIS-9)."""

    per_service = "per_service"
    per_provider = "per_provider"
    per_hour = "per_hour"
    per_km = "per_km"


class Tariff(PKMixin, TimestampMixin, Base):
    __tablename__ = "tariffs"

    service_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subservice_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("subservices.id", ondelete="SET NULL"), nullable=True
    )
    # When the modality is ``per_provider`` the tariff is tied to a provider.
    provider_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("providers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    modality: Mapped[TariffModality] = mapped_column(
        Enum(TariffModality, name="tariff_modality"),
        default=TariffModality.per_service,
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    # Effective-date range so historical settlements keep their original price.
    valid_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    valid_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    service: Mapped[Service] = relationship(back_populates="tariffs")


class CertificateRequirement(PKMixin, TimestampMixin, Base):
    __tablename__ = "certificate_requirements"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    # Role the requirement applies to (e.g. "empleado", "proveedor").
    applies_to: Mapped[str] = mapped_column(String(50), default="empleado", nullable=False)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
