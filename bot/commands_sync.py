from __future__ import annotations

from discord.ext.commands import Bot

from shared.logger import get_logger

log = get_logger("bot.commands_sync")


async def sync_tree(bot: Bot, guild_id: int | None = None) -> int:
    if guild_id:
        synced = await bot.tree.sync(guild=None)
    else:
        synced = await bot.tree.sync()
    count = len(synced)
    log.info("commands_synced", count=count, guild_id=guild_id)
    return count
