from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database import Base, engine
from app.routes import bot, dashboard, tasks

app = FastAPI(title="ADDY HQ", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/dashboard")


app.include_router(tasks.router)
app.include_router(bot.router)
app.include_router(dashboard.router)
