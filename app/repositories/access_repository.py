from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AccessStatus, GuildAccessGrant, GuildPremium


class PremiumAccessRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_premium(self, guild_id: int) -> GuildPremium | None:
        return self.db.scalar(select(GuildPremium).where(GuildPremium.guild_id == guild_id))

    def get_active_grant(self, guild_id: int, now: datetime) -> GuildAccessGrant | None:
        query = (
            select(GuildAccessGrant)
            .where(GuildAccessGrant.guild_id == guild_id)
            .where(GuildAccessGrant.status == AccessStatus.active)
            .where((GuildAccessGrant.ends_at.is_(None)) | (GuildAccessGrant.ends_at > now))
            .order_by(GuildAccessGrant.created_at.desc())
        )
        return self.db.scalar(query)

    def list_grants(self, guild_id: int, limit: int = 50) -> list[GuildAccessGrant]:
        stmt = select(GuildAccessGrant).where(GuildAccessGrant.guild_id == guild_id).order_by(GuildAccessGrant.created_at.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count_active_premium(self, now: datetime) -> int:
        stmt = select(func.count()).select_from(GuildPremium).where(
            GuildPremium.ends_at.is_(None) | (GuildPremium.ends_at > now)
        )
        return int(self.db.scalar(stmt) or 0)


class AccessRepository(PremiumAccessRepository):
    pass
