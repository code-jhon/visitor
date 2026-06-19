"""Business helpers for the Clients/Patients module (VIS-7).

Search by criteria, the per-patient visit calendar, and role-based visibility of
sensitive health fields. The sensitive-field masking implemented here is the
module-level application of the cross-cutting rule hardened by VIS-4.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import Client, Patient, User, Visit

# Roles allowed to see sensitive patient health data (e.g. medical notes).
# VIS-4 replaces this with a permission-driven policy.
SENSITIVE_ROLES = {"admin", "empresa", "empleado", "soporte"}


def can_see_sensitive(user: User) -> bool:
    return bool({r.name.lower() for r in user.roles} & SENSITIVE_ROLES)


def serialize_patient(patient: Patient, *, sensitive: bool) -> dict:
    return {
        "id": patient.id,
        "client_id": patient.client_id,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "document_id": patient.document_id,
        "birth_date": patient.birth_date,
        "address": patient.address,
        # Masked for roles without permission.
        "medical_notes": patient.medical_notes if sensitive else "",
    }


def search_clients(
    db: Session, *, q: str | None = None, document_id: str | None = None,
    is_active: bool | None = None, skip: int = 0, limit: int = 100,
) -> list[Client]:
    stmt = select(Client)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Client.first_name.ilike(like), Client.last_name.ilike(like)))
    if document_id:
        stmt = stmt.where(Client.document_id == document_id)
    if is_active is not None:
        stmt = stmt.where(Client.is_active.is_(is_active))
    return list(db.execute(stmt.offset(skip).limit(limit)).scalars().all())


def search_patients(
    db: Session, *, q: str | None = None, document_id: str | None = None,
    client_id: str | None = None, skip: int = 0, limit: int = 100,
) -> list[Patient]:
    stmt = select(Patient)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Patient.first_name.ilike(like), Patient.last_name.ilike(like)))
    if document_id:
        stmt = stmt.where(Patient.document_id == document_id)
    if client_id:
        stmt = stmt.where(Patient.client_id == client_id)
    return list(db.execute(stmt.offset(skip).limit(limit)).scalars().all())


def patient_calendar(
    db: Session, patient_id: str, *,
    start: datetime | None = None, end: datetime | None = None,
) -> list[dict]:
    stmt = select(Visit).where(Visit.patient_id == patient_id)
    if start is not None:
        stmt = stmt.where((Visit.scheduled_end.is_(None)) | (Visit.scheduled_end >= start))
    if end is not None:
        stmt = stmt.where((Visit.scheduled_start.is_(None)) | (Visit.scheduled_start <= end))
    stmt = stmt.order_by(Visit.scheduled_start)
    return [
        {
            "visit_id": v.id,
            "status": v.status.value,
            "scheduled_start": v.scheduled_start,
            "scheduled_end": v.scheduled_end,
            "address": v.address,
        }
        for v in db.execute(stmt).scalars().all()
    ]
