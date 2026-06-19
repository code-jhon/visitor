"""Audit trail and sensitive-field protection helpers (VIS-4).

``record_audit`` is the single entry point services/routers use to append an
immutable ``AuditLog`` row (actor, timestamp, action, entity, before/after and
geolocation where applicable). ``mask_fields`` provides role-based serialization
so sensitive health fields are never returned to roles without permission.
"""
from __future__ import annotations

import json
from typing import Any, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AuditLog, User


def _dump(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, default=str, sort_keys=True)


def record_audit(
    db: Session, *, action: str, entity_type: str, entity_id: str = "",
    actor_id: str | None = None, before: Any = None, after: Any = None,
    latitude: float | None = None, longitude: float | None = None,
    commit: bool = True,
) -> AuditLog:
    entry = AuditLog(
        actor_user_id=actor_id, action=action, entity_type=entity_type,
        entity_id=entity_id, before=_dump(before), after=_dump(after),
        latitude=latitude, longitude=longitude,
    )
    db.add(entry)
    if commit:
        db.commit()
        db.refresh(entry)
    return entry


def user_has_permission(user: User, code: str) -> bool:
    granted = {p.code.lower() for r in user.roles for p in r.permissions}
    return code.lower() in granted


def mask_fields(
    data: dict, *, sensitive: Iterable[str], allowed: bool, placeholder: str = ""
) -> dict:
    """Return a copy of ``data`` with sensitive keys masked unless ``allowed``."""
    if allowed:
        return dict(data)
    out = dict(data)
    for key in sensitive:
        if key in out:
            out[key] = placeholder
    return out
