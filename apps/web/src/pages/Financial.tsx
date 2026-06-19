// Financial — payroll liquidations, KPIs + table, matching the mockup.
import { AppShell, Kpi } from "../components/AppShell";
import { IconPlus } from "../components/icons";
import { financialKpis, payroll } from "../data/demo";

export function Financial(): JSX.Element {
  return (
    <AppShell
      title="Financial"
      subtitle="Payroll liquidations and calculations"
      actions={<>
        <button className="btn">Jun 1 – Jun 15, 2026 ▾</button>
        <button className="btn btn-primary"><IconPlus /> Generate Liquidation</button>
      </>}
    >
      <div className="grid grid-4">
        {financialKpis.map((k) => <Kpi key={k.label} {...k} />)}
      </div>

      <div className="card mt-16">
        <table className="table">
          <thead>
            <tr>
              <th>Employee</th><th>Contract</th><th>Hours</th><th>Base Pay</th>
              <th>Pension</th><th>Vacation</th><th>Sick</th><th>Mileage</th><th>Net Pay</th>
            </tr>
          </thead>
          <tbody>
            {payroll.map((r) => (
              <tr key={r.name}>
                <td style={{ fontWeight: 600 }}>{r.name}</td>
                <td className="muted">{r.contract}</td>
                <td>{r.hours}</td>
                <td>{r.base}</td>
                <td className="muted">{r.pension}</td>
                <td className="muted">{r.vac}</td>
                <td className="muted">{r.sick}</td>
                <td className="muted">{r.mileage}</td>
                <td style={{ fontWeight: 700 }}>{r.net}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="pagination" style={{ padding: "14px 16px" }}>
          <span>Showing 1–6 of 24 employees</span>
          <div className="pager">
            <button>‹</button><button className="active">1</button><button>2</button><button>3</button><button>4</button><button>›</button>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
