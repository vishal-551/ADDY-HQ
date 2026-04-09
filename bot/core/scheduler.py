from __future__ import annotations

import asyncio
import contextlib

from bot.core.healthcheck import heartbeat


async def _tick_loop(bot) -> None:
    while not bot.is_closed():
        heartbeat("bot_scheduler")
        await asyncio.sleep(30)


async def start_scheduler(bot) -> None:
    if getattr(bot, "_scheduler_task", None):
        return
    bot._scheduler_task = asyncio.create_task(_tick_loop(bot), name="bot_scheduler")


async def stop_scheduler(bot) -> None:
    task = getattr(bot, "_scheduler_task", None)
    if task:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
        bot._scheduler_task = None
