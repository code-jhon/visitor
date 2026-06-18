"""Factory that builds a permission-guarded CRUD router for a model (VIS-3).

Every master-data endpoint group is generated from this factory so the API is
uniform: ``GET`` (list), ``POST`` (create), ``GET /{id}``, ``PATCH /{id}`` and
``DELETE /{id}``. Reads require ``read_perm``; writes require ``write_perm``
(the role→permission matrix is seeded by the migrations).

NOTE: this module deliberately does *not* use ``from __future__ import
annotations`` — the generated handlers reference the create/update Pydantic
schemas as live annotations so FastAPI can build request validation from them.
"""
from typing import Type

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.session import Base, get_db
from app.services.crud import CRUDService


def make_crud_router(
    *,
    prefix: str,
    tags: list[str],
    model: Type[Base],
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    out_schema: Type[BaseModel],
    read_perm: str,
    write_perm: str,
    allow_update: bool = True,
    allow_delete: bool = True,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)
    svc = CRUDService(model)
    not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    @router.get("", response_model=list[out_schema])
    def list_items(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        _=Depends(require_permission(read_perm)),
    ):
        return svc.list(db, skip=skip, limit=limit)

    @router.post("", response_model=out_schema, status_code=status.HTTP_201_CREATED)
    def create_item(
        body: create_schema,
        db: Session = Depends(get_db),
        _=Depends(require_permission(write_perm)),
    ):
        try:
            return svc.create(db, body.model_dump(exclude_unset=False))
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referential integrity error (check foreign keys)",
            )

    @router.get("/{item_id}", response_model=out_schema)
    def get_item(
        item_id: str,
        db: Session = Depends(get_db),
        _=Depends(require_permission(read_perm)),
    ):
        obj = svc.get(db, item_id)
        if obj is None:
            raise not_found
        return obj

    if allow_update:

        @router.patch("/{item_id}", response_model=out_schema)
        def update_item(
            item_id: str,
            body: update_schema,
            db: Session = Depends(get_db),
            _=Depends(require_permission(write_perm)),
        ):
            obj = svc.get(db, item_id)
            if obj is None:
                raise not_found
            try:
                return svc.update(db, obj, body.model_dump(exclude_unset=True))
            except IntegrityError:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Referential integrity error (check foreign keys)",
                )

    if allow_delete:

        @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_item(
            item_id: str,
            db: Session = Depends(get_db),
            _=Depends(require_permission(write_perm)),
        ):
            obj = svc.get(db, item_id)
            if obj is None:
                raise not_found
            svc.delete(db, obj)

    return router
