// Auth session store (VIS-2). A minimal observable store keeps the current
// user in memory and notifies subscribers on sign-in/out. Redux Toolkit or
// Zustand can replace this without changing the public API (see VIS-1 §3).
import {
  CurrentUser,
  getMe,
  login as apiLogin,
  logout as apiLogout,
} from "../api/client";

export interface AuthState {
  user: CurrentUser | null;
  status: "anonymous" | "authenticating" | "authenticated";
}

let state: AuthState = { user: null, status: "anonymous" };
const listeners = new Set<(s: AuthState) => void>();

function setState(next: Partial<AuthState>): void {
  state = { ...state, ...next };
  listeners.forEach((l) => l(state));
}

export function getAuthState(): AuthState {
  return state;
}

export function subscribe(listener: (s: AuthState) => void): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export async function signIn(email: string, password: string): Promise<void> {
  setState({ status: "authenticating" });
  try {
    await apiLogin(email, password);
    const user = await getMe();
    setState({ user, status: "authenticated" });
  } catch (err) {
    setState({ user: null, status: "anonymous" });
    throw err;
  }
}

export function signOut(): void {
  apiLogout();
  setState({ user: null, status: "anonymous" });
}

export function hasRole(role: string): boolean {
  return state.user?.roles.some((r) => r.name === role) ?? false;
}
