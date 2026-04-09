from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.settings_repository import SettingsRepository


class GeneralSettingsService:
    def __init__(self, db: Session):
        self.repo = SettingsRepository(db)

    def get(self, guild_id: int):
        return self.repo.get(guild_id)

    def update(self, guild_id: int, payload: dict):
        return self.repo.update(guild_id, payload)
