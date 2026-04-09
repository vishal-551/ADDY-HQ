from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.jwt_utils import (
    create_access_token,
    create_refresh_token,
    decode_jwt,
    generate_session_id,
    hash_token,
    verify_token_hash,
)
from app.repositories.auth_repository import AuthRepository
from app.repositories.users_repository import UsersRepository
from app.services.discord_oauth_service import DiscordOAuthService


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuthRepository(db)
        self.users = UsersRepository(db)
        self.oauth = DiscordOAuthService(db)

    def discord_auth_url(self, state: str) -> str:
        return self.oauth.auth_url(state)

    async def exchange_code(self, code: str) -> tuple[dict, dict]:
        return await self.oauth.exchange_code(code)

    def _build_login_tokens(self, discord_id: int, user_is_admin: bool, session_id: str) -> dict[str, str]:
        refresh_token = create_refresh_token(str(discord_id), session_id)
        access_token = create_access_token(str(discord_id), session_id, claims={"admin": user_is_admin})
        return {"access_token": access_token, "refresh_token": refresh_token}

    def finalize_login(self, user_data: dict, ip_address: str | None, user_agent: str | None) -> dict:
        discord_id = int(user_data["id"])
        is_admin = discord_id in settings.admin_user_ids
        user = self.repo.upsert_user(
            discord_id=discord_id,
            username=user_data.get("username", f"user-{discord_id}"),
            avatar=user_data.get("avatar"),
            is_admin=is_admin,
            discriminator=user_data.get("discriminator"),
            email=user_data.get("email"),
        )

        session_id = generate_session_id()
        tokens = self._build_login_tokens(discord_id=discord_id, user_is_admin=user.is_admin, session_id=session_id)

        expires_at = datetime.now(UTC) + timedelta(days=settings.jwt_refresh_ttl_days)
        self.repo.create_session(
            sid=session_id,
            user_id=user.id,
            refresh_hash=hash_token(tokens["refresh_token"]),
            expires_at=expires_at,
            ip=ip_address,
            ua=user_agent,
        )

        return {
            "user": user,
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "session_id": session_id,
            "expires_at": expires_at,
        }

    def refresh_session(self, session_id: str, refresh_token: str) -> dict[str, str | datetime]:
        payload = decode_jwt(refresh_token)
        if payload.get("typ") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        if payload.get("sid") != session_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session mismatch")

        now = datetime.now(UTC)
        session = self.repo.get_active_session(session_id, now)
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or revoked")

        if not verify_token_hash(refresh_token, session.refresh_token_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token invalid")

        user = self.repo.get_user_by_discord_id(int(payload["sub"]))
        if not user or user.id != session.user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        tokens = self._build_login_tokens(discord_id=user.discord_id, user_is_admin=user.is_admin, session_id=session.id)
        expires_at = now + timedelta(days=settings.jwt_refresh_ttl_days)
        self.repo.rotate_session_refresh_hash(session.id, hash_token(tokens["refresh_token"]), expires_at)

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "session_id": session.id,
            "expires_at": expires_at,
        }

    def logout(self, session_id: str) -> None:
        session = self.repo.get_session(session_id)
        if session:
            self.repo.revoke_session(session, datetime.now(UTC), reason="user_logout")

    def logout_all(self, user_id: int) -> int:
        return self.repo.revoke_all_user_sessions(user_id=user_id, revoked_at=datetime.now(UTC), reason="user_logout_all")

    def set_user_password(self, user_id: int, password: str) -> None:
        user = self.users.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.users.set_password(user, password)

    def verify_user_password(self, user_id: int, password: str) -> bool:
        user = self.users.get_by_id(user_id)
        if not user:
            return False
        return self.users.verify_password(user, password)
