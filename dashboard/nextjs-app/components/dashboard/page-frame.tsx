import { DashboardTable } from "./ui";

export function DashboardPageFrame({
  title,
  subtitle,
  stats,
  rows,
}: {
  title: string;
  subtitle: string;
  stats: Array<{ label: string; value: string }>;
  rows: Array<Array<string | number>>;
}) {
  return (
    <section className="dash-main-grid">
      <div>
        <h2>{title}</h2>
        <p className="muted">{subtitle}</p>
      </div>
      <div className="grid grid-4">
        {stats.map((stat) => (
          <article className="card" key={stat.label}>
            <p className="muted">{stat.label}</p>
            <h3>{stat.value}</h3>
          </article>
        ))}
      </div>
      <DashboardTable columns={["Name", "Value A", "Value B", "Status"]} rows={rows} />
    </section>
  );
}
