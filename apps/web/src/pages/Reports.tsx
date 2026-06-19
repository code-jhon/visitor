// Reports — generator card grid matching the mockup.
import { useState } from "react";
import { AppShell } from "../components/AppShell";
import {
  IconClock, IconEmployees, IconFinancial, IconMail, IconPlus,
  IconProviders, IconShield,
} from "../components/icons";
import { reports } from "../data/demo";

const TABS = ["All", "Operational", "Financial", "Compliance"];
const ICONS: Record<string, (p: any) => JSX.Element> = {
  clock: IconClock, financial: IconFinancial, shield: IconShield,
  employees: IconEmployees, providers: IconProviders,
};

export function Reports(): JSX.Element {
  const [tab, setTab] = useState("All");
  const shown = reports.filter((r) => tab === "All" || r.cat === tab);
  return (
    <AppShell
      title="Reports"
      subtitle="Generate operational and financial reports"
      search="Search reports…"
      actions={<button className="btn btn-primary"><IconPlus /> Generate Report</button>}
    >
      <div className="tabs" style={{ marginBottom: 18 }}>
        {TABS.map((t) => (
          <button key={t} className={`tab${tab === t ? " active" : ""}`}
            style={tab === t ? { background: "var(--brand)" } : {}} onClick={() => setTab(t)}>{t}</button>
        ))}
      </div>

      <div className="grid grid-2">
        {shown.map((r) => {
          const Icon = ICONS[r.icon] ?? IconClock;
          return (
            <div key={r.name} className="card report-card">
              <div className="flex items-center gap-12">
                <span className="report-icon"><Icon style={{ width: 19, height: 19 }} /></span>
                <strong style={{ fontSize: 15 }}>{r.name}</strong>
              </div>
              <p className="person-sub" style={{ margin: 0, lineHeight: 1.5 }}>{r.desc}</p>
              <div className="report-foot">
                <span className="gen">Last generated: {r.last}</span>
                <button className="btn">Generate</button>
              </div>
            </div>
          );
        })}
      </div>

      <div className="flex items-center gap-8 mt-24" style={{ justifyContent: "flex-end" }}>
        <span className="helper" style={{ marginRight: 6 }}>Export format:</span>
        <button className="btn"><IconFinancial style={{ width: 15, height: 15 }} /> PDF</button>
        <button className="btn">XLS</button>
        <button className="btn">DOC</button>
        <button className="btn"><IconMail style={{ width: 15, height: 15 }} /> Email</button>
      </div>
    </AppShell>
  );
}
