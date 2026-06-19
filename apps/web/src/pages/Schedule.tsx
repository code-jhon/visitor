// VIS-10 — Scheduling page: calendar list with status filters, the unassigned
// queue and inline lifecycle actions. The backend is the single source of truth
// for visit state (consistent across web and mobile). Design: docs/web_screens
// (Schedule Main); the full map view is VIS-11.
import { useEffect, useState } from "react";
import {
  Visit,
  VisitStatus,
  getSchedule,
  getUnassigned,
  transition,
} from "../features/schedule/api";

const FILTERS: { label: string; value?: VisitStatus }[] = [
  { label: "All" },
  { label: "Scheduled", value: "scheduled" },
  { label: "In progress", value: "in_progress" },
  { label: "Completed", value: "completed" },
  { label: "Cancelled", value: "cancelled" },
];

const NEXT_ACTION: Partial<Record<VisitStatus, "start" | "finish">> = {
  scheduled: "start",
  en_route: "start",
  in_progress: "finish",
};

export function Schedule(): JSX.Element {
  const [visits, setVisits] = useState<Visit[]>([]);
  const [unassigned, setUnassigned] = useState<Visit[]>([]);
  const [status, setStatus] = useState<VisitStatus | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  async function reload(s = status): Promise<void> {
    try {
      const [all, un] = await Promise.all([getSchedule({ status: s }), getUnassigned()]);
      setVisits(all);
      setUnassigned(un);
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    void reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function act(v: Visit): Promise<void> {
    const next = NEXT_ACTION[v.status];
    if (!next) return;
    await transition(v.id, next);
    void reload();
  }

  return (
    <section>
      <h2>Schedule</h2>
      <nav>
        {FILTERS.map((f) => (
          <button
            key={f.label}
            type="button"
            onClick={() => {
              setStatus(f.value);
              void reload(f.value);
            }}
          >
            {f.label}
          </button>
        ))}
      </nav>
      {error && <p role="alert">Could not load schedule: {error}</p>}

      <h3>Unassigned ({unassigned.length})</h3>
      <ul>
        {unassigned.map((v) => (
          <li key={v.id}>
            {v.scheduled_start ?? "unscheduled"} — {v.address}
          </li>
        ))}
      </ul>

      <h3>Visits</h3>
      <table>
        <thead>
          <tr>
            <th>Start</th>
            <th>Address</th>
            <th>Status</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {visits.map((v) => (
            <tr key={v.id}>
              <td>{v.scheduled_start ?? "—"}</td>
              <td>{v.address}</td>
              <td>{v.status}</td>
              <td>
                {NEXT_ACTION[v.status] && (
                  <button type="button" onClick={() => void act(v)}>
                    {NEXT_ACTION[v.status]}
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
