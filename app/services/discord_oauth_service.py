from __future__ import annotations

from urllib.parse import urlencode

import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.services.bot_config_service import BotConfigService


class DiscordOAuthService:
    def __init__(self, db: Session):
        self.db = db

    def auth_url(self, state: str) -> str:
        active = BotConfigService(self.db).get_active_discord_config()
        client_id = active.client_id if active else settings.discord_client_id
        redirect_uri = active.redirect_uri if active else settings.discord_redirect_uri
        query = urlencode(
            {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": "identify guilds email",
                "state": state,
                "prompt": "none",
            }
        )
        return f"https://discord.com/oauth2/authorize?{query}"

    async def exchange_code(self, code: str) -> tuple[dict, dict]:
        active = BotConfigService(self.db).get_active_discord_config()
        client_id = active.client_id if active else settings.discord_client_id
        client_secret = active.client_secret if active else settings.discord_client_secret
        redirect_uri = active.redirect_uri if active else settings.discord_redirect_uri
        async with httpx.AsyncClient(timeout=20) as client:
            token_resp = await client.post(
                f"{settings.discord_api_base}/oauth2/token",
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            if token_resp.status_code >= 400:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Discord token exchange failed")
            token_data = token_resp.json()

            user_resp = await client.get(
                f"{settings.discord_api_base}/users/@me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
            if user_resp.status_code >= 400:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Discord profile fetch failed")
            return token_data, user_resp.json()
