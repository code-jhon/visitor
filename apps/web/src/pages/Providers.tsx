// Providers & coordinators — table + detail panel matching the mockup.
import { useState } from "react";
import { AppShell, Badge } from "../components/AppShell";
import { IconFilter, IconMail, IconPhone, IconPin, IconPlus, IconUser } from "../components/icons";
import { colorFor, initials, providers } from "../data/demo";

export function Providers(): JSX.Element {
  const [sel, setSel] = useState(0);
  const p = providers[sel];
  return (
    <AppShell
      title="Providers & Coordinators"
      subtitle="14 providers managing patient services"
      search="Search providers…"
      actions={<>
        <button className="btn"><IconFilter /> Filters</button>
        <button className="btn btn-primary"><IconPlus /> Add Provider</button>
      </>}
    >
      <div className="grid" style={{ gridTemplateColumns: "1.7fr 1fr" }}>
        <div className="card">
          <table className="table">
            <thead><tr><th>Provider</th><th>Type</th><th>Clients</th><th>Contract</th><th>Status</th><th></th></tr></thead>
            <tbody>
              {providers.map((row, i) => (
                <tr key={row.name} onClick={() => setSel(i)}
                    style={{ cursor: "pointer", background: i === sel ? "var(--brand-soft)" : undefined,
                             boxShadow: i === sel ? "inset 3px 0 0 var(--brand)" : undefined }}>
                  <td>
                    <div className="person">
                      <span className={`ava-sm ${colorFor(row.name)}`}>{initials(row.name)}</span>
                      <div><div className="person-name">{row.name}</div><div className="person-sub">{row.contact}</div></div>
                    </div>
                  </td>
                  <td className="muted">{row.type}</td>
                  <td style={{ fontWeight: 600 }}>{row.clients}</td>
                  <td className="muted">{row.contract}</td>
                  <td><Badge kind={row.badge}>{row.status}</Badge></td>
                  <td className="right"><span className="row-actions">···</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card card-pad">
          <div style={{ textAlign: "center", color: "#fff", background: "#0f172a", borderRadius: "var(--radius)", padding: "20px" }}>
            <span className="brand-logo" style={{ margin: "0 auto 10px", width: 46, height: 46, background: "#1e293b" }}>
              <IconUser style={{ width: 22, height: 22 }} />
            </span>
            <div style={{ fontSize: 18, fontWeight: 700 }}>{p.name}</div>
            <div style={{ fontSize: 13, color: "#cbd5e1", marginTop: 2 }}>{p.type} · <span style={{ color: "#34d399" }}>{p.status}</span></div>
            <div className="grid grid-3" style={{ marginTop: 16, gap: 10 }}>
              <div style={{ background: "#1e293b", borderRadius: 10, padding: "10px 4px" }}><div style={{ fontSize: 18, fontWeight: 700 }}>{p.clients}</div><div style={{ fontSize: 11, color: "#94a3b8" }}>Clients</div></div>
              <div style={{ background: "#1e293b", borderRadius: 10, padding: "10px 4px" }}><div style={{ fontSize: 18, fontWeight: 700 }}>12</div><div style={{ fontSize: 11, color: "#94a3b8" }}>Employees</div></div>
              <div style={{ background: "#1e293b", borderRadius: 10, padding: "10px 4px" }}><div style={{ fontSize: 18, fontWeight: 700 }}>186</div><div style={{ fontSize: 11, color: "#94a3b8" }}>Visits/Mo</div></div>
            </div>
          </div>

          <h4 style={{ margin: "18px 0 10px", fontSize: 14 }}>Contact Information</h4>
          <div className="profile-list" style={{ marginTop: 0, borderTop: "none", paddingTop: 0 }}>
            <div className="row"><IconUser /><div><div className="lbl">Primary Contact</div>{p.contact}</div></div>
            <div className="row"><IconPhone /><div><div className="lbl">Phone</div>+1 (555) 890-1234</div></div>
            <div className="row"><IconMail /><div><div className="lbl">Email</div><span style={{ color: "var(--brand)" }}>linda@healthfirst.com</span></div></div>
            <div className="row"><IconPin /><div><div className="lbl">Address</div>450 Healthcare Blvd, Suite 200</div></div>
          </div>

          <h4 style={{ margin: "18px 0 10px", fontSize: 14 }}>Contract Details</h4>
          <table className="table" style={{ fontSize: 13 }}>
            <tbody>
              <tr><td className="muted" style={{ padding: "8px 0", border: "none" }}>Contract Type</td><td className="right" style={{ padding: "8px 0", border: "none", fontWeight: 600 }}>Annual Agreement</td></tr>
              <tr><td className="muted" style={{ padding: "8px 0", border: "none" }}>Start Date</td><td className="right" style={{ padding: "8px 0", border: "none", fontWeight: 600 }}>Jan 15, 2026</td></tr>
              <tr><td className="muted" style={{ padding: "8px 0", border: "none" }}>Renewal Date</td><td className="right" style={{ padding: "8px 0", border: "none", fontWeight: 600 }}>Jan 15, 2027</td></tr>
              <tr><td className="muted" style={{ padding: "8px 0", border: "none" }}>Base Tariff</td><td className="right" style={{ padding: "8px 0", border: "none", fontWeight: 600 }}>$52/hr</td></tr>
            </tbody>
          </table>
          <div className="flex gap-8 mt-16">
            <button className="btn" style={{ flex: 1, justifyContent: "center" }}>Edit</button>
            <button className="btn btn-primary" style={{ flex: 1, justifyContent: "center" }}>View Clients</button>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
