from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Session as UserSession
from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_discord_id(self, discord_id: int) -> User | None:
        return self.db.scalar(select(User).where(User.discord_id == discord_id))

    def upsert_discord_user(self, discord_id: int, username: str, avatar: str | None, is_admin: bool) -> User:
        user = self.get_by_discord_id(discord_id)
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


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def get_user_by_discord_id(self, discord_id: int) -> User | None:
        return self.users.get_by_discord_id(discord_id)

    def upsert_user(self, discord_id: int, username: str, avatar: str | None, is_admin: bool) -> User:
        return self.users.upsert_discord_user(discord_id, username, avatar, is_admin)

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
        self.db.refresh(session)
        return session

    def get_session(self, sid: str) -> UserSession | None:
        return self.db.get(UserSession, sid)

    def get_active_session(self, sid: str, now: datetime) -> UserSession | None:
        query = select(UserSession).where(UserSession.id == sid, UserSession.revoked_at.is_(None), UserSession.expires_at > now)
        return self.db.scalar(query)

    def revoke_session(self, session: UserSession, revoked_at: datetime) -> None:
        session.revoked_at = revoked_at
        self.db.flush()

    def count_sessions(self) -> int:
        return len(list(self.db.scalars(select(UserSession.id)).all()))
