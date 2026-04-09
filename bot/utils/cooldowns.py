from __future__ import annotations

from discord import app_commands


def light_cooldown() -> app_commands.Check:
    return app_commands.checks.cooldown(2, 10)


def strict_cooldown() -> app_commands.Check:
    return app_commands.checks.cooldown(1, 20)
