"""Search, calendar and role-aware reads for Clients/Patients (VIS-7)."""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.permissions import get_current_user, require_permission
from app.db.models import Patient, User
from app.db.session import get_db
from app.schemas.people import ClientOut
from app.services import clients as clients_svc

router = APIRouter(tags=["people"])


@router.get("/clients/search", response_model=list[ClientOut])
def search_clients(
    q: str | None = None, document_id: str | None = None, is_active: bool | None = None,
    skip: int = 0, limit: int = Query(default=100, le=250),
    db: Session = Depends(get_db),
    _=Depends(require_permission("clients:read")),
):
    return clients_svc.search_clients(
        db, q=q, document_id=document_id, is_active=is_active, skip=skip, limit=limit
    )


@router.get("/patients/search")
def search_patients(
    q: str | None = None, document_id: str | None = None, client_id: str | None = None,
    skip: int = 0, limit: int = Query(default=100, le=250),
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("patients:read")),
):
    sensitive = clients_svc.can_see_sensitive(user)
    rows = clients_svc.search_patients(
        db, q=q, document_id=document_id, client_id=client_id, skip=skip, limit=limit
    )
    return [clients_svc.serialize_patient(p, sensitive=sensitive) for p in rows]


@router.get("/patients/{patient_id}/calendar")
def patient_calendar(
    patient_id: str,
    start: datetime | None = Query(default=None, alias="from"),
    end: datetime | None = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
    _=Depends(require_permission("patients:read")),
):
    if db.get(Patient, patient_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return {
        "patient_id": patient_id,
        "visits": clients_svc.patient_calendar(db, patient_id, start=start, end=end),
    }
