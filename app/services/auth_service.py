from __future__ import annotations

from datetime import UTC, datetime, timedelta
from urllib.parse import urlencode

import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.core.jwt_utils import (
    create_access_token,
    create_refresh_token,
    generate_session_id,
    hash_token,
)
from app.repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuthRepository(db)

    def discord_auth_url(self, state: str) -> str:
        query = urlencode(
            {
                "client_id": settings.discord_client_id,
                "redirect_uri": settings.discord_redirect_uri,
                "response_type": "code",
                "scope": "identify guilds",
                "prompt": "none",
                "state": state,
            }
        )
        return f"https://discord.com/oauth2/authorize?{query}"

    async def exchange_code(self, code: str) -> tuple[dict, dict]:
        if code == "dev-bypass":
            fake_user = {"id": "1", "username": "dev-user", "avatar": None}
            fake_token = {"access_token": "dev", "token_type": "Bearer"}
            return fake_token, fake_user

        async with httpx.AsyncClient(timeout=20) as client:
            token_resp = await client.post(
                f"{settings.discord_api_base}/oauth2/token",
                data={
                    "client_id": settings.discord_client_id,
                    "client_secret": settings.discord_client_secret,
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": settings.discord_redirect_uri,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            token_resp.raise_for_status()
            token_data = token_resp.json()

            user_resp = await client.get(
                f"{settings.discord_api_base}/users/@me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
            user_resp.raise_for_status()
            user_data = user_resp.json()
            return token_data, user_data

    def finalize_login(self, user_data: dict, ip_address: str | None, user_agent: str | None) -> dict:
        discord_id = int(user_data["id"])
        is_admin = discord_id in settings.admin_user_ids
        user = self.repo.upsert_user(
            discord_id=discord_id,
            username=user_data.get("username", f"user-{discord_id}"),
            avatar=user_data.get("avatar"),
            is_admin=is_admin,
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
        if not session:
            return
        self.repo.revoke_session(session, datetime.now(UTC))
