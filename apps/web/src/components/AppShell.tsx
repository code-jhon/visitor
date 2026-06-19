// Application shell (fix/styling): fixed sidebar navigation + top bar, matching
// the approved web_screens mockups. Wraps every authenticated page.
import { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import {
  IconActivity, IconBell, IconCalendar, IconDashboard, IconEmployees,
  IconFinancial, IconHeart, IconMap, IconMessages, IconProviders, IconReports,
  IconSearch, IconSettings, IconSupport,
} from "./icons";

const NAV = [
  { to: "/", label: "Dashboard", icon: IconDashboard, end: true },
  { to: "/employees", label: "Employees", icon: IconEmployees },
  { to: "/patients", label: "Patients", icon: IconHeart },
  { to: "/providers", label: "Providers", icon: IconProviders },
  { to: "/scheduling", label: "Scheduling", icon: IconCalendar },
  { to: "/visit-map", label: "Visit Map", icon: IconMap },
  { to: "/reports", label: "Reports", icon: IconReports },
  { to: "/financial", label: "Financial", icon: IconFinancial },
  { to: "/configuration", label: "Configuration", icon: IconSettings },
];

export function Sidebar(): JSX.Element {
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-logo"><IconActivity style={{ width: 18, height: 18 }} /></span>
        <span className="brand-name">Visitor</span>
      </div>
      <nav className="nav">
        {NAV.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => "nav-item" + (isActive ? " active" : "")}
          >
            <Icon />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="nav nav-section">
        <NavLink to="/messages" className="nav-item"><IconMessages /><span>Messages</span></NavLink>
        <NavLink to="/support" className="nav-item"><IconSupport /><span>Support</span></NavLink>
      </div>
    </aside>
  );
}

interface TopbarProps {
  title: string;
  subtitle?: string;
  search?: string;
  actions?: ReactNode;
}

export function Topbar({ title, subtitle, search = "Search…", actions }: TopbarProps): JSX.Element {
  return (
    <header className="topbar">
      <div>
        <h1 className="page-title">{title}</h1>
        {subtitle && <p className="page-sub">{subtitle}</p>}
      </div>
      <div className="topbar-actions">
        {actions}
        <div className="search"><IconSearch style={{ width: 16, height: 16 }} /><input placeholder={search} aria-label="Search" /></div>
        <button className="icon-btn" aria-label="Notifications"><IconBell style={{ width: 18, height: 18 }} /></button>
        <div className="avatar">SA</div>
      </div>
    </header>
  );
}

export function AppShell({
  title, subtitle, search, actions, children,
}: TopbarProps & { children: ReactNode }): JSX.Element {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main">
        <Topbar title={title} subtitle={subtitle} search={search} actions={actions} />
        <div className="content">{children}</div>
      </div>
    </div>
  );
}

// Small shared building blocks ------------------------------------------------
export function Badge({ kind, children }: { kind: string; children: ReactNode }): JSX.Element {
  return <span className={`badge ${kind}`}>{children}</span>;
}

export function Avatar({ initials, color = "ava-blue" }: { initials: string; color?: string }): JSX.Element {
  return <span className={`ava-sm ${color}`}>{initials}</span>;
}

export function Kpi({
  label, value, delta, deltaKind = "up", sub,
}: { label: string; value: string; delta?: string; deltaKind?: string; sub?: string }): JSX.Element {
  return (
    <div className="card kpi">
      <div className="kpi-head">
        <span className="kpi-label">{label}</span>
        {delta && <span className={`delta ${deltaKind}`}>{delta}</span>}
      </div>
      <div className="kpi-value">{value}</div>
      {sub && <div className="kpi-sub">{sub}</div>}
    </div>
  );
}
