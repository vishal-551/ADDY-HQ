from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Guild, GuildSettings


class GuildRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_guilds_for_owner(self, owner_discord_id: int) -> list[Guild]:
        return list(
            self.db.scalars(select(Guild).where(Guild.owner_discord_id == owner_discord_id).order_by(Guild.name.asc())).all()
        )

    def get_guild(self, guild_id: int) -> Guild | None:
        return self.db.get(Guild, guild_id)

    def get_or_create_settings(self, guild_id: int) -> GuildSettings:
        settings = self.db.scalar(select(GuildSettings).where(GuildSettings.guild_id == guild_id))
        if settings:
            return settings
        settings = GuildSettings(guild_id=guild_id)
        self.db.add(settings)
        self.db.flush()
        self.db.refresh(settings)
        return settings

    def save_settings(self, settings: GuildSettings) -> GuildSettings:
        self.db.add(settings)
        self.db.flush()
        self.db.refresh(settings)
        return settings
