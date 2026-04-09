"use client";

import { FormEvent, useState } from "react";
import { demoLogin } from "@/lib/api";

export default function LoginPage() {
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState(false);

  async function handleDemoLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await demoLogin();
      setResult(`${response.message} — ${response.data.user.name} (${response.data.user.plan})`);
    } catch (error) {
      setResult(error instanceof Error ? error.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="section">
      <h2>Login page</h2>
      <p className="muted">Demo auth is wired to backend endpoint /api/preview/auth/login.</p>
      <form className="card form" onSubmit={handleDemoLogin}>
        <label>
          Email
          <input className="input" type="email" defaultValue="aarav@addy.gg" />
        </label>
        <label>
          Password
          <input className="input" type="password" defaultValue="demo-password" />
        </label>
        <button className="btn btn-primary" type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Demo Login"}
        </button>
        {result ? <p>{result}</p> : null}
      </form>
    </section>
  );
}
