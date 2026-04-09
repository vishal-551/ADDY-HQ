import { DashboardPageFrame } from "@/components/dashboard/page-frame";

export default function AdminBroadcastsPage() {
  return (
    <DashboardPageFrame
      title="Admin Broadcasts"
      subtitle="Platform-wide controls for broadcasts."
      stats={[
        { label: "Managed", value: "248" },
        { label: "Active", value: "221" },
        { label: "Queued", value: "14" },
        { label: "Errors", value: "2" },
      ]}
      rows={[
        ["Global", "92", "41", "Operational"],
        ["North America", "80", "34", "Operational"],
        ["Europe", "76", "30", "Monitoring"],
      ]}
    />
  );
}
