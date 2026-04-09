import Link from "next/link";

const docsSections = [
  { title: "Getting Started", description: "Invite Addy, select a guild, and activate your first module.", href: "/invite" },
  { title: "Module Registry", description: "Understand free and premium modules and their capabilities.", href: "/dashboard/modules" },
  { title: "Admin Controls", description: "Run platform operations with audit-safe controls.", href: "/dashboard/admin" },
];

export default function DocsPage() {
  return (
    <section className="section">
      <h1>Addy Documentation</h1>
      <p className="muted">Official usage guides for users, moderators, and platform admins.</p>
      <div className="grid grid-3">
        {docsSections.map((section) => (
          <article key={section.title} className="card">
            <h3>{section.title}</h3>
            <p className="muted">{section.description}</p>
            <Link href={section.href} className="btn btn-dark">Open</Link>
          </article>
        ))}
      </div>
    </section>
  );
}
