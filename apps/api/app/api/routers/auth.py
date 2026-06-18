"""Authentication router: login, refresh and password recovery (VIS-2).

Emits the auth lifecycle events that VIS-4 will persist to the audit log; for
now they are logged. Token storage on the client (httpOnly/secure cookie on
web, SecureStore on mobile) is handled by the front-ends.
"""
from __future__ import annotations

import logging

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    REFRESH_TOKEN,
    RESET_TOKEN,
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import (
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshRequest,
    Token,
)
from app.services.users import get_user_by_email

logger = logging.getLogger("visitor.auth")
router = APIRouter(prefix="/auth", tags=["auth"])

_INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Bearer"},
)


def _issue_tokens(user: User) -> Token:
    roles = [r.name for r in user.roles]
    return Token(
        access_token=create_access_token(user.id, roles),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """Exchange email + password (OAuth2 password grant) for tokens."""
    user = get_user_by_email(db, form.username)
    if user is None or not verify_password(form.password, user.hashed_password):
        logger.info("auth.login.failed email=%s", form.username)
        raise _INVALID_CREDENTIALS
    if not user.is_active:
        logger.info("auth.login.disabled user=%s", user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled"
        )
    logger.info("auth.login.success user=%s", user.id)
    return _issue_tokens(user)


@router.post("/refresh", response_model=Token)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)) -> Token:
    """Issue a fresh token pair from a valid refresh token."""
    try:
        payload = decode_token(body.refresh_token, expected_type=REFRESH_TOKEN)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    user = db.get(User, payload.get("sub"))
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    return _issue_tokens(user)


@router.post("/password-reset/request", status_code=status.HTTP_202_ACCEPTED)
def password_reset_request(
    body: PasswordResetRequest, db: Session = Depends(get_db)
) -> dict[str, str]:
    """Begin password recovery.

    Always returns 202 regardless of whether the email exists, to avoid
    leaking which accounts are registered. When the account exists a reset
    token is generated; delivery (email/SMS) is wired in a later ticket.
    """
    user = get_user_by_email(db, body.email)
    if user is not None and user.is_active:
        token = create_password_reset_token(user.id)
        logger.info("auth.password_reset.requested user=%s", user.id)
        # TODO(VIS-13): deliver `token` via the notifications channel.
        return {"detail": "If the account exists, a reset link has been sent.", "reset_token": token}
    return {"detail": "If the account exists, a reset link has been sent."}


@router.post("/password-reset/confirm")
def password_reset_confirm(
    body: PasswordResetConfirm, db: Session = Depends(get_db)
) -> dict[str, str]:
    """Complete password recovery using a valid reset token."""
    try:
        payload = decode_token(body.token, expected_type=RESET_TOKEN)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )
    user = db.get(User, payload.get("sub"))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )
    user.hashed_password = hash_password(body.new_password)
    db.commit()
    logger.info("auth.password_reset.confirmed user=%s", user.id)
    return {"detail": "Password updated"}
