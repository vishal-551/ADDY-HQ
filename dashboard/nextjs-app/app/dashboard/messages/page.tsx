export default function MessagesPage() {
  return (
    <section className="dash-main-grid">
      <article className="card">
        <h2>Message Templates</h2>
        <p className="muted">Build high-quality message flows for onboarding, alerts, and support.</p>
        <div className="form">
          <label>Template Name<input className="input" defaultValue="Welcome Onboarding" /></label>
          <label>Channel<select className="input" defaultValue="#welcome"><option>#welcome</option><option>#announcements</option><option>#tickets</option></select></label>
          <label>Message Body<textarea className="input" defaultValue="Hey {user}, welcome to {server}! Read #rules and choose your roles." rows={5} /></label>
          <button className="btn btn-primary">Save Template</button>
        </div>
      </article>
    </section>
  );
}
