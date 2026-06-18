"""Pydantic schemas for auth and user management (VIS-2)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = ""


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    roles: list[str] = Field(default_factory=list, description="Role names to assign")


class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None


class RoleAssignment(BaseModel):
    roles: list[str] = Field(description="Role names the user should have")


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    is_active: bool
    roles: list[RoleOut] = Field(default_factory=list)
