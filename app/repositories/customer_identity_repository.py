from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CustomerIdentity


class CustomerIdentityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_for_guild(self, guild_id: int) -> list[CustomerIdentity]:
        return list(self.db.scalars(select(CustomerIdentity).where(CustomerIdentity.guild_id == guild_id)).all())

    def get_for_user(self, user_id: int) -> list[CustomerIdentity]:
        return list(self.db.scalars(select(CustomerIdentity).where(CustomerIdentity.user_id == user_id)).all())

    def get_by_provider_customer(self, provider: str, provider_customer_id: str) -> CustomerIdentity | None:
        stmt = select(CustomerIdentity).where(
            CustomerIdentity.provider == provider,
            CustomerIdentity.provider_customer_id == provider_customer_id,
        )
        return self.db.scalar(stmt)

    def upsert(
        self,
        *,
        provider: str,
        provider_customer_id: str,
        user_id: int | None,
        guild_id: int | None,
        email: str | None,
    ) -> CustomerIdentity:
        identity = self.get_by_provider_customer(provider=provider, provider_customer_id=provider_customer_id)
        if identity:
            identity.user_id = user_id
            identity.guild_id = guild_id
            identity.email = email
        else:
            identity = CustomerIdentity(
                provider=provider,
                provider_customer_id=provider_customer_id,
                user_id=user_id,
                guild_id=guild_id,
                email=email,
            )
            self.db.add(identity)

        self.db.flush()
        self.db.refresh(identity)
        return identity
