# PRD — Visitor Platform

**Project:** Visitor  
**Product type:** Web platform + Backend API + Mobile app  
**Primary language:** English  
**Source documents reviewed:**
- `Requirements.docx`
- `Propuesta técnica.docx`
- `Copia de Hoja de cálculo sin título.xlsx`
- `Presentación sin título.pptx`

---

## 1. Product Summary

Visitor is a digital platform for managing home healthcare visits for elderly patients. The product will support company administrators, employees/caregivers, providers/coordinators, clients/patients, and support users through a synchronized web and mobile experience.

The platform must help the business manage patients, employees, providers, visit scheduling, visit execution, notifications, reports, billing/financial calculations, and real-time geolocation. The system must prioritize operational reliability, data security, traceability, and real-time visibility.

---

## 2. Background & Problem

The client is a foreign family-owned company providing home healthcare visits for elderly patients. Their current application does not fully satisfy operational needs.

Current pain points:

- Patient, employee, and provider information is not managed effectively.
- Visit scheduling and status tracking require better visibility.
- Mobile staff need a simple way to start, finish, and report incidents during visits.
- The company needs real-time dashboards, maps, reports, and billing/financial outputs.
- Healthcare/patient data must be handled securely and protected from unauthorized access.
- The platform must work across web and mobile environments in a synchronized way.

---

## 3. Goals

### Business Goals

- Improve control and visibility of home healthcare operations.
- Reduce manual effort in scheduling, assignment, reporting, and financial calculations.
- Provide a scalable platform that can support future growth.
- Deliver a high-quality, reliable product within an estimated maximum timeline of 5 months.

### Product Goals

- Provide a web dashboard for administrative and operational management.
- Provide a mobile app for field employees, clients, and relevant operational users.
- Enable real-time visit tracking and georeferenced maps.
- Generate reports and billing/financial information.
- Support alerts, notifications, and internal communication flows.
- Protect sensitive patient and operational data.

---

## 4. User Roles

| Role | Description |
|---|---|
| Admin | Full platform administration and configuration access. |
| Company | Business/operator role with access to operational, scheduling, financial, and reporting modules. |
| Employee | Field professional/caregiver who performs visits. |
| Provider / Coordinator | External provider or coordinator involved in visit delivery and assignments. |
| Client / Patient | Service recipient or requester, able to view visit information, request service, and evaluate service. |
| Support | Support role for assisting users and troubleshooting platform operations. |

---

## 5. Scope

### In Scope

- Web application
- Backend/API/server
- Mobile application for Android and iOS
- Role-based access control
- Employee, client/patient, provider/coordinator management
- Service configuration
- Scheduling and visit lifecycle management
- Real-time map of visits
- Patient detail views
- Service evaluation
- Service request flow
- Alerts and messages
- Financial calculations/liquidations
- Reports and exports
- Search/filtering in core modules
- Data security and auditability
- Support/help affordances

### Out of Scope / To Confirm

- Payment gateway integration
- Electronic medical record integrations
- Insurance provider integrations
- Government tax/pension API integrations
- Offline-first mobile mode
- Video calls or telemedicine features
- Automated route optimization
- Native biometric authentication

---

## 6. Product Architecture

The product should use a client-server architecture:

- **Web Client:** administrative and operational interface.
- **Mobile Client:** field and client-facing experience.
- **Backend Server:** centralized API, business logic, authentication, authorization, reporting, notifications, audit logs, and integrations.
- **Database:** centralized relational database.
- **Infrastructure:** hosted in AWS or equivalent cloud environment.

Preferred implementation technologies:

- Web: React
- Mobile: React Native / cross-platform Android + iOS
- Backend: Python
- Database: PostgreSQL
- Cloud: AWS or equivalent cloud infrastructure

These choices supersede the historical proposal references to Angular, Ionic, Laravel/PHP, and MySQL. Final framework selections within this stack should be validated before development starts, for example React + TypeScript for web, React Native + TypeScript for mobile, and FastAPI or Django for the Python backend.

---

# 7. Web Application PRD

## 7.1 Web Purpose

The web platform is the primary administrative and operational tool. It enables company users, admins, providers/coordinators, employees, and support users to manage master data, schedules, finances, notifications, reports, and visit maps.

## 7.2 Web Core Modules

### 7.2.1 Dashboard

**Description:** Main operational dashboard with real-time visibility.

Functional requirements:

