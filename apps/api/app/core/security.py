"""Password hashing and JWT issuance/verification (VIS-2).

Security primitives shared by the auth router and the RBAC dependencies:

* Passwords are hashed with bcrypt via passlib — never stored in plaintext.
* Access and refresh tokens are signed JWTs (HS256 by default). The token
  ``type`` claim distinguishes them so a refresh token can't be used as an
  access token and vice-versa.
* A dedicated short-lived "reset" token backs the password-recovery flow.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"
RESET_TOKEN = "reset"


def hash_password(password: str) -> str:
    """Return a bcrypt hash for ``password``."""
    return _pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Check ``password`` against a stored bcrypt ``hashed`` value."""
    return _pwd_context.verify(password, hashed)


def _create_token(
    subject: str,
    token_type: str,
    expires_minutes: int,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
        "jti": uuid.uuid4().hex,
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str, roles: list[str]) -> str:
    """Issue a short-lived access token carrying the user's roles."""
    return _create_token(
        subject,
        ACCESS_TOKEN,
        settings.access_token_expire_minutes,
        {"roles": roles},
    )


def create_refresh_token(subject: str) -> str:
    """Issue a long-lived refresh token used to mint new access tokens."""
    return _create_token(subject, REFRESH_TOKEN, settings.refresh_token_expire_minutes)


def create_password_reset_token(subject: str) -> str:
    """Issue a single-purpose token for confirming a password reset."""
    return _create_token(subject, RESET_TOKEN, settings.password_reset_expire_minutes)


def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    """Decode and validate a JWT.

    Raises ``jwt.InvalidTokenError`` (or a subclass such as
    ``ExpiredSignatureError``) when the signature, expiry or token type is
    invalid, so callers can map the failure to a 401.
    """
    payload = jwt.decode(
        token, settings.secret_key, algorithms=[settings.jwt_algorithm]
    )
    if expected_type is not None and payload.get("type") != expected_type:
        raise jwt.InvalidTokenError("unexpected token type")
    return payload
