from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import GuildRole, PlanType
from app.repositories.access_repository import PremiumAccessRepository

ROLE_RANK = {
    GuildRole.member: 10,
    GuildRole.manager: 50,
    GuildRole.admin: 80,
    GuildRole.owner: 100,
}


def enforce_role(current: GuildRole, minimum: GuildRole) -> None:
    if ROLE_RANK[current] < ROLE_RANK[minimum]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")


def require_guild_premium(guild_id: int, db: Session) -> None:
    grant = PremiumAccessRepository(db).get_active_grant(guild_id, datetime.now(UTC))
    if not grant:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="No active plan")
    if grant.plan not in {PlanType.trial, PlanType.premium}:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Premium required")


def ensure_guild_access(user_discord_id: int, guild_owner_discord_id: int) -> None:
    if user_discord_id != guild_owner_discord_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Guild access denied")
