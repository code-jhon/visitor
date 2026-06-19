// VIS-5 — Operational dashboard: landing screen with key indicators, today's
// agenda and shortcuts to visits by state. Polls periodically for near-real-time
// updates (websockets are a later option). The real-time map is VIS-11.
import { useEffect, useState } from "react";
import { DashboardSummary, getSummary } from "../features/dashboard/api";

const REFRESH_MS = 30_000;

function Card({ label, value }: { label: string; value: number }): JSX.Element {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16, minWidth: 120 }}>
      <div style={{ fontSize: 28, fontWeight: 700 }}>{value}</div>
      <div style={{ color: "#666" }}>{label}</div>
    </div>
  );
}

export function Dashboard(): JSX.Element {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const load = (): void => {
      getSummary()
        .then((s) => active && setSummary(s))
        .catch((e: Error) => active && setError(e.message));
    };
    load();
    const id = setInterval(load, REFRESH_MS);
    return () => {
      active = false;
      clearInterval(id);
    };
  }, []);

  if (error) return <p role="alert">Could not load dashboard: {error}</p>;
  if (!summary) return <p>Loading dashboard…</p>;

  return (
    <section>
      <h2>Dashboard</h2>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <Card label="Total visits" value={summary.total_visits} />
        <Card label="Today's agenda" value={summary.today_agenda} />
        <Card label="Active" value={summary.active} />
        <Card label="Unassigned" value={summary.unassigned} />
        <Card label="Completed" value={summary.by_status.completed ?? 0} />
        <Card label="Cancelled" value={summary.by_status.cancelled ?? 0} />
      </div>
      {/* Real-time map widget is integrated here once VIS-11 lands. */}
    </section>
  );
}
