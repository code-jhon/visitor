import { useEffect, useState } from "react";
import { getHealth } from "./api/client";
import { t } from "./i18n";

export function App(): JSX.Element {
  const [status, setStatus] = useState<string>("...");

  useEffect(() => {
    getHealth()
      .then((h) => setStatus(h.status))
      .catch(() => setStatus("unreachable"));
  }, []);

  return (
    <main style={{ fontFamily: "sans-serif", padding: 24 }}>
      <h1>{t("app.title")}</h1>
      <p>
        {t("app.apiStatus")}: <strong>{status}</strong>
      </p>
    </main>
  );
}
