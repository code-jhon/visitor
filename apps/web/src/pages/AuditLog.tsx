// VIS-4 — Audit log viewer: immutable trail of data changes and visit-lifecycle
// events, filterable by entity. Visible only to Admin/Soporte (enforced by the
// audit:read permission server-side).
import { FormEvent, useEffect, useState } from "react";
import { AuditEntry, listAuditLogs } from "../features/audit/api";

export function AuditLog(): JSX.Element {
  const [rows, setRows] = useState<AuditEntry[]>([]);
  const [entity, setEntity] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function load(e = ""): Promise<void> {
    try {
      setRows(await listAuditLogs(e || undefined));
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  function onFilter(ev: FormEvent): void {
    ev.preventDefault();
    void load(entity);
  }

  return (
    <section>
      <h2>Audit log</h2>
      <form onSubmit={onFilter} role="search">
        <input
          aria-label="Filter by entity type"
          placeholder="Entity type (e.g. visit)…"
          value={entity}
          onChange={(e) => setEntity(e.target.value)}
        />
        <button type="submit">Filter</button>
      </form>
      {error && <p role="alert">Could not load audit log: {error}</p>}
      <table>
        <thead>
          <tr>
            <th>When</th>
            <th>Actor</th>
            <th>Action</th>
            <th>Entity</th>
            <th>Before → After</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td>{r.created_at}</td>
              <td>{r.actor_user_id ?? "system"}</td>
              <td>{r.action}</td>
              <td>
                {r.entity_type} {r.entity_id}
              </td>
              <td>
                {(r.before || "—") + " → " + (r.after || "—")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
