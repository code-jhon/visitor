// VIS-10 — Scheduling module API client (calendar, lifecycle, availability).
import { apiFetch } from "../../api/client";

export type VisitStatus =
  | "scheduled"
  | "en_route"
  | "in_progress"
  | "completed"
  | "cancelled"
  | "no_show";

export interface Visit {
  id: string;
  client_id: string | null;
  patient_id: string | null;
  status: VisitStatus;
  scheduled_start: string | null;
  scheduled_end: string | null;
  address: string;
}

async function getJson<T>(path: string): Promise<T> {
  const res = await apiFetch(path);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as T;
}

export function getSchedule(filter?: { status?: VisitStatus }): Promise<Visit[]> {
  const qs = new URLSearchParams();
  if (filter?.status) qs.set("status", filter.status);
  return getJson(`/schedule?${qs.toString()}`);
}

export const getUnassigned = (): Promise<Visit[]> => getJson("/schedule/unassigned");

export async function transition(
  visitId: string,
  action: "start" | "finish" | "cancel" | "enroute" | "no-show",
): Promise<Visit> {
  const res = await apiFetch(`/visits/${visitId}/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: "{}",
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as Visit;
}
