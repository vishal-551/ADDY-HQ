from __future__ import annotations

from shared.enums import ModuleAccessLevel, ModuleCategory


APP_SLUG = "addy"
DEFAULT_TIMEZONE = "UTC"
DISCORD_EPOCH = 1420070400000

DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100

PREMIUM_BADGES = {
    "free": "🟩 Free",
    "trial": "🟨 Trial",
    "premium": "🟪 Premium",
    "manual_access": "🟦 Manual Access",
}

RATE_LIMITS = {
    "auth.login": (20, 60),
    "auth.callback": (30, 60),
    "premium.redeem": (8, 60),
    "premium.trial": (3, 86400),
    "admin.broadcast": (5, 300),
}

MODULE_REGISTRY = [
    {
        "id": "core-general",
        "slug": "general",
        "title": "Addy Core",
        "short_description": "General commands, help and utility",
        "long_description": "Essential command suite including info, support, and quality of life utilities.",
        "icon": "Sparkles",
        "category": ModuleCategory.CORE.value,
        "access_level": ModuleAccessLevel.FREE.value,
        "standalone_available": False,
        "documentation_url": "/docs/core",
        "dashboard_supported": True,
        "admin_visible": True,
    },
    {
        "id": "mod-welcome",
        "slug": "welcome",
        "title": "Addy Welcome",
        "short_description": "Welcome, goodbye, verification, autoroles",
        "long_description": "Onboard users with rich welcome cards, onboarding rules, and automatic role assignments.",
        "icon": "DoorOpen",
        "category": ModuleCategory.ENGAGEMENT.value,
        "access_level": ModuleAccessLevel.FREE.value,
        "standalone_available": True,
        "documentation_url": "/docs/welcome",
        "dashboard_supported": True,
        "admin_visible": True,
    },
    {
        "id": "mod-moderation",
        "slug": "moderation",
        "title": "Addy Moderation",
        "short_description": "Warnings, punishments, and moderation workflows",
        "long_description": "Powerful moderation toolkit with logs, warning profiles, and configurable enforcement policies.",
        "icon": "Shield",
        "category": ModuleCategory.MODERATION.value,
        "access_level": ModuleAccessLevel.FREE.value,
        "standalone_available": True,
        "documentation_url": "/docs/moderation",
        "dashboard_supported": True,
        "admin_visible": True,
    },
    {
        "id": "mod-automod",
        "slug": "automod",
        "title": "Addy AutoMod",
        "short_description": "Anti-spam, anti-scam, anti-raid protections",
        "long_description": "Realtime automated moderation and raid prevention engine with intelligent heuristics and guardrails.",
        "icon": "Radar",
        "category": ModuleCategory.AUTOMATION.value,
        "access_level": ModuleAccessLevel.PREMIUM.value,
        "standalone_available": True,
        "documentation_url": "/docs/automod",
        "dashboard_supported": True,
        "admin_visible": True,
    },
    {
        "id": "mod-ai",
        "slug": "ai",
        "title": "Addy AI",
        "short_description": "AI chat, FAQ, summaries, moderation assistance",
        "long_description": "AI-powered assistant for community support, moderation aid, and context-aware conversational features.",
        "icon": "Bot",
        "category": ModuleCategory.AI.value,
        "access_level": ModuleAccessLevel.PREMIUM.value,
        "standalone_available": True,
        "documentation_url": "/docs/ai",
        "dashboard_supported": True,
        "admin_visible": True,
    },
    {
        "id": "mod-levels",
        "slug": "levels",
        "title": "Addy Levels",
        "short_description": "Gamified XP, ranks, and progression",
        "long_description": "Drive engagement with customizable level systems, rank rewards, and progression analytics.",
        "icon": "Trophy",
        "category": ModuleCategory.ENGAGEMENT.value,
        "access_level": ModuleAccessLevel.FREE.value,
        "standalone_available": True,
        "documentation_url": "/docs/levels",
        "dashboard_supported": True,
        "admin_visible": True,
    },
    {
        "id": "mod-tickets",
        "slug": "tickets",
        "title": "Addy Tickets",
        "short_description": "Support ticket channels and transcripts",
        "long_description": "Structured ticket flow with category routing, SLA-inspired workflows, and archive-ready transcripts.",
        "icon": "LifeBuoy",
        "category": ModuleCategory.AUTOMATION.value,
        "access_level": ModuleAccessLevel.PREMIUM.value,
        "standalone_available": True,
        "documentation_url": "/docs/tickets",
        "dashboard_supported": True,
        "admin_visible": True,
    },
    {
        "id": "mod-youtube",
        "slug": "youtube",
        "title": "Addy YouTube",
        "short_description": "Creator upload notifications",
        "long_description": "Track channels and post rich upload notifications directly to configured Discord channels.",
        "icon": "Youtube",
        "category": ModuleCategory.AUTOMATION.value,
        "access_level": ModuleAccessLevel.PREMIUM.value,
        "standalone_available": True,
        "documentation_url": "/docs/youtube",
        "dashboard_supported": True,
        "admin_visible": True,
    },
]
