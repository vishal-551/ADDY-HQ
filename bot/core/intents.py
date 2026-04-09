from __future__ import annotations

import discord


def build_intents() -> discord.Intents:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    intents.moderation = True
    intents.guild_messages = True
    intents.guild_reactions = True
    return intents
