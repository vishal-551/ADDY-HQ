from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Guild, GuildGeneralSettings, GuildModule
from shared.constants import MODULE_REGISTRY


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

    def sync_modules(self, guild_id: int) -> list[GuildModule]:
        existing_stmt = select(GuildModule).where(GuildModule.guild_id == guild_id)
        existing = list(self.db.scalars(existing_stmt).all())
        existing_by_key = {item.module_key: item for item in existing}
        changed = False
        for module in MODULE_REGISTRY:
            module_key = module["slug"]
            if module_key in existing_by_key:
                continue
            self.db.add(
                GuildModule(
                    guild_id=guild_id,
                    module_key=module_key,
                    enabled=False,
                    config={"module_id": module["id"], "category": module["category"]},
                )
            )
            changed = True
        if changed:
            self.db.flush()
            existing = list(self.db.scalars(existing_stmt).all())
        return sorted(existing, key=lambda item: item.module_key)

    def count_guilds(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(Guild)) or 0)
