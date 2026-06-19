"""Business helpers for the People modules (VIS-6 employees, VIS-7 patients).

Search by configured criteria and employee availability derived from assigned
visits. Availability is exposed so the scheduling engine (VIS-10) can avoid
double-booking a caregiver.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import Employee, Visit, VisitAssignment
from app.db.models.visits import VisitStatus

# Statuses that still occupy a caregiver's calendar.
_ACTIVE_STATUSES = (
    VisitStatus.scheduled,
    VisitStatus.en_route,
    VisitStatus.in_progress,
)


def search_employees(
    db: Session,
    *,
    q: str | None = None,
    document_id: str | None = None,
    position: str | None = None,
    is_active: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Employee]:
    stmt = select(Employee)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(Employee.first_name.ilike(like), Employee.last_name.ilike(like))
        )
    if document_id:
        stmt = stmt.where(Employee.document_id == document_id)
    if position:
        stmt = stmt.where(Employee.position.ilike(f"%{position}%"))
    if is_active is not None:
        stmt = stmt.where(Employee.is_active.is_(is_active))
    stmt = stmt.offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def employee_busy_slots(
    db: Session,
    employee_id: str,
    *,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[dict]:
    """Return the scheduled visit windows that keep the employee busy."""
    stmt = (
        select(Visit)
        .join(VisitAssignment, VisitAssignment.visit_id == Visit.id)
        .where(VisitAssignment.employee_id == employee_id)
        .where(Visit.status.in_(_ACTIVE_STATUSES))
    )
    if start is not None:
        stmt = stmt.where(
            (Visit.scheduled_end.is_(None)) | (Visit.scheduled_end >= start)
        )
    if end is not None:
        stmt = stmt.where(
            (Visit.scheduled_start.is_(None)) | (Visit.scheduled_start <= end)
        )
    visits = db.execute(stmt).scalars().all()
    return [
        {
            "visit_id": v.id,
            "scheduled_start": v.scheduled_start,
            "scheduled_end": v.scheduled_end,
            "status": v.status.value,
        }
        for v in visits
    ]
