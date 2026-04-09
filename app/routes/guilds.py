from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db_session
from app.models import User
from app.schemas import AccessStatusResponse, GuildRead, GuildSettingsUpdate
from app.services.access_service import AccessService
from app.services.guild_service import GuildService

router = APIRouter(prefix="/guilds", tags=["guilds"])


@router.get("", response_model=list[GuildRead])
def list_guilds(user: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    guilds = GuildService(db).list_user_guilds(user.discord_id)
    return guilds


@router.get("/{guild_id}")
def guild_overview(guild_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    data = GuildService(db).get_overview(guild_id)
    if not data:
        raise HTTPException(status_code=404, detail="Guild not found")
    return data


@router.put("/{guild_id}/settings")
def update_guild_settings(
    guild_id: int,
    payload: GuildSettingsUpdate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    settings = GuildService(db).update_settings(guild_id, payload.model_dump())
    return settings


@router.get("/{guild_id}/premium", response_model=AccessStatusResponse)
def premium_status(guild_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    return AccessService(db).get_status(guild_id)
