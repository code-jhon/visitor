"""Visit lifecycle, calendar and availability endpoints (VIS-10)."""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.permissions import get_current_user, require_permission
from app.db.models import User
from app.db.models.visits import VisitStatus
from app.db.session import get_db
from app.schemas.scheduling import AssignRequest, IncidentRequest, TransitionRequest
from app.schemas.visits import VisitOut
from app.services import scheduling as svc

router = APIRouter(tags=["scheduling"])


def _transition_endpoint(new_status: VisitStatus):
    def handler(
        visit_id: str,
        body: TransitionRequest,
        db: Session = Depends(get_db),
        user: User = Depends(require_permission("visits:write")),
    ):
        visit = svc.get_visit_or_404(db, visit_id)
        return svc.transition(
            db, visit, new_status, actor_id=user.id,
            latitude=body.latitude, longitude=body.longitude,
            note=body.note, event_at=body.event_at,
        )
    return handler


@router.post("/visits/{visit_id}/assign", status_code=status.HTTP_201_CREATED)
def assign_visit(
    visit_id: str, body: AssignRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("visits:write")),
):
    visit = svc.get_visit_or_404(db, visit_id)
    assignment = svc.assign(
        db, visit, employee_id=body.employee_id,
        provider_id=body.provider_id, actor_id=user.id,
    )
    return {"id": assignment.id, "visit_id": visit.id,
            "employee_id": assignment.employee_id, "provider_id": assignment.provider_id}


router.add_api_route("/visits/{visit_id}/enroute", _transition_endpoint(VisitStatus.en_route),
                     methods=["POST"], response_model=VisitOut)
router.add_api_route("/visits/{visit_id}/start", _transition_endpoint(VisitStatus.in_progress),
                     methods=["POST"], response_model=VisitOut)
router.add_api_route("/visits/{visit_id}/finish", _transition_endpoint(VisitStatus.completed),
                     methods=["POST"], response_model=VisitOut)
router.add_api_route("/visits/{visit_id}/cancel", _transition_endpoint(VisitStatus.cancelled),
                     methods=["POST"], response_model=VisitOut)
router.add_api_route("/visits/{visit_id}/no-show", _transition_endpoint(VisitStatus.no_show),
                     methods=["POST"], response_model=VisitOut)


@router.post("/visits/{visit_id}/incidents", status_code=status.HTTP_201_CREATED)
def report_incident(
    visit_id: str, body: IncidentRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("visits:write")),
):
    visit = svc.get_visit_or_404(db, visit_id)
    inc = svc.report_incident(
        db, visit, type=body.type, severity=body.severity,
        description=body.description, actor_id=user.id,
    )
    return {"id": inc.id, "visit_id": visit.id, "type": inc.type, "severity": inc.severity}


@router.get("/schedule", response_model=list[VisitOut])
def schedule(
    start: datetime | None = Query(default=None, alias="from"),
    end: datetime | None = Query(default=None, alias="to"),
    status_filter: VisitStatus | None = Query(default=None, alias="status"),
    employee_id: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_permission("visits:read")),
):
    return svc.calendar(db, start=start, end=end,
                        status_filter=status_filter, employee_id=employee_id)


@router.get("/schedule/unassigned", response_model=list[VisitOut])
def unassigned(
    db: Session = Depends(get_db),
    _=Depends(require_permission("visits:read")),
):
    return svc.unassigned_visits(db)


@router.get("/schedule/sla-risk", response_model=list[VisitOut])
def sla_risk(
    within_minutes: int = 60,
    db: Session = Depends(get_db),
    _=Depends(require_permission("visits:read")),
):
    return svc.sla_risk_visits(db, within_minutes=within_minutes)


@router.get("/availability")
def availability(
    start: datetime | None = Query(default=None, alias="from"),
    end: datetime | None = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
    _=Depends(require_permission("visits:read")),
):
    return svc.employee_availability(db, start=start, end=end)
