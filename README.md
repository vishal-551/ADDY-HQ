# Addy — Discord Bot SaaS Platform

Addy is a modular Discord bot + SaaS control plane with a FastAPI backend, Next.js dashboard, workers, and premium monetization controls.

## Phase Coverage In This Commit

This commit delivers **Phase 1 (Root + Shared Foundation)**:

- Root runtime and local development foundation (`.env.example`, dependencies, compose, scripts package manifest)
- Shared cross-layer modules for configuration, logging, enums, constants, security, validation, response formatting, and trial utilities
- A centralized module registry powering the future bot, API, and dashboard feature cards.

## Core Design

- **Monorepo layout** with Python backend/bot/workers and Next.js dashboard.
- **Shared package** used by API and bot for consistent config, enums, and access logic.
- **Module metadata registry** (`shared/constants.py`) as single source of truth for feature cards and premium gates.
- **Security baseline** with JWT creation/validation, password hashing, and role-check helpers.

## Quick Start

### 1) Prerequisites

- Python 3.12+
- Node 20+
- Docker + Docker Compose

### 2) Configure environment

```bash
cp .env.example .env
```

Fill required secrets:

- `JWT_SECRET`
- Discord OAuth values
- `DISCORD_BOT_TOKEN`
- `DATABASE_URL` + `SYNC_DATABASE_URL`

### 3) Start infrastructure and services

```bash
docker compose up --build
```

### 4) Run locally without Docker (optional)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
npm run api:dev
```

In a second shell:

```bash
npm run dashboard:dev
```

## Environment Variable Notes

See `.env.example` for complete variable list grouped by:

- Core app/runtime
- Security/auth
- Discord integration
- AI provider
- Billing and premium
- Worker scheduling
- Dashboard runtime

## Next Steps

Upcoming phases will add:

1. API core bootstrap and middleware
2. SQLAlchemy models and Pydantic schemas
3. Repository/service/route layers
4. Bot core, cogs, interactions
5. Dashboard public pages + guild management + admin
6. Workers, scripts, tests, docs

