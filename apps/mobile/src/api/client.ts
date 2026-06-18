import { tokenStorage } from "./secureStore";

const BASE_URL = process.env.API_BASE_URL ?? "http://localhost:8000";

const ACCESS_KEY = "visitor.access";
const REFRESH_KEY = "visitor.refresh";

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

export async function setTokens(tokens: Tokens | null): Promise<void> {
  if (tokens) {
    await tokenStorage.set(ACCESS_KEY, tokens.access_token);
    await tokenStorage.set(REFRESH_KEY, tokens.refresh_token);
  } else {
    await tokenStorage.remove(ACCESS_KEY);
    await tokenStorage.remove(REFRESH_KEY);
  }
}

async function refreshAccessToken(): Promise<boolean> {
  const refresh = await tokenStorage.get(REFRESH_KEY);
  if (!refresh) return false;
  const res = await fetch(`${BASE_URL}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refresh }),
  });
  if (!res.ok) {
    await setTokens(null);
    return false;
  }
  await setTokens((await res.json()) as Tokens);
  return true;
}

/** fetch wrapper that attaches the bearer token and retries once after refresh. */
export async function apiFetch(
  path: string,
  init: RequestInit = {},
  retry = true,
): Promise<Response> {
  const access = await tokenStorage.get(ACCESS_KEY);
  const headers = new Headers(init.headers);
  if (access) headers.set("Authorization", `Bearer ${access}`);
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
    body: body.toString(),
  });
  if (!res.ok) throw new Error("invalid_credentials");
  const tokens = (await res.json()) as Tokens;
  await setTokens(tokens);
  return tokens;
}

export async function getMe(): Promise<CurrentUser> {
  const res = await apiFetch("/users/me");
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as CurrentUser;
}

export async function logout(): Promise<void> {
  await setTokens(null);
}
