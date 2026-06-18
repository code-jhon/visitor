"""RBAC dependencies for FastAPI routers (VIS-2).

Usage pattern adopted by every protected router:

    from app.core.permissions import require_roles, get_current_user

    @router.get("/employees", dependencies=[Depends(require_roles("admin", "empresa"))])
    def list_employees(...): ...

``get_current_user`` resolves the bearer token to a ``User`` row and rejects
inactive accounts. ``require_roles`` / ``require_permission`` build on top of it
to enforce the role→permission matrix defined in the PRD (§4).
"""
from __future__ import annotations

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import ACCESS_TOKEN, decode_token
from app.db.models import User
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_CREDENTIALS_EXC = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the access token to an active user, or raise 401."""
    try:
        payload = decode_token(token, expected_type=ACCESS_TOKEN)
        user_id = payload.get("sub")
        if user_id is None:
            raise _CREDENTIALS_EXC
    except jwt.InvalidTokenError:
        raise _CREDENTIALS_EXC

    user = db.get(User, user_id)
    if user is None:
        raise _CREDENTIALS_EXC
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled"
        )
    return user


def require_roles(*roles: str):
    """Dependency factory: allow only users holding one of ``roles``."""
    allowed = {r.lower() for r in roles}

    def _checker(user: User = Depends(get_current_user)) -> User:
        user_roles = {r.name.lower() for r in user.roles}
        if not (allowed & user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role",
            )
        return user

    return _checker


def require_permission(*permissions: str):
    """Dependency factory: allow only users whose roles grant ``permissions``."""
    needed = {p.lower() for p in permissions}

    def _checker(user: User = Depends(get_current_user)) -> User:
        granted = {
            perm.code.lower() for role in user.roles for perm in role.permissions
        }
        if not needed.issubset(granted):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permission",
            )
        return user

    return _checker
