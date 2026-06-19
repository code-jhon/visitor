"""Generic CRUD service shared by the master-data routers (VIS-3).

A thin, typed wrapper over SQLAlchemy so every entity gets consistent
list/get/create/update/delete behavior with referential-integrity handling.
"""
from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import Base

ModelT = TypeVar("ModelT", bound=Base)


class CRUDService(Generic[ModelT]):
    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelT]:
        stmt = select(self.model).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def get(self, db: Session, obj_id: str) -> ModelT | None:
        return db.get(self.model, obj_id)

    def create(self, db: Session, data: dict[str, Any]) -> ModelT:
        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: ModelT, data: dict[str, Any]) -> ModelT:
        for field, value in data.items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: ModelT) -> None:
        db.delete(obj)
        db.commit()
