// VIS-6 Employees — styled card grid matching the web_screens mockup.
// Component normalization: the view now consumes the live employees feature API
// (search + active filter) with the demo dataset as an offline fallback, instead
// of rendering a purely static list. Search and tab filters are functional.
import { FormEvent, useEffect, useMemo, useState } from "react";
import { AppShell } from "../components/AppShell";
import { IconFilter, IconPhone, IconPlus, IconShield } from "../components/icons";
import { colorFor, employees, employeeTabs, initials } from "../data/demo";
import { Employee, searchEmployees } from "../features/employees/api";

// Unified card view-model shared by the demo seed and API-mapped rows.
interface EmpCard {
  name: string;
  role: string;
  status: string;
  st: string;
  patients: number | string;
  visits: string;
  phone: string;
  cert: string;
}

const toCard = (e: Employee): EmpCard => ({
  name: `${e.first_name} ${e.last_name}`.trim() || e.email,
  role: e.position || "—",
  status: e.is_active ? "Active" : "Inactive",
  st: e.is_active ? "green" : "gray",
  patients: "—",
  visits: "—",
  phone: e.phone || "—",
  cert: e.email || "—",
});

// Active vs off-duty grouping so the tabs filter both API and demo rows.
const groupOf = (c: EmpCard): "active" | "off" => (c.st === "gray" || c.st === "amber" ? "off" : "active");
const TAB_GROUP: Record<string, "all" | "active" | "off"> = {
  "All Employees": "all", "On Duty": "active", "Available": "active",
  "Off Duty": "off", "On Leave": "off",
};

export function Employees(): JSX.Element {
  const [cards, setCards] = useState<EmpCard[]>(employees);
  const [active, setActive] = useState("All Employees");
  const [q, setQ] = useState("");

  // Load live employees on mount; keep the demo seed when the API is offline.
  useEffect(() => {
    searchEmployees({}).then((r) => r.length && setCards(r.map(toCard))).catch(() => undefined);
  }, []);

  function onSearch(e: FormEvent): void {
    e.preventDefault();
    const isActive = TAB_GROUP[active] === "all" ? undefined : TAB_GROUP[active] === "active";
    searchEmployees({ q: q || undefined, is_active: isActive })
      .then((r) => setCards(r.map(toCard)))
      .catch(() => undefined);
  }

  // Client-side filtering keeps search/tabs responsive even on the demo seed.
  const visible = useMemo(() => {
    const group = TAB_GROUP[active] ?? "all";
    const needle = q.trim().toLowerCase();
    return cards.filter((c) =>
      (group === "all" || groupOf(c) === group) &&
      (!needle || c.name.toLowerCase().includes(needle) || c.role.toLowerCase().includes(needle)),
    );
  }, [cards, active, q]);

  return (
    <AppShell
      title="Employees"
      subtitle={`${cards.length} caregivers and staff members`}
      search="Search employees…"
      actions={
        <>
          <button className="btn"><IconFilter /> Filters</button>
          <button className="btn btn-primary"><IconPlus /> Add Employee</button>
        </>
      }
    >
      <form onSubmit={onSearch} className="flex gap-8" style={{ marginBottom: 14 }}>
        <div className="search" style={{ background: "#fff", border: "1px solid var(--border-strong)" }}>
          <input placeholder="Search by name or position…" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
        <button className="btn">Search</button>
      </form>

      <div className="tabs" style={{ marginBottom: 18 }}>
        {employeeTabs.map((t) => (
          <button key={t.label} className={`tab${active === t.label ? " active" : ""}`} onClick={() => setActive(t.label)}>
            {t.label} <span className="tab-count">{t.count}</span>
          </button>
        ))}
      </div>

      {visible.length === 0
        ? <div className="card card-pad person-sub">No employees match your search.</div>
        : (
          <div className="grid grid-3">
            {visible.map((e) => (
              <div key={e.name} className="card emp-card">
                <div className="emp-head">
                  <div className="person">
                    <span className={`ava-sm ${colorFor(e.name)}`} style={{ width: 42, height: 42, flexBasis: 42, fontSize: 14 }}>{initials(e.name)}</span>
                    <div>
                      <div className="person-name">{e.name}</div>
                      <div className="person-sub">{e.role}</div>
                    </div>
                  </div>
                  <span className={`status-text ${e.st === "blue" ? "green" : e.st === "gray" ? "amber" : e.st}`} style={e.st === "gray" ? { color: "var(--text-faint)" } : {}}>
                    <span className={`dot ${e.st === "gray" ? "amber" : e.st}`} style={e.st === "gray" ? { background: "#cbd5e1" } : {}} />{e.status}
                  </span>
                </div>
                <div className="emp-stats">
                  <div className="emp-stat"><div className="lbl">Patients</div><div className="val">{e.patients}</div></div>
                  <div className="emp-stat"><div className="lbl">Visits</div><div className="val">{e.visits}</div></div>
                </div>
                <div className="emp-foot">
                  <span><IconPhone style={{ width: 14, height: 14 }} /> {e.phone}</span>
                  <span><IconShield style={{ width: 14, height: 14 }} /> {e.cert}</span>
                </div>
              </div>
            ))}
          </div>
        )}
    </AppShell>
  );
}
