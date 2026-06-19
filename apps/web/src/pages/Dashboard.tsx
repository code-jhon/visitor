// VIS-5 Dashboard — styled to match the web_screens mockup (fix/styling).
import { useEffect, useState } from "react";
import { AppShell, Badge, Kpi } from "../components/AppShell";
import { IconActivity, IconAlert, IconCalendar, IconFile, IconPin } from "../components/icons";
import { getSummary } from "../features/dashboard/api";
import { dashboardKpis, mapPins, recentActivity, recentAlerts, todaySchedule } from "../data/demo";

export function Dashboard(): JSX.Element {
  const [kpis, setKpis] = useState(dashboardKpis);

  useEffect(() => {
    getSummary()
      .then((s) => {
        setKpis((prev) => prev.map((k, i) =>
          i === 0 ? { ...k, value: String(s.today_agenda) } : k));
      })
      .catch(() => undefined);
  }, []);

  return (
    <AppShell title="Dashboard" subtitle="Welcome back, Sarah. Here's your overview.">
      <div className="grid grid-4">
        {kpis.map((k) => <Kpi key={k.label} {...k} />)}
      </div>

      <div className="grid mt-16" style={{ gridTemplateColumns: "1.7fr 1fr" }}>
        <div className="card card-pad">
          <div className="section-head">
            <span className="section-title"><IconPin /> Visit Map</span>
            <div className="seg">
              <button className="active">All</button><button>Scheduled</button><button>In Progress</button>
            </div>
          </div>
          <div className="map">
            {mapPins.map((p, i) => (
              <span key={i} className={`pin ${p.kind}`} style={{ top: p.top, left: p.left }} />
            ))}
          </div>
        </div>

        <div className="card card-pad">
          <div className="section-head">
            <span className="section-title"><IconCalendar /> Today's Schedule</span>
            <span className="pill-count">8 visits</span>
          </div>
          <div className="list">
            {todaySchedule.map((v) => (
              <div key={v.name} className="list-row">
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
