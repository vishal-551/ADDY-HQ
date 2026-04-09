from __future__ import annotations

import discord


def build_presence(bot) -> dict:
    return {
        "activity": discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | /help"),
        "status": discord.Status.online,
    }
