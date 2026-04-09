from __future__ import annotations

from functools import lru_cache

from pydantic import BaseModel

from shared.config import get_settings


class BotRuntimeConfig(BaseModel):
    default_prefix: str = "/"
    support_url: str = "https://discord.gg/addy"
    docs_url: str = "https://addy.example.com/docs"


@lru_cache(maxsize=1)
def get_bot_runtime_config() -> BotRuntimeConfig:
    settings = get_settings()
    return BotRuntimeConfig(
        default_prefix="/",
        support_url=f"{settings.app_url}/support",
        docs_url=f"{settings.app_url}/docs",
    )
