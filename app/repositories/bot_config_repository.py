from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import BotConfig


class BotConfigRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[BotConfig]:
        stmt = select(BotConfig).order_by(BotConfig.is_active.desc(), BotConfig.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, bot_id: int) -> BotConfig | None:
        return self.db.get(BotConfig, bot_id)

    def get_active(self) -> BotConfig | None:
        stmt = select(BotConfig).where(BotConfig.is_active.is_(True)).limit(1)
        return self.db.scalar(stmt)

    def create(self, payload: dict) -> BotConfig:
        bot = BotConfig(**payload)
        self.db.add(bot)
        self.db.flush()
        self.db.refresh(bot)
        return bot

    def save(self, bot: BotConfig) -> BotConfig:
        self.db.add(bot)
        self.db.flush()
        self.db.refresh(bot)
        return bot

    def deactivate_all(self) -> None:
        self.db.execute(update(BotConfig).values(is_active=False, status="inactive"))
