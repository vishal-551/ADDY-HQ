import { DashboardShell } from "@/components/dashboard/shell";
import { fetchWithFallback } from "@/lib/api";
import type { CurrentUser, GuildSummary } from "@/lib/api";

const fallbackGuilds: GuildSummary[] = [
  { id: 101, name: "Addy Community", icon: null, owner_discord_id: 1 },
  { id: 102, name: "Creator Hub", icon: null, owner_discord_id: 1 },
  { id: 103, name: "Gaming Alliance", icon: null, owner_discord_id: 1 },
];

const fallbackUser: CurrentUser = {
  id: 1,
  discord_id: 1,
  username: "NovaDev#1001",
  email: "owner@addy.gg",
  is_admin: true,
};

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [guilds, user] = await Promise.all([
    fetchWithFallback<GuildSummary[]>("/guilds/list", fallbackGuilds),
    fetchWithFallback<{ user: CurrentUser }>("/auth/me", { user: fallbackUser }).then((res) => res.user),
  ]);

  return (
    <DashboardShell guilds={guilds} selectedGuildId={guilds[0]?.id} user={user}>
      {children}
    </DashboardShell>
  );
}
