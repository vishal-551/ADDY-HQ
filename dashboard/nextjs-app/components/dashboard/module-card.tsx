import Link from "next/link";
import type { GuildModuleCard } from "@/lib/api";

export function DashboardModuleCard({ module }: { module: GuildModuleCard }) {
  const canManage = module.available;

  return (
    <article className="card module-tile">
      <div className="row space-between">
        <div className="row gap">
          <span className="icon">{module.icon}</span>
          <div>
            <h3>{module.title}</h3>
            <p className="muted">{module.description}</p>
          </div>
        </div>
        <span className={`badge ${module.tier === "premium" ? "premium" : "free"}`}>
          {module.tier === "premium" ? "Premium" : "Free"}
        </span>
      </div>

      <div className="toggle-row">
        <span>{module.enabled ? "Enabled" : "Disabled"}</span>
        <span className={`badge ${module.enabled ? "free" : "premium"}`}>
          {module.connected ? "Connected" : "Not connected"}
        </span>
      </div>

      <div className="row gap">
        <Link href={module.invite_url} className="btn btn-primary">
          {module.connected ? "Reconnect" : "Connect / Invite"}
        </Link>
        <Link
          href={module.manage_url}
          className="btn btn-dark"
          aria-disabled={!canManage}
          style={!canManage ? { opacity: 0.6, pointerEvents: "none" } : undefined}
        >
          Manage
        </Link>
      </div>
    </article>
  );
}
