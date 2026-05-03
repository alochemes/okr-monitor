// /app/integrations — read-only landing showing connection status for
// every integration in the registry. Reads `web/public/integration_status.json`
// (written by scripts/daily_evening.py); falls back to registry-only
// rendering if the snapshot is missing.

import type { Metadata } from "next";
import Link from "next/link";
import fs from "node:fs/promises";
import path from "node:path";

import {
  ALL_INTEGRATIONS,
  KPI_SOURCES,
  OKR_SOURCES,
  STATUS_LABEL,
  WORK_EVENT_SOURCES,
  WORK_EVENT_SUBCATS,
  sortByStatus,
  type IntegrationEntry,
  type IntegrationStatus,
  type WorkEventSubcat,
} from "@/lib/integrations/registry";

export const metadata: Metadata = {
  title: "OKR Monitor — integrations",
  description: "Connection status for every supported integration.",
  robots: { index: false, follow: false },
};

export const dynamic = "force-dynamic";

// Snapshot shape — must match what scripts/daily_evening.py writes.
type LiveStatus = "connected" | "partial" | "error" | "stale" | "not_configured";

type LiveSourceRow = {
  category: string;
  kind: string;
  status: LiveStatus;
  last_sync_at: string | null;
  stats_24h: Record<string, number>;
  error: string | null;
};

type LiveSnapshot = {
  schema: 1;
  generated_at: string;
  workspace_slug: string;
  sources: LiveSourceRow[];
};

async function loadStatus(): Promise<LiveSnapshot | null> {
  const file = path.join(process.cwd(), "public", "integration_status.json");
  try {
    const raw = await fs.readFile(file, "utf-8");
    const parsed = JSON.parse(raw) as LiveSnapshot;
    if (parsed.schema !== 1) return null;
    return parsed;
  } catch {
    return null;
  }
}

function liveFor(
  snapshot: LiveSnapshot | null,
  entry: IntegrationEntry,
): LiveSourceRow | null {
  if (!snapshot) return null;
  return (
    snapshot.sources.find(
      (s) => s.kind === entry.key && s.category.startsWith(entry.category),
    ) ?? null
  );
}

function statusBadge(
  entry: IntegrationEntry,
  live: LiveSourceRow | null,
): { label: string; tone: string; dot: string } {
  // Live status from snapshot wins over registry status when present.
  if (live) {
    switch (live.status) {
      case "connected":
        return { label: "🟢 connected", tone: "text-verdict-on", dot: "bg-verdict-on" };
      case "partial":
        return { label: "🟡 partial", tone: "text-verdict-drift", dot: "bg-verdict-drift" };
      case "error":
        return { label: "🔴 error", tone: "text-verdict-off", dot: "bg-verdict-off" };
      case "stale":
        return { label: "🟠 stale", tone: "text-verdict-drift", dot: "bg-verdict-drift" };
      case "not_configured":
      default:
        return { label: "⚪ not configured", tone: "text-v2-muted", dot: "bg-v2-muted" };
    }
  }
  // Fall back to registry status — what we KNOW about the source even
  // when the snapshot is missing.
  const tones: Record<IntegrationStatus, { tone: string; dot: string }> = {
    shipped:     { tone: "text-verdict-on",    dot: "bg-verdict-on" },
    in_progress: { tone: "text-verdict-drift", dot: "bg-verdict-drift" },
    stub:        { tone: "text-v2-cyan",       dot: "bg-v2-cyan" },
    planned:     { tone: "text-v2-muted",      dot: "bg-v2-muted" },
    deferred:    { tone: "text-v2-muted",      dot: "bg-v2-muted" },
  };
  return { label: STATUS_LABEL[entry.status], ...tones[entry.status] };
}

function fmtDate(iso: string | null): string {
  if (!iso) return "never";
  return iso.replace("T", " ").slice(0, 19) + " UTC";
}

function IntegrationCard({
  entry,
  live,
}: {
  entry: IntegrationEntry;
  live: LiveSourceRow | null;
}) {
  const badge = statusBadge(entry, live);
  const eventsCount = live?.stats_24h
    ? Object.values(live.stats_24h).reduce((a, b) => a + b, 0)
    : 0;

  return (
    <div className="border border-v2-rule bg-v2-bg-card p-4 transition-colors hover:border-v2-rule-strong">
      <div className="flex items-baseline justify-between">
        <span className="font-sans text-[14px] font-medium text-v2-text">
          {entry.name}
        </span>
        <span className={`font-mono text-[10px] uppercase tracking-[0.14em] ${badge.tone}`}>
          <span className={`mr-1.5 inline-block h-1.5 w-1.5 ${badge.dot}`} aria-hidden />
          {badge.label}
        </span>
      </div>
      <dl className="mt-3 grid grid-cols-2 gap-x-4 gap-y-1.5 font-mono text-[10.5px] uppercase tracking-[0.14em] text-v2-muted">
        <dt>auth</dt>
        <dd className="text-right text-v2-text-dim">{entry.auth}</dd>
        <dt>last sync</dt>
        <dd className="text-right text-v2-text-dim">{fmtDate(live?.last_sync_at ?? null)}</dd>
        <dt>24h events</dt>
        <dd className="text-right text-v2-text-dim">{eventsCount || "—"}</dd>
      </dl>
      {live?.error && (
        <p className="mt-3 border-t border-v2-rule pt-3 font-mono text-[10.5px] text-verdict-off">
          {live.error.slice(0, 140)}
        </p>
      )}
    </div>
  );
}

