import { useEffect, useState } from "react";
import { getHealth } from "./api/client";
import { LoginForm } from "./features/auth/LoginForm";
import { AuditLog } from "./pages/AuditLog";
import { Dashboard } from "./pages/Dashboard";
import { Employees } from "./pages/Employees";
import { Patients } from "./pages/Patients";
import { AuthState, getAuthState, signOut, subscribe } from "./store";
import { t } from "./i18n";

export function App(): JSX.Element {
  const [status, setStatus] = useState<string>("...");
  const [auth, setAuth] = useState<AuthState>(getAuthState());

  useEffect(() => {
    getHealth()
      .then((h) => setStatus(h.status))
      .catch(() => setStatus("unreachable"));
    return subscribe(setAuth);
  }, []);

  return (
    <main style={{ fontFamily: "sans-serif", padding: 24 }}>
      <h1>{t("app.title")}</h1>
      <p>
        {t("app.apiStatus")}: <strong>{status}</strong>
      </p>
      {auth.status === "authenticated" && auth.user ? (
        <section>
          <p>
            {t("auth.signedInAs")}: <strong>{auth.user.email}</strong> (
            {auth.user.roles.map((r) => r.name).join(", ")})
          </p>
          <button onClick={signOut}>{t("auth.signOut")}</button>
          <AuditLog />
          <Dashboard />
          <Employees />
          <Patients />
        </section>
      ) : (
        <LoginForm />
      )}
    </main>
  );
}
