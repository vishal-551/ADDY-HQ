from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.database import Base, engine
from app.middleware.http import AuditContextMiddleware, RateLimitMiddleware
from app.routes import auth, bot, dashboard, guilds, tasks

app = FastAPI(title=settings.app_name, version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


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
app.include_router(dashboard.router)
