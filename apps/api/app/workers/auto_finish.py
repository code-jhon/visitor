"""Forgotten-finish auto-management worker (VIS-10).

A visit left ``in_progress`` well past its scheduled end is auto-completed and a
status event + audit row are written so the timeline stays accurate. Schedule
this via cron/Celery in production (wiring is infra, VIS-1). The grace period
must be agreed with the business (PRD §14 open question).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Visit
from app.db.models.visits import VisitStatus
from app.services import scheduling


def auto_finish_overdue(db: Session, *, grace_hours: int = 2) -> list[str]:
    """Auto-complete in-progress visits whose scheduled_end is well past.

    Returns the ids of the visits that were auto-completed.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=grace_hours)
    stmt = (
        select(Visit)
        .where(Visit.status == VisitStatus.in_progress)
        .where(Visit.scheduled_end.is_not(None))
        .where(Visit.scheduled_end < cutoff)
    )
    finished: list[str] = []
    for visit in db.execute(stmt).scalars().all():
        scheduling.transition(
            db, visit, VisitStatus.completed,
            note="auto-completed: forgotten finish (VIS-10 worker)",
        )
        finished.append(visit.id)
    return finished
