import { moduleCatalog } from "../_data";

export default function ModulesPage() {
  return (
    <section>
      <h2>Module System</h2>
      <p className="muted">Enable premium modules and configure integrations in one place.</p>
      <div className="grid grid-3">
        {moduleCatalog.map((module) => (
          <article key={module.name} className="card module-tile">
            <div className="row space-between">
              <h3>{module.name}</h3>
              {module.premium ? <span className="badge premium">Premium</span> : <span className="badge free">Free</span>}
            </div>
            <div className="toggle-row">
              <span>Enabled</span>
              <span className={`toggle ${module.enabled ? "enabled" : ""}`}>
                <span className="knob" />
              </span>
            </div>
            <div className="row gap">
              <button className="btn btn-primary">Connect</button>
              <button className="btn btn-dark">Manage</button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
