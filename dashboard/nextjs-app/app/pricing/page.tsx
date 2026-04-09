import { Section } from "@/components/ui";
import { fetchPreview } from "@/lib/api";

type Plan = { name: string; price: string; description: string; cta: string; features: string[] };

export default async function PricingPage() {
  const data = await fetchPreview<{ plans: Plan[] }>("/api/preview/public");
  return (
    <Section title="Pricing" subtitle="Transparent plans for every community stage.">
      <div className="grid grid-3">
        {data.plans.map((plan) => (
          <article className="card" key={plan.name}>
            <h3>{plan.name}</h3>
            <h2>{plan.price}</h2>
            <p className="muted">{plan.description}</p>
            <ul>{plan.features.map((feature) => <li key={feature}>{feature}</li>)}</ul>
            <button className="btn btn-primary">{plan.cta}</button>
          </article>
        ))}
      </div>
    </Section>
  );
}
