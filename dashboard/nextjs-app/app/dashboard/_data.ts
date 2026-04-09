export const homeCards = [
  {
    icon: "📝",
    title: "Custom messages",
    description: "Configure rich embeds, autoresponders, and scheduled announcements.",
    cta: "Manage Messages",
  },
  {
    icon: "🛡️",
    title: "Moderation cases",
    description: "Track incidents, escalations, and active punishments from one panel.",
    cta: "Open Cases",
  },
  {
    icon: "👋",
    title: "Role greetings",
    description: "Send contextual greetings with role-based flows and onboarding steps.",
    cta: "Edit Workflow",
  },
  {
    icon: "🚨",
    title: "User reports",
    description: "Route reports to moderation teams with SLA and ownership controls.",
    cta: "Review Reports",
  },
  {
    icon: "🤖",
    title: "AI moderation",
    description: "Classify toxicity, spam, and raids using Addy AI policy models.",
    cta: "Tune Policies",
  },
  {
    icon: "#️⃣",
    title: "Prefix settings",
    description: "Set custom prefix fallbacks with per-channel command behavior.",
    cta: "Update Prefix",
  },
];

export const moduleCatalog = [
  { name: "Addy Welcome", premium: false, enabled: true },
  { name: "Addy Moderation", premium: false, enabled: true },
  { name: "Addy AI", premium: true, enabled: true },
  { name: "Addy Tickets", premium: true, enabled: false },
  { name: "Addy YouTube", premium: true, enabled: false },
  { name: "Addy Levels", premium: false, enabled: true },
];
