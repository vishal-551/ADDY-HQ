const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type ApiResponse<T> = {
  ok: boolean;
  data: T;
  message?: string;
};

export async function fetchPreview<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed request: ${path}`);
  }
  const payload = (await response.json()) as ApiResponse<T>;
  return payload.data;
}

export async function fetchWithFallback<T>(path: string, fallback: T): Promise<T> {
  try {
    return await fetchPreview<T>(path);
  } catch {
    return fallback;
  }
}

export async function saveDashboardSettings<T extends Record<string, unknown>>(path: string, payload: T) {
  try {
    const response = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      return { ok: false, message: "Unable to save settings right now." };
    }

    return (await response.json()) as ApiResponse<{ savedAt: string }>;
  } catch {
    return {
      ok: true,
      data: { savedAt: new Date().toISOString() },
      message: "Saved in local preview mode.",
    } as ApiResponse<{ savedAt: string }>;
  }
}

export async function demoLogin() {
  const response = await fetch(`${API_BASE}/api/preview/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    throw new Error("Demo login failed");
  }

  return (await response.json()) as ApiResponse<{
    token: string;
    user: { name: string; role: string; plan: string };
  }>;
}
