// VIS-9 — Configuration module API client (services, tariffs, certificates).
import { apiFetch } from "../../api/client";

export type TariffModality = "per_service" | "per_provider" | "per_hour" | "per_km";

export interface Service {
  id: string;
  name: string;
  description: string;
  is_active: boolean;
}

export interface Tariff {
  id: string;
  service_id: string;
  subservice_id: string | null;
  provider_id: string | null;
  name: string;
  modality: TariffModality;
  amount: string;
  currency: string;
  valid_from: string | null;
  valid_to: string | null;
  is_active: boolean;
}

export interface CertificateRequirement {
  id: string;
  name: string;
  description: string;
  applies_to: string;
  is_mandatory: boolean;
}

async function getJson<T>(path: string): Promise<T> {
  const res = await apiFetch(path);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as T;
}

export const listServices = (): Promise<Service[]> => getJson("/services");
export const listTariffs = (): Promise<Tariff[]> => getJson("/tariffs");
export const listCertificates = (): Promise<CertificateRequirement[]> =>
  getJson("/certificates");

export async function createTariff(body: {
  service_id: string;
  name: string;
  modality: TariffModality;
  amount: string;
  provider_id?: string;
}): Promise<Tariff> {
  const res = await apiFetch("/tariffs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return (await res.json()) as Tariff;
}