- Display key operational indicators.
- Show agenda/schedule summary.
- Show real-time map or map widget.
- Provide shortcuts to scheduled, active, pending, cancelled, and finalized visits.
- Support dashboard layouts inspired by admin dashboard templates reviewed in the presentation.

Acceptance criteria:

- Authorized users can view summary metrics after login.
- Dashboard updates reflect current visit status.
- Users can navigate from dashboard widgets to detailed module views.

---

### 7.2.2 Employees

**Description:** Manage employee information.

Functional requirements:

- CRUD employees.
- Store personal information.
- Store professional information.
- Store contract/engagement conditions.
- Search employees by configured criteria.
- Associate employees with schedules/visits.

Roles:

- Admin
- Company
- Employee
- Support

Acceptance criteria:

- Users with permission can create, edit, view, and deactivate employees.
- Employee records can be searched and filtered.
- Employee availability can be used during scheduling.

---

### 7.2.3 Clients / Patients

**Description:** Manage client/patient records and scheduling visibility.

Functional requirements:

- CRUD clients/patients.
- Store relevant patient profile information.
- Show client/patient visit calendar.
- Show visit status history.
- Support search by predefined criteria.

Roles:

- Admin
- Company
- Employee
- Client
- Support

Acceptance criteria:

- Authorized users can manage patient information.
- Client/patient records can be linked to visits.
- Visit calendars display correct visit state.

---

### 7.2.4 Provider / Coordinator

**Description:** Manage providers and coordinators involved in service delivery.

Functional requirements:

- CRUD providers/coordinators.
- Store personal, professional, and contract information.
- Associate providers/coordinators with visits or clients where applicable.
- Search and filter provider/coordinator records.

Roles:

- Admin
- Company
- Provider / Coordinator
- Support

Acceptance criteria:

- Authorized users can create, update, view, and deactivate providers/coordinators.
- Provider/coordinator records can be used in scheduling and reports.

---

### 7.2.5 Configuration

**Description:** Configure operational catalogues.

Functional requirements:

- Manage services.
- Manage subservices.
- Manage tariffs:
  - By service
  - By provider
  - By hour
  - By kilometer/mileage allowance
- Manage required certificates/documents.

Roles:

- Admin
- Company
- Support

Acceptance criteria:

- Configuration changes are reflected in scheduling, financial calculations, and reports.
- Only authorized users can modify configuration.

---

### 7.2.6 Scheduling / Visit Management

**Description:** Central module for visit creation, assignment, and lifecycle management.

Functional requirements:

- Create visit/service requests.
- Assign visits to employees/providers.
- Start visits.
- Finalize visits.
- Cancel visits.
- Register incidents/novelties before, during, or after visits.
- Automatically assist status management if employees forget to finalize visits.
- Store every scheduling transaction with timestamp and geolocation where applicable.
- Calendar views:
  - Day
  - Week
  - Month
  - Custom range
- Filters:
  - Scheduled
  - Unscheduled
  - All
  - Cancelled
  - In progress
  - Finalized
  - Employee availability
  - Provider availability

Roles:

- Admin
- Company
- Employee
- Provider / Coordinator
- Client, for request-related flows
- Support

Acceptance criteria:

- Visits can move through defined lifecycle statuses.
- Every status change is auditable.
- Calendar filters return accurate results.
- Users can identify unassigned visits and visits close to SLA/non-compliance.

---

### 7.2.7 Financial Module

**Description:** Generate payroll/liquidation and financial calculations.

Functional requirements:

- Calculate worked hours by date range and contract type.
- Calculate pension according to legal percentages.
- Track vacations.
- Track sick leave/incapacity days.
- Calculate mileage/transportation allowance.
- Handle calculations for natural person employees.
- Use tariff configuration and visit records as calculation inputs.

Roles:

- Admin
- Company
- Support

Acceptance criteria:

- Authorized users can generate liquidations by date range.
- Calculations are traceable to source visits/hours/configuration.
- Financial outputs can feed reports and exports.

---

### 7.2.8 Messages & Alerts

**Description:** Notification and communication channel for operational events.

Functional requirements:

Alerts:

- Services not assigned and close to non-compliance.
- Taxes close to payment deadline.
- Cancelled appointments.
- Visit incidents/novelties.
- Licenses/certificates close to expiration.

Messages:

- Service request.
- Service start.
- Service completion.

Delivery targets:

