"""Schemas for the service catalog and tariffs (VIS-3)."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class _ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- Service ---------------------------------------------------------------
class ServiceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str = ""
    is_active: bool = True


class ServiceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    is_active: bool | None = None


class ServiceOut(_ORM):
    id: str
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# --- Subservice ------------------------------------------------------------
class SubserviceCreate(BaseModel):
    service_id: str
    name: str = Field(min_length=1, max_length=150)
    description: str = ""
    is_active: bool = True


class SubserviceUpdate(BaseModel):
    service_id: str | None = None
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    is_active: bool | None = None


class SubserviceOut(_ORM):
    id: str
    service_id: str
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# --- Tariff ----------------------------------------------------------------
class TariffCreate(BaseModel):
    service_id: str
    subservice_id: str | None = None
    name: str = Field(min_length=1, max_length=150)
    amount: Decimal = Field(ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    is_active: bool = True


class TariffUpdate(BaseModel):
    service_id: str | None = None
    subservice_id: str | None = None
    name: str | None = Field(default=None, min_length=1, max_length=150)
    amount: Decimal | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    is_active: bool | None = None


class TariffOut(_ORM):
    id: str
    service_id: str
    subservice_id: str | None
    name: str
    amount: Decimal
    currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# --- CertificateRequirement -----------------------------------------------
class CertificateRequirementCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str = ""
    applies_to: str = "empleado"
    is_mandatory: bool = True


class CertificateRequirementUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    applies_to: str | None = None
    is_mandatory: bool | None = None


class CertificateRequirementOut(_ORM):
    id: str
    name: str
    description: str
    applies_to: str
    is_mandatory: bool
    created_at: datetime
    updated_at: datetime
