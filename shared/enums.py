from __future__ import annotations

from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class PlanType(str, Enum):
    FREE = "free"
    TRIAL = "trial"
    PREMIUM = "premium"


class AccessSource(str, Enum):
    FREE_DEFAULT = "free_default"
    TRIAL = "trial"
    BILLING = "billing"
    OWNER_GRANT = "owner_grant"
    MANUAL_ACCESS = "manual_access"
    PROMO_CODE = "promo_code"
    OFFER_CAMPAIGN = "offer_campaign"


class AccessStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"


class ModuleCategory(str, Enum):
    CORE = "core"
    MODERATION = "moderation"
    ENGAGEMENT = "engagement"
    AUTOMATION = "automation"
    AI = "ai"
    ANALYTICS = "analytics"
    MONETIZATION = "monetization"


class ModuleAccessLevel(str, Enum):
    FREE = "free"
    PREMIUM = "premium"


class GuildRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"


class AuditActorType(str, Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"


class BillingEventType(str, Enum):
    CHECKOUT_STARTED = "checkout_started"
    CHECKOUT_COMPLETED = "checkout_completed"
    SUBSCRIPTION_RENEWED = "subscription_renewed"
    SUBSCRIPTION_CANCELED = "subscription_canceled"
    PAYMENT_FAILED = "payment_failed"
    REFUND_ISSUED = "refund_issued"


class OfferType(str, Enum):
    FLAT_DISCOUNT = "flat_discount"
    PERCENT_DISCOUNT = "percent_discount"
    BONUS_DAYS = "bonus_days"
    TRIAL_EXTENSION = "trial_extension"
