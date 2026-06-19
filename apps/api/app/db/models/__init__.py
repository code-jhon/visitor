"""SQLAlchemy models.

VIS-2 introduced auth/RBAC tables; VIS-3 adds the full domain model (catalog,
people, visits and operations). All models are imported here so Alembic's
autogenerate and ``Base.metadata`` see them.
"""
from app.db.models.user import (
    Permission,
    Role,
    User,
    UserProfile,
    role_permissions,
    user_roles,
)
from app.db.models.catalog import (
    CertificateRequirement,
    Service,
    Subservice,
    Tariff,
    TariffModality,
)
from app.db.models.people import Client, Employee, Patient, Provider
from app.db.models.visits import (
    Visit,
    VisitAssignment,
    VisitIncident,
    VisitStatus,
    VisitStatusEvent,
)
from app.db.models.operations import (
    AuditLog,
    Evaluation,
    FinancialLiquidation,
    Message,
    Notification,
    ReportRequest,
    ServiceRequest,
    SupportTicket,
)

__all__ = [
    # auth / rbac (VIS-2)
    "User",
    "Role",
    "Permission",
    "UserProfile",
    "user_roles",
    "role_permissions",
    # catalog
    "Service",
    "Subservice",
    "Tariff",
    "TariffModality",
    "CertificateRequirement",
    # people
    "Employee",
    "Provider",
    "Client",
    "Patient",
    # visits
    "Visit",
    "VisitAssignment",
    "VisitStatusEvent",
    "VisitIncident",
    "VisitStatus",
    # operations
    "ServiceRequest",
    "Evaluation",
    "Notification",
    "Message",
    "ReportRequest",
    "FinancialLiquidation",
    "AuditLog",
    "SupportTicket",
]