function CategorySection({
  title,
  subtitle,
  entries,
  live,
}: {
  title: string;
  subtitle: string;
  entries: IntegrationEntry[];
  live: LiveSnapshot | null;
}) {
  return (
    <section className="mt-12">
      <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan">
        {title}
      </div>
      <p className="mt-3 max-w-[60ch] text-[13px] leading-[1.7] text-v2-text-dim">
        {subtitle}
      </p>
      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {sortByStatus(entries).map((e) => (
          <IntegrationCard key={`${e.category}-${e.key}`} entry={e} live={liveFor(live, e)} />
        ))}
      </div>
    </section>
  );
}

export default async function IntegrationsPage() {
  const snapshot = await loadStatus();

  const totals = {
    all: ALL_INTEGRATIONS.length,
    shipped: ALL_INTEGRATIONS.filter((e) => e.status === "shipped").length,
    stub: ALL_INTEGRATIONS.filter((e) => e.status === "stub").length,
    planned: ALL_INTEGRATIONS.filter((e) => e.status === "planned").length,
  };

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
            <Link href="/app/dashboard" className="hover:text-v2-cyan transition-colors">
              dashboard
            </Link>
            <span className="text-v2-text-dim">integrations</span>
            <Link href="/app/login" className="hover:text-v2-cyan transition-colors">
              sign_out
            </Link>
          </nav>
        </header>

        <section className="mt-10">
          <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan">
            [01] _ INTEGRATIONS
          </div>
          <h1 className="mt-3 font-sans font-medium leading-[1.05] tracking-tighter text-[clamp(28px,4vw,40px)] text-v2-text">
            Every tool, every flow, every customer.
          </h1>
          <p className="mt-3 max-w-[64ch] text-[14px] leading-[1.7] text-v2-text-dim">
            OKR Monitor reads from whatever stack you already run. We don&rsquo;t
            ask you to change tools. The matrix below covers OKR systems, code
            and ticket tools, docs, async chat, CRMs, and KPI dashboards. Any
            combination works.
          </p>

          <dl className="mt-8 grid grid-cols-2 gap-x-6 gap-y-4 sm:grid-cols-4">
            <Stat label="total" value={String(totals.all)} />
            <Stat label="shipped" value={String(totals.shipped)} />
            <Stat label="stubbed" value={String(totals.stub)} />
            <Stat label="planned" value={String(totals.planned)} />
          </dl>

          {!snapshot && (
            <p className="mt-8 border-l-2 border-v2-cyan-faint pl-4 font-mono text-[11px] uppercase tracking-[0.14em] text-v2-cyan">
              no live snapshot yet · status reflects the registry only · run{" "}
              <code className="text-v2-text-dim">python scripts/daily_evening.py</code>{" "}
              to populate
            </p>
          )}
        </section>

        <CategorySection
          title="[02] _ OKR_SOURCES"
          subtitle="Where the customer&rsquo;s OKRs live. The KR catalog the mapper maps work to. One source per workspace."
          entries={OKR_SOURCES}
          live={snapshot}
        />

        {WORK_EVENT_SUBCATS.map((sc) => (
          <CategorySection
            key={sc.key}
            title={`[03·${sc.key.toUpperCase()}] _ WORK_EVENTS · ${sc.name.toUpperCase()}`}
            subtitle={sc.q}
            entries={WORK_EVENT_SOURCES.filter((e) => e.subcat === sc.key)}
            live={snapshot}
          />
        ))}

        <CategorySection
          title="[04] _ KPI_SOURCES"
          subtitle="The metrics that should always be green. Distinct from OKRs &mdash; we alert on red, we don&rsquo;t weekly-review."
          entries={KPI_SOURCES}
          live={snapshot}
        />

        <footer className="mt-16 border-t border-v2-rule pt-6 font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted">
          design · {" "}
          <code className="text-v2-text-dim">notion/02_product/04_okr_source_integrations.md</code>
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
