from __future__ import annotations

from dataclasses import dataclass

from shared.enums import GuildRole
from shared.exceptions import ForbiddenError


ROLE_RANK = {
    GuildRole.MEMBER: 10,
    GuildRole.MANAGER: 50,
    GuildRole.ADMIN: 80,
    GuildRole.OWNER: 100,
}


@dataclass(slots=True)
class GuildPermissionContext:
    user_id: int
    guild_id: int
    role: GuildRole
    is_owner_override: bool = False



def has_minimum_role(context: GuildPermissionContext, minimum: GuildRole) -> bool:
    if context.is_owner_override:
        return True
    return ROLE_RANK[context.role] >= ROLE_RANK[minimum]


def require_minimum_role(context: GuildPermissionContext, minimum: GuildRole) -> None:
    if not has_minimum_role(context, minimum):
        raise ForbiddenError(
            "Insufficient permissions for this action",
            details={"required_role": minimum.value, "current_role": context.role.value},
        )
