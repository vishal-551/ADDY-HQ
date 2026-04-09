import { ReactNode } from "react";

export function StatCard({ title, value, trend }: { title: string; value: string; trend: string }) {
  return (
    <article className="card stat-card">
      <p className="muted">{title}</p>
      <h3>{value}</h3>
      <p className="trend">{trend}</p>
    </article>
  );
}

export function FeatureCard({ icon, title, description, cta }: { icon: string; title: string; description: string; cta: string }) {
  return (
    <article className="card feature-card">
      <div className="feature-icon">{icon}</div>
      <h3>{title}</h3>
      <p className="muted">{description}</p>
      <button className="btn btn-primary">{cta}</button>
    </article>
  );
}

export function FormCard({ title, description, children }: { title: string; description: string; children: ReactNode }) {
  return (
    <section className="card settings-card">
      <h3>{title}</h3>
      <p className="muted">{description}</p>
      <div className="form">{children}</div>
    </section>
  );
}

export function ToggleField({ label, enabled }: { label: string; enabled: boolean }) {
  return (
    <label className="toggle-row">
      <span>{label}</span>
      <span className={`toggle ${enabled ? "enabled" : ""}`}>
        <span className="knob" />
      </span>
    </label>
  );
}

export function DashboardTable({
  columns,
  rows,
}: {
  columns: string[];
  rows: Array<Array<string | number | ReactNode>>;
}) {
  return (
    <div className="card">
      <table className="table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={`row-${rowIndex}`}>
              {row.map((cell, cellIndex) => (
                <td key={`cell-${rowIndex}-${cellIndex}`}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
