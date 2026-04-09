from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models import PlanType
from app.repositories.access_repository import AccessRepository


class AccessService:
    def __init__(self, db: Session):
        self.repo = AccessRepository(db)

    def get_status(self, guild_id: int) -> dict:
        now = datetime.now(UTC)
        grant = self.repo.get_active_grant(guild_id, now)
        if not grant:
            return {
                "guild_id": guild_id,
                "plan": PlanType.free,
                "source": "free_default",
                "starts_at": now,
                "ends_at": None,
                "active": True,
            }
        return {
            "guild_id": guild_id,
            "plan": grant.plan,
            "source": grant.source,
            "starts_at": grant.starts_at,
            "ends_at": grant.ends_at,
            "active": True,
        }
