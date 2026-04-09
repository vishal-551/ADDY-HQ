from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import GuildGeneralSettings
from app.repositories.guild_repository import GuildRepository


class SettingsRepository:
    def __init__(self, db: Session):
        self.db = db
        self.guilds = GuildRepository(db)

    def get(self, guild_id: int) -> GuildGeneralSettings:
        return self.guilds.get_or_create_general_settings(guild_id)

    def update(self, guild_id: int, payload: dict) -> GuildGeneralSettings:
        settings = self.guilds.get_or_create_general_settings(guild_id)
        for field, value in payload.items():
            if value is not None and hasattr(settings, field):
                setattr(settings, field, value)
        return self.guilds.save_settings(settings)
