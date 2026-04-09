import { SettingsForm } from "@/components/dashboard/settings-form";

export default function TicketsSettingsPage() {
  return (
    <SettingsForm
      title="Tickets Settings"
      endpoint="/api/preview/settings/tickets"
      fields={[
        { key: "enabled", label: "Enabled", type: "toggle", value: true },
        { key: "channel", label: "Target Channel", type: "text", value: "#general" },
        { key: "mode", label: "Mode", type: "text", value: "balanced" },
      ]}
    />
  );
}
