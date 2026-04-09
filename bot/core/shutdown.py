from __future__ import annotations

from bot.core.scheduler import stop_scheduler
from shared.logger import get_logger

log = get_logger("bot.shutdown")


async def on_shutdown(bot) -> None:
    await stop_scheduler(bot)
    log.info("shutdown_complete")
