"""Search and availability endpoints for People modules (VIS-6, VIS-7).

These complement the generic master-data CRUD generated in ``domain.py`` with
the search-by-criteria and availability/calendar reads that the web modules and
the scheduling engine need.
"""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.models import Employee
from app.db.session import get_db
from app.schemas.people import EmployeeOut
from app.services import people as people_svc

router = APIRouter(tags=["people"])


@router.get("/employees/search", response_model=list[EmployeeOut])
def search_employees(
    q: str | None = Query(default=None, description="Name fragment"),
    document_id: str | None = None,
    position: str | None = None,
    is_active: bool | None = None,
    skip: int = 0,
    limit: int = Query(default=100, le=250),
    db: Session = Depends(get_db),
    _=Depends(require_permission("employees:read")),
):
    return people_svc.search_employees(
        db, q=q, document_id=document_id, position=position,
        is_active=is_active, skip=skip, limit=limit,
    )


@router.get("/employees/{employee_id}/availability")
def employee_availability(
    employee_id: str,
    start: datetime | None = Query(default=None, alias="from"),
    end: datetime | None = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
    _=Depends(require_permission("employees:read")),
):
    emp = db.get(Employee, employee_id)
    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    busy = people_svc.employee_busy_slots(db, employee_id, start=start, end=end)
    return {
        "employee_id": employee_id,
        "is_active": emp.is_active,
        "available": emp.is_active and len(busy) == 0,
        "busy_slots": busy,
    }
