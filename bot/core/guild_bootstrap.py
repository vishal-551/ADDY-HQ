from __future__ import annotations

from shared.constants import MODULE_REGISTRY


async def bootstrap_guild(bot, guild) -> None:
    defaults = {
        "prefix": "/",
        "enabled_modules": [m["slug"] for m in MODULE_REGISTRY if m["category"] != "ai"],
        "locale": "en",
    }
    bot.guild_settings_cache[guild.id] = defaults
