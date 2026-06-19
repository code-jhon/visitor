"""Immutable audit-log query endpoint (VIS-4).

Read-only for Admin/Soporte (``audit:read``). The log is append-only: there is
deliberately no create/update/delete endpoint — entries are written only by the
``audit`` service from within business operations.
"""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.models import AuditLog
from app.db.session import get_db
from app.schemas.audit import AuditLogOut

router = APIRouter(prefix="/audit-logs", tags=["audit"])


@router.get("", response_model=list[AuditLogOut])
def list_audit_logs(
    entity_type: str | None = None,
    actor_id: str | None = None,
    action: str | None = None,
    start: datetime | None = Query(default=None, alias="from"),
    end: datetime | None = Query(default=None, alias="to"),
    skip: int = 0,
    limit: int = Query(default=100, le=500),
    db: Session = Depends(get_db),
    _=Depends(require_permission("audit:read")),
):
    stmt = select(AuditLog)
    if entity_type:
        stmt = stmt.where(AuditLog.entity_type == entity_type)
    if actor_id:
        stmt = stmt.where(AuditLog.actor_user_id == actor_id)
    if action:
        stmt = stmt.where(AuditLog.action == action)
    if start is not None:
        stmt = stmt.where(AuditLog.created_at >= start)
    if end is not None:
        stmt = stmt.where(AuditLog.created_at <= end)
    stmt = stmt.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())
