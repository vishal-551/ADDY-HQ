from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.enums import Environment


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Environment = Field(default=Environment.DEVELOPMENT, alias="APP_ENV")
    app_name: str = Field(default="Addy", alias="APP_NAME")
    app_url: str = Field(default="http://localhost:3000", alias="APP_URL")
    api_url: str = Field(default="http://localhost:8000", alias="API_URL")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_json: bool = Field(default=False, alias="LOG_JSON")

    database_url: str = Field(default="sqlite:///./addy_hq.db", alias="DATABASE_URL")
    sync_database_url: str = Field(default="sqlite:///./addy_hq.db", alias="SYNC_DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    jwt_secret: str = Field(default="dev-insecure-secret-change-me", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_ttl_minutes: int = Field(default=30, alias="JWT_ACCESS_TTL_MINUTES")
    jwt_refresh_ttl_days: int = Field(default=14, alias="JWT_REFRESH_TTL_DAYS")

    cookie_domain: str = Field(default="localhost", alias="COOKIE_DOMAIN")
    cookie_secure: bool = Field(default=False, alias="COOKIE_SECURE")
    cookie_samesite: str = Field(default="lax", alias="COOKIE_SAMESITE")

    discord_bot_token: str = Field(default="", alias="DISCORD_BOT_TOKEN")
    discord_client_id: str = Field(default="", alias="DISCORD_CLIENT_ID")
    discord_client_secret: str = Field(default="", alias="DISCORD_CLIENT_SECRET")
    discord_redirect_uri: str = Field(default="", alias="DISCORD_REDIRECT_URI")
    discord_permissions: int = Field(default=8, alias="DISCORD_PERMISSIONS")
    discord_api_base: str = Field(default="https://discord.com/api/v10", alias="DISCORD_API_BASE")
    discord_bot_invite_scopes: str = Field(default="bot applications.commands", alias="DISCORD_BOT_INVITE_SCOPES")
    discord_bot_invite_url: str = Field(default="", alias="DISCORD_BOT_INVITE_URL")
    discord_owner_ids: str = Field(default="", alias="DISCORD_OWNER_IDS")

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    ai_moderation_model: str = Field(default="omni-moderation-latest", alias="AI_MODERATION_MODEL")
    ai_request_timeout: int = Field(default=30, alias="AI_REQUEST_TIMEOUT")

    billing_provider: str = Field(default="stripe", alias="BILLING_PROVIDER")
    stripe_secret_key: str = Field(default="", alias="STRIPE_SECRET_KEY")
    stripe_webhook_secret: str = Field(default="", alias="STRIPE_WEBHOOK_SECRET")
    stripe_premium_price_id: str = Field(default="", alias="STRIPE_PREMIUM_PRICE_ID")

    trial_days: int = Field(default=7, alias="TRIAL_DAYS")
    default_premium_days: int = Field(default=30, alias="DEFAULT_PREMIUM_DAYS")
    premium_grace_days: int = Field(default=2, alias="PREMIUM_GRACE_DAYS")

    enable_analytics: bool = Field(default=True, alias="ENABLE_ANALYTICS")
    enable_workers: bool = Field(default=True, alias="ENABLE_WORKERS")
    enable_trials: bool = Field(default=True, alias="ENABLE_TRIALS")
    enable_offers: bool = Field(default=True, alias="ENABLE_OFFERS")
    enable_promo_codes: bool = Field(default=True, alias="ENABLE_PROMO_CODES")
    enable_rate_limiting: bool = Field(default=True, alias="ENABLE_RATE_LIMITING")

    worker_poll_seconds: int = Field(default=15, alias="WORKER_POLL_SECONDS")

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.app_env == Environment.PRODUCTION

    @computed_field
    @property
    def discord_owner_id_set(self) -> set[int]:
        raw = [piece.strip() for piece in self.discord_owner_ids.split(",") if piece.strip()]
        out: set[int] = set()
        for item in raw:
            if item.isdigit():
                out.add(int(item))
        return out

    @computed_field
    @property
    def resolved_bot_invite_url(self) -> str:
        if self.discord_bot_invite_url:
            return self.discord_bot_invite_url
        if not self.discord_client_id:
            return ""
        scope = self.discord_bot_invite_scopes.replace(" ", "%20")
        return (
            "https://discord.com/oauth2/authorize"
            f"?client_id={self.discord_client_id}&permissions={self.discord_permissions}&scope={scope}"
        )

    def as_safe_dict(self) -> dict[str, Any]:
        data = self.model_dump(mode="json")
        for key in list(data.keys()):
            if "secret" in key or "token" in key or "key" in key:
                if data[key]:
                    data[key] = "***"
        return data


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
