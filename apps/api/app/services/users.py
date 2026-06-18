"""User/role service helpers shared by the auth and users routers (VIS-2)."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models import Role, User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()


def resolve_roles(db: Session, role_names: list[str]) -> list[Role]:
    """Return Role rows for the given names, raising on unknown names."""
    if not role_names:
        return []
    roles = db.execute(
        select(Role).where(Role.name.in_([r.lower() for r in role_names]))
    ).scalars().all()
    found = {r.name for r in roles}
    missing = {r.lower() for r in role_names} - found
    if missing:
        raise ValueError(f"Unknown roles: {', '.join(sorted(missing))}")
    return list(roles)


def create_user(
    db: Session, email: str, password: str, full_name: str, role_names: list[str]
) -> User:
    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
        roles=resolve_roles(db, role_names),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
