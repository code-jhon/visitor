"""Schemas for people master data: employees, providers, clients, patients."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class _ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- Employee --------------------------------------------------------------
class EmployeeCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    user_id: str | None = None
    document_id: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    position: str = ""
    is_active: bool = True


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=120)
    last_name: str | None = Field(default=None, min_length=1, max_length=120)
    user_id: str | None = None
    document_id: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    position: str | None = None
    is_active: bool | None = None


class EmployeeOut(_ORM):
    id: str
    user_id: str | None
    first_name: str
    last_name: str
    document_id: str
    email: str
    phone: str
    address: str
    position: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# --- Provider --------------------------------------------------------------
class ProviderCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    user_id: str | None = None
    contact_name: str = ""
    email: str = ""
    phone: str = ""
    is_active: bool = True


class ProviderUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    user_id: str | None = None
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    is_active: bool | None = None


class ProviderOut(_ORM):
    id: str
    user_id: str | None
    name: str
    contact_name: str
    email: str
    phone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# --- Client ----------------------------------------------------------------
class ClientCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    user_id: str | None = None
    document_id: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    is_active: bool = True


class ClientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=120)
    last_name: str | None = Field(default=None, min_length=1, max_length=120)
    user_id: str | None = None
    document_id: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool | None = None


class ClientOut(_ORM):
    id: str
    user_id: str | None
    first_name: str
    last_name: str
    document_id: str
    email: str
    phone: str
    address: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# --- Patient ---------------------------------------------------------------
class PatientCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    client_id: str | None = None
    document_id: str = ""
    birth_date: date | None = None
    address: str = ""
    medical_notes: str = ""


class PatientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=120)
    last_name: str | None = Field(default=None, min_length=1, max_length=120)
    client_id: str | None = None
    document_id: str | None = None
    birth_date: date | None = None
    address: str | None = None
    medical_notes: str | None = None


class PatientOut(_ORM):
    id: str
    client_id: str | None
    first_name: str
    last_name: str
    document_id: str
    birth_date: date | None
    address: str
    medical_notes: str
    created_at: datetime
    updated_at: datetime
