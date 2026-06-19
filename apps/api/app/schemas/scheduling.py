"""Request/response schemas for the scheduling lifecycle (VIS-10)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AssignRequest(BaseModel):
    employee_id: str | None = None
    provider_id: str | None = None


class TransitionRequest(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    note: str = ""
    event_at: datetime | None = None


class IncidentRequest(BaseModel):
    type: str = Field(default="general", max_length=80)
    severity: str = Field(default="low", max_length=30)
    description: str = ""
