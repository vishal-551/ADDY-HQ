from __future__ import annotations


def format_bool(value: bool) -> str:
    return "Enabled" if value else "Disabled"


def format_duration(days: int) -> str:
    return f"{days} day" if days == 1 else f"{days} days"
