// Visit Map — real-time map with nearby-visits panel, matching the mockup.
import { Badge, Sidebar } from "../components/AppShell";
import { IconSearch } from "../components/icons";
import { colorFor, initials, mapPins, nearbyVisits } from "../data/demo";

const FILTERS = ["All", "Scheduled", "In Progress", "Completed", "Incidents"];
const RANGE = ["Today", "This Week", "This Month"];

export function VisitMap(): JSX.Element {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main">
        <div style={{ display: "flex", gap: 16, padding: 16, height: "100vh" }}>
          <div className="map" style={{ flex: 1, minHeight: 0 }}>
            <div style={{ position: "absolute", top: 16, left: 16, right: 16, display: "flex", flexDirection: "column", gap: 10 }}>
              <div className="search" style={{ background: "#fff", border: "1px solid var(--border)", maxWidth: 320 }}>
                <IconSearch style={{ width: 16, height: 16 }} /><input placeholder="Search visits on map…" />
              </div>
              <div className="tabs">
                {FILTERS.map((f, i) => <button key={f} className={`tab${i === 0 ? " active" : ""}`}>{f}</button>)}
              </div>
              <div className="seg" style={{ width: "fit-content" }}>
                {RANGE.map((r, i) => <button key={r} className={i === 0 ? "active" : ""}>{r}</button>)}
              </div>
            </div>
            {mapPins.map((p, i) => <span key={i} className={`pin ${p.kind}`} style={{ top: p.top, left: p.left }} />)}
            <div className="map-legend">
              <span><span className="dot green" /> Completed</span>
              <span><span className="dot blue" /> Scheduled</span>
              <span><span className="dot amber" /> Incident</span>
              <span><span className="dot red" /> Cancelled</span>
            </div>
          </div>

          <div className="card card-pad" style={{ width: 360, overflowY: "auto" }}>
            <div className="section-head">
              <strong style={{ fontSize: 16 }}>Nearby Visits</strong>
              <span className="pill-count">12 visits</span>
            </div>
            <div className="list">
              {nearbyVisits.map((v) => (
                <div key={v.name} className="list-row" style={{ alignItems: "flex-start" }}>
                  <span className={`ava-sm ${colorFor(v.name)}`}>{initials(v.name)}</span>
                  <div style={{ flex: 1 }}>
                    <div className="flex between items-center"><span className="person-name">{v.name}</span><Badge kind={v.badge}>{v.status}</Badge></div>
                    <div className="person-sub">{v.service}</div>
                    <div className="flex between" style={{ marginTop: 4 }}>
                      <span className="helper">{v.time}</span><span className="helper">{v.who}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
