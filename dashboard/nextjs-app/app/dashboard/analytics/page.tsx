import { AreaChart, ActivityBars } from "@/components/dashboard/charts";
import { DashboardTable, StatCard } from "@/components/dashboard/ui";

const users = [
  ["Lumen", 9421, 312, "Verified"],
  ["ByteMage", 8362, 288, "Trusted"],
  ["NeonRift", 8034, 275, "Trusted"],
];

export default function AnalyticsPage() {
  return (
    <div className="dash-main-grid">
      <section className="grid grid-4">
        <StatCard title="Daily users" value="21,440" trend="+8.2%" />
        <StatCard title="Commands" value="44,301" trend="+11.0%" />
        <StatCard title="Reports" value="421" trend="-2.1%" />
        <StatCard title="Avg response" value="178ms" trend="-12ms" />
      </section>
      <section className="grid grid-2">
        <article className="card"><h3>User activity</h3><AreaChart points={[120, 132, 140, 167, 189, 175, 201, 223, 219, 248]} color="#4be4c8" /></article>
        <article className="card"><h3>Command activity</h3><ActivityBars points={[20, 35, 41, 55, 43, 50, 62, 71, 66, 73]} /></article>
      </section>
      <section>
        <h3>Top users</h3>
        <DashboardTable columns={["User", "Messages", "Commands", "Status"]} rows={users} />
      </section>
    </div>
  );
}
