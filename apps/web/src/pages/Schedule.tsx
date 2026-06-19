// VIS-10 Scheduling — week calendar styled to match the web_screens mockup.
// VIS-5 wires the status filter so the dashboard shortcuts land here pre-filtered
// (e.g. /scheduling?status=in_progress) and the filter tabs stay in sync via the
// URL, so a filtered view is shareable/bookmarkable.
import { useSearchParams } from "react-router-dom";
import { AppShell } from "../components/AppShell";
import { IconChevronLeft, IconChevronRight, IconPlus } from "../components/icons";
import { weekDays, weekEvents } from "../data/demo";

// label -> URL status value (null = no filter) and the demo event "kind" it maps to.
const FILTERS: { label: string; status: string | null; kind: string | null }[] = [
  { label: "All", status: null, kind: null },
  { label: "Scheduled", status: "scheduled", kind: "gray" },
  { label: "In Progress", status: "in_progress", kind: "blue" },
  { label: "Completed", status: "completed", kind: "green" },
  { label: "Cancelled", status: "cancelled", kind: "red" },
  { label: "Unassigned", status: "unassigned", kind: null },
];

export function Schedule(): JSX.Element {
  const [params, setParams] = useSearchParams();
  const active = params.get("status");
  const activeFilter = FILTERS.find((f) => f.status === active) ?? FILTERS[0];

  const selectFilter = (status: string | null): void => {
    if (status) setParams({ status });
    else setParams({});
  };

  // Apply the active status filter to the demo week events.
  const visibleEvents = weekEvents.map((day) =>
    activeFilter.kind ? day.filter((e) => e.kind === activeFilter.kind) : day,
  );

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
        {FILTERS.map((f) => (
          <button
            key={f.label}
            className={`tab${f.label === activeFilter.label ? " active" : ""}`}
            onClick={() => selectFilter(f.status)}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="card card-pad">
        <div className="cal">
          {weekDays.map((d, i) => (
            <div key={d.dow} className="cal-col">
              <div className="cal-day">{d.dow}<span className={`num${d.today ? " today" : ""}`}>{d.num}</span></div>
              {visibleEvents[i].length === 0
                ? <div className="person-sub" style={{ textAlign: "center", marginTop: 8 }}>No visits</div>
                : visibleEvents[i].map((e, j) => (
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
