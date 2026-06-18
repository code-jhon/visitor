"""Visitor API entrypoint (VIS-1 scaffolding).

Exposes a health check only. Auth (VIS-2), data model (VIS-3) and domain
routers are added by later tickets.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(title="Visitor API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness/readiness probe used by CI/CD and load balancers."""
    return {"status": "ok", "environment": settings.environment}
