import { AreaChart, ActivityBars } from "@/components/dashboard/charts";
import { DashboardModuleCard } from "@/components/dashboard/module-card";
import { DashboardTable, FeatureCard, StatCard } from "@/components/dashboard/ui";
import { homeCards } from "./_data";
import { fetchWithFallback, type GuildModuleCard } from "@/lib/api";

type HomePayload = {
  stats: { label: string; value: string; trend: string }[];
  topUsers: { user: string; messages: number; commands: number; trust: string }[];
  activity: number[];
  commandTraffic: number[];
  logs: { time: string; event: string; level: string }[];
};

const fallback: HomePayload = {
  stats: [
    { label: "Active members", value: "14,892", trend: "+6.4% vs last week" },
    { label: "Commands/day", value: "42,308", trend: "+12.1% automation" },
    { label: "Moderation actions", value: "1,221", trend: "-4.8% incidents" },
    { label: "AI safety score", value: "98.2%", trend: "+0.7 policy match" },
  ],
  topUsers: [
    { user: "NovaKnight", messages: 1880, commands: 292, trust: "High" },
    { user: "Asteria", messages: 1730, commands: 198, trust: "High" },
    { user: "Cipher", messages: 1212, commands: 241, trust: "Medium" },
  ],
  activity: [44, 52, 63, 59, 72, 84, 90, 88, 96, 110, 103, 98],
  commandTraffic: [24, 20, 40, 54, 66, 52, 47, 58, 70, 76, 62, 55],
  logs: [
    { time: "14:02", event: "Raid shield auto-blocked 19 joins", level: "Critical" },
    { time: "13:48", event: "Welcome flow A/B test published", level: "Info" },
    { time: "13:12", event: "Ticket category SLA updated", level: "Warning" },
  ],
};

const fallbackModules: GuildModuleCard[] = [
  { key: "general", icon: "🤖", title: "Addy Main Bot", description: "Core utility and slash commands.", tier: "free", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/general" },
  { key: "welcome", icon: "👋", title: "Addy Welcome", description: "Onboarding and auto-role flows.", tier: "free", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/welcome" },
  { key: "moderation", icon: "🛡️", title: "Addy Moderation", description: "Smart moderation actions and logs.", tier: "free", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/moderation" },
  { key: "youtube", icon: "▶️", title: "Addy YouTube", description: "Creator upload tracking.", tier: "premium", enabled: false, connected: false, available: false, invite_url: "/invite", manage_url: "/dashboard/settings/youtube" },
  { key: "tickets", icon: "🎫", title: "Addy Tickets", description: "Support ticket channels.", tier: "premium", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/tickets" },
  { key: "ai", icon: "✨", title: "Addy AI", description: "AI moderation and assistant.", tier: "premium", enabled: false, connected: false, available: false, invite_url: "/invite", manage_url: "/dashboard/settings/ai" },
  { key: "levels", icon: "🏆", title: "Addy Levels", description: "XP, leaderboards, rewards.", tier: "free", enabled: true, connected: true, available: true, invite_url: "/invite", manage_url: "/dashboard/settings/levels" },
];

export default async function DashboardHomePage({
  searchParams,
}: {
  searchParams: { guild?: string };
}) {
  const guildId = Number(searchParams.guild ?? 101);
  const [data, modules] = await Promise.all([
    fetchWithFallback<HomePayload>("/api/dashboard/home", fallback),
    fetchWithFallback<GuildModuleCard[]>(`/guilds/${guildId}/modules`, fallbackModules),
  ]);

  return (
    <div className="dash-main-grid">
      <section className="grid grid-4">
        {data.stats.map((stat) => (
          <StatCard key={stat.label} title={stat.label} value={stat.value} trend={stat.trend} />
        ))}
      </section>

      <section>
        <h2>Automation Hub</h2>
        <p className="muted">Deploy, tune, and monitor core community workflows.</p>
        <div className="grid grid-3">
          {homeCards.map((card) => (
            <FeatureCard key={card.title} {...card} />
          ))}
        </div>
      </section>

      <section>
        <h2>Module System</h2>
        <p className="muted">Enable Addy modules per guild with premium access awareness.</p>
        <div className="grid grid-3">
          {modules.map((module) => (
            <DashboardModuleCard key={module.key} module={module} />
          ))}
        </div>
      </section>

      <section className="grid grid-2">
        <article className="card">
          <h3>Community activity</h3>
          <AreaChart points={data.activity} color="#8a7dff" />
        </article>
        <article className="card">
          <h3>Commands execution</h3>
          <ActivityBars points={data.commandTraffic} />
        </article>
      </section>

      <section className="grid grid-2">
        <article>
          <h3>Top users</h3>
          <DashboardTable
            columns={["User", "Messages", "Commands", "Trust"]}
            rows={data.topUsers.map((row) => [row.user, row.messages, row.commands, row.trust])}
          />
        </article>
        <article className="card">
          <h3>Logs preview</h3>
          <div className="logs-list">
            {data.logs.map((log) => (
              <div key={`${log.time}-${log.event}`} className="log-row">
                <span className="muted">{log.time}</span>
                <p>{log.event}</p>
                <span className="badge premium">{log.level}</span>
              </div>
            ))}
          </div>
        </article>
      </section>
    </div>
  );
}