- Web notification inbox.
- Mobile notifications where supported.
- Email notifications where configured.

Roles:

- Admin
- Company
- Employee
- Provider / Coordinator
- Client
- Support

Acceptance criteria:

- Users receive relevant alerts according to role and permissions.
- Alerts are stored and can be marked as read.
- Critical operational alerts are visible in dashboard or notification center.

---

### 7.2.9 Reports

**Description:** Generate operational, financial, and compliance-oriented reports.

Functional requirements:

Reports must include:

- Paid hours by employee.
- Billed hours by provider.
- Pension report using configured percentage.
- Taxes paid to government by employee.
- Hours assigned by client.
- Vacations.
- Employee sick days.
- Incident history reported by clients.
- Service billing.
- Employee absenteeism.
- Government tax list.
- Periodic service report per client.
- Services provided to each client by provider.
- Periodic client service report per provider.

Export formats:

- PDF
- XLS
- DOC
- Email delivery

Roles:

- Admin
- Company
- Support

Acceptance criteria:

- Authorized users can generate each report by selected filters/date ranges.
- Reports can be exported to supported formats.
- Generated report data matches source operational records.

---

### 7.2.10 Visit Map

**Description:** Real-time map with georeferenced visit/patient data.

Functional requirements:

- Show georeferenced patients/visits on a map.
- Display marker tooltip/summary with relevant patient or visit information.
- Filter by:
  - Scheduled
  - Unscheduled
  - Cancelled
  - Incidents/novelties
- Date filters:
  - Today
  - This week
  - This month
- Support real-time updates where technically feasible.
- Consider heatmaps as an enhancement.

Roles:

- Admin
- Company
- Employee
- Provider / Coordinator
- Support

Acceptance criteria:

- Users can view visits/patients on a map according to permissions.
- Filters update visible markers correctly.
- Clicking a marker opens a useful summary.

---

### 7.2.11 Patient Detail

**Description:** View relevant patient information.

Functional requirements:

- Show patient summary.
- Show relevant visit-related information.
- Show details needed before or during a visit.
- Respect role-based visibility for sensitive fields.

Roles:

- Admin
- Company
- Employee
- Provider / Coordinator
- Client
- Support

Acceptance criteria:

- Authorized users can access patient details.
- Sensitive patient data is only visible to roles with permission.

---

### 7.2.12 Evaluation

**Description:** Client evaluation of completed service.

Functional requirements:

- Provide post-service evaluation form.
- Allow client to rate service quality.
- Link evaluation to visit, employee/provider, and client.
- Make evaluation data available for reports.

Roles:

- Admin
- Company
- Employee
- Client
- Support

Acceptance criteria:

- Clients can evaluate completed services.
- Evaluations are stored and visible to authorized roles.

---

### 7.2.13 Service Request

**Description:** Guided service request flow.

Functional requirements:

- Provide step-by-step service request form.
- Allow registered clients to request assistance.
- Allow non-scheduled or potentially unregistered clients to request service, subject to business rules.
- Display available services and tariffs configured by company.
- Create request notification for company/admin users.

Roles:

- Admin
- Company
- Employee
- Client
- Support

Acceptance criteria:

- Users can submit a service request using a guided flow.
- Submitted requests appear in scheduling/work queue.
- Users receive confirmation after submitting.

---

# 8. Backend PRD

## 8.1 Backend Purpose

The backend provides centralized business logic, APIs, authentication, authorization, database access, reporting, notifications, auditability, geolocation processing, and integrations for web and mobile clients.

## 8.2 Backend Core Capabilities

### Authentication & Authorization

Functional requirements:

- Secure login.
- Role-based access control.
- Permission checks on all APIs.
- Password reset flow.
- Session/token management.
- Optional future support for MFA.

Acceptance criteria:

- Users can only access resources allowed by role/permission.
- Unauthorized requests are rejected.
- Authentication events are auditable.

---

### User & Role Management

Functional requirements:

- Manage users.
- Assign roles.
- Support role-specific profiles:
  - Employee profile
  - Client/patient profile
  - Provider/coordinator profile
  - Support profile
- Activate/deactivate accounts.

Acceptance criteria:

- User account changes are reflected across web and mobile.
- Deactivated users cannot access the system.

---

### Master Data APIs

Entities:

- Employees
- Clients/patients
- Providers/coordinators
- Services
- Subservices
- Tariffs
- Certificates/documents
- Contract types
- Tax/pension configuration

