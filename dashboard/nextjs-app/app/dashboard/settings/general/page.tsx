import { SettingsForm } from "@/components/dashboard/settings-form";

export default function GeneralSettingsPage() {
  return (
    <SettingsForm
      title="General Settings"
      endpoint="/api/dashboard/settings/general"
      fields={[
        { key: "prefix", label: "Bot Prefix", type: "text", value: "!" },
        { key: "language", label: "Language", type: "select", value: "English", options: ["English", "Spanish", "German"] },
        { key: "timezone", label: "Timezone", type: "select", value: "UTC", options: ["UTC", "US/Eastern", "US/Pacific"] },
        { key: "allowDmCommands", label: "Allow DM Commands", type: "toggle", value: true },
      ]}
    />
  );
}
