// VIS-7 — Patients module API client (search + calendar). Sensitive fields are
// masked server-side based on the caller's role.
import { apiFetch } from "../../api/client";

export interface Patient {
  id: string;
  client_id: string | null;
  first_name: string;
  last_name: string;
  document_id: string;
  birth_date: string | null;
  address: string;
  medical_notes: string;
}

export interface CalendarEntry {
  visit_id: string;
  status: string;
  scheduled_start: string | null;
  scheduled_end: string | null;
  address: string;
}

export async function searchPatients(q?: string): Promise<Patient[]> {
  const qs = new URLSearchParams();
  if (q) qs.set("q", q);
  const res = await apiFetch(`/patients/search?${qs.toString()}`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as Patient[];
}

export async function getCalendar(id: string): Promise<CalendarEntry[]> {
  const res = await apiFetch(`/patients/${id}/calendar`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return ((await res.json()) as { visits: CalendarEntry[] }).visits;
}
