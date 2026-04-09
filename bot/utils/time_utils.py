from __future__ import annotations

from datetime import datetime, timezone


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def format_relative(ts: datetime) -> str:
    return f"<t:{int(ts.timestamp())}:R>"
