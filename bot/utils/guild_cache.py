from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class GuildCacheEntry:
    guild_id: int
    settings: dict
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class GuildCache:
    def __init__(self) -> None:
        self._cache: dict[int, GuildCacheEntry] = {}

    def get(self, guild_id: int) -> GuildCacheEntry | None:
        return self._cache.get(guild_id)

    def set(self, guild_id: int, settings: dict) -> GuildCacheEntry:
        entry = GuildCacheEntry(guild_id=guild_id, settings=settings)
        self._cache[guild_id] = entry
        return entry

    def delete(self, guild_id: int) -> None:
        self._cache.pop(guild_id, None)
