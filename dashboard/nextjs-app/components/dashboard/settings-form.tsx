"use client";

import { useState } from "react";
import { saveDashboardSettings } from "@/lib/api";

type Field = {
  key: string;
  label: string;
  type: "text" | "number" | "select" | "toggle";
  value: string | number | boolean;
  options?: string[];
};

export function SettingsForm({
  title,
  endpoint,
  fields,
}: {
  title: string;
  endpoint: string;
  fields: Field[];
}) {
  const [values, setValues] = useState<Record<string, string | number | boolean>>(
    Object.fromEntries(fields.map((field) => [field.key, field.value])),
  );
  const [status, setStatus] = useState<string>("");

  async function onSave() {
    setStatus("Saving...");
    const result = await saveDashboardSettings(endpoint, values);
    setStatus(result.ok ? `Saved: ${result.data.savedAt}` : result.message ?? "Save failed");
  }

  return (
    <section className="card settings-card">
      <h2>{title}</h2>
      <div className="form">
        {fields.map((field) => {
          if (field.type === "select") {
            return (
              <label key={field.key}>
                {field.label}
                <select
                  className="input"
                  value={String(values[field.key])}
                  onChange={(event) => setValues((prev) => ({ ...prev, [field.key]: event.target.value }))}
                >
                  {(field.options ?? []).map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>
            );
          }

          if (field.type === "toggle") {
            return (
              <label key={field.key} className="toggle-row">
                <span>{field.label}</span>
                <button
                  type="button"
                  className={`toggle ${values[field.key] ? "enabled" : ""}`}
                  onClick={() => setValues((prev) => ({ ...prev, [field.key]: !Boolean(prev[field.key]) }))}
                >
                  <span className="knob" />
                </button>
              </label>
            );
          }

          return (
            <label key={field.key}>
              {field.label}
              <input
                className="input"
                type={field.type}
                value={String(values[field.key])}
                onChange={(event) =>
                  setValues((prev) => ({
                    ...prev,
                    [field.key]: field.type === "number" ? Number(event.target.value) : event.target.value,
                  }))
                }
              />
            </label>
          );
        })}
      </div>
      <div className="row gap">
        <button className="btn btn-primary" type="button" onClick={onSave}>
          Save Changes
        </button>
        {status ? <span className="muted">{status}</span> : null}
      </div>
    </section>
  );
}
