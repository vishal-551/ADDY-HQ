from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.customer_identity_repository import CustomerIdentityRepository


class CustomerIdentityService:
    def __init__(self, db: Session):
        self.repo = CustomerIdentityRepository(db)

    def guild_identities(self, guild_id: int):
        return self.repo.get_for_guild(guild_id)

    def user_identities(self, user_id: int):
        return self.repo.get_for_user(user_id)

    def upsert_identity(
        self,
        *,
        provider: str,
        provider_customer_id: str,
        user_id: int | None,
        guild_id: int | None,
        email: str | None,
    ):
        return self.repo.upsert(
            provider=provider,
            provider_customer_id=provider_customer_id,
            user_id=user_id,
            guild_id=guild_id,
            email=email,
        )
