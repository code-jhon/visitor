"""Schemas for operational/cross-cutting entities (VIS-3)."""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class _ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- ServiceRequest --------------------------------------------------------
class ServiceRequestCreate(BaseModel):
    client_id: str | None = None
    service_id: str | None = None
    status: str = "pending"
    description: str = ""
    requested_at: datetime | None = None


class ServiceRequestUpdate(BaseModel):
    client_id: str | None = None
    service_id: str | None = None
    status: str | None = None
    description: str | None = None
    requested_at: datetime | None = None


class ServiceRequestOut(_ORM):
    id: str
    client_id: str | None
    service_id: str | None
    status: str
    description: str
    requested_at: datetime | None
    created_at: datetime
    updated_at: datetime


# --- Evaluation ------------------------------------------------------------
class EvaluationCreate(BaseModel):
    visit_id: str | None = None
    client_id: str | None = None
    score: int | None = Field(default=None, ge=0, le=10)
    comments: str = ""


class EvaluationUpdate(BaseModel):
    score: int | None = Field(default=None, ge=0, le=10)
    comments: str | None = None


class EvaluationOut(_ORM):
    id: str
    visit_id: str | None
    client_id: str | None
    score: int | None
    comments: str
    created_at: datetime
    updated_at: datetime


# --- Notification ----------------------------------------------------------
class NotificationCreate(BaseModel):
    user_id: str | None = None
    title: str = Field(min_length=1, max_length=200)
    body: str = ""
    channel: str = "in_app"
    is_read: bool = False


class NotificationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    body: str | None = None
    channel: str | None = None
    is_read: bool | None = None


class NotificationOut(_ORM):
    id: str
    user_id: str | None
    title: str
    body: str
    channel: str
    is_read: bool
    created_at: datetime
    updated_at: datetime


# --- FinancialLiquidation --------------------------------------------------
class FinancialLiquidationCreate(BaseModel):
    employee_id: str | None = None
    provider_id: str | None = None
    period_start: date | None = None
    period_end: date | None = None
    gross_amount: Decimal = Field(default=Decimal("0"), ge=0)
    deductions: Decimal = Field(default=Decimal("0"), ge=0)
    net_amount: Decimal = Field(default=Decimal("0"), ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    status: str = "draft"


class FinancialLiquidationUpdate(BaseModel):
    period_start: date | None = None
    period_end: date | None = None
    gross_amount: Decimal | None = Field(default=None, ge=0)
    deductions: Decimal | None = Field(default=None, ge=0)
    net_amount: Decimal | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    status: str | None = None


class FinancialLiquidationOut(_ORM):
    id: str
    employee_id: str | None
    provider_id: str | None
    period_start: date | None
    period_end: date | None
    gross_amount: Decimal
    deductions: Decimal
    net_amount: Decimal
    currency: str
    status: str
    created_at: datetime
    updated_at: datetime


# --- SupportTicket ---------------------------------------------------------
class SupportTicketCreate(BaseModel):
    requester_user_id: str | None = None
    subject: str = Field(min_length=1, max_length=200)
    description: str = ""
    status: str = "open"
    priority: str = "normal"


class SupportTicketUpdate(BaseModel):
    subject: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: str | None = None
    priority: str | None = None


class SupportTicketOut(_ORM):
    id: str
    requester_user_id: str | None
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
