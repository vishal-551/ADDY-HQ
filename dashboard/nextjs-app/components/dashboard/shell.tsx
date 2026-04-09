import Link from "next/link";
import { ReactNode } from "react";

const navItems = [
  { label: "Home", href: "/dashboard", icon: "🏠" },
  { label: "General Settings", href: "/dashboard/settings/general", icon: "⚙️" },
  { label: "Commands", href: "/dashboard/commands", icon: "⌨️" },
  { label: "Messages", href: "/dashboard/messages", icon: "💬" },
  { label: "Branding", href: "/dashboard/branding", icon: "🎨" },
];

const moduleItems = [
  { label: "Auto Moderation", href: "/dashboard/settings/automod" },
  { label: "Moderation", href: "/dashboard/settings/moderation" },
  { label: "Social Notifications", href: "/dashboard/modules" },
  { label: "Join Roles", href: "/dashboard/settings/roles" },
  { label: "Reaction Roles", href: "/dashboard/settings/roles" },
  { label: "Welcome Messages", href: "/dashboard/settings/welcome" },
  { label: "Logging", href: "/dashboard/settings/logging" },
  { label: "AI Moderation", href: "/dashboard/settings/ai" },
];

export function DashboardShell({ children }: { children: ReactNode }) {
  return (
    <div className="dash-root">
      <aside className="dash-sidebar">
        <div className="dash-brand">
          <div className="brand-dot" />
          <div>
            <strong>Addy Dashboard</strong>
            <p className="muted">Premium guild manager</p>
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

        <p className="dash-nav-title">Modules</p>
        <nav className="dash-nav dash-nav-modules">
          {moduleItems.map((item) => (
            <Link key={item.label} href={item.href} className="dash-link dash-link-module">
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      <section className="dash-content">
        <header className="dash-topbar">
          <div>
            <h1>Guild Control Center</h1>
            <p className="muted">Realtime controls, analytics, and module orchestration</p>
          </div>
          <div className="dash-topbar-actions">
            <select className="input" defaultValue="arcane-hub">
              <option value="arcane-hub">Arcane Hub</option>
              <option value="gaming-alliance">Gaming Alliance</option>
              <option value="creator-house">Creator House</option>
            </select>
            <button className="btn btn-dark">NovaDev#1001</button>
          </div>
        </header>
        {children}
      </section>
    </div>
  );
}
