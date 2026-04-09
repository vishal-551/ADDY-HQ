import Link from "next/link";
import { ReactNode } from "react";

export function TopNav() {
  const links = [
    ["Home", "/"],
    ["Features", "/features"],
    ["Pricing", "/pricing"],
    ["Docs", "/docs"],
    ["Support", "/support"],
    ["Invite Bot", "/invite"],
  ];

  return (
    <header className="nav-shell">
      <div className="brand">Addy</div>
      <nav>
        {links.map(([label, href]) => (
          <Link key={href} href={href} className="nav-link">
            {label}
          </Link>
        ))}
      </nav>
      <div className="row gap">
        <Link href="/dashboard" className="btn">Dashboard</Link>
        <Link href="/login" className="btn btn-primary">Login</Link>
      </div>
    </header>
  );
}

export function Section({ title, subtitle, children }: { title: string; subtitle?: string; children: ReactNode }) {
  return (
    <section className="section">
      <h2>{title}</h2>
      {subtitle ? <p className="muted">{subtitle}</p> : null}
      {children}
    </section>
  );
}

export function Footer() {
  return (
    <footer className="footer">
      <div>© 2026 Addy Bot Platform</div>
      <div className="muted">Discord-ready SaaS automation suite</div>
    </footer>
  );
}

export function TinyChart({ points, color = "#7c8cff" }: { points: number[]; color?: string }) {
  const max = Math.max(...points, 1);
  return (
    <div className="mini-chart">
      {points.map((point, idx) => (
        <div
          key={`${point}-${idx}`}
          className="bar"
          style={{ height: `${Math.round((point / max) * 100)}%`, backgroundColor: color }}
          title={`${point}`}
        />
      ))}
    </div>
  );
}
