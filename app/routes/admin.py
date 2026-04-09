from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session, require_admin
from app.schemas import (
    AdminBotConfigCreate,
    AdminBotConfigRead,
    AdminBotConfigUpdate,
    AdminStatsRead,
    AuditLogRead,
)
from app.services.audit_service import AdminStatsService, AuditService
from app.services.bot_config_service import BotConfigService

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/dashboard/templates")


@router.get("/stats", response_model=AdminStatsRead)
def admin_stats(_: object = Depends(require_admin), db: Session = Depends(get_db_session)):
    return AdminStatsService(db).stats()


@router.get("/audit-logs", response_model=list[AuditLogRead])
def admin_audit_logs(
    _: object = Depends(require_admin),
    guild_id: int | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db_session),
):
    return AuditService(db).list_logs(guild_id=guild_id, limit=limit)


@router.get("/bots", response_model=list[AdminBotConfigRead])
def admin_list_bots(_: object = Depends(require_admin), db: Session = Depends(get_db_session)):
    return BotConfigService(db).list_for_admin()


@router.post("/bots", response_model=AdminBotConfigRead)
def admin_create_bot(
    payload: AdminBotConfigCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db_session),
):
    bot = BotConfigService(db).create_bot(payload.model_dump())
    AuditService(db).log(
        actor_user_id=admin.id,
        actor_type="user",
        action="admin.bot_config.create",
        resource="bot_config",
        resource_id=str(bot["id"]),
        metadata={"name": bot["name"], "is_active": bot["is_active"]},
    )
    return bot


@router.patch("/bots/{bot_id}", response_model=AdminBotConfigRead)
def admin_update_bot(
    bot_id: int,
    payload: AdminBotConfigUpdate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db_session),
):
    bot = BotConfigService(db).update_bot(bot_id=bot_id, payload=payload.model_dump(exclude_unset=True))
    if not bot:
        raise HTTPException(status_code=404, detail="Bot config not found")
    AuditService(db).log(
        actor_user_id=admin.id,
        actor_type="user",
        action="admin.bot_config.update",
        resource="bot_config",
        resource_id=str(bot["id"]),
        metadata={"name": bot["name"], "is_active": bot["is_active"]},
    )
    return bot


@router.post("/bots/{bot_id}/activate", response_model=AdminBotConfigRead)
def admin_activate_bot(bot_id: int, admin=Depends(require_admin), db: Session = Depends(get_db_session)):
    bot = BotConfigService(db).set_active(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot config not found")
    AuditService(db).log(
        actor_user_id=admin.id,
        actor_type="user",
        action="admin.bot_config.activate",
        resource="bot_config",
        resource_id=str(bot["id"]),
        metadata={"name": bot["name"]},
    )
    return bot


@router.get("/panel/bots", response_class=HTMLResponse, include_in_schema=False)
def admin_bots_page(request: Request, _: object = Depends(require_admin)):
    return templates.TemplateResponse(request=request, name="admin_bots.html", context={})
