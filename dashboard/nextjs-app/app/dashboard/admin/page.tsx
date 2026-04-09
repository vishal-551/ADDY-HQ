import { AreaChart } from "@/components/dashboard/charts";
import { DashboardTable, StatCard } from "@/components/dashboard/ui";
import { fetchWithFallback } from "@/lib/api";

type AdminPayload = {
  health: { service: string; status: string; latency: string }[];
};

const fallback: AdminPayload = {
  health: [
    { service: "API Gateway", status: "Operational", latency: "112ms" },
    { service: "Discord Worker", status: "Operational", latency: "86ms" },
    { service: "Billing", status: "Degraded", latency: "283ms" },
  ],
};

export default async function AdminDashboardPage() {
  const data = await fetchWithFallback<AdminPayload>("/api/dashboard/admin", fallback);

  return (
    <div className="dash-main-grid">
      <section className="grid grid-4">
        <StatCard title="Managed bots" value="27" trend="+2 this month" />
        <StatCard title="Premium guilds" value="2,431" trend="+8.4%" />
        <StatCard title="Customers" value="15,210" trend="+5.1%" />
        <StatCard title="MRR" value="$84,900" trend="+11.8%" />
      </section>

      <section className="grid grid-2">
        <article>
          <h3>Bots management</h3>
          <DashboardTable
            columns={["Bot", "Version", "Cluster", "Status"]}
            rows={[["Addy Core", "2.8.1", "us-east-1", "Healthy"], ["Addy Music", "1.9.4", "us-west-2", "Healthy"], ["Addy Support", "1.3.2", "eu-central-1", "Updating"]]}
          />
        </article>
        <article>
          <h3>Module control</h3>
          <DashboardTable
            columns={["Module", "Tier", "Guilds", "Action"]}
            rows={[["AI Moderation", "Premium", "1,184", "Manage"], ["Tickets", "Premium", "692", "Manage"], ["Welcome", "Free", "8,321", "Manage"]]}
          />
        </article>
      </section>

      <section className="grid grid-2">
        <article>
          <h3>Premium management / customers</h3>
          <DashboardTable
            columns={["Customer", "Plan", "Guilds", "Renewal"]}
            rows={[["Nebula Studios", "Enterprise", "12", "2026-05-10"], ["Arc Labs", "Pro", "4", "2026-04-28"], ["LimeVerse", "Pro", "3", "2026-04-19"]]}
          />
        </article>
        <article className="card">
          <h3>Revenue trend</h3>
          <AreaChart points={[30, 36, 41, 44, 49, 57, 60, 64, 71, 75, 78]} color="#8a7dff" />
        </article>
      </section>

      <section className="grid grid-2">
        <article>
          <h3>Audit logs</h3>
          <DashboardTable
            columns={["Time", "Actor", "Action", "Result"]}
            rows={[["14:44", "System", "Redeploy workers", "Success"], ["14:12", "Ops", "Rotate API keys", "Success"], ["13:51", "Billing", "Retry failed invoice", "Queued"]]}
          />
        </article>
        <article>
          <h3>Offers & promo codes</h3>
          <DashboardTable
            columns={["Offer", "Code", "Usage", "Expires"]}
            rows={[["Spring 25%", "ADDYSPRING", "421", "2026-05-01"], ["AI Upgrade 15%", "AIGUARD", "211", "2026-04-22"], ["Community 10%", "COMMUNITY10", "684", "2026-06-15"]]}
          />
        </article>
      </section>

      <section>
        <h3>System health</h3>
        <DashboardTable
          columns={["Service", "Status", "Latency"]}
          rows={data.health.map((item) => [item.service, item.status, item.latency])}
        />
      </section>
    </div>
  );
}
