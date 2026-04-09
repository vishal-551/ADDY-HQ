from __future__ import annotations

from datetime import UTC, datetime, timedelta


def utcnow() -> datetime:
    return datetime.now(UTC)


def add_days(value: datetime, days: int) -> datetime:
    return value + timedelta(days=days)


def add_minutes(value: datetime, minutes: int) -> datetime:
    return value + timedelta(minutes=minutes)


def is_expired(expires_at: datetime | None, now: datetime | None = None) -> bool:
    if not expires_at:
        return False
    compare = now or utcnow()
    return expires_at <= compare


def to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(UTC).isoformat()
