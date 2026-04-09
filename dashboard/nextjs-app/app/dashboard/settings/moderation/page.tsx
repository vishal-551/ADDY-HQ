import { SettingsForm } from "@/components/dashboard/settings-form";

export default function ModerationSettingsPage() {
  return (
    <SettingsForm
      title="Moderation Settings"
      endpoint="/api/dashboard/settings/moderation"
      fields={[
        { key: "modLogChannel", label: "Mod Log Channel", type: "text", value: "#mod-logs" },
        { key: "warnLimit", label: "Warn Limit", type: "number", value: 3 },
        { key: "muteDuration", label: "Default Mute (minutes)", type: "number", value: 30 },
        { key: "autoEscalate", label: "Auto Escalation", type: "toggle", value: true },
      ]}
    />
  );
}
