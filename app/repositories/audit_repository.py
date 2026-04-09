from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        actor_user_id: int | None,
        actor_type: str,
        action: str,
        guild_id: int | None,
        resource: str | None,
        resource_id: str | None,
        metadata_json: dict,
    ) -> AuditLog:
        log = AuditLog(
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            action=action,
            guild_id=guild_id,
            resource=resource,
            resource_id=resource_id,
            metadata_json=metadata_json,
        )
        self.db.add(log)
        self.db.flush()
        self.db.refresh(log)
        return log

    def list_logs(self, guild_id: int | None = None, limit: int = 100) -> list[AuditLog]:
        stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        if guild_id is not None:
            stmt = stmt.where(AuditLog.guild_id == guild_id)
        return list(self.db.scalars(stmt).all())

    def count_logs(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(AuditLog)) or 0)
