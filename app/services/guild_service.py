from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.guild_repository import GuildRepository


class GuildService:
    def __init__(self, db: Session):
        self.repo = GuildRepository(db)

    def list_user_guilds(self, user_discord_id: int):
        return self.repo.list_guilds_for_owner(user_discord_id)

    def get_overview(self, guild_id: int):
        guild = self.repo.get_guild(guild_id)
        if not guild:
            return None
        settings = self.repo.get_or_create_general_settings(guild_id)
        modules = self.repo.sync_modules(guild_id)
        return {"guild": guild, "settings": settings, "modules": modules}


    def list_modules(self, guild_id: int):
        return self.repo.sync_modules(guild_id)

    def set_module_enabled(self, guild_id: int, module_key: str, enabled: bool):
        self.repo.sync_modules(guild_id)
        return self.repo.update_module(guild_id, module_key, enabled=enabled)
