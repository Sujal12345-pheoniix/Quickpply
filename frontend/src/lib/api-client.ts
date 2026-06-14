const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function getToken(): Promise<string | null> {
  if (typeof window === "undefined") return null;
  // Clerk session token injected by useAuth in components
  return null;
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = await getToken();
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: response.statusText }));
    throw new ApiError(response.status, error.message ?? "Request failed");
  }

  return response.json();
}

export const api = {
  auth: {
    me: () => apiFetch<{ id: string; email: string }>("/auth/me"),
  },
  jobs: {
    list: (params?: Record<string, string>) =>
      apiFetch(`/jobs?${new URLSearchParams(params ?? {})}`),
    discover: () => apiFetch("/jobs/discover", { method: "POST" }),
  },
  applications: {
    generate: (jobId: string) =>
      apiFetch("/applications/generate", {
        method: "POST",
        body: JSON.stringify({ job_id: jobId }),
      }),
    approve: (id: string) =>
      apiFetch(`/applications/${id}/approve`, { method: "POST" }),
  },
};
