# Visitor

Digital platform for managing home healthcare visits for elderly patients —
web dashboard, backend API, and mobile app, synchronized in real time.

See [`PRD_Visitor_Web_Backend_Mobile.md`](./PRD_Visitor_Web_Backend_Mobile.md)
for the full product spec and [`docs/tickets/`](./docs/tickets/) for per-ticket
implementation strategies. Architecture conventions live in
[`docs/tickets/_ARQUITECTURA.md`](./docs/tickets/_ARQUITECTURA.md).

## Stack

| Layer | Technology |
|---|---|
| Web | React + TypeScript (Vite), React Query, strict TS |
| Mobile | React Native + TypeScript (Android + iOS) |
| Backend | Python + FastAPI, SQLAlchemy + Alembic |
| Database | PostgreSQL |
| Infrastructure | AWS (VPC, RDS, ECS/Fargate, S3, Secrets Manager, ACM) |
| CI/CD | GitHub Actions |

These supersede the historical Angular/Ionic/Laravel/MySQL references in the
original proposal.

## Repository layout

```
apps/
  api/      # FastAPI backend (health check, DB + Alembic wiring)
  web/      # React + TS web app (Vite)
  mobile/   # React Native + TS app
infra/      # Terraform (AWS) — environment stubs
.github/workflows/  # CI (lint/build/test) and Deploy pipelines
docs/       # PRD, technical proposal, screens, ticket strategies
```

## Quick start

Backend:
```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../../.env.example .env
uvicorn app.main:app --reload --port 8000   # http://localhost:8000/health
```

Web:
```bash
cd apps/web
npm install
npm run dev   # http://localhost:5173
```

Mobile:
```bash
cd apps/mobile
npm install && npm start
npm run android   # or: npm run ios
```

Copy `.env.example` to `.env` and adjust per environment. Environments
(dev / staging / prod) are kept isolated via separate infra backends and
`infra/env/*.tfvars`.

## Status

- **VIS-1** — architecture base, infrastructure & CI/CD scaffolding: done.
- **VIS-2** — authentication, RBAC and user/role management: done. JWT
  access/refresh tokens, bcrypt hashing, role→permission matrix with reusable
  FastAPI guards, user CRUD + role assignment + activate/deactivate, password
  recovery, and login flows on web and mobile. Seeded roles (PRD §4) and an
  initial admin via Alembic migration `0001_auth_rbac`.
- **VIS-3** — data model and master-data APIs: done. Full relational schema
  (catalog, people, visit lifecycle and operational tables) with versioned
  Alembic migration `0002_master_data`, plus uniform permission-guarded CRUD
  routers for every API group (PRD §8.4) generated from a shared factory.
  Visit status is a typed enum aligned with VIS-10; the status-event log is
  append-only. Per-group `:read`/`:write` permissions seeded and granted across
  roles.

The modules below were each built on their own `feature/VIS-N` branch off `dev`
(which was fast-forwarded to VIS-3, their shared foundation) and are **QA ready**
in Linear, pending review/merge. Every module ships green pytest cases.

- **VIS-4** — audit trail, security & data protection: QA ready
  (`feature/VIS-4`). `record_audit` writes immutable `AuditLog` rows (actor,
  timestamp, action, entity, before/after, geolocation); `mask_fields` masks
  sensitive health data by role; read-only `GET /audit-logs` (`audit:read`,
  Admin/Soporte) with no write routes (append-only). Migration
  `0003_audit_permissions`.
- **VIS-5** — operational dashboard: QA ready (`feature/VIS-5`).
  `GET /dashboard/summary` aggregates visits by status, today's agenda and
  unassigned backlog. The web landing page renders indicator cards fed by the
  live summary, a direct-access status shortcut row (scheduled / in progress /
  completed / cancelled / unassigned) with live counts, and a map/agenda layout
  where every widget navigates into its detailed module — KPIs and the agenda to
  Scheduling, the map to Visit Map, and each shortcut to Scheduling pre-filtered
  by status (`/scheduling?status=…`, kept in sync with the filter tabs).
- **VIS-6** — employees module: QA ready (`feature/VIS-6`).
  `GET /employees/search` (name/document/position/active) and
  `GET /employees/{id}/availability` from assigned visits; web list + searchbox.
- **VIS-7** — clients/patients module: QA ready (`feature/VIS-7`).
  Client/patient search, `GET /patients/{id}/calendar`, and role-based masking
  of sensitive notes; web patients page with per-patient calendar.
- **VIS-9** — configuration / tariffs: QA ready (`feature/VIS-9`). Flexible
  tariff modalities (per service / provider / hour / km) with effective-date
  ranges (migration `0003_tariff_modality`); web configuration page.
- **VIS-10** — scheduling & visit lifecycle engine: QA ready
  (`feature/VIS-10`). Validated state machine with per-transition status events
  (timestamp + geolocation) and audit; assign/start/finish/cancel/incident
  endpoints, calendar/availability/unassigned/SLA-risk queries, and a
  forgotten-finish worker; web schedule page.

See the changelog in the PRD (§16) for full per-ticket detail.
