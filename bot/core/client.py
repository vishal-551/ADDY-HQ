from __future__ import annotations

from datetime import datetime
from typing import Any

import discord
from discord.ext import commands

from shared.config import Settings, get_settings
from shared.logger import get_logger


class AddyClient(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.settings: Settings = get_settings()
        self.log = get_logger("bot.client")
        self.started_at = datetime.utcnow()
        self.guild_settings_cache: dict[int, dict[str, Any]] = {}

    async def fetch_guild_settings(self, guild_id: int) -> dict[str, Any]:
        cached = self.guild_settings_cache.get(guild_id)
        if cached:
            return cached
        value = {
            "prefix": "/",
            "language": "en",
            "enabled_modules": ["general", "welcome", "moderation"],
        }
        self.guild_settings_cache[guild_id] = value
        return value

    async def invalidate_guild_cache(self, guild_id: int) -> None:
        self.guild_settings_cache.pop(guild_id, None)
