from __future__ import annotations

from discord import app_commands

from shared.config import get_settings


def is_owner_only() -> app_commands.Check:
    settings = get_settings()

    async def predicate(interaction) -> bool:
        user_id = interaction.user.id
        return user_id in settings.discord_owner_id_set

    return app_commands.check(predicate)
