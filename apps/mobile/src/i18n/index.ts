// i18n scaffolding (base language: English). Full setup in VIS-19.
import en from "./en.json";

const dict: Record<string, string> = en;

export function t(key: string): string {
  return dict[key] ?? key;
}
