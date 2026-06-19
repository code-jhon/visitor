// VIS-7 Patients — styled list matching the web_screens mockup (fix/styling).
import { Link } from "react-router-dom";
import { AppShell, Badge } from "../components/AppShell";
import { IconFilter, IconPlus } from "../components/icons";
import { colorFor, initials, patients } from "../data/demo";

export function Patients(): JSX.Element {
  return (
    <AppShell
      title="Patients"
      subtitle="186 active patients"
      search="Search patients…"
      actions={
        <>
          <button className="btn"><IconFilter /> Filters</button>
          <button className="btn btn-primary"><IconPlus /> Add Patient</button>
        </>
      }
    >
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Patient</th><th>Age</th><th>Contact</th><th>Service</th><th>Last Visit</th><th>Status</th><th></th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p) => (
              <tr key={p.name}>
                <td>
                  <Link to="/patients/eleanor-thompson" className="person">
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
          <span>Showing 1–8 of 186 patients</span>
          <div className="pager">
            <button>‹</button><button className="active">1</button><button>2</button><button>3</button>
            <span style={{ color: "var(--text-faint)" }}>…</span><button>24</button><button>›</button>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
