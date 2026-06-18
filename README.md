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

See the changelog in the PRD (§16) for full per-ticket detail.
