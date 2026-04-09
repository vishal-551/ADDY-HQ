import { DashboardPageFrame } from "@/components/dashboard/page-frame";

export default function AdminRevenuePage() {
  return (
    <DashboardPageFrame
      title="Admin Revenue"
      subtitle="Platform-wide controls for revenue."
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
