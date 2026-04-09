from __future__ import annotations

from fastapi import APIRouter

from shared.response_builder import ok

router = APIRouter(prefix="/api/preview", tags=["preview"])

MODULES = [
    {
        "id": "main",
        "icon": "🤖",
        "title": "Addy Main Bot",
        "description": "Core automation, slash commands, and server utility actions.",
        "tier": "free",
        "features": ["Slash commands", "Server insights", "Fast setup"],
        "connected": True,
    },
    {
        "id": "welcome",
        "icon": "👋",
        "title": "Addy Welcome",
        "description": "Personalized onboarding with embeds and role assignment.",
        "tier": "free",
        "features": ["Join messages", "Auto roles", "Embed templates"],
        "connected": True,
    },
    {
        "id": "moderation",
        "icon": "🛡️",
        "title": "Addy Moderation",
        "description": "Smart moderation workflows with warnings, mute and ban tools.",
        "tier": "free",
        "features": ["Warn system", "Timeout tools", "Case history"],
        "connected": True,
    },
    {
        "id": "youtube",
        "icon": "▶️",
        "title": "Addy YouTube",
        "description": "Notify channels instantly whenever creators publish new videos.",
        "tier": "premium",
        "features": ["Channel tracking", "Smart posting", "Video filters"],
        "connected": False,
    },
    {
        "id": "tickets",
        "icon": "🎫",
        "title": "Addy Tickets",
        "description": "Structured support ticket panel with private staff channels.",
        "tier": "premium",
        "features": ["Ticket panels", "SLA tags", "Auto close rules"],
        "connected": False,
    },
    {
        "id": "ai",
        "icon": "✨",
        "title": "Addy AI",
        "description": "AI assistant for replies, summaries, and community guidance.",
        "tier": "premium",
        "features": ["Thread summaries", "AI auto-reply", "Prompt controls"],
        "connected": False,
    },
    {
        "id": "levels",
        "icon": "🏆",
        "title": "Addy Levels",
        "description": "Gamified XP, role progression, and leaderboard competitions.",
        "tier": "premium",
        "features": ["XP tuning", "Role rewards", "Leaderboard cards"],
        "connected": True,
    },
]


@router.get("/modules")
def modules() -> dict:
    return ok(MODULES)


@router.get("/public")
def public_preview() -> dict:
    return ok(
        {
            "brand": {
                "name": "Addy",
                "tagline": "Discord Growth OS",
                "description": "Operate, automate, and monetize your Discord communities from one premium control plane.",
                "trustedBy": ["Nova Labs", "GuildForge", "Velocity", "PixelFrame", "Orbital"],
            },
            "stats": [
                {"label": "Active guilds", "value": "2,184"},
                {"label": "Monthly actions", "value": "14.2M"},
                {"label": "Avg. response", "value": "110ms"},
            ],
            "plans": [
                {
                    "name": "Free",
                    "price": "$0",
                    "description": "Ideal for small communities",
                    "cta": "Start Free",
                    "features": ["Welcome", "Moderation", "Basic analytics"],
                },
                {
                    "name": "Pro",
                    "price": "$19/mo",
                    "description": "Scaling communities and creators",
                    "cta": "Upgrade to Pro",
                    "features": ["AI module", "Tickets", "YouTube alerts", "Advanced analytics"],
                },
                {
                    "name": "Scale",
                    "price": "$79/mo",
                    "description": "Multi-community operations",
                    "cta": "Talk to Sales",
                    "features": ["Unlimited guilds", "Admin broadcasts", "Revenue insights"],
                },
            ],
            "analytics": {
                "weeklyCommands": [1200, 1800, 1400, 2200, 2600, 2800, 3100],
                "engagement": [62, 66, 65, 70, 74, 77, 81],
            },
        }
    )


@router.get("/user")
def user_dashboard_preview() -> dict:
    return ok(
        {
            "user": {"name": "Aarav Sharma", "plan": "Pro", "email": "aarav@addy.gg"},
            "guilds": [
                {"id": "g1", "name": "Addy Community", "members": 28421, "health": "Excellent"},
                {"id": "g2", "name": "Creator Hub", "members": 8320, "health": "Good"},
                {"id": "g3", "name": "Tech Syndicate", "members": 15210, "health": "Needs attention"},
            ],
            "overview": {
                "automodTriggers": 182,
                "welcomeMessages": 1204,
                "ticketsResolved": 387,
                "aiReplies": 521,
            },
            "settings": {
                "welcome": {"enabled": True, "channel": "#welcome", "autoRole": "Member"},
                "moderation": {"maxWarnings": 3, "defaultTimeout": "30m", "modLog": "#mod-logs"},
                "automod": {"spam": True, "caps": True, "links": False},
                "ai": {"model": "Addy Assist v2", "tone": "Friendly", "replyMode": "Assist-only"},
                "youtube": {"trackedChannels": 6, "targetChannel": "#announcements", "delay": "Instant"},
                "levels": {"xpPerMessage": 8, "cooldown": "30s", "levelUpChannel": "#general"},
                "tickets": {"panelChannel": "#support", "staffRole": "Support Team", "autoCloseHours": 72},
            },
            "analytics": {
                "messages": [4200, 3980, 4600, 4890, 5120, 5300, 5520],
                "retention": [72, 73, 71, 75, 76, 78, 79],
            },
            "premium": {
                "status": "Active",
                "renewalDate": "2026-05-04",
                "lockedModules": ["AI AutoPilot", "Advanced Audit Streams"],
            },
        }
    )


@router.get("/admin")
def admin_dashboard_preview() -> dict:
    return ok(
        {
            "kpis": {
                "customers": 814,
                "premiumGuilds": 291,
                "mrr": 18542,
                "incidentCount": 1,
            },
            "customers": [
                {"name": "Nova Labs", "tier": "Scale", "joined": "2025-11-20", "status": "Active"},
                {"name": "Creator Hub", "tier": "Pro", "joined": "2026-01-09", "status": "Trial"},
                {"name": "Questline", "tier": "Pro", "joined": "2026-02-18", "status": "Active"},
            ],
            "guilds": [
                {"name": "Addy Community", "members": 28421, "region": "US East", "plan": "Scale"},
                {"name": "Tech Syndicate", "members": 15210, "region": "Europe", "plan": "Pro"},
                {"name": "Chill Space", "members": 6120, "region": "US West", "plan": "Free"},
            ],
            "auditLogs": [
                "[12:03] Premium upgraded for Nova Labs",
                "[12:11] Promo code ADDYSPRING applied",
                "[12:42] Broadcast sent to 291 premium guilds",
            ],
            "offers": [
                {"name": "Creator Pro Annual", "discount": "20%", "active": True},
                {"name": "Scale Starter", "discount": "15%", "active": False},
            ],
            "promoCodes": [
                {"code": "ADDYPRO10", "usage": 124, "expires": "2026-06-01"},
                {"code": "WELCOME20", "usage": 66, "expires": "2026-07-15"},
            ],
            "revenue": [12200, 13050, 14220, 15100, 16740, 17590, 18542],
            "health": [
                {"service": "Gateway", "status": "Operational", "latencyMs": 98},
                {"service": "API", "status": "Operational", "latencyMs": 72},
                {"service": "Worker Queue", "status": "Degraded", "latencyMs": 220},
            ],
        }
    )


@router.post("/auth/login")
def demo_login() -> dict:
    return ok(
        {
            "token": "demo-session-token",
            "user": {"name": "Aarav Sharma", "role": "Owner", "plan": "Pro"},
        },
        message="Demo login successful",
    )
