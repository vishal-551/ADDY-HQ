import { Kpi } from "@/components/cards";
import { Section, TinyChart } from "@/components/ui";
import { fetchPreview } from "@/lib/api";

type AdminData = {
  kpis: { customers: number; premiumGuilds: number; mrr: number; incidentCount: number };
  customers: { name: string; tier: string; joined: string; status: string }[];
  guilds: { name: string; members: number; region: string; plan: string }[];
  auditLogs: string[];
  offers: { name: string; discount: string; active: boolean }[];
  promoCodes: { code: string; usage: number; expires: string }[];
  revenue: number[];
  health: { service: string; status: string; latencyMs: number }[];
};

export default async function AdminDashboardPage() {
  const data = await fetchPreview<AdminData>("/api/preview/admin");

  return (
    <>
      <Section title="Admin dashboard preview" subtitle="Customers, guilds, premium management, revenue, logs, offers and system health.">
        <div className="grid grid-3">
          {Object.entries(data.kpis).map(([label, value]) => <Kpi key={label} label={label} value={value} />)}
        </div>
      </Section>

      <Section title="Customers">
        <div className="card">
          <table className="table"><thead><tr><th>Name</th><th>Tier</th><th>Joined</th><th>Status</th></tr></thead><tbody>
            {data.customers.map((customer) => <tr key={customer.name}><td>{customer.name}</td><td>{customer.tier}</td><td>{customer.joined}</td><td>{customer.status}</td></tr>)}
          </tbody></table>
        </div>
      </Section>

      <Section title="Guilds + premium management">
        <div className="card">
          <table className="table"><thead><tr><th>Guild</th><th>Members</th><th>Region</th><th>Plan</th></tr></thead><tbody>
            {data.guilds.map((guild) => <tr key={guild.name}><td>{guild.name}</td><td>{guild.members}</td><td>{guild.region}</td><td>{guild.plan}</td></tr>)}
          </tbody></table>
        </div>
      </Section>

      <Section title="Revenue analytics">
        <div className="card"><TinyChart points={data.revenue} color="#7c8cff" /></div>
      </Section>

      <Section title="Audit logs + broadcasts">
        <div className="card"><ul>{data.auditLogs.map((entry) => <li key={entry}>{entry}</li>)}</ul><button className="btn btn-dark">Send Broadcast</button></div>
      </Section>

      <Section title="Offers + promo codes">
        <div className="grid grid-2">
          <div className="card"><h3>Offers</h3><ul>{data.offers.map((offer) => <li key={offer.name}>{offer.name} • {offer.discount} • {offer.active ? "Active" : "Paused"}</li>)}</ul></div>
          <div className="card"><h3>Promo codes</h3><ul>{data.promoCodes.map((promo) => <li key={promo.code}>{promo.code} • {promo.usage} uses • exp {promo.expires}</li>)}</ul></div>
        </div>
      </Section>

      <Section title="System health">
        <div className="card"><table className="table"><thead><tr><th>Service</th><th>Status</th><th>Latency</th></tr></thead><tbody>
          {data.health.map((service) => <tr key={service.service}><td>{service.service}</td><td>{service.status}</td><td>{service.latencyMs}ms</td></tr>)}
        </tbody></table></div>
      </Section>
    </>
  );
}
