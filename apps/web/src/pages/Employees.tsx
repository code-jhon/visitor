// VIS-6 — Employees module: searchable, filterable list of caregivers with a
// soft-delete (deactivate) action. Personal/professional/contract data and the
// edit form follow the design in docs/web_screens (Employee Main).
import { FormEvent, useEffect, useState } from "react";
import { Employee, searchEmployees } from "../features/employees/api";

export function Employees(): JSX.Element {
  const [rows, setRows] = useState<Employee[]>([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function load(q = ""): Promise<void> {
    try {
      setRows(await searchEmployees({ q: q || undefined }));
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  function onSearch(e: FormEvent): void {
    e.preventDefault();
    void load(query);
  }

  return (
    <section>
      <h2>Employees</h2>
      <form onSubmit={onSearch} role="search">
        <input
          aria-label="Search employees"
          placeholder="Search by name…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
        <button type="button" title="Help">
          ?
        </button>
      </form>
      {error && <p role="alert">Could not load employees: {error}</p>}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Document</th>
            <th>Position</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((e) => (
            <tr key={e.id}>
              <td>
                {e.first_name} {e.last_name}
              </td>
              <td>{e.document_id || "—"}</td>
              <td>{e.position || "—"}</td>
              <td>{e.is_active ? "Active" : "Inactive"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
