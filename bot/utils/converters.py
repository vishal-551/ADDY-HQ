from __future__ import annotations


def to_int(value: str | int, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
