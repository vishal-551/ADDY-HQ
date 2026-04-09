from __future__ import annotations

from dataclasses import dataclass

from app.database import get_session
from app.services.bot_config_service import BotConfigService
from shared.config import get_settings


@dataclass(frozen=True)
class DiscordCredentials:
    token: str
    client_id: str
    client_secret: str
    redirect_uri: str
    owner_ids: list[int]
    invite_url: str | None
    source: str


def load_discord_credentials() -> DiscordCredentials:
    settings = get_settings()
    with get_session() as db:
        active = BotConfigService(db).get_active_discord_config()
    if active:
        return DiscordCredentials(
            token=active.token,
            client_id=active.client_id,
            client_secret=active.client_secret,
            redirect_uri=active.redirect_uri,
            owner_ids=active.owner_ids,
            invite_url=active.invite_url,
            source="database",
        )

    return DiscordCredentials(
        token=settings.discord_bot_token,
        client_id=settings.discord_client_id,
        client_secret=settings.discord_client_secret,
        redirect_uri=settings.discord_redirect_uri,
        owner_ids=list(settings.discord_owner_id_set),
        invite_url=settings.resolved_bot_invite_url,
        source="env",
    )
