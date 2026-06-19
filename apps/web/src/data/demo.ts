// Demo dataset (fix/styling) mirroring the approved web_screens mockups so each
// view renders fully populated for design review even without the API running.
// Pages that have a live API still fetch; this is the fallback/seed shape.

export const AVATAR_COLORS = ["ava-blue", "ava-green", "ava-pink", "ava-purple", "ava-amber", "ava-gray"];
export const initials = (name: string): string =>
  name.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase();
export const colorFor = (seed: string): string =>
  AVATAR_COLORS[seed.charCodeAt(0) % AVATAR_COLORS.length];

export const dashboardKpis = [
  { label: "Today's Visits", value: "24", delta: "+8%", deltaKind: "up", sub: "vs last week" },
  { label: "Active Patients", value: "186", delta: "+3%", deltaKind: "up", sub: "This month" },
  { label: "Employees On Duty", value: "12", delta: "4 available", deltaKind: "info", sub: "Right now" },
  { label: "Incidents", value: "3", delta: "-15%", deltaKind: "up", sub: "This week" },
];

export const todaySchedule = [
  { time: "08:00 AM", name: "Martha Williams", service: "Physical Therapy", status: "Completed", kind: "green" },
  { time: "09:30 AM", name: "Robert Chen", service: "General Checkup", status: "In Progress", kind: "blue" },
  { time: "11:00 AM", name: "Eleanor Thompson", service: "Medication Review", status: "Scheduled", kind: "gray" },
  { time: "01:00 PM", name: "James Morrison", service: "Wound Care", status: "Scheduled", kind: "gray" },
];

export const recentAlerts = [
  { icon: "alert", color: "amber", title: "Visit #1842 not finalized", body: "Employee forgot to mark completion — auto-closed", time: "12 min ago" },
  { icon: "x", color: "red", title: "Appointment cancelled", body: "Patricia Davis cancelled 3:00 PM visit", time: "28 min ago" },
  { icon: "file", color: "amber", title: "Certificate expiring soon", body: "Dr. Rodriguez — CPR cert expires in 5 days", time: "1 hr ago" },
];

export const recentActivity = [
  { color: "green", text: "Visit completed — Martha Williams", time: "9:15 AM" },
  { color: "blue", text: "Visit started — Robert Chen", time: "9:32 AM" },
  { color: "purple", text: "New patient registered — Luis Gomez", time: "8:45 AM" },
  { color: "amber", text: "Evaluation received — 4.8 stars", time: "Yesterday" },
];

export const mapPins = [
  { top: "16%", left: "29%", kind: "green" },
  { top: "12%", left: "40%", kind: "blue" },
  { top: "21%", left: "62%", kind: "amber" },
  { top: "47%", left: "52%", kind: "green" },
  { top: "57%", left: "32%", kind: "blue" },
  { top: "67%", left: "45%", kind: "green" },
  { top: "70%", left: "70%", kind: "red" },
];

export const patients = [
  { name: "Eleanor Thompson", age: 78, contact: "+1 (555) 234-5678", service: "Physical Therapy", last: "Jun 16, 2026", status: "Active", badge: "green" },
  { name: "Martha Williams", age: 82, contact: "+1 (555) 345-6789", service: "General Checkup", last: "Jun 16, 2026", status: "Active", badge: "green" },
  { name: "Robert Chen", age: 71, contact: "+1 (555) 456-7890", service: "Wound Care", last: "Jun 15, 2026", status: "Active", badge: "green" },
  { name: "James Morrison", age: 85, contact: "+1 (555) 567-8901", service: "Medication Review", last: "Jun 14, 2026", status: "Pending", badge: "amber" },
  { name: "Patricia Davis", age: 69, contact: "+1 (555) 678-9012", service: "Vital Signs", last: "Jun 13, 2026", status: "Active", badge: "green" },
  { name: "Luis Gomez", age: 74, contact: "+1 (555) 789-0123", service: "Physical Therapy", last: "Jun 12, 2026", status: "Active", badge: "green" },
  { name: "Anna Park", age: 88, contact: "+1 (555) 890-1234", service: "Urgent Care", last: "Jun 11, 2026", status: "Critical", badge: "red" },
  { name: "Samuel Kim", age: 76, contact: "+1 (555) 901-2345", service: "General Checkup", last: "Jun 10, 2026", status: "Inactive", badge: "gray" },
];

