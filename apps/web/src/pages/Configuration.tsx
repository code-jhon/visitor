// VIS-9 Configuration — services, tariffs and certificate requirements (styled).
import { useEffect, useState } from "react";
import { AppShell, Badge } from "../components/AppShell";
import { IconPlus } from "../components/icons";
import {
  CertificateRequirement, Service, Tariff,
  listCertificates, listServices, listTariffs,
} from "../features/configuration/api";

const MODALITY: Record<string, string> = {
  per_service: "Per service", per_provider: "Per provider",
  per_hour: "Per hour", per_km: "Per km / mileage",
};
const DEMO_SERVICES = [
  { id: "1", name: "Physical Therapy", description: "", is_active: true },
  { id: "2", name: "General Checkup", description: "", is_active: true },
  { id: "3", name: "Wound Care", description: "", is_active: true },
];
const DEMO_TARIFFS = [
  { id: "1", service_id: "1", subservice_id: null, provider_id: null, name: "Standard PT", modality: "per_hour" as const, amount: "52.00", currency: "USD", valid_from: "2026-01-01", valid_to: null, is_active: true },
  { id: "2", service_id: "3", subservice_id: null, provider_id: null, name: "Mileage allowance", modality: "per_km" as const, amount: "0.62", currency: "USD", valid_from: "2026-01-01", valid_to: null, is_active: true },
];
const DEMO_CERTS = [
  { id: "1", name: "CPR Certification", description: "", applies_to: "empleado", is_mandatory: true },
  { id: "2", name: "Liability Insurance", description: "", applies_to: "proveedor", is_mandatory: true },
];

export function Configuration(): JSX.Element {
  const [services, setServices] = useState<Service[]>(DEMO_SERVICES);
  const [tariffs, setTariffs] = useState<Tariff[]>(DEMO_TARIFFS as Tariff[]);
  const [certs, setCerts] = useState<CertificateRequirement[]>(DEMO_CERTS);

  useEffect(() => {
    listServices().then((s) => s.length && setServices(s)).catch(() => undefined);
    listTariffs().then((t) => t.length && setTariffs(t)).catch(() => undefined);
    listCertificates().then((c) => c.length && setCerts(c)).catch(() => undefined);
  }, []);

  return (
    <AppShell
      title="Configuration"
      subtitle="Services, tariffs and required certificates"
      actions={<button className="btn btn-primary"><IconPlus /> Add</button>}
    >
      <div className="stack-16">
        <div className="card card-pad">
          <div className="section-head"><strong style={{ fontSize: 16 }}>Services</strong></div>
          <table className="table">
            <thead><tr><th>Name</th><th>Status</th></tr></thead>
            <tbody>{services.map((s) => (
              <tr key={s.id}><td style={{ fontWeight: 600 }}>{s.name}</td><td><Badge kind={s.is_active ? "green" : "gray"}>{s.is_active ? "Active" : "Inactive"}</Badge></td></tr>
            ))}</tbody>
          </table>
        </div>

        <div className="card card-pad">
          <div className="section-head"><strong style={{ fontSize: 16 }}>Tariffs</strong></div>
          <table className="table">
            <thead><tr><th>Name</th><th>Modality</th><th>Amount</th><th>Valid From</th></tr></thead>
            <tbody>{tariffs.map((t) => (
              <tr key={t.id}>
                <td style={{ fontWeight: 600 }}>{t.name}</td>
                <td><Badge kind="blue">{MODALITY[t.modality] ?? t.modality}</Badge></td>
                <td>{t.amount} {t.currency}</td>
                <td className="muted">{t.valid_from ?? "—"}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>

        <div className="card card-pad">
          <div className="section-head"><strong style={{ fontSize: 16 }}>Certificate Requirements</strong></div>
          <table className="table">
            <thead><tr><th>Name</th><th>Applies To</th><th>Mandatory</th></tr></thead>
            <tbody>{certs.map((c) => (
              <tr key={c.id}><td style={{ fontWeight: 600 }}>{c.name}</td><td className="muted">{c.applies_to}</td><td><Badge kind={c.is_mandatory ? "amber" : "gray"}>{c.is_mandatory ? "Required" : "Optional"}</Badge></td></tr>
            ))}</tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
