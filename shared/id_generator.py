from __future__ import annotations

import secrets
import string


def random_token(length: int = 32) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def prefixed_id(prefix: str, length: int = 16) -> str:
    clean_prefix = prefix.strip().lower().replace(" ", "_")
    return f"{clean_prefix}_{random_token(length)}"
