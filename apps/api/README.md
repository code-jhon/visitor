# Visitor API (apps/api)

FastAPI backend. VIS-1 scaffolding: health check + DB/Alembic wiring only.

## Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../../.env.example .env
uvicorn app.main:app --reload --port 8000
# http://localhost:8000/health
```

## Tests
```bash
pytest
```

## Migrations (no business tables yet — see VIS-3)
```bash
alembic revision -m "init"
alembic upgrade head
```
