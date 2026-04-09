from __future__ import annotations

import discord


BASE_COLOR = discord.Color.blurple()
ERROR_COLOR = discord.Color.red()
SUCCESS_COLOR = discord.Color.green()


def base_embed(title: str, description: str, *, color: discord.Color = BASE_COLOR) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=color)


def success_embed(title: str, description: str) -> discord.Embed:
    return base_embed(title, description, color=SUCCESS_COLOR)


def error_embed(title: str, description: str) -> discord.Embed:
    return base_embed(title, description, color=ERROR_COLOR)
