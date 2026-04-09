from __future__ import annotations

from typing import Any

from shared.constants import MODULE_REGISTRY


def module_by_slug(slug: str) -> dict[str, Any] | None:
    for module in MODULE_REGISTRY:
        if module["slug"] == slug:
            return module
    return None


def active_module_view(modules: list[dict[str, Any]], enabled_slugs: set[str], has_premium: bool) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for module in modules:
        access_level = module["access_level"]
        locked = access_level == "premium" and not has_premium
        out.append(
            {
                **module,
                "enabled": module["slug"] in enabled_slugs and not locked,
                "locked": locked,
                "can_enable": not locked,
            }
        )
    return out


def paginate(items: list[Any], page: int, page_size: int) -> dict[str, Any]:
    count = len(items)
    start = max(page - 1, 0) * page_size
    end = start + page_size
    return {
        "items": items[start:end],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": count,
            "pages": max((count + page_size - 1) // page_size, 1),
        },
    }
