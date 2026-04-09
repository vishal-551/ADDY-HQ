from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.audit_repository import AuditRepository


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
    ) -> None:
        self.repo.create(
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            action=action,
            guild_id=guild_id,
            resource=resource,
            resource_id=resource_id,
            metadata_json=metadata or {},
        )
