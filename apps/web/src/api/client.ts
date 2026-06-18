const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface Health {
  status: string;
  environment: string;
}

export interface Tokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Role {
  id: string;
  name: string;
  description: string;
}

export interface CurrentUser {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  roles: Role[];
}

/**
 * In-memory token store (VIS-2). Tokens are never written to localStorage; the
 * production deployment uses httpOnly+secure cookies. A refresh callback lets
 * the interceptor transparently renew an expired access token once per request.
 */
let accessToken: string | null = null;
let refreshToken: string | null = null;

export function setTokens(tokens: Tokens | null): void {
  accessToken = tokens?.access_token ?? null;
  refreshToken = tokens?.refresh_token ?? null;
}

export function getAccessToken(): string | null {
  return accessToken;
}

async function refreshAccessToken(): Promise<boolean> {
  if (!refreshToken) return false;
  const res = await fetch(`${BASE_URL}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!res.ok) {
    setTokens(null);
    return false;
  }
  setTokens((await res.json()) as Tokens);
  return true;
}

/** fetch wrapper that attaches the bearer token and retries once after refresh. */
export async function apiFetch(
  path: string,
  init: RequestInit = {},
  retry = true,
): Promise<Response> {
  const headers = new Headers(init.headers);
  if (accessToken) headers.set("Authorization", `Bearer ${accessToken}`);
  const res = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  if (res.status === 401 && retry && (await refreshAccessToken())) {
    return apiFetch(path, init, false);
  }
  return res;
}

export async function getHealth(): Promise<Health> {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as Health;
}

export async function login(email: string, password: string): Promise<Tokens> {
  const body = new URLSearchParams({ username: email, password });
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!res.ok) throw new Error("invalid_credentials");
  const tokens = (await res.json()) as Tokens;
  setTokens(tokens);
  return tokens;
}

export async function getMe(): Promise<CurrentUser> {
  const res = await apiFetch("/users/me");
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as CurrentUser;
}

export function logout(): void {
  setTokens(null);
}
