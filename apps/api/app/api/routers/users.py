"""User management router: CRUD, role assignment, activation (VIS-2).

Every endpoint is guarded by RBAC. ``users:write`` / ``roles:assign`` are held
by admin and empresa roles per the seeded matrix.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.permissions import get_current_user, require_permission
from app.core.security import hash_password
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import (
    RoleAssignment,
    UserCreate,
    UserOut,
    UserUpdate,
)
from app.services.users import create_user, get_user_by_email, resolve_roles

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def read_me(current: User = Depends(get_current_user)) -> User:
    """Return the authenticated user's own profile."""
    return current


@router.get("", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users:read")),
) -> list[User]:
    return list(db.execute(select(User)).scalars().all())


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create(
    body: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users:write")),
) -> User:
    if get_user_by_email(db, body.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    try:
        return create_user(db, body.email, body.password, body.full_name, body.roles)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users:read")),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: str,
    body: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users:write")),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if body.full_name is not None:
        user.full_name = body.full_name
    if body.password is not None:
        user.hashed_password = hash_password(body.password)
    if body.is_active is not None:
        user.is_active = body.is_active
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/roles", response_model=UserOut)
def assign_roles(
    user_id: str,
    body: RoleAssignment,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("roles:assign")),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        user.roles = resolve_roles(db, body.roles)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    db.commit()
    db.refresh(user)
    return user


@router.post("/{user_id}/deactivate", response_model=UserOut)
def deactivate(
    user_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users:write")),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


@router.post("/{user_id}/activate", response_model=UserOut)
def activate(
    user_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users:write")),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user
