type Module = {
  id: string;
  icon: string;
  title: string;
  description: string;
  tier: string;
  features: string[];
  connected: boolean;
};

export function ModuleCard({ module }: { module: Module }) {
  return (
    <article className="card module-card">
      <div className="card-head">
        <span className="icon">{module.icon}</span>
        <div>
          <h3>{module.title}</h3>
          <span className={`badge ${module.tier === "premium" ? "premium" : "free"}`}>{module.tier}</span>
        </div>
      </div>
      <p className="muted">{module.description}</p>
      <ul>
        {module.features.map((feature) => (
          <li key={feature}>{feature}</li>
        ))}
      </ul>
      <div className="row gap">
        <button className="btn btn-primary">{module.connected ? "Connected" : "Connect / Invite"}</button>
        <button className="btn btn-dark">Manage</button>
      </div>
    </article>
  );
}

export function Kpi({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="card kpi">
      <p className="muted">{label}</p>
      <h3>{value}</h3>
    </div>
  );
}
