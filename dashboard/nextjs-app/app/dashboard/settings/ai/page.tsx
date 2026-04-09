import { SettingsForm } from "@/components/dashboard/settings-form";

export default function AISettingsPage() {
  return (
    <SettingsForm
      title="AI Moderation Settings"
      endpoint="/api/dashboard/settings/ai"
      fields={[
        { key: "aiEnabled", label: "Enable AI Moderation", type: "toggle", value: true },
        { key: "toxicitySensitivity", label: "Toxicity Sensitivity", type: "select", value: "High", options: ["Low", "Medium", "High"] },
        { key: "autoDelete", label: "Auto Delete Flagged Content", type: "toggle", value: true },
        { key: "escalationRole", label: "Escalation Role", type: "text", value: "@Moderators" },
      ]}
    />
  );
}
