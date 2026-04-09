import Link from "next/link";
import { Kpi, ModuleCard } from "@/components/cards";
import { Section, TinyChart } from "@/components/ui";
import { fetchPreview } from "@/lib/api";

type PublicData = {
  stats: { label: string; value: string }[];
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

export default async function DemoDashboardPage() {
  const [publicData, modules] = await Promise.all([
    fetchPreview<PublicData>("/api/preview/public"),
    fetchPreview<Module[]>("/api/preview/modules"),
  ]);

  return (
    <>
      <Section title="Demo dashboard preview" subtitle="A real product-like layout with cards, analytics and module controls.">
        <div className="grid grid-3">
          {publicData.stats.map((item) => (
            <Kpi key={item.label} label={item.label} value={item.value} />
          ))}
        </div>
      </Section>
      <Section title="Module controls">
        <div className="grid grid-3">{modules.map((module) => <ModuleCard key={module.id} module={module} />)}</div>
      </Section>
      <Section title="Analytics charts">
        <div className="grid grid-2">
          <div className="card"><p className="muted">Commands / week</p><TinyChart points={publicData.analytics.weeklyCommands} /></div>
          <div className="card"><p className="muted">Engagement score</p><TinyChart points={publicData.analytics.engagement} color="#4be4c8" /></div>
        </div>
      </Section>
      <Section title="Jump to full dashboard previews">
        <div className="row gap">
          <Link className="btn btn-primary" href="/dashboard/user">User Dashboard</Link>
          <Link className="btn" href="/dashboard/admin">Admin Dashboard</Link>
        </div>
      </Section>
    </>
  );
}
