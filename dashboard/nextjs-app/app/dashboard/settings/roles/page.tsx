import { SettingsForm } from "@/components/dashboard/settings-form";

export default function RolesSettingsPage() {
  return (
    <SettingsForm
      title="Roles Settings"
      endpoint="/api/dashboard/settings/roles"
      fields={[
        { key: "joinRole", label: "Join Role", type: "text", value: "Community" },
        { key: "reactionMode", label: "Reaction Role Mode", type: "select", value: "Single", options: ["Single", "Multiple"] },
        { key: "requireVerification", label: "Require Verification", type: "toggle", value: true },
        { key: "syncExternal", label: "Sync External Membership", type: "toggle", value: false },
      ]}
    />
  );
}
