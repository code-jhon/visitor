// VIS-6 Employees — styled card grid matching the web_screens mockup (fix/styling).
import { useState } from "react";
import { AppShell } from "../components/AppShell";
import { IconFilter, IconPhone, IconPlus, IconShield } from "../components/icons";
import { colorFor, employees, employeeTabs, initials } from "../data/demo";

export function Employees(): JSX.Element {
  const [active, setActive] = useState("All Employees");
  return (
    <AppShell
      title="Employees"
      subtitle="32 caregivers and staff members"
      search="Search employees…"
      actions={
        <>
          <button className="btn"><IconFilter /> Filters</button>
          <button className="btn btn-primary"><IconPlus /> Add Employee</button>
        </>
      }
    >
      <div className="tabs" style={{ marginBottom: 18 }}>
        {employeeTabs.map((t) => (
          <button key={t.label} className={`tab${active === t.label ? " active" : ""}`} onClick={() => setActive(t.label)}>
            {t.label} <span className="tab-count">{t.count}</span>
          </button>
        ))}
      </div>

      <div className="grid grid-3">
        {employees.map((e) => (
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
    </AppShell>
  );
}
