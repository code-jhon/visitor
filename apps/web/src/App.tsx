// App routing (fix/styling). Each page renders inside the shared AppShell
// (sidebar + topbar). For visual review on this branch the routes are reachable
// directly; the auth gate (LoginForm / store) remains available at /login and
// is re-applied when the backend is wired in.
import { Route, Routes } from "react-router-dom";
import { AuditLog } from "./pages/AuditLog";
import { Configuration } from "./pages/Configuration";
import { Dashboard } from "./pages/Dashboard";
import { Employees } from "./pages/Employees";
import { Financial } from "./pages/Financial";
import { Patients } from "./pages/Patients";
import { PatientDetail } from "./pages/PatientDetail";
import { Providers } from "./pages/Providers";
import { Reports } from "./pages/Reports";
import { Schedule } from "./pages/Schedule";
import { VisitMap } from "./pages/VisitMap";
import { LoginForm } from "./features/auth/LoginForm";

export function App(): JSX.Element {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/employees" element={<Employees />} />
      <Route path="/patients" element={<Patients />} />
      <Route path="/patients/:id" element={<PatientDetail />} />
      <Route path="/providers" element={<Providers />} />
      <Route path="/scheduling" element={<Schedule />} />
      <Route path="/visit-map" element={<VisitMap />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/financial" element={<Financial />} />
      <Route path="/configuration" element={<Configuration />} />
      <Route path="/audit" element={<AuditLog />} />
      <Route path="/login" element={<LoginForm />} />
      <Route path="*" element={<Dashboard />} />
    </Routes>
  );
}
