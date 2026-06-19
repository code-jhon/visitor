// VIS-10 Scheduling — week calendar styled to match the web_screens mockup.
// Component normalization: the view now consumes the live scheduling feature API
// (status-filtered list + unassigned queue) driven by the ?status query param,
// so filter tabs are functional and shareable. When the API returns visits they
// render as a live list; otherwise the styled demo calendar is the fallback.
import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { AppShell, Badge } from "../components/AppShell";
import { IconChevronLeft, IconChevronRight, IconPlus } from "../components/icons";
import { weekDays, weekEvents } from "../data/demo";
import { getSchedule, getUnassigned, Visit, VisitStatus } from "../features/schedule/api";

// label -> URL status value (null = all) and the demo event "kind" it maps to.
const FILTERS: { label: string; status: string | null; kind: string | null }[] = [
  { label: "All", status: null, kind: null },
  { label: "Scheduled", status: "scheduled", kind: "gray" },
  { label: "In Progress", status: "in_progress", kind: "blue" },
  { label: "Completed", status: "completed", kind: "green" },
  { label: "Cancelled", status: "cancelled", kind: "red" },
  { label: "Unassigned", status: "unassigned", kind: null },
];

const STATUS_BADGE: Record<string, string> = {
  scheduled: "gray", en_route: "blue", in_progress: "blue",
  completed: "green", cancelled: "red", no_show: "amber",
};

export function Schedule(): JSX.Element {
  const [params, setParams] = useSearchParams();
  const active = params.get("status");
  const activeFilter = FILTERS.find((f) => f.status === active) ?? FILTERS[0];
  const [visits, setVisits] = useState<Visit[]>([]);

  // Fetch the live schedule for the active filter; empty result -> demo fallback.
  useEffect(() => {
    const load = activeFilter.status === "unassigned"
      ? getUnassigned()
      : getSchedule(activeFilter.status ? { status: activeFilter.status as VisitStatus } : undefined);
    load.then(setVisits).catch(() => setVisits([]));
  }, [activeFilter.status]);

  const selectFilter = (status: string | null): void => setParams(status ? { status } : {});

  // Demo calendar, filtered by the active status when offline.
  const visibleEvents = useMemo(
    () => weekEvents.map((day) => (activeFilter.kind ? day.filter((e) => e.kind === activeFilter.kind) : day)),
    [activeFilter.kind],
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

      {visits.length > 0 ? (
        // Live data from the scheduling API.
        <div className="card">
          <table className="table">
            <thead>
              <tr><th>Visit</th><th>Patient</th><th>When</th><th>Address</th><th>Status</th></tr>
            </thead>
            <tbody>
              {visits.map((v) => (
                <tr key={v.id}>
                  <td className="muted">#{v.id.slice(0, 8)}</td>
                  <td>{v.patient_id ?? "—"}</td>
                  <td className="muted">{v.scheduled_start ? new Date(v.scheduled_start).toLocaleString() : "—"}</td>
                  <td className="muted">{v.address || "—"}</td>
                  <td><Badge kind={STATUS_BADGE[v.status] ?? "gray"}>{v.status.replace("_", " ")}</Badge></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        // Styled demo calendar fallback (offline / no matching visits).
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
      )}
    </AppShell>
  );
}
