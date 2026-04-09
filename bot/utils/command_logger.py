from __future__ import annotations

from shared.logger import get_logger

log = get_logger("bot.commands")


def log_command(command: str, user_id: int, guild_id: int | None) -> None:
    log.info("command_invoked", command=command, user_id=user_id, guild_id=guild_id)
