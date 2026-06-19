// Patient detail — profile, next-visit banner and visit history (mockup).
import { Link } from "react-router-dom";
import { AppShell, Badge } from "../components/AppShell";
import {
  IconArrowRight, IconBriefcase, IconHeart, IconMail, IconPhone, IconPin,
  IconShield, IconStar, IconUser,
} from "../components/icons";
import { patientDetail as p } from "../data/demo";

export function PatientDetail(): JSX.Element {
  return (
    <AppShell
      title=""
      actions={<>
        <button className="btn">Edit</button>
        <button className="btn btn-primary">Schedule Visit</button>
      </>}
    >
      <div className="flex items-center gap-8" style={{ marginTop: -8, marginBottom: 16, color: "var(--text-muted)", fontSize: 14 }}>
        <Link to="/patients" style={{ color: "var(--text-muted)" }}>Patients</Link> / <strong style={{ color: "var(--text)" }}>{p.name}</strong>
      </div>

      <div className="grid" style={{ gridTemplateColumns: "minmax(0,360px) 1fr" }}>
        <div className="card profile">
          <div className="ava-lg ava-blue">ET</div>
          <h3>{p.name}</h3>
          <div className="meta">{p.age} years old · <span style={{ color: "var(--green-text)" }}>● {p.status}</span></div>
          <div className="profile-list">
            <div className="row"><IconPhone /><div><div className="lbl">Phone</div>{p.phone}</div></div>
            <div className="row"><IconMail /><div><div className="lbl">Email</div>{p.email}</div></div>
            <div className="row"><IconPin /><div><div className="lbl">Address</div>{p.address}</div></div>
            <div className="row"><IconHeart /><div><div className="lbl">Primary Service</div>{p.service}</div></div>
            <div className="row"><IconUser /><div><div className="lbl">Provider</div>{p.provider}</div></div>
            <div className="row"><IconShield /><div><div className="lbl">Insurance</div>{p.insurance}</div></div>
          </div>
        </div>

        <div className="stack-16">
          <div className="banner">
            <div>
              <div className="eyebrow"><span className="dot green" /> Next Scheduled Visit</div>
              <div className="big">{p.next.when}</div>
              <div className="sub">{p.next.what}</div>
            </div>
            <button className="btn btn-primary">View Details <IconArrowRight /></button>
          </div>

          <div className="card card-pad">
            <div className="section-head">
              <span className="section-title"><IconBriefcase /> Visit History</span>
              <span className="pill-count">42 total</span>
            </div>
            <div className="list">
              {p.history.map((h, i) => (
                <div key={i} className="list-row">
                  <div style={{ minWidth: 110 }}>
                    <div className="person-name">{h.date}</div>
                    <div className="person-sub">{h.time}</div>
                  </div>
                  <div style={{ flex: 1 }}>
                    <div className="person-name">{h.service}</div>
                    <div className="person-sub">{h.provider}</div>
                  </div>
                  <Badge kind={h.badge}>{h.status}</Badge>
                  <span className="flex items-center gap-8" style={{ minWidth: 52, justifyContent: "flex-end", color: "var(--amber-text)", fontWeight: 600, fontSize: 13 }}>
                    {h.rating !== "—" && <IconStar style={{ width: 14, height: 14 }} />}{h.rating}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
