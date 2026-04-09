import { ModuleCard } from "@/components/cards";
import { Section } from "@/components/ui";
import { fetchPreview } from "@/lib/api";

type Module = {
  id: string;
  icon: string;
  title: string;
  description: string;
  tier: string;
  features: string[];
  connected: boolean;
};

export default async function FeaturesPage() {
  const modules = await fetchPreview<Module[]>("/api/preview/modules");
  return (
    <Section title="Addy features" subtitle="Automation, safety, engagement, and growth modules.">
      <div className="grid grid-3">
        {modules.map((module) => (
          <ModuleCard key={module.id} module={module} />
        ))}
      </div>
    </Section>
  );
}
