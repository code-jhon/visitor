// VIS-7 — Clients/Patients module: searchable patient list and a per-patient
// visit calendar. Sensitive health fields (medical notes) are only returned by
// the API to authorized roles (VIS-4). Design: docs/web_screens (Patient Main).
import { FormEvent, useEffect, useState } from "react";
import { CalendarEntry, Patient, getCalendar, searchPatients } from "../features/patients/api";

export function Patients(): JSX.Element {
  const [rows, setRows] = useState<Patient[]>([]);
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Patient | null>(null);
  const [calendar, setCalendar] = useState<CalendarEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function load(q = ""): Promise<void> {
    try {
      setRows(await searchPatients(q || undefined));
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function openCalendar(p: Patient): Promise<void> {
    setSelected(p);
    setCalendar(await getCalendar(p.id));
  }

  function onSearch(e: FormEvent): void {
    e.preventDefault();
    void load(query);
  }

  return (
    <section>
      <h2>Patients</h2>
      <form onSubmit={onSearch} role="search">
        <input
          aria-label="Search patients"
          placeholder="Search by name…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
        <button type="button" title="Help">
          ?
        </button>
      </form>
      {error && <p role="alert">Could not load patients: {error}</p>}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Document</th>
            <th>Notes</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {rows.map((p) => (
            <tr key={p.id}>
              <td>
                {p.first_name} {p.last_name}
              </td>
              <td>{p.document_id || "—"}</td>
              <td>{p.medical_notes ? p.medical_notes : "—"}</td>
              <td>
                <button type="button" onClick={() => void openCalendar(p)}>
                  Calendar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selected && (
        <aside>
          <h3>
            Calendar — {selected.first_name} {selected.last_name}
          </h3>
          {calendar.length === 0 ? (
            <p>No visits.</p>
          ) : (
            <ul>
              {calendar.map((c) => (
                <li key={c.visit_id}>
                  {c.scheduled_start ?? "unscheduled"} — {c.status} ({c.address})
                </li>
              ))}
            </ul>
          )}
        </aside>
      )}
    </section>
  );
}
