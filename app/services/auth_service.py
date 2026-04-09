from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.config import settings
from app.core.jwt_utils import create_access_token, create_refresh_token, generate_session_id, hash_token
from app.repositories.auth_repository import AuthRepository
from app.services.discord_oauth_service import DiscordOAuthService


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuthRepository(db)
        self.oauth = DiscordOAuthService(db)

    def discord_auth_url(self, state: str) -> str:
        return self.oauth.auth_url(state)

    async def exchange_code(self, code: str) -> tuple[dict, dict]:
        return await self.oauth.exchange_code(code)

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
        refresh_token = create_refresh_token(str(discord_id), session_id)
        refresh_hash = hash_token(refresh_token)
        expires_at = datetime.now(UTC) + timedelta(days=settings.jwt_refresh_ttl_days)

        self.repo.create_session(
            sid=session_id,
            user_id=user.id,
            refresh_hash=refresh_hash,
            expires_at=expires_at,
            ip=ip_address,
            ua=user_agent,
        )

        access_token = create_access_token(str(discord_id), session_id, claims={"admin": user.is_admin})
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "session_id": session_id,
            "expires_at": expires_at,
        }

    def logout(self, session_id: str) -> None:
        session = self.repo.get_session(session_id)
        if session:
            self.repo.revoke_session(session, datetime.now(UTC), reason="user_logout")
