from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models import AccessSource, GuildRole, PlanType, TaskPriority, TaskStatus


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

    class Config:
        from_attributes = True


class DiscordLoginResponse(BaseModel):
    auth_url: str


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: int
    discord_id: int
    username: str
    avatar: str | None
    is_admin: bool


class SessionRead(BaseModel):
    session_id: str
    expires_at: datetime


class MeResponse(BaseModel):
    user: UserRead
    session: SessionRead


class GuildRead(BaseModel):
    id: int
    name: str
    icon: str | None
    owner_discord_id: int


class GuildSettingsUpdate(BaseModel):
    general: dict = Field(default_factory=dict)
    modules: dict = Field(default_factory=dict)
    welcome: dict = Field(default_factory=dict)
    moderation: dict = Field(default_factory=dict)
    automod: dict = Field(default_factory=dict)
    ai: dict = Field(default_factory=dict)
    levels: dict = Field(default_factory=dict)
    tickets: dict = Field(default_factory=dict)
    logs: dict = Field(default_factory=dict)
    youtube: dict = Field(default_factory=dict)
    giveaways: dict = Field(default_factory=dict)


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
