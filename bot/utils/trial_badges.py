from __future__ import annotations

from shared.constants import PREMIUM_BADGES


def badge_for_plan(plan: str) -> str:
    return PREMIUM_BADGES.get(plan, PREMIUM_BADGES["free"])
