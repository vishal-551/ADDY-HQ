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
