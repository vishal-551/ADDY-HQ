import { SettingsForm } from "@/components/dashboard/settings-form";

export default function LoggingSettingsPage() {
  return (
    <SettingsForm
      title="Logging Settings"
      endpoint="/api/dashboard/settings/logging"
      fields={[
        { key: "loggingEnabled", label: "Enable Logging", type: "toggle", value: true },
        { key: "channel", label: "Logging Channel", type: "text", value: "#audit-log" },
        { key: "retention", label: "Retention (days)", type: "number", value: 30 },
        { key: "includeEdits", label: "Track Message Edits", type: "toggle", value: true },
      ]}
    />
  );
}
