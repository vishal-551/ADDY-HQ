import { Section } from "@/components/ui";

export default function InvitePage() {
  return (
    <Section title="Invite/Add Bot page" subtitle="Connect Addy to your Discord guild instantly.">
      <div className="card form">
        <label>
          Discord Server
          <select defaultValue="Addy Community">
            <option>Addy Community</option>
            <option>Creator Hub</option>
            <option>Tech Syndicate</option>
          </select>
        </label>
        <label>
          Bot permissions preset
          <select defaultValue="Full Management">
            <option>Full Management</option>
            <option>Moderation only</option>
            <option>Welcome + Levels</option>
          </select>
        </label>
        <label>
          Setup note
          <input className="input" defaultValue="Enable onboarding and moderation modules" />
        </label>
        <div className="row gap">
          <button className="btn btn-primary">Invite Addy</button>
          <button className="btn">Save preset</button>
        </div>
      </div>
    </Section>
  );
}
