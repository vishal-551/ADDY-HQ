import Link from "next/link";
import { ModuleCard, Kpi } from "@/components/cards";
import { Section, TinyChart } from "@/components/ui";
import { fetchPreview } from "@/lib/api";

type PublicData = {
  brand: { name: string; tagline: string; description: string; trustedBy: string[] };
  stats: { label: string; value: string }[];
  plans: { name: string; price: string; description: string; cta: string; features: string[] }[];
  analytics: { weeklyCommands: number[]; engagement: number[] };
};

type Module = {
  id: string;
  icon: string;
  title: string;
  description: string;
  tier: string;
  features: string[];
  connected: boolean;
};

export default async function HomePage() {
  const [publicData, modules] = await Promise.all([
    fetchPreview<PublicData>("/api/preview/public"),
    fetchPreview<Module[]>("/api/preview/modules"),
  ]);

  return (
    <>
      <section className="hero">
        <div>
          <p className="muted">{publicData.brand.tagline}</p>
          <h1>Build, moderate, and grow Discord with Addy.</h1>
          <p>{publicData.brand.description}</p>
          <div className="row gap">
            <Link href="/invite" className="btn btn-primary">Invite Addy</Link>
            <Link href="/dashboard/demo" className="btn btn-dark">View dashboard preview</Link>
          </div>
        </div>
        <div className="card">
          <h3>Live analytics preview</h3>
          <p className="muted">Weekly command volume</p>
          <TinyChart points={publicData.analytics.weeklyCommands} />
        </div>
      </section>

      <Section title="Trusted SaaS branding section" subtitle="Teams building their communities with Addy">
        <div className="grid grid-3">
          {publicData.brand.trustedBy.map((brand) => (
            <div className="card" key={brand}><strong>{brand}</strong></div>
          ))}
        </div>
      </Section>

      <Section title="Feature cards">
        <div className="grid grid-3">
          {publicData.stats.map((item) => <Kpi key={item.label} label={item.label} value={item.value} />)}
          <Kpi label="Uptime" value="99.98%" />
        </div>
      </Section>

      <Section title="Bot/module section" subtitle="Real cards with premium locks and actions">
        <div className="grid grid-3">
          {modules.map((module) => <ModuleCard key={module.id} module={module} />)}
        </div>
      </Section>

      <Section title="Premium comparison section">
        <div className="grid grid-3">
          {publicData.plans.map((plan) => (
            <article className="card" key={plan.name}>
              <h3>{plan.name}</h3><h2>{plan.price}</h2><p className="muted">{plan.description}</p>
              <ul>{plan.features.map((feature) => <li key={feature}>{feature}</li>)}</ul>
              <button className="btn btn-primary">{plan.cta}</button>
            </article>
          ))}
        </div>
      </Section>

      <Section title="Dashboard preview section">
        <div className="grid grid-2">
          <div className="card"><h3>User dashboard</h3><p className="muted">Guild overview, settings, analytics, premium.</p><Link href="/dashboard/user" className="btn btn-dark">Open user dashboard</Link></div>
          <div className="card"><h3>Admin dashboard</h3><p className="muted">Customers, revenue, system health and offers.</p><Link href="/dashboard/admin" className="btn btn-dark">Open admin dashboard</Link></div>
        </div>
      </Section>

      <Section title="Analytics preview section">
        <div className="card">
          <p className="muted">Engagement trend</p>
          <TinyChart points={publicData.analytics.engagement} color="#4be4c8" />
        </div>
      </Section>

      <Section title="CTA section" subtitle="Ready to launch Addy across your Discord servers?">
        <div className="row gap">
          <Link href="/login" className="btn btn-primary">Start with demo login</Link>
          <Link href="/pricing" className="btn">See pricing</Link>
        </div>
      </Section>
    </>
  );
}
