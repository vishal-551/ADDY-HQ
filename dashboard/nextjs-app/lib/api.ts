const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type ApiResponse<T> = {
  ok: boolean;
  data: T;
  message?: string;
};

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: Record<string, unknown>;
  headers?: Record<string, string>;
};

export type GuildSummary = {
  id: number;
  name: string;
  icon?: string | null;
  owner_discord_id: number;
};

export type CurrentUser = {
  id: number;
  discord_id: number;
  username: string;
  email?: string | null;
  is_admin: boolean;
};

export type GuildModuleCard = {
  key: string;
  icon: string;
  title: string;
  description: string;
  tier: "free" | "premium";
  enabled: boolean;
  connected: boolean;
  available: boolean;
  invite_url: string;
  manage_url: string;
};

export async function fetchPreview<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error(`Failed request: ${path}`);
  }

  const payload = (await response.json()) as ApiResponse<T>;
  return payload.data;
}

export async function requestApi<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: options.method ?? "GET",
    cache: "no-store",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

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

export async function saveDashboardSettings<T extends Record<string, unknown>>(path: string, payload: T): Promise<{ ok: boolean; data?: { savedAt: string }; message?: string }> {
  try {
    const response = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
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
