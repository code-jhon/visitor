"""Schemas for visits and related lifecycle tables (VIS-3)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.visits import VisitStatus


class _ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- Visit -----------------------------------------------------------------
class VisitCreate(BaseModel):
    client_id: str | None = None
    patient_id: str | None = None
    service_id: str | None = None
    subservice_id: str | None = None
    status: VisitStatus = VisitStatus.scheduled
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    address: str = ""
    latitude: float | None = None
    longitude: float | None = None
    notes: str = ""


class VisitUpdate(BaseModel):
    client_id: str | None = None
    patient_id: str | None = None
    service_id: str | None = None
    subservice_id: str | None = None
    status: VisitStatus | None = None
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    notes: str | None = None


class VisitOut(_ORM):
    id: str
    client_id: str | None
    patient_id: str | None
    service_id: str | None
    subservice_id: str | None
    status: VisitStatus
    scheduled_start: datetime | None
    scheduled_end: datetime | None
    address: str
    latitude: float | None
    longitude: float | None
    notes: str
    created_at: datetime
    updated_at: datetime


# --- VisitAssignment -------------------------------------------------------
class VisitAssignmentCreate(BaseModel):
    visit_id: str
    employee_id: str | None = None
    provider_id: str | None = None
    assigned_at: datetime | None = None


class VisitAssignmentUpdate(BaseModel):
    employee_id: str | None = None
    provider_id: str | None = None
    assigned_at: datetime | None = None


class VisitAssignmentOut(_ORM):
    id: str
    visit_id: str
    employee_id: str | None
    provider_id: str | None
    assigned_at: datetime | None
    created_at: datetime
    updated_at: datetime


# --- VisitStatusEvent ------------------------------------------------------
class VisitStatusEventCreate(BaseModel):
    visit_id: str
    status: VisitStatus
    event_at: datetime | None = None
    actor_user_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    note: str = ""


class VisitStatusEventOut(_ORM):
    id: str
    visit_id: str
    status: VisitStatus
    event_at: datetime | None
    actor_user_id: str | None
    latitude: float | None
    longitude: float | None
    note: str


# --- VisitIncident ---------------------------------------------------------
class VisitIncidentCreate(BaseModel):
    visit_id: str
    type: str = "general"
    severity: str = "low"
    description: str = ""
    reported_by_user_id: str | None = None


class VisitIncidentUpdate(BaseModel):
    type: str | None = None
    severity: str | None = None
    description: str | None = None


class VisitIncidentOut(_ORM):
    id: str
    visit_id: str
    type: str
    severity: str
    description: str
    reported_by_user_id: str | None
    created_at: datetime
    updated_at: datetime
