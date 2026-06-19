"""Visit lifecycle state machine and scheduling helpers (VIS-10).

Central module of the product. It validates visit state transitions, records an
append-only ``VisitStatusEvent`` (with timestamp and geolocation) on every
change, writes an audit entry (hardened by VIS-4), and exposes calendar,
availability and unassigned/SLA-risk queries consumed by the dashboard (VIS-5),
the map (VIS-11) and the mobile app (VIS-18).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import (
    AuditLog,
    Employee,
    Visit,
    VisitAssignment,
    VisitIncident,
    VisitStatusEvent,
)
from app.db.models.visits import VisitStatus

# Allowed transitions of the visit state machine. Empty set == terminal state.
VALID_TRANSITIONS: dict[VisitStatus, set[VisitStatus]] = {
    VisitStatus.scheduled: {
        VisitStatus.en_route,
        VisitStatus.in_progress,
        VisitStatus.cancelled,
        VisitStatus.no_show,
    },
    VisitStatus.en_route: {
        VisitStatus.in_progress,
        VisitStatus.cancelled,
        VisitStatus.no_show,
    },
    VisitStatus.in_progress: {VisitStatus.completed, VisitStatus.cancelled},
    VisitStatus.completed: set(),
    VisitStatus.cancelled: set(),
    VisitStatus.no_show: set(),
}

_BUSY_STATUSES = (VisitStatus.scheduled, VisitStatus.en_route, VisitStatus.in_progress)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def get_visit_or_404(db: Session, visit_id: str) -> Visit:
    visit = db.get(Visit, visit_id)
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    return visit


def _audit(db: Session, *, actor_id: str | None, action: str, visit: Visit,
           before: str, after: str, lat: float | None, lon: float | None) -> None:
    db.add(AuditLog(
        actor_user_id=actor_id, action=action, entity_type="visit",
        entity_id=visit.id, before=before, after=after, latitude=lat, longitude=lon,
    ))


def transition(
    db: Session, visit: Visit, new_status: VisitStatus, *,
    actor_id: str | None = None, latitude: float | None = None,
    longitude: float | None = None, note: str = "", event_at: datetime | None = None,
) -> Visit:
    """Validate and apply a state transition, logging an event + audit row."""
    current = visit.status
    if new_status == current:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Visit already in state '{current.value}'")
    if new_status not in VALID_TRANSITIONS.get(current, set()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid transition {current.value} -> {new_status.value}",
        )
    before = current.value
    visit.status = new_status
    db.add(VisitStatusEvent(
        visit_id=visit.id, status=new_status, event_at=event_at or _now(),
        actor_user_id=actor_id, latitude=latitude, longitude=longitude, note=note,
    ))
    _audit(db, actor_id=actor_id, action=f"visit.{new_status.value}", visit=visit,
           before=before, after=new_status.value, lat=latitude, lon=longitude)
    db.commit()
    db.refresh(visit)
    return visit


def assign(
    db: Session, visit: Visit, *, employee_id: str | None = None,
    provider_id: str | None = None, actor_id: str | None = None,
) -> VisitAssignment:
    if not employee_id and not provider_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="employee_id or provider_id is required")
    assignment = VisitAssignment(
        visit_id=visit.id, employee_id=employee_id, provider_id=provider_id,
        assigned_at=_now(),
    )
    db.add(assignment)
    _audit(db, actor_id=actor_id, action="visit.assign", visit=visit,
           before="", after=employee_id or provider_id or "", lat=None, lon=None)
    db.commit()
    db.refresh(assignment)
    return assignment


def report_incident(
    db: Session, visit: Visit, *, type: str = "general", severity: str = "low",
    description: str = "", actor_id: str | None = None,
) -> VisitIncident:
    incident = VisitIncident(
        visit_id=visit.id, type=type, severity=severity, description=description,
        reported_by_user_id=actor_id,
    )
    db.add(incident)
    _audit(db, actor_id=actor_id, action="visit.incident", visit=visit,
           before="", after=type, lat=None, lon=None)
    db.commit()
    db.refresh(incident)
    return incident


def calendar(
    db: Session, *, start: datetime | None = None, end: datetime | None = None,
    status_filter: VisitStatus | None = None, employee_id: str | None = None,
) -> list[Visit]:
    stmt = select(Visit)
    if start is not None:
        stmt = stmt.where((Visit.scheduled_end.is_(None)) | (Visit.scheduled_end >= start))
    if end is not None:
        stmt = stmt.where((Visit.scheduled_start.is_(None)) | (Visit.scheduled_start <= end))
    if status_filter is not None:
        stmt = stmt.where(Visit.status == status_filter)
    if employee_id is not None:
        stmt = stmt.join(VisitAssignment, VisitAssignment.visit_id == Visit.id).where(
            VisitAssignment.employee_id == employee_id
        )
    return list(db.execute(stmt.order_by(Visit.scheduled_start)).scalars().all())


def unassigned_visits(db: Session) -> list[Visit]:
    """Active visits with no assignment yet (need scheduling attention)."""
    assigned = select(VisitAssignment.visit_id)
    stmt = (
        select(Visit)
        .where(Visit.status.in_(_BUSY_STATUSES))
        .where(Visit.id.notin_(assigned))
        .order_by(Visit.scheduled_start)
    )
    return list(db.execute(stmt).scalars().all())


def sla_risk_visits(db: Session, *, within_minutes: int = 60) -> list[Visit]:
    """Unassigned visits starting within ``within_minutes`` (SLA risk)."""
    threshold = _now() + timedelta(minutes=within_minutes)
    return [
        v for v in unassigned_visits(db)
        if v.scheduled_start is not None and v.scheduled_start <= threshold
    ]


def employee_availability(
    db: Session, *, start: datetime | None = None, end: datetime | None = None,
) -> list[dict]:
    employees = db.execute(select(Employee).where(Employee.is_active.is_(True))).scalars().all()
    out = []
    for emp in employees:
        stmt = (
            select(Visit)
            .join(VisitAssignment, VisitAssignment.visit_id == Visit.id)
            .where(VisitAssignment.employee_id == emp.id)
            .where(Visit.status.in_(_BUSY_STATUSES))
        )
        if start is not None:
            stmt = stmt.where((Visit.scheduled_end.is_(None)) | (Visit.scheduled_end >= start))
        if end is not None:
            stmt = stmt.where((Visit.scheduled_start.is_(None)) | (Visit.scheduled_start <= end))
        busy = db.execute(stmt).scalars().all()
        out.append({
            "employee_id": emp.id,
            "name": f"{emp.first_name} {emp.last_name}",
            "available": len(busy) == 0,
            "busy_count": len(busy),
        })
    return out
