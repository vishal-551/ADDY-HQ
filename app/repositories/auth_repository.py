from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.models import Session as UserSession
from app.models import User
from app.repositories.users_repository import UsersRepository


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db
        self.users = UsersRepository(db)

    def get_user_by_discord_id(self, discord_id: int) -> User | None:
        return self.users.get_by_discord_id(discord_id)

    def upsert_user(
        self,
        discord_id: int,
        username: str,
        avatar: str | None,
        is_admin: bool,
        discriminator: str | None = None,
        email: str | None = None,
    ) -> User:
        return self.users.upsert_discord_user(
            discord_id=discord_id,
            username=username,
            avatar=avatar,
            is_admin=is_admin,
            discriminator=discriminator,
            email=email,
        )

    def create_session(
        self,
        sid: str,
        user_id: int,
        refresh_hash: str,
        expires_at: datetime,
        ip: str | None,
        ua: str | None,
    ) -> UserSession:
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

    def rotate_session_refresh_hash(self, session_id: str, refresh_hash: str, expires_at: datetime) -> UserSession | None:
        session = self.db.get(UserSession, session_id)
        if not session:
            return None
        session.refresh_token_hash = refresh_hash
        session.expires_at = expires_at
        self.db.flush()
        self.db.refresh(session)
        return session

    def revoke_session(self, session: UserSession, revoked_at: datetime, reason: str | None = None) -> None:
        session.revoked_at = revoked_at
        session.revoked_reason = reason
        self.db.flush()

    def revoke_all_user_sessions(self, user_id: int, revoked_at: datetime, reason: str) -> int:
        stmt = (
            update(UserSession)
            .where(UserSession.user_id == user_id, UserSession.revoked_at.is_(None))
            .values(revoked_at=revoked_at, revoked_reason=reason)
        )
        result = self.db.execute(stmt)
        return int(result.rowcount or 0)

    def count_sessions(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(UserSession)) or 0)
