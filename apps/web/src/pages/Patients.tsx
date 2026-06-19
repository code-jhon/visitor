// VIS-7 Patients — styled list matching the web_screens mockup.
// Component normalization: the table now consumes the live patients feature API
// (server-side search with role-masked notes) with the demo dataset as an
// offline fallback. The search box is functional and rows link to the detail view.
import { FormEvent, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { AppShell, Badge } from "../components/AppShell";
import { IconFilter, IconPlus } from "../components/icons";
import { colorFor, initials, patients } from "../data/demo";
import { Patient, searchPatients } from "../features/patients/api";

// Unified row view-model shared by the demo seed and API-mapped rows.
interface PatientRow {
  id: string;
  name: string;
  age: number | string;
  contact: string;
  service: string;
  last: string;
  status: string;
  badge: string;
}

const ageFrom = (birth: string | null): number | string => {
  if (!birth) return "—";
  const d = new Date(birth);
  if (Number.isNaN(d.getTime())) return "—";
  return Math.floor((Date.now() - d.getTime()) / 3.15576e10);
};

const toRow = (p: Patient): PatientRow => ({
  id: p.id,
  name: `${p.first_name} ${p.last_name}`.trim() || p.document_id,
  age: ageFrom(p.birth_date),
  contact: p.document_id || p.address || "—",
  service: "—",
  last: "—",
  status: "Active",
  badge: "green",
});

const demoRows: PatientRow[] = patients.map((p) => ({
  id: p.name.toLowerCase().replace(/\s+/g, "-"),
  name: p.name, age: p.age, contact: p.contact, service: p.service,
  last: p.last, status: p.status, badge: p.badge,
}));

export function Patients(): JSX.Element {
  const [rows, setRows] = useState<PatientRow[]>(demoRows);
  const [q, setQ] = useState("");

  // Load live patients on mount; keep the demo seed when the API is offline.
  useEffect(() => {
    searchPatients().then((r) => r.length && setRows(r.map(toRow))).catch(() => undefined);
  }, []);

  function onSearch(e: FormEvent): void {
    e.preventDefault();
    searchPatients(q || undefined).then((r) => setRows(r.map(toRow))).catch(() => undefined);
  }

  // Client-side filtering keeps search responsive even on the demo seed.
  const visible = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return needle ? rows.filter((r) => r.name.toLowerCase().includes(needle)) : rows;
  }, [rows, q]);

  return (
    <AppShell
      title="Patients"
      subtitle={`${rows.length} patients`}
      search="Search patients…"
      actions={
        <>
          <button className="btn"><IconFilter /> Filters</button>
          <button className="btn btn-primary"><IconPlus /> Add Patient</button>
        </>
      }
    >
      <form onSubmit={onSearch} className="flex gap-8" style={{ marginBottom: 14 }}>
        <div className="search" style={{ background: "#fff", border: "1px solid var(--border-strong)" }}>
          <input placeholder="Search by patient name…" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
        <button className="btn">Search</button>
      </form>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Patient</th><th>Age</th><th>Contact</th><th>Service</th><th>Last Visit</th><th>Status</th><th></th>
            </tr>
          </thead>
          <tbody>
            {visible.map((p) => (
              <tr key={p.id}>
                <td>
                  <Link to={`/patients/${p.id}`} className="person">
                    <span className={`ava-sm ${colorFor(p.name)}`}>{initials(p.name)}</span>
                    <span className="person-name">{p.name}</span>
                  </Link>
                </td>
                <td className="muted">{p.age}</td>
                <td className="muted">{p.contact}</td>
                <td>{p.service}</td>
                <td className="muted">{p.last}</td>
                <td><Badge kind={p.badge}>{p.status}</Badge></td>
                <td className="right"><span className="row-actions">···</span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="pagination" style={{ padding: "14px 16px" }}>
          <span>Showing {visible.length} of {rows.length} patients</span>
          <div className="pager">
            <button>‹</button><button className="active">1</button><button>2</button><button>3</button>
            <span style={{ color: "var(--text-faint)" }}>…</span><button>24</button><button>›</button>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