export const patientDetail = {
  name: "Eleanor Thompson", age: 78, status: "Active",
  phone: "+1 (555) 234-5678", email: "eleanor.t@email.com", address: "142 Oak Street, Apt 3B",
  service: "Physical Therapy", provider: "Dr. Sarah Martinez", insurance: "MediCare Plus #4582",
  next: { when: "Tomorrow, June 18 · 08:30 AM", what: "Physical Therapy — Dr. Sarah Martinez" },
  history: [
    { date: "Jun 16, 2026", time: "09:00 AM", service: "Physical Therapy", provider: "Dr. Martinez", status: "Completed", badge: "green", rating: "4.8" },
    { date: "Jun 12, 2026", time: "10:30 AM", service: "General Checkup", provider: "Dr. Rodriguez", status: "Completed", badge: "green", rating: "5.0" },
    { date: "Jun 8, 2026", time: "09:00 AM", service: "Physical Therapy", provider: "Dr. Martinez", status: "Completed", badge: "green", rating: "4.5" },
    { date: "Jun 4, 2026", time: "02:00 PM", service: "Medication Review", provider: "Dr. Martinez", status: "Incident", badge: "amber", rating: "—" },
    { date: "May 30, 2026", time: "09:00 AM", service: "Physical Therapy", provider: "Dr. Martinez", status: "Completed", badge: "green", rating: "4.9" },
  ],
};

export const weekDays = [
  { dow: "MON", num: "16" }, { dow: "TUE", num: "17", today: true }, { dow: "WED", num: "18" },
  { dow: "THU", num: "19" }, { dow: "FRI", num: "20" }, { dow: "SAT", num: "21" }, { dow: "SUN", num: "22" },
];
export const weekEvents: { time: string; who: string; kind: string }[][] = [
  [{ time: "08:00", who: "M. Williams", kind: "green" }, { time: "10:30", who: "R. Chen", kind: "blue" }, { time: "14:00", who: "J. Morrison", kind: "blue" }],
  [{ time: "09:00", who: "E. Thompson", kind: "amber" }, { time: "13:00", who: "P. Davis", kind: "green" }],
  [{ time: "08:30", who: "L. Gomez", kind: "blue" }, { time: "11:00", who: "M. Williams", kind: "green" }, { time: "15:00", who: "A. Park", kind: "red" }, { time: "16:30", who: "R. Chen", kind: "blue" }],
  [{ time: "09:30", who: "J. Morrison", kind: "green" }, { time: "14:00", who: "S. Kim", kind: "blue" }],
  [{ time: "08:00", who: "P. Davis", kind: "blue" }, { time: "10:00", who: "E. Thompson", kind: "amber" }, { time: "13:30", who: "L. Gomez", kind: "blue" }],
  [{ time: "10:00", who: "M. Williams", kind: "gray" }],
  [],
];

export const employees = [
  { name: "Dr. Sarah Martinez", role: "Physical Therapist", status: "On Duty", st: "green", patients: 14, visits: "6 today", phone: "+1 (555) 111-2233", cert: "PT License · CPR" },
  { name: "Dr. Carlos Rodriguez", role: "General Practitioner", status: "On Duty", st: "green", patients: 22, visits: "4 today", phone: "+1 (555) 222-3344", cert: "MD License · BLS" },
  { name: "Maria Lopez", role: "Registered Nurse", status: "Available", st: "blue", patients: 18, visits: "0 today", phone: "+1 (555) 333-4455", cert: "RN License · ACLS" },
  { name: "James Wilson", role: "Wound Care Specialist", status: "On Duty", st: "green", patients: 9, visits: "3 today", phone: "+1 (555) 444-5566", cert: "WCC · CPR" },
  { name: "Emily Chang", role: "Medication Specialist", status: "Off Duty", st: "gray", patients: 16, visits: "— today", phone: "+1 (555) 555-6677", cert: "PharmD · BLS" },
  { name: "David Okafor", role: "Physical Therapist", status: "On Leave", st: "amber", patients: 11, visits: "— today", phone: "+1 (555) 666-7788", cert: "PT License · CPR" },
];
export const employeeTabs = [
  { label: "All Employees", count: 32 }, { label: "On Duty", count: 12 },
  { label: "Available", count: 8 }, { label: "Off Duty", count: 10 }, { label: "On Leave", count: 2 },
];

