// VIS-9 — Configuration page: catalogs that feed scheduling, financials and
// reports (services, tariffs with their four modalities, and certificate
// requirements). Admin / Empresa / Soporte only (enforced server-side via RBAC).
import { useEffect, useState } from "react";
import {
  CertificateRequirement,
  Service,
  Tariff,
  listCertificates,
  listServices,
  listTariffs,
} from "../features/configuration/api";

const MODALITY_LABEL: Record<string, string> = {
  per_service: "Per service",
  per_provider: "Per provider",
  per_hour: "Per hour",
  per_km: "Per km / mileage",
};

export function Configuration(): JSX.Element {
  const [services, setServices] = useState<Service[]>([]);
  const [tariffs, setTariffs] = useState<Tariff[]>([]);
  const [certs, setCerts] = useState<CertificateRequirement[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([listServices(), listTariffs(), listCertificates()])
      .then(([s, t, c]) => {
        setServices(s);
        setTariffs(t);
        setCerts(c);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  if (error) return <p role="alert">Could not load configuration: {error}</p>;

  return (
    <section>
      <h2>Configuration</h2>

      <h3>Services</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          {services.map((s) => (
            <tr key={s.id}>
              <td>{s.name}</td>
              <td>{s.is_active ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Tariffs</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Modality</th>
            <th>Amount</th>
            <th>Valid from</th>
            <th>Valid to</th>
          </tr>
        </thead>
        <tbody>
          {tariffs.map((t) => (
            <tr key={t.id}>
              <td>{t.name}</td>
              <td>{MODALITY_LABEL[t.modality] ?? t.modality}</td>
              <td>
                {t.amount} {t.currency}
              </td>
              <td>{t.valid_from ?? "—"}</td>
              <td>{t.valid_to ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Certificate requirements</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Applies to</th>
            <th>Mandatory</th>
          </tr>
        </thead>
        <tbody>
          {certs.map((c) => (
            <tr key={c.id}>
              <td>{c.name}</td>
              <td>{c.applies_to}</td>
              <td>{c.is_mandatory ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
