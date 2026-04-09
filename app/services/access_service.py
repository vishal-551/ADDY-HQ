from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models import PlanType
from app.repositories.access_repository import PremiumAccessRepository


class PremiumAccessService:
    def __init__(self, db: Session):
        self.repo = PremiumAccessRepository(db)

    def get_status(self, guild_id: int) -> dict:
        now = datetime.now(UTC)
        premium = self.repo.get_premium(guild_id)
        if premium:
            active = premium.ends_at is None or premium.ends_at > now
            return {
                "guild_id": guild_id,
                "plan": premium.plan,
                "source": premium.source,
                "starts_at": premium.starts_at,
                "ends_at": premium.ends_at,
                "active": active,
            }

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

    def access_history(self, guild_id: int, limit: int = 50):
        return self.repo.list_grants(guild_id, limit=limit)


class AccessService(PremiumAccessService):
    pass
