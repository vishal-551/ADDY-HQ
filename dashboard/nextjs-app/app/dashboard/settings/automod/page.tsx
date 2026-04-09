import { SettingsForm } from "@/components/dashboard/settings-form";

export default function AutomodSettingsPage() {
  return (
    <SettingsForm
      title="Auto Moderation Settings"
      endpoint="/api/dashboard/settings/automod"
      fields={[
        { key: "spamProtection", label: "Spam Protection", type: "toggle", value: true },
        { key: "raidProtection", label: "Raid Protection", type: "toggle", value: true },
        { key: "linkFilter", label: "Link Filter", type: "select", value: "Strict", options: ["Off", "Balanced", "Strict"] },
        { key: "capsThreshold", label: "Caps Threshold %", type: "number", value: 75 },
      ]}
    />
  );
}
