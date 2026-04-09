from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Guild, GuildGeneralSettings


class GuildRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_guilds_for_owner(self, owner_discord_id: int) -> list[Guild]:
        stmt = select(Guild).where(Guild.owner_discord_id == owner_discord_id).order_by(Guild.name.asc())
        return list(self.db.scalars(stmt).all())

    def get_guild(self, guild_id: int) -> Guild | None:
        return self.db.get(Guild, guild_id)

    def ensure_guild(self, guild_id: int, *, name: str, icon: str | None, owner_discord_id: int) -> Guild:
        guild = self.get_guild(guild_id)
        if guild:
            guild.name = name
            guild.icon = icon
            guild.owner_discord_id = owner_discord_id
        else:
            guild = Guild(id=guild_id, name=name, icon=icon, owner_discord_id=owner_discord_id)
            self.db.add(guild)
        self.db.flush()
        self.db.refresh(guild)
        return guild

    def get_general_settings(self, guild_id: int) -> GuildGeneralSettings | None:
        return self.db.scalar(select(GuildGeneralSettings).where(GuildGeneralSettings.guild_id == guild_id))

    def get_or_create_general_settings(self, guild_id: int) -> GuildGeneralSettings:
        settings = self.get_general_settings(guild_id)
        if settings:
            return settings
        settings = GuildGeneralSettings(guild_id=guild_id)
        self.db.add(settings)
        self.db.flush()
        self.db.refresh(settings)
        return settings

    def save_settings(self, settings: GuildGeneralSettings) -> GuildGeneralSettings:
        self.db.add(settings)
        self.db.flush()
        self.db.refresh(settings)
        return settings

    def count_guilds(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(Guild)) or 0)
