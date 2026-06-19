"""Master-data CRUD routers for the domain model (VIS-3, PRD §8.4).

Each API group is generated from ``make_crud_router`` so behavior and RBAC are
uniform. Business-logic-heavy groups (visits state machine, financial
calculations, audit population) expose the base CRUD here; their rules are
implemented by the dedicated tickets (VIS-10, VIS-16, VIS-4...).
"""
from __future__ import annotations

from app.api.crud_router import make_crud_router
from app.db import models
from app.schemas import catalog as cat
from app.schemas import operations as ops
from app.schemas import people as ppl
from app.schemas import visits as vis

# --- Catalog ---------------------------------------------------------------
services_router = make_crud_router(
    prefix="/services", tags=["catalog"], model=models.Service,
    create_schema=cat.ServiceCreate, update_schema=cat.ServiceUpdate,
    out_schema=cat.ServiceOut, read_perm="services:read", write_perm="services:write",
)
subservices_router = make_crud_router(
    prefix="/subservices", tags=["catalog"], model=models.Subservice,
    create_schema=cat.SubserviceCreate, update_schema=cat.SubserviceUpdate,
    out_schema=cat.SubserviceOut, read_perm="services:read", write_perm="services:write",
)
tariffs_router = make_crud_router(
    prefix="/tariffs", tags=["catalog"], model=models.Tariff,
    create_schema=cat.TariffCreate, update_schema=cat.TariffUpdate,
    out_schema=cat.TariffOut, read_perm="tariffs:read", write_perm="tariffs:write",
)
certificates_router = make_crud_router(
    prefix="/certificates", tags=["catalog"], model=models.CertificateRequirement,
    create_schema=cat.CertificateRequirementCreate,
    update_schema=cat.CertificateRequirementUpdate,
    out_schema=cat.CertificateRequirementOut,
    read_perm="certificates:read", write_perm="certificates:write",
)

# --- People ----------------------------------------------------------------
employees_router = make_crud_router(
    prefix="/employees", tags=["people"], model=models.Employee,
    create_schema=ppl.EmployeeCreate, update_schema=ppl.EmployeeUpdate,
    out_schema=ppl.EmployeeOut, read_perm="employees:read", write_perm="employees:write",
)
providers_router = make_crud_router(
    prefix="/providers", tags=["people"], model=models.Provider,
    create_schema=ppl.ProviderCreate, update_schema=ppl.ProviderUpdate,
    out_schema=ppl.ProviderOut, read_perm="providers:read", write_perm="providers:write",
)
clients_router = make_crud_router(
    prefix="/clients", tags=["people"], model=models.Client,
    create_schema=ppl.ClientCreate, update_schema=ppl.ClientUpdate,
    out_schema=ppl.ClientOut, read_perm="clients:read", write_perm="clients:write",
)
patients_router = make_crud_router(
    prefix="/patients", tags=["people"], model=models.Patient,
    create_schema=ppl.PatientCreate, update_schema=ppl.PatientUpdate,
    out_schema=ppl.PatientOut, read_perm="patients:read", write_perm="patients:write",
)

# --- Visits (structure only; state machine in VIS-10) ----------------------
visits_router = make_crud_router(
    prefix="/visits", tags=["visits"], model=models.Visit,
    create_schema=vis.VisitCreate, update_schema=vis.VisitUpdate,
    out_schema=vis.VisitOut, read_perm="visits:read", write_perm="visits:write",
)
visit_assignments_router = make_crud_router(
    prefix="/visit-assignments", tags=["visits"], model=models.VisitAssignment,
    create_schema=vis.VisitAssignmentCreate, update_schema=vis.VisitAssignmentUpdate,
    out_schema=vis.VisitAssignmentOut, read_perm="visits:read", write_perm="visits:write",
)
# Append-only status-event log: create + read only.
visit_status_events_router = make_crud_router(
    prefix="/visit-status-events", tags=["visits"], model=models.VisitStatusEvent,
    create_schema=vis.VisitStatusEventCreate, update_schema=vis.VisitStatusEventCreate,
    out_schema=vis.VisitStatusEventOut, read_perm="visits:read", write_perm="visits:write",
    allow_update=False, allow_delete=False,
)
visit_incidents_router = make_crud_router(
    prefix="/visit-incidents", tags=["visits"], model=models.VisitIncident,
    create_schema=vis.VisitIncidentCreate, update_schema=vis.VisitIncidentUpdate,
    out_schema=vis.VisitIncidentOut, read_perm="visits:read", write_perm="visits:write",
)

# --- Operations ------------------------------------------------------------
service_requests_router = make_crud_router(
    prefix="/service-requests", tags=["operations"], model=models.ServiceRequest,
    create_schema=ops.ServiceRequestCreate, update_schema=ops.ServiceRequestUpdate,
    out_schema=ops.ServiceRequestOut,
    read_perm="service-requests:read", write_perm="service-requests:write",
)
evaluations_router = make_crud_router(
    prefix="/evaluations", tags=["operations"], model=models.Evaluation,
    create_schema=ops.EvaluationCreate, update_schema=ops.EvaluationUpdate,
    out_schema=ops.EvaluationOut,
    read_perm="evaluations:read", write_perm="evaluations:write",
)
notifications_router = make_crud_router(
    prefix="/notifications", tags=["operations"], model=models.Notification,
    create_schema=ops.NotificationCreate, update_schema=ops.NotificationUpdate,
    out_schema=ops.NotificationOut,
    read_perm="notifications:read", write_perm="notifications:write",
)
financial_router = make_crud_router(
    prefix="/financial/liquidations", tags=["financial"],
    model=models.FinancialLiquidation,
    create_schema=ops.FinancialLiquidationCreate,
    update_schema=ops.FinancialLiquidationUpdate,
    out_schema=ops.FinancialLiquidationOut,
    read_perm="financial:read", write_perm="financial:write",
)
support_router = make_crud_router(
    prefix="/support/tickets", tags=["support"], model=models.SupportTicket,
    create_schema=ops.SupportTicketCreate, update_schema=ops.SupportTicketUpdate,
    out_schema=ops.SupportTicketOut, read_perm="support:read", write_perm="support:write",
)

ALL_ROUTERS = [
    services_router,
    subservices_router,
    tariffs_router,
    certificates_router,
    employees_router,
    providers_router,
    clients_router,
    patients_router,
    visits_router,
    visit_assignments_router,
    visit_status_events_router,
    visit_incidents_router,
    service_requests_router,
    evaluations_router,
    notifications_router,
    financial_router,
    support_router,
]
