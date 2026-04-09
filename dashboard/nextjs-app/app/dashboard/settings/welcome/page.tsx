import { SettingsForm } from "@/components/dashboard/settings-form";

export default function WelcomeSettingsPage() {
  return (
    <SettingsForm
      title="Welcome Settings"
      endpoint="/api/dashboard/settings/welcome"
      fields={[
        { key: "enabled", label: "Enable Welcome", type: "toggle", value: true },
        { key: "channel", label: "Welcome Channel", type: "text", value: "#welcome" },
        { key: "message", label: "Welcome Message", type: "text", value: "Welcome {user} to {server}!" },
        { key: "autoRole", label: "Auto Role", type: "text", value: "Member" },
      ]}
    />
  );
}
