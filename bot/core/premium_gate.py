from __future__ import annotations

from shared.enums import ModuleAccessLevel
from shared.helpers import module_by_slug


def has_module_access(module_slug: str, *, enabled_modules: set[str], is_premium: bool) -> bool:
    module = module_by_slug(module_slug)
    if not module:
        return False
    if module["access_level"] == ModuleAccessLevel.PREMIUM.value and not is_premium:
        return False
    return module_slug in enabled_modules
