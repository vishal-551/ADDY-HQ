from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.encryption import decrypt_value, encrypt_value
from app.repositories.bot_config_repository import BotConfigRepository


@dataclass(frozen=True)
class ActiveDiscordConfig:
    bot_id: int
    name: str
    token: str
    client_id: str
    client_secret: str
    redirect_uri: str
    owner_ids: list[int]
    invite_url: str | None


class BotConfigService:
    def __init__(self, db: Session):
        self.repo = BotConfigRepository(db)

    def _owner_ids_to_list(self, owner_ids_csv: str) -> list[int]:
        out: list[int] = []
        for value in owner_ids_csv.split(","):
            item = value.strip()
            if item.isdigit():
                out.append(int(item))
        return out

    def list_for_admin(self) -> list[dict]:
        bots = self.repo.list_all()
        return [
            {
                "id": bot.id,
                "name": bot.name,
                "status": bot.status,
                "is_active": bot.is_active,
                "client_id": bot.client_id,
                "redirect_uri": bot.redirect_uri,
                "owner_ids": self._owner_ids_to_list(bot.owner_ids_csv),
                "invite_url": bot.invite_url,
                "token_configured": bool(bot.token_encrypted),
                "client_secret_configured": bool(bot.client_secret_encrypted),
                "created_at": bot.created_at,
                "updated_at": bot.updated_at,
            }
            for bot in bots
        ]

    def create_bot(self, payload: dict) -> dict:
        encrypted_payload = {
            "name": payload["name"],
            "status": "active" if payload.get("is_active", False) else payload.get("status", "inactive"),
            "is_active": bool(payload.get("is_active", False)),
            "token_encrypted": encrypt_value(payload["token"]),
            "client_id": payload["client_id"],
            "client_secret_encrypted": encrypt_value(payload["client_secret"]),
            "redirect_uri": payload["redirect_uri"],
            "owner_ids_csv": ",".join(str(x) for x in payload.get("owner_ids", [])),
            "invite_url": payload.get("invite_url"),
        }
        if encrypted_payload["is_active"]:
            self.repo.deactivate_all()
        bot = self.repo.create(encrypted_payload)
        return self._to_admin_dict(bot)

    def update_bot(self, bot_id: int, payload: dict) -> dict | None:
        bot = self.repo.get_by_id(bot_id)
        if not bot:
            return None
        if payload.get("name") is not None:
            bot.name = payload["name"]
        if payload.get("token"):
            bot.token_encrypted = encrypt_value(payload["token"])
        if payload.get("client_id") is not None:
            bot.client_id = payload["client_id"]
        if payload.get("client_secret"):
            bot.client_secret_encrypted = encrypt_value(payload["client_secret"])
        if payload.get("redirect_uri") is not None:
            bot.redirect_uri = payload["redirect_uri"]
        if payload.get("owner_ids") is not None:
            bot.owner_ids_csv = ",".join(str(x) for x in payload["owner_ids"])
        if payload.get("invite_url") is not None:
            bot.invite_url = payload["invite_url"]
        if payload.get("status") is not None:
            bot.status = payload["status"]
        if payload.get("is_active") is True:
            self.repo.deactivate_all()
            bot.is_active = True
            bot.status = "active"
        elif payload.get("is_active") is False:
            bot.is_active = False
            if bot.status == "active":
                bot.status = "inactive"
        bot = self.repo.save(bot)
        return self._to_admin_dict(bot)

    def set_active(self, bot_id: int) -> dict | None:
        bot = self.repo.get_by_id(bot_id)
        if not bot:
            return None
        self.repo.deactivate_all()
        bot.is_active = True
        bot.status = "active"
        bot = self.repo.save(bot)
        return self._to_admin_dict(bot)

    def get_active_discord_config(self) -> ActiveDiscordConfig | None:
        active = self.repo.get_active()
        if not active:
            return None
        return ActiveDiscordConfig(
            bot_id=active.id,
            name=active.name,
            token=decrypt_value(active.token_encrypted),
            client_id=active.client_id,
            client_secret=decrypt_value(active.client_secret_encrypted),
            redirect_uri=active.redirect_uri,
            owner_ids=self._owner_ids_to_list(active.owner_ids_csv),
            invite_url=active.invite_url,
        )

    def _to_admin_dict(self, bot) -> dict:
        return {
            "id": bot.id,
            "name": bot.name,
            "status": bot.status,
            "is_active": bot.is_active,
            "client_id": bot.client_id,
            "redirect_uri": bot.redirect_uri,
            "owner_ids": self._owner_ids_to_list(bot.owner_ids_csv),
            "invite_url": bot.invite_url,
            "token_configured": bool(bot.token_encrypted),
            "client_secret_configured": bool(bot.client_secret_encrypted),
            "created_at": bot.created_at,
            "updated_at": bot.updated_at,
        }
