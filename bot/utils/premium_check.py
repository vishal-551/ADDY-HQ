from __future__ import annotations

from bot.core.premium_gate import has_module_access


def ensure_premium_access(module_slug: str, *, enabled_modules: set[str], is_premium: bool) -> bool:
    return has_module_access(module_slug, enabled_modules=enabled_modules, is_premium=is_premium)
