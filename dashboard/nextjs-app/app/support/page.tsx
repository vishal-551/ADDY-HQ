export default function SupportPage() {
  return (
    <section className="section">
      <h1>Support Center</h1>
      <p className="muted">Need help with setup, billing, premium access, or module behavior? Reach the Addy team.</p>
      <div className="grid grid-2">
        <article className="card">
          <h3>Live Support</h3>
          <p className="muted">Average response time: under 15 minutes for premium guilds.</p>
          <button className="btn btn-primary">Open ticket</button>
        </article>
        <article className="card">
          <h3>Status & Incidents</h3>
          <p className="muted">Gateway, API, and workers are monitored continuously.</p>
          <button className="btn">View status</button>
        </article>
      </div>
    </section>
  );
}
