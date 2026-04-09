from __future__ import annotations

from shared.config import get_settings


def feature_flags() -> dict[str, bool]:
    settings = get_settings()
    return {
        "analytics": settings.enable_analytics,
        "trials": settings.enable_trials,
        "offers": settings.enable_offers,
        "promo_codes": settings.enable_promo_codes,
        "rate_limiting": settings.enable_rate_limiting,
    }
