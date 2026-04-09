from __future__ import annotations

from datetime import datetime, timezone

_STATE: dict[str, datetime] = {}


def heartbeat(name: str) -> None:
    _STATE[name] = datetime.now(timezone.utc)


def in_memory_health() -> dict[str, str]:
    return {k: v.isoformat() for k, v in _STATE.items()}
