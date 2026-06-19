"""Operational dashboard aggregation (VIS-5).

Read-only aggregates over the visit data: counts by status, today's agenda and
the unassigned/active backlog. The map widget is VIS-11; here we only expose the
summary numbers and shortcuts the landing dashboard renders.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Visit, VisitAssignment
from app.db.models.visits import VisitStatus

_ACTIVE = (VisitStatus.scheduled, VisitStatus.en_route, VisitStatus.in_progress)


def summary(db: Session, *, today: datetime | None = None) -> dict:
    now = today or datetime.now(timezone.utc)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Counts by status.
    rows = db.execute(
        select(Visit.status, func.count()).group_by(Visit.status)
    ).all()
    by_status = {s.value: 0 for s in VisitStatus}
    total = 0
    for status_value, count in rows:
        key = status_value.value if hasattr(status_value, "value") else str(status_value)
        by_status[key] = count
        total += count

    today_count = db.execute(
        select(func.count()).select_from(Visit).where(
            Visit.scheduled_start >= day_start, Visit.scheduled_start <= day_end
        )
    ).scalar_one()

    assigned = select(VisitAssignment.visit_id)
    unassigned_count = db.execute(
        select(func.count()).select_from(Visit).where(
            Visit.status.in_(_ACTIVE), Visit.id.notin_(assigned)
        )
    ).scalar_one()

    return {
        "total_visits": total,
        "by_status": by_status,
        "today_agenda": today_count,
        "unassigned": unassigned_count,
        "active": sum(by_status[s.value] for s in _ACTIVE),
    }
