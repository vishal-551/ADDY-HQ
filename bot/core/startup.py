from __future__ import annotations

from bot.core.presence import build_presence
from bot.core.scheduler import start_scheduler
from shared.logger import get_logger

log = get_logger("bot.startup")


async def on_startup(bot) -> None:
    await bot.change_presence(**build_presence(bot))
    await start_scheduler(bot)
    log.info("startup_complete", guilds=len(bot.guilds))
