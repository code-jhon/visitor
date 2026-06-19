// VIS-5 — Dashboard module API client.
import { apiFetch } from "../../api/client";

export interface DashboardSummary {
  total_visits: number;
  by_status: Record<string, number>;
  today_agenda: number;
  unassigned: number;
  active: number;
}

export async function getSummary(): Promise<DashboardSummary> {
  const res = await apiFetch("/dashboard/summary");
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as DashboardSummary;
}
