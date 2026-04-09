from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Session as UserSession
from app.models import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_discord_id(self, discord_id: int) -> User | None:
        return self.db.scalar(select(User).where(User.discord_id == discord_id))

    def upsert_user(self, discord_id: int, username: str, avatar: str | None, is_admin: bool) -> User:
        user = self.get_user_by_discord_id(discord_id)
        if user:
            user.username = username
            user.avatar = avatar
            user.is_admin = is_admin
        else:
            user = User(discord_id=discord_id, username=username, avatar=avatar, is_admin=is_admin)
            self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user

    def create_session(self, sid: str, user_id: int, refresh_hash: str, expires_at: datetime, ip: str | None, ua: str | None) -> UserSession:
        session = UserSession(
            id=sid,
            user_id=user_id,
            refresh_token_hash=refresh_hash,
            expires_at=expires_at,
            ip_address=ip,
            user_agent=ua,
        )
        self.db.add(session)
        self.db.flush()
        return session

    def get_session(self, sid: str) -> UserSession | None:
        return self.db.get(UserSession, sid)

    def revoke_session(self, session: UserSession, revoked_at: datetime) -> None:
        session.revoked_at = revoked_at
        self.db.flush()
