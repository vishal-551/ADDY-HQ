# ADDY HQ

Production-style task operations service built with FastAPI and SQLite.

## Features
- Task domain models and persistence.
- Service layer for business logic.
- REST routes for CRUD operations.
- Bot command endpoint for operational shortcuts.
- Dashboard rendering task metrics and current queue.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Then open:
- API docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:8000/dashboard`

## Bot commands
- `create <owner> | <title> | <description>`
- `complete <id>`
- `escalate <id>`
