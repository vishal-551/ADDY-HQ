from __future__ import annotations

from collections.abc import Sequence

from discord.ext.commands import Bot

from shared.logger import get_logger

log = get_logger("bot.loader")

CORE_EXTENSIONS: Sequence[str] = (
    "bot.core.events",
)


async def setup_extensions(bot: Bot) -> None:
    for ext in CORE_EXTENSIONS:
        try:
            await bot.load_extension(ext)
            log.info("extension_loaded", extension=ext)
        except Exception as exc:  # pragma: no cover - discord internals
            log.exception("extension_load_failed", extension=ext, error=str(exc))
