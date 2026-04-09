from __future__ import annotations

from discord.ext import commands

from bot.config.bot_config import get_bot_runtime_config
from bot.core.client import AddyClient
from bot.core.intents import build_intents
from bot.core.startup import on_startup
from bot.core.shutdown import on_shutdown
from bot.loader import setup_extensions
from shared.logger import get_logger

log = get_logger("bot.bot")


class AddyBot(AddyClient):
    def __init__(self) -> None:
        runtime = get_bot_runtime_config()
        super().__init__(
            command_prefix=commands.when_mentioned_or(runtime.default_prefix),
            intents=build_intents(),
            activity=None,
            help_command=None,
        )
        self.runtime = runtime

    async def setup_hook(self) -> None:
        await on_startup(self)
        await setup_extensions(self)

    async def close(self) -> None:
        await on_shutdown(self)
        await super().close()


async def run_bot() -> None:
    bot = AddyBot()
    token = bot.settings.discord_bot_token
    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN is required")
    log.info("bot_start", user_cache_enabled=True)
    await bot.start(token)
