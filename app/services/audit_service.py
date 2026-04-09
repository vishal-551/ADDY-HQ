from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.repositories.access_repository import PremiumAccessRepository
from app.repositories.audit_repository import AuditRepository
from sqlalchemy import func, select

from app.core.request_context import merge_audit_metadata
from app.models import Session as UserSession
from app.models import User
from app.repositories.guild_repository import GuildRepository


class AuditService:
    def __init__(self, db: Session):
        self.repo = AuditRepository(db)

    def log(
        self,
        *,
        actor_user_id: int | None,
        actor_type: str,
        action: str,
        guild_id: int | None = None,
        resource: str | None = None,
        resource_id: str | None = None,
        metadata: dict | None = None,
    ):
        return self.repo.create(
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            action=action,
            guild_id=guild_id,
            resource=resource,
            resource_id=resource_id,
            metadata_json=merge_audit_metadata(metadata),
        )

    def list_logs(self, guild_id: int | None = None, limit: int = 100):
        return self.repo.list_logs(guild_id=guild_id, limit=limit)


class AdminStatsService:
    def __init__(self, db: Session):
        self.guilds = GuildRepository(db)
        self.premium = PremiumAccessRepository(db)
        self.audit = AuditRepository(db)
        self.db = db

    def stats(self) -> dict:
        return {
            "users": int(self.db.scalar(select(func.count()).select_from(User)) or 0),
            "guilds": self.guilds.count_guilds(),
            "sessions": int(self.db.scalar(select(func.count()).select_from(UserSession)) or 0),
            "active_premium": self.premium.count_active_premium(datetime.now(UTC)),
            "audit_logs": self.audit.count_logs(),
        }
