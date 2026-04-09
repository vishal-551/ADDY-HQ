from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.core.dependencies import (
    get_audit_service,
    get_current_user,
    get_customer_identity_service,
    get_guild_service,
    get_premium_service,
    get_settings_service,
)
from app.core.guards import ensure_owner_or_admin
from app.models import User
from app.schemas import (
    AccessStatusResponse,
    CustomerIdentityRead,
    GuildAccessGrantRead,
    GuildGeneralSettingsRead,
    GuildGeneralSettingsUpdate,
    GuildOverviewResponse,
    GuildRead,
)
from app.services.access_service import PremiumAccessService
from app.services.audit_service import AuditService
from app.services.customer_identity_service import CustomerIdentityService
from app.services.guild_service import GuildService
from app.services.settings_service import GeneralSettingsService
from shared.constants import MODULE_REGISTRY
from shared.response_builder import ok

router = APIRouter(prefix="/guilds", tags=["guilds"])


class GuildModuleUpdate(BaseModel):
    enabled: bool


@router.get("/list", response_model=list[GuildRead])
def list_guilds(user: User = Depends(get_current_user), service: GuildService = Depends(get_guild_service)):
    return service.list_user_guilds(user.discord_id)


@router.get("/{guild_id}", response_model=GuildOverviewResponse)
def guild_overview(guild_id: int, user: User = Depends(get_current_user), service: GuildService = Depends(get_guild_service)):
    data = service.get_overview(guild_id)
    if not data:
        raise HTTPException(status_code=404, detail="Guild not found")
    ensure_owner_or_admin(user.discord_id, data["guild"].owner_discord_id, user.is_admin)
    return data


@router.get("/{guild_id}/general-settings", response_model=GuildGeneralSettingsRead)
def get_general_settings(
    guild_id: int,
    user: User = Depends(get_current_user),
    guild_service: GuildService = Depends(get_guild_service),
    service: GeneralSettingsService = Depends(get_settings_service),
):
    guild = guild_service.get_overview(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")
    ensure_owner_or_admin(user.discord_id, guild["guild"].owner_discord_id, user.is_admin)
    return service.get(guild_id)


@router.put("/{guild_id}/general-settings", response_model=GuildGeneralSettingsRead)
def update_general_settings(
    guild_id: int,
    payload: GuildGeneralSettingsUpdate,
    user: User = Depends(get_current_user),
    guild_service: GuildService = Depends(get_guild_service),
    settings_service: GeneralSettingsService = Depends(get_settings_service),
    audit: AuditService = Depends(get_audit_service),
):
    guild = guild_service.get_overview(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")
    ensure_owner_or_admin(user.discord_id, guild["guild"].owner_discord_id, user.is_admin)
    out = settings_service.update(guild_id, payload.model_dump(exclude_unset=True))
    audit.log(actor_user_id=user.id, actor_type="user", action="guild.settings.update", guild_id=guild_id)
    return out


@router.get("/{guild_id}/modules")
def guild_modules(
    guild_id: int,
    user: User = Depends(get_current_user),
    guild_service: GuildService = Depends(get_guild_service),
    premium_service: PremiumAccessService = Depends(get_premium_service),
):
    overview = guild_service.get_overview(guild_id)
    if not overview:
        raise HTTPException(status_code=404, detail="Guild not found")
    ensure_owner_or_admin(user.discord_id, overview["guild"].owner_discord_id, user.is_admin)

    premium = premium_service.get_status(guild_id)
    registry_by_slug = {item["slug"]: item for item in MODULE_REGISTRY}
    cards: list[dict] = []

    for module in guild_service.list_modules(guild_id):
        registry = registry_by_slug.get(module.module_key, {})
        is_premium = registry.get("access_level") == "premium"
        available = (premium.plan.value == "premium") or not is_premium
        cards.append(
            {
                "key": module.module_key,
                "icon": "✨" if is_premium else "🤖",
                "title": registry.get("title", module.module_key.title()),
                "description": registry.get("short_description", "Guild module"),
                "tier": "premium" if is_premium else "free",
                "enabled": module.enabled,
                "connected": module.enabled,
                "available": available,
                "invite_url": f"/invite?guild={guild_id}&module={module.module_key}",
                "manage_url": f"/dashboard/settings/{module.module_key}?guild={guild_id}",
            }
        )

    return ok(cards)


@router.put("/{guild_id}/modules/{module_key}")
def set_guild_module(
    guild_id: int,
    module_key: str,
    payload: GuildModuleUpdate,
    user: User = Depends(get_current_user),
    guild_service: GuildService = Depends(get_guild_service),
    audit: AuditService = Depends(get_audit_service),
):
    overview = guild_service.get_overview(guild_id)
    if not overview:
        raise HTTPException(status_code=404, detail="Guild not found")
    ensure_owner_or_admin(user.discord_id, overview["guild"].owner_discord_id, user.is_admin)

    module = guild_service.set_module_enabled(guild_id, module_key=module_key, enabled=payload.enabled)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    audit.log(
        actor_user_id=user.id,
        actor_type="user",
        action="guild.module.update",
        guild_id=guild_id,
        resource="module",
        resource_id=module.module_key,
        metadata={"enabled": module.enabled},
    )
    return ok({"guild_id": guild_id, "module_key": module.module_key, "enabled": module.enabled})


@router.get("/{guild_id}/premium", response_model=AccessStatusResponse)
def premium_status(
    guild_id: int,
    user: User = Depends(get_current_user),
    guild_service: GuildService = Depends(get_guild_service),
    service: PremiumAccessService = Depends(get_premium_service),
):
    guild = guild_service.get_overview(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")
    ensure_owner_or_admin(user.discord_id, guild["guild"].owner_discord_id, user.is_admin)
    return service.get_status(guild_id)


@router.get("/{guild_id}/access-history", response_model=list[GuildAccessGrantRead])
def access_history(
    guild_id: int,
    limit: int = Query(50, ge=1, le=200),
    user: User = Depends(get_current_user),
    guild_service: GuildService = Depends(get_guild_service),
    service: PremiumAccessService = Depends(get_premium_service),
):
    guild = guild_service.get_overview(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")
    ensure_owner_or_admin(user.discord_id, guild["guild"].owner_discord_id, user.is_admin)
    return service.access_history(guild_id, limit=limit)


@router.get("/{guild_id}/customer-identity", response_model=list[CustomerIdentityRead])
def customer_identity(
    guild_id: int,
    user: User = Depends(get_current_user),
    guild_service: GuildService = Depends(get_guild_service),
    service: CustomerIdentityService = Depends(get_customer_identity_service),
):
    guild = guild_service.get_overview(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")
    ensure_owner_or_admin(user.discord_id, guild["guild"].owner_discord_id, user.is_admin)
    return service.guild_identities(guild_id)


# Backward compatibility with previous /guilds path.
router.add_api_route("", list_guilds, methods=["GET"], response_model=list[GuildRead])
router.add_api_route("/{guild_id}/settings", update_general_settings, methods=["PUT"], response_model=GuildGeneralSettingsRead)