Acceptance criteria:

- CRUD APIs exist for each master entity.
- APIs validate required fields.
- APIs enforce role permissions.

---

### Scheduling & Visit Lifecycle Engine

Visit statuses should include at minimum:

- Requested
- Pending assignment
- Scheduled
- In progress
- Completed
- Cancelled
- Incident / novelty reported

Functional requirements:

- Create visits from service requests.
- Assign employees/providers.
- Track status changes.
- Store timestamps and geolocation for relevant transitions.
- Prevent invalid status transitions.
- Support automated status rules for forgotten finalization cases.
- Expose calendar and availability APIs.

Acceptance criteria:

- Every visit lifecycle event is persisted.
- Status transitions are validated.
- Web and mobile clients receive consistent visit state.

---

### Geolocation & Maps

Functional requirements:

- Store patient/visit coordinates.
- Store employee location at visit start/end where permission is granted.
- Provide map marker API.
- Provide filtered map data by status and date range.
- Support real-time or near-real-time location/status updates.

Acceptance criteria:

- Map APIs return only data authorized for the requesting user.
- Visit location records include timestamp and actor.

---

### Notifications & Messaging

Functional requirements:

- Generate alerts from operational events.
- Persist notification records.
- Deliver notifications to web/mobile inbox.
- Support email notification delivery where configured.
- Support read/unread status.
- Support alert rules for nearing SLA/non-compliance and expiring licenses/certificates.

Acceptance criteria:

- Relevant users receive role-appropriate alerts.
- Notification records are queryable and auditable.

---

### Reporting & Export Engine

Functional requirements:

- Generate operational and financial reports.
- Support filters by date range, employee, provider, client, service, status.
- Export to PDF, XLS, DOC.
- Send reports by email.

Acceptance criteria:

- Reports return accurate data from source records.
- Exported files can be downloaded by authorized users.

---

### Financial / Liquidation Engine

Functional requirements:

- Calculate worked hours.
- Calculate billable hours.
- Calculate pension percentages.
- Calculate vacations and sick leave impacts.
- Calculate mileage/transport allowance.
- Support tariff rules by service, provider, hour, and kilometer.

Acceptance criteria:

- Financial calculations are reproducible and traceable.
- Calculation inputs and outputs are stored or logged.

---

### Audit Trail

Functional requirements:

- Record important data changes.
- Record visit lifecycle events.
- Record actor, timestamp, action, entity, and before/after values where applicable.
- Record geolocation for visit actions where applicable.

Acceptance criteria:

- Admin/support users can trace operational events.
- Audit records cannot be modified by normal users.

---

### Security & Data Protection

Functional requirements:

- Encrypt data in transit using HTTPS/TLS.
- Encrypt sensitive data at rest where appropriate.
- Securely hash passwords.
- Apply least-privilege access control.
- Protect patient and healthcare-related data.
- Validate and sanitize all API inputs.
- Keep server, framework, and dependencies updated.
- Maintain backups for code, database, and uploaded documents.

Acceptance criteria:

- Sensitive endpoints require authentication.
- Sensitive fields are not exposed to unauthorized roles.
- Backups are configured and restorable.

---

## 8.3 Suggested Data Model

Core entities:

- User
- Role
- Permission
- Employee
- Client/Patient
- Provider/Coordinator
- Service
- Subservice
- Tariff
- Certificate/Document Requirement
- Visit
- Visit Assignment
- Visit Status Event
- Visit Incident/Novelty
- Service Request
- Evaluation
- Notification
- Message
- Report Request
- Financial Liquidation
- Audit Log
- Support Ticket

---

## 8.4 Suggested API Groups

- `/auth`
- `/users`
- `/roles`
- `/employees`
- `/clients`
- `/patients`
- `/providers`
- `/services`
- `/tariffs`
- `/certificates`
- `/visits`
- `/visits/{id}/start`
- `/visits/{id}/finish`
- `/visits/{id}/cancel`
- `/visits/{id}/incidents`
- `/schedule`
- `/availability`
- `/map/visits`
- `/service-requests`
- `/evaluations`
- `/notifications`
- `/reports`
- `/exports`
- `/financial/liquidations`
- `/support/tickets`

---

# 9. Mobile App PRD

## 9.1 Mobile Purpose

The mobile app supports real-time field operations and client interactions. It must make visit execution simple for employees and provide clients with service request, visit detail, and evaluation capabilities.

