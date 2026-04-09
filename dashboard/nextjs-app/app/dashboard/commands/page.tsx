import { DashboardTable } from "@/components/dashboard/ui";

export default function CommandsPage() {
  return (
    <section className="dash-main-grid">
      <article className="card">
        <h2>Commands Manager</h2>
        <p className="muted">Enable command groups, set cooldowns, and lock permissions by role.</p>
        <div className="form grid-3">
          <label>Prefix<input className="input" defaultValue="!" /></label>
          <label>Default cooldown (sec)<input className="input" type="number" defaultValue={3} /></label>
          <label>Permission baseline<select className="input" defaultValue="members"><option value="members">Members</option><option value="staff">Staff</option><option value="admins">Admins</option></select></label>
        </div>
        <button className="btn btn-primary">Save Command Settings</button>
      </article>
      <DashboardTable
        columns={["Command", "Usage/day", "Cooldown", "Status"]}
        rows={[["/warn", 402, "5s", "Enabled"], ["/ban", 83, "15s", "Enabled"], ["/ticket", 294, "3s", "Enabled"], ["/rank", 1291, "2s", "Enabled"]]}
      />
    </section>
  );
}
