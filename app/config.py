from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    app_name: str = os.getenv("APP_NAME", "ADDY HQ")
    app_env: str = os.getenv("APP_ENV", "development")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./addy_hq.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-insecure-secret-change-me")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_ttl_minutes: int = int(os.getenv("JWT_ACCESS_TTL_MINUTES", "30"))
    jwt_refresh_ttl_days: int = int(os.getenv("JWT_REFRESH_TTL_DAYS", "14"))
    discord_client_id: str = os.getenv("DISCORD_CLIENT_ID", "")
    discord_client_secret: str = os.getenv("DISCORD_CLIENT_SECRET", "")
    discord_redirect_uri: str = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:8000/auth/discord/callback")
    discord_api_base: str = os.getenv("DISCORD_API_BASE", "https://discord.com/api/v10")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    admin_user_ids: set[int] = frozenset(
        int(x.strip()) for x in os.getenv("ADMIN_USER_IDS", "").split(",") if x.strip().isdigit()
    )
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "120"))


settings = AppSettings()
