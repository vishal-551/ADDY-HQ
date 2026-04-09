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
        settings = self.repo.get_or_create_settings(guild_id)
        return {"guild": guild, "settings": settings}

    def update_settings(self, guild_id: int, payload: dict):
        settings = self.repo.get_or_create_settings(guild_id)
        for key, val in payload.items():
            if hasattr(settings, key):
                setattr(settings, key, val)
        return self.repo.save_settings(settings)
