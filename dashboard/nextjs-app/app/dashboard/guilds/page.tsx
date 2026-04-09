import { DashboardPageFrame } from "@/components/dashboard/page-frame";

export default function GuildsPage() {
  return (
    <DashboardPageFrame
      title="Guilds"
      subtitle="Manage guilds for the selected guild."
      stats={[
        { label: "Total", value: "128" },
        { label: "Active", value: "104" },
        { label: "Pending", value: "18" },
        { label: "Alerts", value: "6" },
      ]}
      rows={[
        ["Primary", "42", "19", "Healthy"],
        ["Secondary", "31", "15", "Healthy"],
        ["Review Queue", "9", "4", "Needs Review"],
      ]}
    />
  );
}
