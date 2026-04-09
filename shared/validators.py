from __future__ import annotations

import re
from typing import Iterable

from shared.exceptions import ValidationError

DISCORD_ID_RE = re.compile(r"^\d{15,21}$")
MODULE_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROMO_CODE_RE = re.compile(r"^[A-Z0-9_-]{4,32}$")


def validate_discord_id(value: str, *, field_name: str = "id") -> str:
    if not DISCORD_ID_RE.match(value):
        raise ValidationError(f"{field_name} must be a valid Discord snowflake")
    return value


def validate_module_slug(value: str) -> str:
    if not MODULE_SLUG_RE.match(value):
        raise ValidationError("Module slug format is invalid")
    return value


def validate_promo_code(value: str) -> str:
    norm = value.strip().upper()
    if not PROMO_CODE_RE.match(norm):
        raise ValidationError("Promo code format is invalid")
    return norm


def ensure_non_empty(value: str, *, field_name: str) -> str:
    clean = value.strip()
    if not clean:
        raise ValidationError(f"{field_name} cannot be empty")
    return clean


def ensure_subset(values: Iterable[str], allowed: set[str], *, field_name: str) -> list[str]:
    normalized = [v.strip() for v in values if v.strip()]
    invalid = [v for v in normalized if v not in allowed]
    if invalid:
        raise ValidationError(
            f"{field_name} contains invalid values",
            details={"invalid": invalid, "allowed": sorted(allowed)},
        )
    return normalized
