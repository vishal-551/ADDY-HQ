from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, IDMixin, TimestampMixin


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class PlanType(str, Enum):
    free = "free"
    trial = "trial"
    premium = "premium"


class AccessSource(str, Enum):
    free_default = "free_default"
    trial = "trial"
    billing = "billing"
    owner_grant = "owner_grant"
    manual_access = "manual_access"


class AccessStatus(str, Enum):
    active = "active"
    expired = "expired"
    revoked = "revoked"


class GuildRole(str, Enum):
    owner = "owner"
    admin = "admin"
    manager = "manager"
    member = "member"


class Task(Base, IDMixin, TimestampMixin):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus), default=TaskStatus.pending, nullable=False, index=True)
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(TaskPriority), default=TaskPriority.medium, nullable=False, index=True
    )
    owner: Mapped[str] = mapped_column(String(120), default="unassigned", nullable=False)


class User(Base, IDMixin, TimestampMixin):
    __tablename__ = "users"

    discord_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    discriminator: Mapped[str | None] = mapped_column(String(10), nullable=True)
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    sessions: Mapped[list[Session]] = relationship(back_populates="user", cascade="all, delete-orphan")
    access_grants: Mapped[list[GuildAccessGrant]] = relationship(back_populates="user", cascade="all, delete-orphan")
    customer_identities: Mapped[list[CustomerIdentity]] = relationship(back_populates="user")
    audit_logs: Mapped[list[AuditLog]] = relationship(back_populates="actor_user")


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_reason: Mapped[str | None] = mapped_column(String(120), nullable=True)

    user: Mapped[User] = relationship(back_populates="sessions")


class Guild(Base, TimestampMixin):
    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(255), nullable=True)
    owner_discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)

    general_settings: Mapped[GuildGeneralSettings] = relationship(
        back_populates="guild", uselist=False, cascade="all, delete-orphan"
    )
    modules: Mapped[list[GuildModule]] = relationship(back_populates="guild", cascade="all, delete-orphan")
    premium: Mapped[GuildPremium | None] = relationship(back_populates="guild", uselist=False, cascade="all, delete-orphan")
    access_grants: Mapped[list[GuildAccessGrant]] = relationship(back_populates="guild", cascade="all, delete-orphan")
    customer_identities: Mapped[list[CustomerIdentity]] = relationship(back_populates="guild")
    audit_logs: Mapped[list[AuditLog]] = relationship(back_populates="guild")


class GuildGeneralSettings(Base, IDMixin, TimestampMixin):
    __tablename__ = "guild_general_settings"

    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    locale: Mapped[str] = mapped_column(String(10), default="en-US", nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", nullable=False)
    prefix: Mapped[str] = mapped_column(String(12), default="!", nullable=False)
    mod_log_channel_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    flags: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    guild: Mapped[Guild] = relationship(back_populates="general_settings")


class GuildModule(Base, IDMixin, TimestampMixin):
    __tablename__ = "guild_modules"
    __table_args__ = (UniqueConstraint("guild_id", "module_key", name="uq_guild_module_key"),)

    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False, index=True)
    module_key: Mapped[str] = mapped_column(String(64), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    guild: Mapped[Guild] = relationship(back_populates="modules")


class GuildPremium(Base, IDMixin, TimestampMixin):
    __tablename__ = "guild_premium"

    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    plan: Mapped[PlanType] = mapped_column(SAEnum(PlanType), nullable=False, default=PlanType.free)
    status: Mapped[AccessStatus] = mapped_column(SAEnum(AccessStatus), nullable=False, default=AccessStatus.active)
    source: Mapped[AccessSource] = mapped_column(SAEnum(AccessSource), nullable=False, default=AccessSource.free_default)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    guild: Mapped[Guild] = relationship(back_populates="premium")


class GuildAccessGrant(Base, IDMixin, TimestampMixin):
    __tablename__ = "guild_access_grants"

    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    source: Mapped[AccessSource] = mapped_column(SAEnum(AccessSource), nullable=False)
    status: Mapped[AccessStatus] = mapped_column(SAEnum(AccessStatus), nullable=False, default=AccessStatus.active)
    plan: Mapped[PlanType] = mapped_column(SAEnum(PlanType), nullable=False, default=PlanType.free)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    guild: Mapped[Guild] = relationship(back_populates="access_grants")
    user: Mapped[User | None] = relationship(back_populates="access_grants")


class CustomerIdentity(Base, IDMixin, TimestampMixin):
    __tablename__ = "customer_identity"
    __table_args__ = (UniqueConstraint("provider", "provider_customer_id", name="uq_provider_customer"),)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    guild_id: Mapped[int | None] = mapped_column(ForeignKey("guilds.id", ondelete="SET NULL"), nullable=True, index=True)
    provider: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    provider_customer_id: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped[User | None] = relationship(back_populates="customer_identities")
    guild: Mapped[Guild | None] = relationship(back_populates="customer_identities")


class AuditLog(Base, IDMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    actor_type: Mapped[str] = mapped_column(String(20), nullable=False, default="user")
    action: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    guild_id: Mapped[int | None] = mapped_column(ForeignKey("guilds.id", ondelete="SET NULL"), index=True)
    resource: Mapped[str | None] = mapped_column(String(120), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    actor_user: Mapped[User | None] = relationship(back_populates="audit_logs")
    guild: Mapped[Guild | None] = relationship(back_populates="audit_logs")


GuildSettings = GuildGeneralSettings
PremiumSubscription = GuildPremium
AccessGrant = GuildAccessGrant