export const providers = [
  { name: "HealthFirst Agency", contact: "Linda Carter", type: "Coordinator", clients: 28, contract: "Annual", status: "Active", badge: "green" },
  { name: "CareLink Solutions", contact: "Marco Rivera", type: "Provider", clients: 15, contract: "Per Service", status: "Active", badge: "green" },
  { name: "HomeWell Partners", contact: "Diana Shah", type: "Coordinator", clients: 22, contract: "Annual", status: "Active", badge: "green" },
  { name: "MedVisit Group", contact: "Thomas Klein", type: "Provider", clients: 9, contract: "Monthly", status: "Pending", badge: "amber" },
  { name: "Senior Care Corp", contact: "Aisha Patel", type: "Provider", clients: 18, contract: "Annual", status: "Active", badge: "green" },
  { name: "NurseConnect LLC", contact: "James Foster", type: "Coordinator", clients: 11, contract: "Per Service", status: "Active", badge: "green" },
  { name: "VitalAid Services", contact: "Rosa Hernandez", type: "Provider", clients: 7, contract: "Monthly", status: "Inactive", badge: "gray" },
  { name: "ElderCare Plus", contact: "Kevin Wu", type: "Coordinator", clients: 20, contract: "Annual", status: "Active", badge: "green" },
];

export const reports = [
  { icon: "clock", name: "Hours by Employee", desc: "Detailed breakdown of hours worked per employee by period and service type.", last: "Jun 12, 2026", cat: "Operational" },
  { icon: "financial", name: "Service Billing", desc: "Invoice summaries and billing details for all completed patient services.", last: "Jun 10, 2026", cat: "Financial" },
  { icon: "financial", name: "Pension Report", desc: "Employee pension contributions and employer matching calculations.", last: "Jun 8, 2026", cat: "Financial" },
  { icon: "shield", name: "Patient Incidents", desc: "Logged incidents, follow-up actions, and compliance documentation.", last: "Jun 5, 2026", cat: "Compliance" },
  { icon: "employees", name: "Employee Absenteeism", desc: "Absence tracking with reason codes, patterns, and impact analysis.", last: "Jun 3, 2026", cat: "Operational" },
  { icon: "providers", name: "Provider Services", desc: "Service volume and performance metrics grouped by healthcare provider.", last: "May 28, 2026", cat: "Operational" },
];

export const financialKpis = [
  { label: "Total Hours Worked", value: "1,842", delta: "+8%", deltaKind: "up", sub: "This period" },
  { label: "Gross Payroll", value: "$48.2K", delta: "+5%", deltaKind: "up", sub: "This period" },
  { label: "Pension Deductions", value: "$4.6K", delta: "+3%", deltaKind: "up", sub: "9.5% rate" },
  { label: "Mileage Allowance", value: "$2.1K", delta: "-2%", deltaKind: "down", sub: "This period" },
];
export const payroll = [
  { name: "María García", contract: "Full-Time", hours: 168, base: "$3,240", pension: "$308", vac: 2, sick: 0, mileage: "$145", net: "$2,787" },
  { name: "Carlos López", contract: "Part-Time", hours: 96, base: "$1,850", pension: "$176", vac: 1, sick: 1, mileage: "$82", net: "$1,592" },
  { name: "Ana Rodríguez", contract: "Full-Time", hours: 172, base: "$3,480", pension: "$331", vac: 3, sick: 0, mileage: "$210", net: "$2,939" },
  { name: "Pedro Martínez", contract: "Full-Time", hours: 160, base: "$3,100", pension: "$295", vac: 1, sick: 2, mileage: "$168", net: "$2,637" },
  { name: "Laura Sánchez", contract: "Contract", hours: 120, base: "$2,400", pension: "$228", vac: 0, sick: 0, mileage: "$95", net: "$2,077" },
  { name: "Diego Herrera", contract: "Full-Time", hours: 176, base: "$3,560", pension: "$338", vac: 2, sick: 1, mileage: "$192", net: "$3,024" },
];

export const nearbyVisits = [
  { name: "Robert Chen", service: "General Checkup", status: "In Progress", badge: "blue", time: "9:30 AM", who: "Dr. Martinez" },
  { name: "Eleanor Thompson", service: "Physical Therapy", status: "Scheduled", badge: "gray", time: "11:00 AM", who: "Dr. Rodriguez" },
  { name: "Anna Park", service: "Urgent Care", status: "Incident", badge: "amber", time: "10:15 AM", who: "M. Lopez" },
  { name: "James Morrison", service: "Wound Care", status: "Scheduled", badge: "gray", time: "1:00 PM", who: "J. Wilson" },
  { name: "Patricia Davis", service: "Vital Signs", status: "Completed", badge: "green", time: "2:30 PM", who: "Dr. Martinez" },
  { name: "Samuel Kim", service: "Checkup", status: "Cancelled", badge: "red", time: "3:00 PM", who: "E. Chang" },
];
