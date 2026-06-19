"""Read schema for the audit log (VIS-4)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    actor_user_id: str | None
    action: str
    entity_type: str
    entity_id: str
    before: str
    after: str
    latitude: float | None
    longitude: float | None
    created_at: datetime
