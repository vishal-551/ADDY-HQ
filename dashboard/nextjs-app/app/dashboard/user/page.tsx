import { Kpi } from "@/components/cards";
import { Section, TinyChart } from "@/components/ui";
import { fetchPreview } from "@/lib/api";

type UserData = {
  user: { name: string; plan: string; email: string };
  guilds: { id: string; name: string; members: number; health: string }[];
  overview: Record<string, number>;
  settings: {
    welcome: Record<string, string | number | boolean>;
    moderation: Record<string, string | number | boolean>;
    automod: Record<string, string | number | boolean>;
    ai: Record<string, string | number | boolean>;
    youtube: Record<string, string | number | boolean>;
    levels: Record<string, string | number | boolean>;
    tickets: Record<string, string | number | boolean>;
  };
  analytics: { messages: number[]; retention: number[] };
  premium: { status: string; renewalDate: string; lockedModules: string[] };
};

function SettingsCard({ title, values }: { title: string; values: Record<string, string | number | boolean> }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <div className="form">
        {Object.entries(values).map(([key, value]) => (
          <label key={key}>
            {key}
            <input className="input" defaultValue={`${value}`} />
          </label>
        ))}
        <button className="btn btn-dark">Save {title}</button>
      </div>
    </div>
  );
}

export default async function UserDashboardPage() {
  const data = await fetchPreview<UserData>("/api/preview/user");

  return (
    <>
      <Section title="User dashboard preview" subtitle={`${data.user.name} • ${data.user.email} • ${data.user.plan}`}>
        <div className="grid grid-2">
          {Object.entries(data.overview).map(([label, value]) => (
            <Kpi key={label} label={label} value={value} />
          ))}
        </div>
      </Section>

      <Section title="Guild list + guild overview">
        <div className="card">
          <table className="table">
            <thead><tr><th>Guild</th><th>Members</th><th>Health</th><th>Action</th></tr></thead>
            <tbody>
              {data.guilds.map((guild) => (
                <tr key={guild.id}><td>{guild.name}</td><td>{guild.members}</td><td>{guild.health}</td><td><button className="btn">Manage</button></td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="Settings preview: welcome, moderation, automod, ai, youtube, levels, tickets">
        <div className="grid grid-2">
          <SettingsCard title="Welcome settings" values={data.settings.welcome} />
          <SettingsCard title="Moderation settings" values={data.settings.moderation} />
          <SettingsCard title="Automod settings" values={data.settings.automod} />
          <SettingsCard title="AI settings" values={data.settings.ai} />
          <SettingsCard title="YouTube settings" values={data.settings.youtube} />
          <SettingsCard title="Levels settings" values={data.settings.levels} />
          <SettingsCard title="Tickets settings" values={data.settings.tickets} />
        </div>
      </Section>

      <Section title="Analytics">
        <div className="grid grid-2">
          <div className="card"><p className="muted">Messages / day</p><TinyChart points={data.analytics.messages} /></div>
          <div className="card"><p className="muted">Retention %</p><TinyChart points={data.analytics.retention} color="#4be4c8" /></div>
        </div>
      </Section>

      <Section title="Premium page">
        <div className="card">
          <h3>Status: {data.premium.status}</h3>
          <p className="muted">Renewal date: {data.premium.renewalDate}</p>
          <p>Locked modules</p>
          <ul>{data.premium.lockedModules.map((item) => <li key={item}>{item}</li>)}</ul>
          <button className="btn btn-primary">Upgrade Premium</button>
        </div>
      </Section>
    </>
  );
}
