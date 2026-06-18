import { FormEvent, useState } from "react";
import { signIn } from "../../store";
import { t } from "../../i18n";

/** Email/password login form (VIS-2). On success the auth store flips to
 * "authenticated" and the app re-renders the dashboard. */
export function LoginForm(): JSX.Element {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit(e: FormEvent): Promise<void> {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await signIn(email, password);
    } catch {
      setError(t("auth.invalidCredentials"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} style={{ display: "grid", gap: 12, maxWidth: 320 }}>
      <h2>{t("auth.signIn")}</h2>
      <label>
        {t("auth.email")}
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </label>
      <label>
        {t("auth.password")}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </label>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      <button type="submit" disabled={submitting}>
        {submitting ? t("auth.signingIn") : t("auth.signIn")}
      </button>
    </form>
  );
}
