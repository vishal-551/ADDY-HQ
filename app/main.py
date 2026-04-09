from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.database import Base, async_engine, engine
from app.middleware.http import AuditContextMiddleware, RateLimitMiddleware, RequestContextMiddleware
from app.routes import admin, auth, bot, dashboard, guilds, tasks


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        await async_engine.dispose()
        engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="2.0.0", lifespan=lifespan)

    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(AuditContextMiddleware)
    app.add_middleware(RateLimitMiddleware)
    register_exception_handlers(app)

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse(url="/dashboard")

    @app.get("/health", tags=["system"])
    def health() -> dict:
        return {"ok": True, "service": settings.app_name, "env": settings.app_env}

    app.include_router(auth.router)
    app.include_router(tasks.router)
    app.include_router(bot.router)
    app.include_router(guilds.router)
    app.include_router(admin.router)
    app.include_router(dashboard.router)

    return app


app = create_app()
