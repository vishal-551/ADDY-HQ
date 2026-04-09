from __future__ import annotations

from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.database import Base, async_engine, engine
from app.middleware.http import (
    AuditContextMiddleware,
    ErrorHandlingMiddleware,
    RateLimitMiddleware,
    RequestContextMiddleware,
    StructuredLoggingMiddleware,
)
from app.routes import admin, auth, bot, dashboard, guilds, preview, tasks
from shared.logger import configure_logging
from shared.response_builder import ok


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        await async_engine.dispose()
        engine.dispose()


def _build_cors_origins() -> list[str]:
    env_origins = {item.strip() for item in os.getenv("CORS_ALLOW_ORIGINS", "").split(",") if item.strip()}
    origins = {
        settings.frontend_url,
        settings.app_url,
        settings.api_url,
        settings.discord_redirect_uri.rsplit("/", 1)[0],
        *env_origins,
    }
    return [origin for origin in origins if origin]


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title=settings.app_name, version="2.2.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_build_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(AuditContextMiddleware)
    app.add_middleware(StructuredLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)
    register_exception_handlers(app)

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse(url="/dashboard")

    @app.get("/health", tags=["system"])
    def health() -> dict:
        return ok({"service": settings.app_name, "env": settings.app_env, "status": "ok"})

    @app.get("/health/live", tags=["system"])
    def health_live() -> dict:
        return ok({"alive": True})

    @app.get("/health/ready", tags=["system"])
    def health_ready() -> dict:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return ok({"ready": True})

    app.include_router(auth.router)
    app.include_router(tasks.router)
    app.include_router(bot.router)
    app.include_router(guilds.router)
    app.include_router(admin.router)
    app.include_router(preview.router)
    app.include_router(dashboard.router)

    return app


app = create_app()
