import type { Metadata } from "next";
import Link from "next/link";
import fs from "node:fs/promises";
import path from "node:path";

export const metadata: Metadata = {
  title: "OKR Monitor — dashboard",
  description: "Real-time KR scoreboard sourced from the daily report.",
  robots: { index: false, follow: false },
};

// Re-read the snapshot on every request rather than at build. The file is
// rewritten by scripts/daily_evening.py so the dashboard tracks the latest
// daily run without needing a deploy.
export const dynamic = "force-dynamic";

type Verdict =
  | "on_track"
  | "active"
  | "drifting"
  | "stale"
  | "off"
  | "qualitative";

type KrRow = {
  kr_id: string;
  computed_at: string;
  events_total: number;
  events_7d: number;
  events_30d: number;
  distinct_actors: number;
  last_event_at: string | null;
  mean_confidence: number | null;
  target_raw: string | null;
  target_numeric: number | null;
  current_numeric: number | null;
  due_date: string | null;
  days_remaining: number | null;
  pace_per_day: number | null;
  pace_required: number | null;
  forecast_verdict: Verdict;
  forecast_p_hit: number | null;
};

type Snapshot = {
  schema: 1;
  generated_at: string;
  report_date: string;
  totals: {
    krs: number;
    events_today: number;
    mappings_today: number;
    proposals_today: number;
    spend_today_usd: number;
  };
  krs: KrRow[];
};

async function loadSnapshot(): Promise<Snapshot | null> {
  const file = path.join(process.cwd(), "public", "kr_signals.json");
  try {
    const raw = await fs.readFile(file, "utf-8");
    const parsed = JSON.parse(raw) as Snapshot;
    if (parsed.schema !== 1) return null;
    return parsed;
  } catch {
    return null;
  }
}

const VERDICT_STYLE: Record<Verdict, { dot: string; label: string; tone: string }> = {
  on_track:    { dot: "bg-verdict-on",    label: "on_track",    tone: "text-verdict-on" },
  active:      { dot: "bg-verdict-on",    label: "active",      tone: "text-verdict-on" },
  drifting:    { dot: "bg-verdict-drift", label: "drifting",    tone: "text-verdict-drift" },
  stale:       { dot: "bg-verdict-drift", label: "stale",       tone: "text-verdict-drift" },
  off:         { dot: "bg-verdict-off",   label: "off",         tone: "text-verdict-off" },
  qualitative: { dot: "bg-v2-muted",      label: "qualitative", tone: "text-v2-muted" },
};

function fmt(n: number | null, digits = 2): string {
  if (n === null || n === undefined) return "—";
  if (Math.abs(n) >= 100) return n.toFixed(0);
  return n.toFixed(digits).replace(/\.?0+$/, "");
}

function fmtDate(iso: string | null): string {
  if (!iso) return "—";
  return iso.slice(0, 10);
}

