// Styled sign-in card (fix/styling). Wraps the existing auth store flow.
import { FormEvent, useState } from "react";
import { IconActivity } from "../../components/icons";
import { signIn } from "../../store";

export function LoginForm(): JSX.Element {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent): Promise<void> {
    e.preventDefault();
    setBusy(true);
    setError(false);
    try {
      await signIn(email, password);
    } catch {
      setError(true);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-wrap">
      <form className="card card-pad login-card" onSubmit={onSubmit}>
        <div className="brand">
          <span className="brand-logo"><IconActivity style={{ width: 18, height: 18 }} /></span>
          <span className="brand-name">Visitor</span>
        </div>
        <p className="page-sub" style={{ textAlign: "center", marginTop: 0, marginBottom: 18 }}>
          Sign in to your account
        </p>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="username" />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" />
        </div>
        {error && <p style={{ color: "var(--red-text)", fontSize: 13, margin: "0 0 10px" }}>Incorrect email or password</p>}
        <button className="btn btn-primary" style={{ width: "100%", justifyContent: "center" }} disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
