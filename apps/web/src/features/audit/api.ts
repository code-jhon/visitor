// VIS-4 — Audit log API client (read-only; Admin/Soporte).
import { apiFetch } from "../../api/client";

export interface AuditEntry {
  id: string;
  actor_user_id: string | null;
  action: string;
  entity_type: string;
  entity_id: string;
  before: string;
  after: string;
  created_at: string;
}

export async function listAuditLogs(entityType?: string): Promise<AuditEntry[]> {
  const qs = new URLSearchParams();
  if (entityType) qs.set("entity_type", entityType);
  const res = await apiFetch(`/audit-logs?${qs.toString()}`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as AuditEntry[];
}
