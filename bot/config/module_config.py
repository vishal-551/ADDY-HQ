from __future__ import annotations

from shared.constants import MODULE_REGISTRY


def all_modules() -> list[dict]:
    return list(MODULE_REGISTRY)


def module_slugs() -> set[str]:
    return {m["slug"] for m in MODULE_REGISTRY}
