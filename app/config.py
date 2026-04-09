from __future__ import annotations

from dataclasses import dataclass
import os

from shared.config import get_settings


@dataclass(frozen=True)
class AppSettings:
    app_name: str
    app_env: str
    app_url: str
    api_url: str
    database_url: str
    sync_database_url: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_access_ttl_minutes: int
    jwt_refresh_ttl_days: int
    discord_client_id: str
    discord_client_secret: str
    discord_redirect_uri: str
    discord_api_base: str
    frontend_url: str
    admin_user_ids: frozenset[int]
    rate_limit_per_minute: int
    cookie_domain: str
    cookie_secure: bool
    cookie_samesite: str
    enable_rate_limiting: bool


try:
    _shared = get_settings()
except Exception:
    _shared = None

settings = AppSettings(
    app_name=_shared.app_name if _shared else os.getenv("APP_NAME", "ADDY HQ"),
    app_env=_shared.app_env.value if _shared else os.getenv("APP_ENV", "development"),
    app_url=_shared.app_url if _shared else os.getenv("APP_URL", "http://localhost:3000"),
    api_url=_shared.api_url if _shared else os.getenv("API_URL", "http://localhost:8000"),
    database_url=_shared.database_url if _shared else os.getenv("DATABASE_URL", "sqlite:///./addy_hq.db"),
    sync_database_url=_shared.sync_database_url if _shared else os.getenv("SYNC_DATABASE_URL", "sqlite:///./addy_hq.db"),
    jwt_secret=_shared.jwt_secret if _shared else os.getenv("JWT_SECRET", "dev-insecure-secret-change-me"),
    jwt_algorithm=_shared.jwt_algorithm if _shared else os.getenv("JWT_ALGORITHM", "HS256"),
    jwt_access_ttl_minutes=_shared.jwt_access_ttl_minutes if _shared else int(os.getenv("JWT_ACCESS_TTL_MINUTES", "30")),
    jwt_refresh_ttl_days=_shared.jwt_refresh_ttl_days if _shared else int(os.getenv("JWT_REFRESH_TTL_DAYS", "14")),
    discord_client_id=_shared.discord_client_id if _shared else os.getenv("DISCORD_CLIENT_ID", ""),
    discord_client_secret=_shared.discord_client_secret if _shared else os.getenv("DISCORD_CLIENT_SECRET", ""),
    discord_redirect_uri=_shared.discord_redirect_uri if _shared else os.getenv("DISCORD_REDIRECT_URI", "http://localhost:8000/auth/callback"),
    discord_api_base=_shared.discord_api_base if _shared else os.getenv("DISCORD_API_BASE", "https://discord.com/api/v10"),
    frontend_url=_shared.app_url if _shared else os.getenv("APP_URL", "http://localhost:3000"),
    admin_user_ids=frozenset(_shared.discord_owner_id_set) if _shared else frozenset(int(x.strip()) for x in os.getenv("DISCORD_OWNER_IDS", "").split(",") if x.strip().isdigit()),
    rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "120")),
    cookie_domain=_shared.cookie_domain if _shared else os.getenv("COOKIE_DOMAIN", "localhost"),
    cookie_secure=_shared.cookie_secure if _shared else os.getenv("COOKIE_SECURE", "false").lower() == "true",
    cookie_samesite=_shared.cookie_samesite if _shared else os.getenv("COOKIE_SAMESITE", "lax"),
    enable_rate_limiting=_shared.enable_rate_limiting if _shared else os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true",
)
