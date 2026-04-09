from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AccessGrant, AccessStatus


class AccessRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_grant(self, guild_id: int, now: datetime) -> AccessGrant | None:
        query = (
            select(AccessGrant)
            .where(AccessGrant.guild_id == guild_id)
            .where(AccessGrant.status == AccessStatus.active)
            .where((AccessGrant.ends_at.is_(None)) | (AccessGrant.ends_at > now))
            .order_by(AccessGrant.created_at.desc())
        )
        return self.db.scalar(query)
