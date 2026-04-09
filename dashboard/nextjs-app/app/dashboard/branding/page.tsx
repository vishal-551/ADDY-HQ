export default function BrandingPage() {
  return (
    <section className="dash-main-grid">
      <article className="card">
        <h2>Branding Settings</h2>
        <p className="muted">Customize colors, bot identity, and embed style for a premium appearance.</p>
        <div className="form grid-2">
          <label>Primary Color<input className="input" defaultValue="#7d78ff" /></label>
          <label>Accent Color<input className="input" defaultValue="#4be4c8" /></label>
          <label>Embed Footer<input className="input" defaultValue="Powered by Addy" /></label>
          <label>Dashboard Logo URL<input className="input" defaultValue="https://cdn.addy/bot-logo.png" /></label>
        </div>
        <button className="btn btn-primary">Save Branding</button>
      </article>
    </section>
  );
}