The app should support Android and iOS.

## 9.2 Mobile Core Modules

### 9.2.1 Login & Role-Based Home

Functional requirements:

- Secure login.
- Show home screen based on role.
- Display upcoming visits, notifications, and relevant actions.

Acceptance criteria:

- Users see only role-appropriate modules.
- Login persists securely according to token/session rules.

---

### 9.2.2 Visit Map

Functional requirements:

- Show real-time map of assigned or visible visits.
- Show patient/visit markers.
- Show marker summary tooltip or bottom sheet.
- Filter by:
  - Scheduled
  - Unscheduled
  - Cancelled
  - Incidents/novelties
  - Today
  - Week
  - Month

Acceptance criteria:

- Employee can view assigned visits on the map.
- Authorized roles can view map data according to permissions.

---

### 9.2.3 Visit Management

Functional requirements:

- View assigned visit details.
- Start visit with one button.
- Finish visit with one button.
- Capture timestamp and geolocation on start/end.
- Register incidents/novelties during visit.
- Prompt evaluation flow after completion where applicable.

Acceptance criteria:

- Employee can start and finish a visit from mobile.
- Visit status updates are reflected in the web app.
- Start/end events include timestamp and geolocation where permissions are granted.

---

### 9.2.4 Patient Detail

Functional requirements:

- Show relevant patient information before a visit.
- Show visit-specific notes/instructions.
- Hide sensitive fields according to role.

Acceptance criteria:

- Employee can quickly review patient details before service.
- Unauthorized users cannot access sensitive patient details.

---

### 9.2.5 Evaluation

Functional requirements:

- Allow client to rate completed service.
- Show evaluation questions configured by business.
- Link evaluation to visit and employee/provider.

Acceptance criteria:

- Client can submit evaluation after service completion.
- Evaluation appears in reporting data.

---

### 9.2.6 Service Request

Functional requirements:

- Guided service request form.
- Select service/subservice.
- Provide contact and patient/service details.
- Submit request to company/admin queue.
- Show confirmation.

Acceptance criteria:

- Client can request a service from mobile.
- Request becomes available for scheduling in web platform.

---

### 9.2.7 Notifications

Functional requirements:

- Receive service request, start, completion, cancellation, and incident notifications.
- Show notification inbox.
- Mark notifications as read.
- Support push notifications if platform configuration allows.

Acceptance criteria:

- Users receive relevant notifications on mobile.
- Notification state syncs with backend.

---

## 9.3 Mobile Non-Functional Requirements

- Responsive and accessible UI.
- Fast access to today’s visits.
- Minimal steps for start/end visit actions.
- Clear error handling when GPS/network is unavailable.
- Secure local storage for auth tokens.
- No sensitive data stored locally unless encrypted and required.

---

# 10. Cross-Platform Functional Requirements

## 10.1 Search

Each main web component must include search functionality based on predefined business criteria.

Applicable modules:

- Employees
- Clients/patients
- Providers/coordinators
- Scheduling
- Reports
- Financial records

## 10.2 Help & Support

Functional requirements:

- Each web component should include a help button.
- Help may include images or videos explaining component usage.
- Support should be available by email and ticketing.
- Support ticket application/documentation should be delivered with project documentation.

## 10.3 Internationalization

Functional requirements:

- Required product language: English.
- Platform should be structured to allow future multilingual support if needed.

---

# 11. Non-Functional Requirements

## 11.1 Performance

- Common dashboard and list screens should load quickly under normal expected usage.
- Search and filters should return results without excessive delay.
- Map views should handle expected visit volume without severe degradation.

## 11.2 Availability & Reliability

- Cloud hosting should provide reliable access for web and mobile clients.
- Database backups must be configured.
- System should recover from expected application errors gracefully.

## 11.3 Scalability

- Backend architecture should support future database scaling.
- Business logic should be separated from presentation clients.
- APIs should support adding future modules without major rewrites.

## 11.4 Security

- HTTPS required.
- Secure password storage.
- Role-based authorization.
- Sensitive data protection.
- Audit trail for critical operations.
- Backup and recovery procedures.

## 11.5 Compliance Considerations

Because the product handles patient/healthcare-related information, the project must confirm applicable legal and regulatory requirements based on the operating country/countries, including privacy, healthcare data handling, retention, consent, and breach response obligations.

---

# 12. Milestones & Delivery Plan

