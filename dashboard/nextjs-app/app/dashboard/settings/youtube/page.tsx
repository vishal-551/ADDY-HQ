import { SettingsForm } from "@/components/dashboard/settings-form";

export default function YoutubeSettingsPage() {
  return (
    <SettingsForm
      title="Youtube Settings"
      endpoint="/api/preview/settings/youtube"
      fields={[
        { key: "enabled", label: "Enabled", type: "toggle", value: true },
        { key: "channel", label: "Target Channel", type: "text", value: "#general" },
        { key: "mode", label: "Mode", type: "text", value: "balanced" },
      ]}
    />
  );
}
