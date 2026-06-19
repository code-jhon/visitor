"""Visitor API entrypoint.

VIS-1 set up the health check; VIS-2 added authentication, RBAC and user
management; VIS-3 adds the master-data CRUD routers for the domain model
(catalog, people, visits and operations).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import audit, auth, users
from app.api.routers.domain import ALL_ROUTERS
from app.core.config import settings

app = FastAPI(title="Visitor API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(audit.router)
for _router in ALL_ROUTERS:
    app.include_router(_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness/readiness probe used by CI/CD and load balancers."""
    return {"status": "ok", "environment": settings.environment}
