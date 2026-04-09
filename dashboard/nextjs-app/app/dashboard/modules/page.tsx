import { DashboardModuleCard } from "@/components/dashboard/module-card";
import { fetchWithFallback, type GuildModuleCard } from "@/lib/api";

const fallbackModules: GuildModuleCard[] = [
  { key: "general", icon: "🤖", title: "Addy Main Bot", description: "Core utility and slash commands.", tier: "free", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/general" },
  { key: "welcome", icon: "👋", title: "Addy Welcome", description: "Onboarding and auto-role flows.", tier: "free", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/welcome" },
  { key: "moderation", icon: "🛡️", title: "Addy Moderation", description: "Smart moderation actions and logs.", tier: "free", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/moderation" },
  { key: "youtube", icon: "▶️", title: "Addy YouTube", description: "Creator upload tracking.", tier: "premium", enabled: false, connected: false, available: false, invite_url: "/invite", manage_url: "/dashboard/settings/youtube" },
  { key: "tickets", icon: "🎫", title: "Addy Tickets", description: "Support ticket channels.", tier: "premium", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/tickets" },
  { key: "ai", icon: "✨", title: "Addy AI", description: "AI moderation and assistant.", tier: "premium", enabled: false, connected: false, available: false, invite_url: "/invite", manage_url: "/dashboard/settings/ai" },
  { key: "levels", icon: "🏆", title: "Addy Levels", description: "XP, leaderboards, rewards.", tier: "free", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/levels" },
];

export default async function ModulesPage({ searchParams }: { searchParams: { guild?: string } }) {
  const guildId = Number(searchParams.guild ?? 101);
  const modules = await fetchWithFallback<GuildModuleCard[]>(`/guilds/${guildId}/modules`, fallbackModules);

  return (
    <section>
      <h2>Module System</h2>
      <p className="muted">Activate and configure every Addy bot module at guild level.</p>
      <div className="grid grid-3">
        {modules.map((module) => (
          <DashboardModuleCard key={module.key} module={module} />
        ))}
      </div>
    </section>
  );
}
