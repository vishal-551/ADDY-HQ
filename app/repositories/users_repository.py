from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from shared.security import hash_password, verify_password


class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_discord_id(self, discord_id: int) -> User | None:
        return self.db.scalar(select(User).where(User.discord_id == discord_id))

    def upsert_discord_user(
        self,
        discord_id: int,
        username: str,
        avatar: str | None,
        is_admin: bool,
        discriminator: str | None = None,
        email: str | None = None,
    ) -> User:
        user = self.get_by_discord_id(discord_id)
        if user:
            user.username = username
            user.avatar = avatar
            user.is_admin = is_admin
            user.discriminator = discriminator
            user.email = email
        else:
            user = User(
                discord_id=discord_id,
                username=username,
                avatar=avatar,
                is_admin=is_admin,
                discriminator=discriminator,
                email=email,
            )
            self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user

    def set_password(self, user: User, password: str) -> User:
        user.password_hash = hash_password(password)
        self.db.flush()
        self.db.refresh(user)
        return user

    def verify_password(self, user: User, password: str) -> bool:
        if not user.password_hash:
            return False
        return verify_password(password, user.password_hash)