export default async function DashboardPage() {
  const snap = await loadSnapshot();

  if (!snap) {
    return <SnapshotMissing />;
  }

  // Verdict roll-up for the chip strip.
  const counts: Record<string, number> = {};
  for (const r of snap.krs) {
    const v = r.forecast_verdict || "qualitative";
    counts[v] = (counts[v] || 0) + 1;
  }
  const verdictOrder: Verdict[] = ["on_track", "active", "drifting", "stale", "off", "qualitative"];

  return (
    <main className="min-h-screen bg-v2-bg text-v2-text font-sans">
      <div className="mx-auto max-w-page px-6 py-10 lg:px-10">
        <header className="flex flex-wrap items-baseline justify-between gap-y-3">
          <Link
            href="/"
            className="font-mono text-[11px] uppercase tracking-[0.22em] text-v2-cyan hover:text-v2-text transition-colors"
          >
            OKR_Monitor
          </Link>
          <nav className="flex items-center gap-6 font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted">
            <span className="text-v2-text-dim">dashboard</span>
            <Link href="/app/login" className="hover:text-v2-cyan transition-colors">
              sign_out
            </Link>
          </nav>
        </header>

        <section className="mt-10">
          <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan">
            [01] _ SCOREBOARD
          </div>
          <h1 className="mt-3 font-sans font-medium leading-[1.05] tracking-tighter text-[clamp(28px,4vw,40px)] text-v2-text">
            17 KRs, in real time.
          </h1>
          <p className="mt-3 max-w-[60ch] text-[14px] leading-[1.7] text-v2-text-dim">
            Snapshot from the daily 7pm OWNER/FINANCE report. The same data
            the operator sees in their inbox, rendered as a scoreboard. This
            is the dogfood view &mdash; in pilot, it&rsquo;s your KRs.
          </p>

          <dl className="mt-8 grid grid-cols-2 gap-x-6 gap-y-4 sm:grid-cols-4 lg:grid-cols-5">
            <Stat label="krs" value={String(snap.totals.krs)} />
            <Stat label="events_today" value={String(snap.totals.events_today)} />
            <Stat label="mappings_today" value={String(snap.totals.mappings_today)} />
            <Stat label="proposals_today" value={String(snap.totals.proposals_today)} />
            <Stat label="spend_today" value={`$${snap.totals.spend_today_usd.toFixed(2)}`} />
          </dl>

          <div className="mt-8 flex flex-wrap gap-2">
            {verdictOrder
              .filter((v) => counts[v])
              .map((v) => (
                <span
                  key={v}
                  className={`inline-flex items-center gap-2 border border-v2-rule-strong bg-v2-bg-card px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.14em] ${VERDICT_STYLE[v].tone}`}
                >
                  <span
                    className={`inline-block h-1.5 w-1.5 ${VERDICT_STYLE[v].dot}`}
                    aria-hidden
                  />
                  {counts[v]} {VERDICT_STYLE[v].label}
                </span>
              ))}
          </div>
        </section>

        <section className="mt-12">
          <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan">
            [02] _ KR_TABLE
          </div>
          <div className="mt-4 overflow-x-auto border border-v2-rule">
            <table className="w-full border-collapse text-left text-[13px]">
              <thead className="bg-v2-bg-elev">
                <tr className="font-mono text-[10px] uppercase tracking-[0.16em] text-v2-muted">
                  <th className="border-b border-v2-rule px-4 py-3">kr</th>
                  <th className="border-b border-v2-rule px-4 py-3">verdict</th>
                  <th className="border-b border-v2-rule px-4 py-3 text-right">7d</th>
                  <th className="border-b border-v2-rule px-4 py-3 text-right">30d</th>
                  <th className="border-b border-v2-rule px-4 py-3 text-right">all</th>
                  <th className="border-b border-v2-rule px-4 py-3 text-right">target</th>
                  <th className="border-b border-v2-rule px-4 py-3 text-right">current</th>
                  <th className="border-b border-v2-rule px-4 py-3 text-right">due</th>
                  <th className="border-b border-v2-rule px-4 py-3 text-right">days_left</th>
                  <th className="border-b border-v2-rule px-4 py-3 text-right">need/d</th>
                </tr>
              </thead>
              <tbody className="font-mono text-[12.5px]">
                {snap.krs.map((r) => {
                  const v = r.forecast_verdict || "qualitative";
                  const style = VERDICT_STYLE[v];
                  return (
                    <tr key={r.kr_id} className="border-t border-v2-rule">
                      <td className="px-4 py-3 text-v2-text">KR {r.kr_id}</td>
                      <td className="px-4 py-3">
                        <span className={`inline-flex items-center gap-2 ${style.tone}`}>
                          <span
                            className={`inline-block h-1.5 w-1.5 ${style.dot}`}
                            aria-hidden
                          />
                          {style.label}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right text-v2-text-dim">{r.events_7d}</td>
                      <td className="px-4 py-3 text-right text-v2-text-dim">{r.events_30d}</td>
                      <td className="px-4 py-3 text-right text-v2-text-dim">{r.events_total}</td>
                      <td className="px-4 py-3 text-right text-v2-text-dim">
                        {r.target_numeric === null ? r.target_raw ?? "—" : fmt(r.target_numeric, 0)}
                      </td>
                      <td className="px-4 py-3 text-right text-v2-text-dim">
                        {fmt(r.current_numeric, 0)}
                      </td>
                      <td className="px-4 py-3 text-right text-v2-text-dim">{fmtDate(r.due_date)}</td>
                      <td className="px-4 py-3 text-right text-v2-text-dim">
                        {r.days_remaining === null ? "—" : r.days_remaining}
                      </td>
                      <td className="px-4 py-3 text-right text-v2-text-dim">
                        {fmt(r.pace_required)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <p className="mt-3 font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted">
            snapshot · {fmtDate(snap.report_date)} · generated {snap.generated_at.replace("T", " ").slice(0, 19)} UTC
          </p>
        </section>

        <section className="mt-12 border-t border-v2-rule pt-8">
          <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan">
            [03] _ NEXT
          </div>
          <p className="mt-3 max-w-[60ch] text-[14px] leading-[1.7] text-v2-text-dim">
            Sprint 0 stub. The Friday brief, weekly narrative, and the per-KR
            event drill-down all land in Sprint 1. For now, this scoreboard
            mirrors the dashboard markdown that ships with the daily email.
          </p>
        </section>

        <footer className="mt-12 border-t border-v2-rule pt-5 font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted">
          © 2026 OKR Monitor · data stays in your tenant · no training
        </footer>
      </div>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted">
        {label}
      </dt>
      <dd className="mt-1 font-sans text-[28px] font-medium leading-tight tracking-tight text-v2-text">
        {value}
      </dd>
    </div>
  );
}

function SnapshotMissing() {
  return (
    <main className="min-h-screen bg-v2-bg text-v2-text font-sans">
      <div className="mx-auto max-w-page px-6 py-10 lg:px-10">
        <Link
          href="/"
          className="font-mono text-[11px] uppercase tracking-[0.22em] text-v2-cyan hover:text-v2-text transition-colors"
        >
          OKR_Monitor
        </Link>
        <section className="mt-20">
          <div className="font-mono text-[10px] tracking-[0.22em] text-verdict-off">
            [!] _ NO_SNAPSHOT
          </div>
          <h1 className="mt-3 font-sans font-medium leading-[1.05] tracking-tighter text-[clamp(28px,4vw,40px)] text-v2-text">
            No snapshot yet.
          </h1>
          <p className="mt-3 max-w-[60ch] text-[14px] leading-[1.7] text-v2-text-dim">
            The dashboard reads <code className="font-mono text-v2-cyan">web/public/kr_signals.json</code>,
            which is rewritten by <code className="font-mono text-v2-cyan">scripts/daily_evening.py</code>.
            Run it once to populate the file:
          </p>
          <pre className="mt-5 overflow-x-auto border border-v2-rule bg-v2-bg-card p-4 font-mono text-[12px] text-v2-cyan">
            {`OKR_MONITOR_DRY_RUN=true python scripts/daily_evening.py --no-email`}
          </pre>
        </section>
      </div>
    </main>
  );
}
