// VIS-5 Dashboard — operational landing view (styled to match web_screens).
// Wires the live /dashboard/summary aggregates into the KPIs and the status
// shortcuts, and makes every widget a navigable entry point into the detailed
// modules (Scheduling filtered by status, Visit Map). Demo data is the visual
// fallback when the API is not reachable (e.g. design review).
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AppShell, Badge, Kpi } from "../components/AppShell";
import { IconActivity, IconAlert, IconCalendar, IconFile, IconPin } from "../components/icons";
import { DashboardSummary, getSummary } from "../features/dashboard/api";
import { dashboardKpis, mapPins, recentActivity, recentAlerts, todaySchedule } from "../data/demo";

// Direct-access shortcuts to visits by state (PRD §7.2.1). Each navigates to the
// Scheduling module pre-filtered by the corresponding visit status.
const STATUS_SHORTCUTS: { label: string; status: string; kind: string }[] = [
  { label: "Scheduled", status: "scheduled", kind: "gray" },
  { label: "In Progress", status: "in_progress", kind: "blue" },
  { label: "Completed", status: "completed", kind: "green" },
  { label: "Cancelled", status: "cancelled", kind: "red" },
  { label: "Unassigned", status: "unassigned", kind: "amber" },
];

export function Dashboard(): JSX.Element {
  const navigate = useNavigate();
  const [kpis, setKpis] = useState(dashboardKpis);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    getSummary()
      .then((s) => {
        setSummary(s);
        // Reflect the live operational state in the KPI cards.
        setKpis((prev) => prev.map((k) => {
          if (k.label === "Today's Visits") return { ...k, value: String(s.today_agenda) };
          if (k.label === "Incidents") return { ...k, value: String(s.by_status.no_show ?? 0) };
          return k;
        }));
      })
      .catch(() => undefined);
  }, []);

  const shortcutCount = (status: string): number | null => {
    if (!summary) return null;
    if (status === "unassigned") return summary.unassigned;
    return summary.by_status[status] ?? 0;
  };

  const goToSchedule = (status?: string): void =>
    navigate(status && status !== "all" ? `/scheduling?status=${status}` : "/scheduling");

  return (
    <AppShell title="Dashboard" subtitle="Welcome back, Sarah. Here's your overview.">
      <div className="grid grid-4">
        {kpis.map((k) => (
          <div
            key={k.label}
            role="button"
            tabIndex={0}
            style={{ cursor: "pointer" }}
            onClick={() => goToSchedule()}
            onKeyDown={(e) => { if (e.key === "Enter") goToSchedule(); }}
          >
            <Kpi {...k} />
          </div>
        ))}
      </div>

      {/* Direct-access shortcuts to visits by state. */}
      <div className="tabs mt-16">
        {STATUS_SHORTCUTS.map((s) => {
          const count = shortcutCount(s.status);
          return (
            <button key={s.status} className="tab" onClick={() => goToSchedule(s.status)}>
              <span className={`dot ${s.kind}`} /> {s.label}
              {count !== null && <span className="tab-count">{count}</span>}
            </button>
          );
        })}
      </div>

      <div className="grid mt-16" style={{ gridTemplateColumns: "1.7fr 1fr" }}>
        <div className="card card-pad">
          <div className="section-head">
            <span className="section-title"><IconPin /> Visit Map</span>
            <div className="seg">
              <button className="active" onClick={() => navigate("/visit-map")}>All</button>
              <button onClick={() => navigate("/visit-map?status=scheduled")}>Scheduled</button>
              <button onClick={() => navigate("/visit-map?status=in_progress")}>In Progress</button>
            </div>
          </div>
          <div className="map" style={{ cursor: "pointer" }} onClick={() => navigate("/visit-map")}>
            {mapPins.map((p, i) => (
              <span key={i} className={`pin ${p.kind}`} style={{ top: p.top, left: p.left }} />
            ))}
          </div>
        </div>

        <div className="card card-pad">
          <div className="section-head">
            <span className="section-title"><IconCalendar /> Today's Schedule</span>
            <button className="pill-count" style={{ cursor: "pointer", border: "none" }} onClick={() => goToSchedule()}>
              {summary ? `${summary.today_agenda} visits` : "8 visits"}
            </button>
          </div>
          <div className="list">
            {todaySchedule.map((v) => (
              <div
                key={v.name}
                className="list-row"
                style={{ cursor: "pointer" }}
                onClick={() => goToSchedule(v.status.toLowerCase().replace(" ", "_"))}
              >
                <span className="time-chip">{v.time}</span>
                <div style={{ flex: 1 }}>
                  <div className="person-name">{v.name}</div>
                  <div className="person-sub">{v.service}</div>
                </div>
                <Badge kind={v.kind}>{v.status}</Badge>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-2 mt-16">
        <div className="card card-pad">
          <div className="section-head">
            <span className="section-title"><IconAlert /> Recent Alerts</span>
            <span className="pill-count" style={{ color: "var(--amber-text)", background: "var(--amber-bg)" }}>5 new</span>
          </div>
          <div className="list">
            {recentAlerts.map((a, i) => (
              <div key={i} className="list-row">
                <span className={`ava-sm ava-${a.color === "red" ? "pink" : "amber"}`}>
                  {a.icon === "file" ? <IconFile style={{ width: 16, height: 16 }} /> : <IconAlert style={{ width: 16, height: 16 }} />}
                </span>
                <div style={{ flex: 1 }}>
                  <div className="person-name">{a.title}</div>
                  <div className="person-sub">{a.body}</div>
                </div>
                <span className="helper">{a.time}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card card-pad">
          <div className="section-head"><span className="section-title"><IconActivity /> Recent Activity</span></div>
          <div className="list">
            {recentActivity.map((a, i) => (
              <div key={i} className="list-row">
                <span className={`dot ${a.color === "purple" ? "blue" : a.color}`} />
                <div style={{ flex: 1 }} className="person-name">{a.text}</div>
                <span className="helper">{a.time}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
