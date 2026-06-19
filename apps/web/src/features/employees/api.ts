// VIS-6 — Employees module API client (search + availability).
import { apiFetch } from "../../api/client";

export interface Employee {
  id: string;
  first_name: string;
  last_name: string;
  document_id: string;
  email: string;
  phone: string;
  position: string;
  is_active: boolean;
}

export interface Availability {
  employee_id: string;
  is_active: boolean;
  available: boolean;
  busy_slots: {
    visit_id: string;
    scheduled_start: string | null;
    scheduled_end: string | null;
    status: string;
  }[];
}

export async function searchEmployees(params: {
  q?: string;
  document_id?: string;
  is_active?: boolean;
}): Promise<Employee[]> {
  const qs = new URLSearchParams();
  if (params.q) qs.set("q", params.q);
  if (params.document_id) qs.set("document_id", params.document_id);
  if (params.is_active !== undefined) qs.set("is_active", String(params.is_active));
  const res = await apiFetch(`/employees/search?${qs.toString()}`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as Employee[];
}

export async function getAvailability(id: string): Promise<Availability> {
  const res = await apiFetch(`/employees/${id}/availability`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as Availability;
}
