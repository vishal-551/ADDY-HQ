from __future__ import annotations

from shared.id_generator import prefixed_id


def customer_identity_for_guild(guild_id: int) -> str:
    return prefixed_id(f"cust_{guild_id}", length=10)