Historical proposal estimates a maximum delivery timeline of **5 months**, split into three deliveries:

| Delivery | Progress | Suggested Content |
|---|---:|---|
| Delivery 1 | 30% | Architecture, authentication, core master data, initial web dashboard, employee/client/provider CRUD, basic scheduling. |
| Delivery 2 | 30% | Visit lifecycle, mobile app core flows, maps, notifications, configuration, service requests. |
| Delivery 3 | 40% | Financial module, reports/exports, evaluations, support/help, hardening, QA, deployment, documentation. |

---

# 13. Success Metrics

- Reduction in manual scheduling effort.
- Percentage of visits with complete start/end timestamp and geolocation.
- Percentage of visits assigned before SLA risk.
- Report generation time.
- Number of unresolved operational incidents.
- User adoption by employees/providers.
- Client evaluation completion rate.
- Support ticket volume after launch.

---

# 14. Risks & Open Questions

## Risks

- Sensitive healthcare data may require stricter compliance controls than initially defined.
- Real-time maps and geolocation can increase technical complexity and cost.
- Financial/tax/pension calculations require precise legal/business rules.
- Mobile GPS permissions and network instability may affect visit traceability.
- Legacy/current app data migration may be needed but is not defined in source documents.

## Open Questions

1. Which country/legal framework governs patient data handling?
2. Is HIPAA or another healthcare privacy framework required?
3. Should the mobile app work offline or only with internet access?
4. What exact fields are required for patients, employees, providers, and visits?
5. What are the exact evaluation questions and scoring model?
6. What map provider should be used?
7. Are push notifications required for MVP?
8. Are SMS/WhatsApp/email integrations required?
9. Does the client need data migration from the current application?
10. What are the exact formulas for taxes, pensions, vacations, sick leave, and mileage?
11. Should billing include invoices, payment status, or only report generation?
12. What languages beyond English may be needed in the future?

---

# 15. MVP Recommendation

For MVP, prioritize:

1. Authentication and role-based access.
2. Core master data: employees, clients/patients, providers/coordinators.
3. Services, subservices, tariffs, certificates.
4. Scheduling and visit assignment.
5. Mobile visit start/end with timestamp and geolocation.
6. Visit incidents/novelties.
7. Real-time or near-real-time operational dashboard.
8. Visit map with basic filters.
9. Service request.
10. Evaluations.
11. Essential reports and exports.
12. Notifications for critical visit events.

Defer advanced heatmaps, complex automations, payment integrations, and deep external integrations until after MVP validation.

---

# 16. Implementation Status (changelog)

This section tracks delivery progress against the Linear tickets (`VIS-N`).
Detailed per-ticket strategies live in `docs/tickets/`.

## VIS-1 — Architecture base, infrastructure (AWS) & CI/CD — _in progress_ (2026-06-18)

Foundational scaffolding landed on branch `feature/VIS-1`:

- **Monorepo** under `apps/`: `api` (Python/FastAPI), `web` (React + TypeScript / Vite), `mobile` (React Native + TypeScript), per `docs/tickets/_ARQUITECTURA.md`.
- **Backend**: FastAPI app with `/health` probe, env-driven config (`app/core/config.py`), PostgreSQL/SQLAlchemy session wiring and an empty Alembic setup (no business tables yet — those are VIS-3). Health test passes (`pytest`).
- **Web**: Vite + React + TS, strict TypeScript (no `any`), ESLint/Prettier, React Query, i18n scaffold (base language English), placeholder view pinging the API.
- **Mobile**: React Native + TS scaffold with the same API client + i18n conventions and a placeholder screen.
- **Infrastructure**: Terraform stubs in `infra/` for the AWS target (VPC, RDS PostgreSQL, ECS/Fargate, S3, Secrets Manager, ACM) with per-environment `tfvars` (dev/staging/prod).
- **CI/CD**: GitHub Actions — `ci.yml` (lint/build/test per app) and `deploy.yml` (per-environment deploy, manual + on `main`).
- **Env**: `.env.example` documenting backend/web/mobile variables; root `.gitignore`.

Confirmed stack decisions (supersede historical Angular/Ionic/Laravel/MySQL references): React+TS web, React Native+TS mobile, Python/FastAPI + SQLAlchemy/Alembic backend, PostgreSQL, AWS. Open infra items to finalize: real IaC modules, domains/TLS, automated backups + a restore drill (VIS-1 acceptance criteria).
