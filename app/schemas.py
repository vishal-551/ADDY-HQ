from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models import AccessSource, AccessStatus, GuildRole, PlanType, TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    owner: str = Field(default="unassigned", min_length=1, max_length=120)
    priority: TaskPriority = TaskPriority.medium


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    owner: str | None = Field(default=None, min_length=1, max_length=120)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    owner: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DiscordLoginResponse(BaseModel):
    auth_url: str


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    session_id: str
    token_type: str = "bearer"
    expires_at: datetime


class RefreshSessionRequest(BaseModel):
    refresh_token: str | None = None


class LogoutAllResponse(BaseModel):
    revoked_sessions: int


class SessionRead(BaseModel):
    session_id: str
    expires_at: datetime


class UserRead(BaseModel):
    id: int
    discord_id: int
    username: str
    discriminator: str | None = None
    avatar: str | None
    email: str | None = None
    is_admin: bool

    model_config = {"from_attributes": True}


class MeResponse(BaseModel):
    user: UserRead
    session: SessionRead


class GuildRead(BaseModel):
    id: int
    name: str
    icon: str | None
    owner_discord_id: int

    model_config = {"from_attributes": True}


class GuildOverviewResponse(BaseModel):
    guild: GuildRead
    settings: "GuildGeneralSettingsRead"


class GuildGeneralSettingsRead(BaseModel):
    guild_id: int
    locale: str
    timezone: str
    prefix: str
    mod_log_channel_id: int | None
    flags: dict

    model_config = {"from_attributes": True}


class GuildGeneralSettingsUpdate(BaseModel):
    locale: str | None = Field(default=None, max_length=10)
    timezone: str | None = Field(default=None, max_length=64)
    prefix: str | None = Field(default=None, max_length=12)
    mod_log_channel_id: int | None = None
    flags: dict | None = None


class GuildModuleRead(BaseModel):
    module_key: str
    enabled: bool
    config: dict

    model_config = {"from_attributes": True}


class GuildPremiumRead(BaseModel):
    guild_id: int
    plan: PlanType
    status: AccessStatus
    source: AccessSource
    starts_at: datetime
    ends_at: datetime | None

    model_config = {"from_attributes": True}


class GuildAccessGrantRead(BaseModel):
    id: int
    guild_id: int
    user_id: int | None
    source: AccessSource
    status: AccessStatus
    plan: PlanType
    starts_at: datetime
    ends_at: datetime | None
    note: str | None

    model_config = {"from_attributes": True}


class CustomerIdentityRead(BaseModel):
    id: int
    user_id: int | None
    guild_id: int | None
    provider: str
    provider_customer_id: str
    email: str | None

    model_config = {"from_attributes": True}


class AccessStatusResponse(BaseModel):
    guild_id: int
    plan: PlanType
    source: AccessSource
    starts_at: datetime
    ends_at: datetime | None
    active: bool


class PermissionContext(BaseModel):
    guild_id: int
    role: GuildRole
    owner_override: bool = False


class AuditLogRead(BaseModel):
    id: int
    actor_user_id: int | None
    actor_type: str
    action: str
    guild_id: int | None
    resource: str | None
    resource_id: str | None
    metadata_json: dict
    created_at: datetime

    model_config = {"from_attributes": True}


class AdminStatsRead(BaseModel):
    users: int
    guilds: int
    sessions: int
    active_premium: int
    audit_logs: int
