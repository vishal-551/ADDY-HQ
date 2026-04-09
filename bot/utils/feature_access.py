from __future__ import annotations

from shared.helpers import active_module_view
from shared.constants import MODULE_REGISTRY


def guild_feature_matrix(enabled_modules: set[str], is_premium: bool) -> list[dict]:
    return active_module_view(MODULE_REGISTRY, enabled_modules=enabled_modules, has_premium=is_premium)
