from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


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
    promo_code = "promo_code"
    offer_campaign = "offer_campaign"


class AccessStatus(str, Enum):
    active = "active"
    expired = "expired"
    revoked = "revoked"


class GuildRole(str, Enum):
    owner = "owner"
    admin = "admin"
    manager = "manager"
    member = "member"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus), default=TaskStatus.pending, nullable=False, index=True)
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(TaskPriority), default=TaskPriority.medium, nullable=False, index=True
    )
    owner: Mapped[str] = mapped_column(String(120), default="unassigned", nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discord_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    discriminator: Mapped[str | None] = mapped_column(String(10), nullable=True)
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    sessions: Mapped[list[Session]] = relationship(back_populates="user", cascade="all, delete-orphan")
    access_grants: Mapped[list[AccessGrant]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="sessions")


class Guild(Base, TimestampMixin):
    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(255), nullable=True)
    owner_discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)

    settings: Mapped[GuildSettings] = relationship(back_populates="guild", uselist=False, cascade="all, delete-orphan")


class GuildSettings(Base, TimestampMixin):
    __tablename__ = "guild_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), unique=True, nullable=False)
    modules: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    welcome: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    moderation: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    automod: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    ai: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    levels: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    tickets: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    logs: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    youtube: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    giveaways: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    guild: Mapped[Guild] = relationship(back_populates="settings")


class PremiumSubscription(Base, TimestampMixin):
    __tablename__ = "premium_subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    plan: Mapped[PlanType] = mapped_column(SAEnum(PlanType), nullable=False, default=PlanType.free)
    status: Mapped[AccessStatus] = mapped_column(SAEnum(AccessStatus), nullable=False, default=AccessStatus.active)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)


class AccessGrant(Base, TimestampMixin):
    __tablename__ = "access_grants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    source: Mapped[AccessSource] = mapped_column(SAEnum(AccessSource), nullable=False)
    status: Mapped[AccessStatus] = mapped_column(SAEnum(AccessStatus), nullable=False, default=AccessStatus.active)
    plan: Mapped[PlanType] = mapped_column(SAEnum(PlanType), nullable=False, default=PlanType.free)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped[User | None] = relationship(back_populates="access_grants")


class CustomerIdentity(Base, TimestampMixin):
    __tablename__ = "customer_identity"
    __table_args__ = (UniqueConstraint("provider", "provider_customer_id", name="uq_provider_customer"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    guild_id: Mapped[int | None] = mapped_column(ForeignKey("guilds.id", ondelete="SET NULL"), nullable=True, index=True)
    provider: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    provider_customer_id: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)


class OfferCampaign(Base, TimestampMixin):
    __tablename__ = "offer_campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[PlanType] = mapped_column(SAEnum(PlanType), nullable=False, default=PlanType.premium)
    bonus_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_redemptions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    redemptions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class PromoCode(Base, TimestampMixin):
    __tablename__ = "promo_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    percent_off: Mapped[int] = mapped_column(Integer, nullable=False)
    max_uses: Mapped[int | None] = mapped_column(Integer, nullable=True)
    uses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (CheckConstraint("percent_off >= 1 AND percent_off <= 100", name="ck_promo_percent"),)


class BillingEvent(Base, TimestampMixin):
    __tablename__ = "billing_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int | None] = mapped_column(ForeignKey("guilds.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    provider: Mapped[str] = mapped_column(String(40), nullable=False)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(8), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class Warning(Base, TimestampMixin):
    __tablename__ = "warnings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    user_discord_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    moderator_discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)


class Punishment(Base, TimestampMixin):
    __tablename__ = "punishments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    user_discord_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class YouTubeSubscription(Base, TimestampMixin):
    __tablename__ = "youtube_subscriptions"
    __table_args__ = (UniqueConstraint("guild_id", "channel_id", name="uq_guild_channel"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    channel_id: Mapped[str] = mapped_column(String(128), nullable=False)
    notify_channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Ticket(Base, TimestampMixin):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    opener_discord_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False)


class Transcript(Base, TimestampMixin):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"), index=True, nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)


class LevelProfile(Base, TimestampMixin):
    __tablename__ = "level_profiles"
    __table_args__ = (UniqueConstraint("guild_id", "user_discord_id", name="uq_guild_user_level"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    user_discord_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class Giveaway(Base, TimestampMixin):
    __tablename__ = "giveaways"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), index=True, nullable=False)
    channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    message_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    prize: Mapped[str] = mapped_column(String(255), nullable=False)
    winner_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    actor_type: Mapped[str] = mapped_column(String(20), nullable=False, default="user")
    action: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    guild_id: Mapped[int | None] = mapped_column(ForeignKey("guilds.id", ondelete="SET NULL"), index=True)
    resource: Mapped[str | None] = mapped_column(String(120), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
