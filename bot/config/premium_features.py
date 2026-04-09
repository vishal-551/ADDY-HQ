from __future__ import annotations

from shared.constants import MODULE_REGISTRY


def premium_modules() -> list[str]:
    return [m["slug"] for m in MODULE_REGISTRY if m["access_level"] == "premium"]
