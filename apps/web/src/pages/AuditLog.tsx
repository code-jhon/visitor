// VIS-4 Audit log — styled viewer inside the app shell (fix/styling).
import { FormEvent, useEffect, useState } from "react";
import { AppShell, Badge } from "../components/AppShell";
import { listAuditLogs, AuditEntry } from "../features/audit/api";

const DEMO: AuditEntry[] = [
  { id: "1", actor_user_id: "sarah", action: "visit.completed", entity_type: "visit", entity_id: "1842", before: "in_progress", after: "completed", created_at: "Jun 18, 2026 09:15" },
  { id: "2", actor_user_id: "carlos", action: "patient.update", entity_type: "patient", entity_id: "ET-01", before: "—", after: "address", created_at: "Jun 18, 2026 08:40" },
  { id: "3", actor_user_id: "system", action: "visit.auto_closed", entity_type: "visit", entity_id: "1839", before: "in_progress", after: "completed", created_at: "Jun 17, 2026 23:02" },
];

export function AuditLog(): JSX.Element {
  const [rows, setRows] = useState<AuditEntry[]>(DEMO);
  const [entity, setEntity] = useState("");

  useEffect(() => {
    listAuditLogs().then((r) => r.length && setRows(r)).catch(() => undefined);
  }, []);

  function onFilter(e: FormEvent): void {
    e.preventDefault();
    listAuditLogs(entity || undefined).then((r) => setRows(r)).catch(() => undefined);
  }

  return (
    <AppShell title="Audit Log" subtitle="Immutable trail of data changes and visit events">
      <form onSubmit={onFilter} className="flex gap-8" style={{ marginBottom: 16 }}>
        <div className="search" style={{ background: "#fff", border: "1px solid var(--border-strong)" }}>
          <input placeholder="Filter by entity type (e.g. visit)…" value={entity} onChange={(e) => setEntity(e.target.value)} />
        </div>
        <button className="btn">Filter</button>
      </form>
      <div className="card">
        <table className="table">
          <thead><tr><th>When</th><th>Actor</th><th>Action</th><th>Entity</th><th>Before → After</th></tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td className="muted">{r.created_at}</td>
                <td>{r.actor_user_id ?? "system"}</td>
                <td><Badge kind="blue">{r.action}</Badge></td>
                <td className="muted">{r.entity_type} {r.entity_id}</td>
                <td className="muted">{(r.before || "—") + " → " + (r.after || "—")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AppShell>
  );
}
