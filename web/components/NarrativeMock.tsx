// A styled mock of the Friday "Weekly Executive Brief" — designed to feel
// like a printed artifact, not a screenshot. Tells the product story by
// being the product output.

type Verdict = "on_track" | "drifting" | "off";

interface KrRow {
  id: string;
  verdict: Verdict;
  events_7d: number;
  title: string;
  cited?: string;
  note?: string;
}

const ROWS: KrRow[] = [
  {
    id: "KR-1",
    verdict: "on_track",
    events_7d: 24,
    title: "Reduce p95 API latency to <150ms",
    cited: "fix(perf): tune redis pipeline, drop p95 to 138ms",
  },
  {
    id: "KR-2",
    verdict: "drifting",
    events_7d: 4,
    title: "Land 5 enterprise pilots by EOQ",
    note: "no new pilots since Apr 12; 1 booked Q1 carryover",
  },
  {
    id: "KR-3",
    verdict: "off",
    events_7d: 0,
    title: "Reach 80 NPS in dashboard surface",
    note: "no work tied this quarter — restate or reassign",
  },
  {
    id: "KR-4",
    verdict: "on_track",
    events_7d: 18,
    title: "Ship onboarding v2 (≤4 min to first value)",
    cited: "feat(onboarding): replace tour with empty-state cards",
  },
];

const verdictMap: Record<Verdict, { label: string; className: string; mark: string }> = {
  on_track: { label: "ON TRACK", className: "text-verdict-on", mark: "●" },
  drifting: { label: "DRIFTING", className: "text-verdict-drift", mark: "◐" },
  off:      { label: "OFF",      className: "text-verdict-off",  mark: "○" },
};

export function NarrativeMock({ className = "" }: { className?: string }) {
  return (
    <div
      className={`memo relative font-mono text-[12.5px] leading-[1.55] text-ink ${className}`}
      role="figure"
      aria-label="Sample weekly executive brief"
    >
      {/* Hatched corner — editorial flourish */}
      <div className="memo-corner absolute right-0 top-0 h-12 w-12 opacity-30" />

      <div className="px-6 py-7 sm:px-9 sm:py-9">
        {/* Header */}
        <div className="flex items-baseline justify-between border-b border-rule-strong/80 pb-3">
          <div className="font-sans text-[10px] tracking-label font-semibold text-ink">
            WEEKLY EXECUTIVE BRIEF
          </div>
          <div className="font-sans text-[10px] tracking-label text-muted">
            WEEK 17 / 2026
          </div>
        </div>
        <div className="flex items-baseline justify-between pt-2 pb-5 text-[11px] uppercase tracking-[0.16em] text-muted">
          <span>Acme Inc · Series B SaaS · 142 employees</span>
          <span>generated fri 9:01 AM PT</span>
        </div>

        {/* Verdict statement — the lede */}
        <div className="mb-6">
          <div className="label-ink mb-2">Verdict</div>
          <p className="font-display text-[19px] leading-[1.45] tracking-editorial text-ink">
            Three of seven KRs at risk this quarter. Engineering shipped 80%
            of work against KR-1; Customer Success shipped 0% against KR-3.
            <span className="text-persimmon"> Reallocate or restate.</span>
          </p>
        </div>

        {/* Per-KR table */}
        <div className="space-y-0">
          <div className="grid grid-cols-[60px_84px_44px_1fr] gap-3 border-y border-rule-strong/70 py-1.5 font-sans text-[10px] tracking-label font-semibold text-ink-soft">
            <span>KR</span>
            <span>Verdict</span>
            <span className="text-right">7d</span>
            <span>Title / Citation</span>
          </div>

          {ROWS.map((r, i) => {
            const v = verdictMap[r.verdict];
            return (
              <div
                key={r.id}
                className={`grid grid-cols-[60px_84px_44px_1fr] gap-3 py-3 ${
                  i < ROWS.length - 1 ? "border-b border-rule" : ""
                }`}
              >
                <span className="font-mono font-semibold text-ink">{r.id}</span>
                <span className={`flex items-center gap-1.5 font-sans text-[10px] tracking-label font-semibold ${v.className}`}>
                  <span aria-hidden="true">{v.mark}</span>
                  {v.label}
                </span>
                <span className="text-right text-muted">{r.events_7d}</span>
                <span>
                  <div className="font-sans text-[13px] text-ink">{r.title}</div>
                  {r.cited && (
                    <div className="mt-0.5 text-muted">
                      <span className="text-ink-soft">cited:</span>{" "}
                      <span className="font-mono">{r.cited}</span>
                    </div>
                  )}
                  {r.note && (
                    <div className="mt-0.5 italic text-muted">{r.note}</div>
                  )}
                </span>
              </div>
            );
          })}
        </div>

        {/* Footer instruction line */}
        <div className="mt-6 border-t border-rule-strong/70 pt-3">
          <div className="label-ink mb-1.5">Action this week</div>
          <p className="font-display text-[14.5px] leading-[1.55] tracking-editorial text-ink-soft">
            Move two engineers from KR-1 to KR-3, or formally close KR-3 with
            a written rationale. The current allocation cannot hit both.
          </p>
        </div>
      </div>
    </div>
  );
}
