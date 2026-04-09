import Link from "next/link";
import { ReactNode, Suspense } from "react";
import type { CurrentUser, GuildSummary } from "@/lib/api";
import { GuildSelector } from "./guild-selector";

const navItems = [
  { label: "Home", href: "/dashboard", icon: "🏠" },
  { label: "Guilds", href: "/dashboard/guilds", icon: "🧩" },
  { label: "Analytics", href: "/dashboard/analytics", icon: "📈" },
  { label: "Modules", href: "/dashboard/modules", icon: "🧠" },
  { label: "Premium", href: "/dashboard/premium", icon: "💎" },
  { label: "Members", href: "/dashboard/members", icon: "👥" },
  { label: "Channels", href: "/dashboard/channels", icon: "#️⃣" },
  { label: "Roles", href: "/dashboard/roles", icon: "🪪" },
  { label: "Import", href: "/dashboard/import", icon: "⬇️" },
  { label: "Export", href: "/dashboard/export", icon: "⬆️" },
];

const settingsItems = [
  { label: "General", href: "/dashboard/settings/general" },
  { label: "Welcome", href: "/dashboard/settings/welcome" },
  { label: "Moderation", href: "/dashboard/settings/moderation" },
  { label: "AutoMod", href: "/dashboard/settings/automod" },
  { label: "AI", href: "/dashboard/settings/ai" },
  { label: "Levels", href: "/dashboard/settings/levels" },
  { label: "Tickets", href: "/dashboard/settings/tickets" },
  { label: "Logs", href: "/dashboard/settings/logs" },
  { label: "YouTube", href: "/dashboard/settings/youtube" },
  { label: "Giveaways", href: "/dashboard/settings/giveaways" },
];

export function DashboardShell({
  children,
  guilds,
  selectedGuildId,
  user,
}: {
  children: ReactNode;
  guilds: GuildSummary[];
  selectedGuildId?: number;
  user: CurrentUser;
}) {
  return (
    <div className="dash-root">
      <aside className="dash-sidebar">
        <div className="dash-brand">
          <div className="brand-dot" />
          <div>
            <strong>Addy Platform</strong>
            <p className="muted">Discord Growth OS</p>
          </div>
        </div>

        <nav className="dash-nav">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="dash-link">
              <span>{item.icon}</span>
              {item.label}
            </Link>
          ))}
        </nav>

        <p className="dash-nav-title">Settings</p>
        <nav className="dash-nav dash-nav-modules">
          {settingsItems.map((item) => (
            <Link key={item.label} href={item.href} className="dash-link dash-link-module">
              {item.label}
            </Link>
          ))}
        </nav>

        {user.is_admin ? (
          <>
            <p className="dash-nav-title">Platform Admin</p>
            <nav className="dash-nav">
              <Link href="/dashboard/admin" className="dash-link">🛠️ Admin Home</Link>
              <Link href="/dashboard/admin/guilds" className="dash-link">🏘️ Guild Control</Link>
              <Link href="/dashboard/admin/premium" className="dash-link">💳 Premium Access</Link>
            </nav>
          </>
        ) : null}
      </aside>

      <section className="dash-content">
        <header className="dash-topbar">
          <div>
            <h1>Guild Control Center</h1>
            <p className="muted">Manage bots, modules, settings, and growth from one place.</p>
          </div>
          <div className="dash-topbar-actions">
            <Suspense fallback={<select className="input guild-select"><option>Loading guilds...</option></select>}><GuildSelector guilds={guilds} selectedGuildId={selectedGuildId} /></Suspense>
            <button className="btn btn-dark">{user.username}{user.is_admin ? " • Admin" : ""}</button>
          </div>
        </header>
        {children}
      </section>
    </div>
  );
}
