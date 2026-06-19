// VIS-10 Scheduling — week calendar styled to match the web_screens mockup.
import { AppShell } from "../components/AppShell";
import { IconChevronLeft, IconChevronRight, IconPlus } from "../components/icons";
import { weekDays, weekEvents } from "../data/demo";

const FILTERS = ["All", "Scheduled", "In Progress", "Completed", "Cancelled", "Unassigned"];

export function Schedule(): JSX.Element {
  return (
    <AppShell
      title="Scheduling"
      subtitle="Manage visits, assignments, and appointments"
      search="Search visits…"
      actions={<button className="btn btn-primary"><IconPlus /> New Visit</button>}
    >
      <div className="flex between items-center" style={{ marginBottom: 14, flexWrap: "wrap", gap: 12 }}>
        <div className="flex items-center gap-12">
          <div className="flex items-center gap-8">
            <button className="pager"><span style={{ padding: 4 }}><IconChevronLeft style={{ width: 16, height: 16 }} /></span></button>
            <strong style={{ fontSize: 15 }}>June 16 – 22, 2026</strong>
            <button className="pager"><span style={{ padding: 4 }}><IconChevronRight style={{ width: 16, height: 16 }} /></span></button>
          </div>
          <button className="btn">Today</button>
        </div>
        <div className="seg">
          <button>Day</button><button className="active">Week</button><button>Month</button>
        </div>
      </div>

      <div className="tabs" style={{ marginBottom: 16 }}>
        {FILTERS.map((f, i) => <button key={f} className={`tab${i === 0 ? " active" : ""}`}>{f}</button>)}
      </div>

      <div className="card card-pad">
        <div className="cal">
          {weekDays.map((d, i) => (
            <div key={d.dow} className="cal-col">
              <div className="cal-day">{d.dow}<span className={`num${d.today ? " today" : ""}`}>{d.num}</span></div>
              {weekEvents[i].length === 0
                ? <div className="person-sub" style={{ textAlign: "center", marginTop: 8 }}>No visits</div>
                : weekEvents[i].map((e, j) => (
                  <div key={j} className={`event ${e.kind}`}>
                    <div className="t">{e.time}</div>{e.who}
                  </div>
                ))}
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
