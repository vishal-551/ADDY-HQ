from __future__ import annotations

from datetime import UTC, datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db_session
from app.models import GuildRole, PlanType, User
from app.repositories.access_repository import AccessRepository

ROLE_RANK = {
    GuildRole.member: 10,
    GuildRole.manager: 50,
    GuildRole.admin: 80,
    GuildRole.owner: 100,
}


def enforce_role(current: GuildRole, minimum: GuildRole) -> None:
    if ROLE_RANK[current] < ROLE_RANK[minimum]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")


def require_guild_premium(
    guild_id: int,
    db: Session,
) -> None:
    grant = AccessRepository(db).get_active_grant(guild_id, datetime.now(UTC))
    if not grant:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="No active plan")
    if grant.plan not in {PlanType.trial, PlanType.premium}:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Premium required")


def get_premium_guard(guild_id: int):
    def _guard(_: User = Depends(get_current_user), db: Session = Depends(get_db_session)) -> None:
        require_guild_premium(guild_id, db)

    return _guard
