from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.customer_identity_repository import CustomerIdentityRepository


class CustomerIdentityService:
    def __init__(self, db: Session):
        self.repo = CustomerIdentityRepository(db)

    def guild_identities(self, guild_id: int):
        return self.repo.get_for_guild(guild_id)
