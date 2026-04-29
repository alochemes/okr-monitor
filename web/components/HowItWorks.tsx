import { SectionHeading } from "./SectionHeading";

const STEPS = [
  {
    n: "01",
    verb: "Connect",
    title: "Plug in your OKR doc and the systems where work happens.",
    detail:
      "OAuth into GitHub, Linear or Jira, Slack, and Notion. We import your quarterly OKRs from your existing source — Notion, Asana, Mooncamp, or a CSV. No re-typing.",
    timing: "Time to first integration: under 4 minutes.",
    code: ["github :: 412 commits / 30d", "linear :: 218 issues / 30d", "slack  :: 14 channels indexed"],
  },
  {
    n: "02",
    verb: "Map",
    title: "Every commit, ticket, and thread gets tied to a KR — with calibrated confidence.",
    detail:
      "OKR-Mapper reads each work event and decides which KR(s) it advances. Confident mappings only — anything below 0.5 confidence is dropped, not faked. We measure ourselves: target ≥85% precision @ ≥70% recall on a labeled set.",
    timing: "First sweep: ≈ 6 minutes for 90 days of history.",
    code: [
      'event :: "fix(perf): tune redis pipeline"',
      "→ KR-1 (latency)  conf 0.92",
      'event :: "Slack: pricing call w/ Chime"',
      "→ KR-2 (pilots)   conf 0.81",
    ],
  },
  {
    n: "03",
    verb: "Narrate",
    title: "Friday at 9 AM, a one-page brief. Verdict per KR. Specific citations.",
    detail:
      "Not a dashboard. A reading. The Narrative agent synthesizes the week — which KRs are on track, which are drifting, which are off — and ends with one paragraph on what to do Monday. Built to be screenshotted into the CEO Slack.",
    timing: "Read time: < 3 minutes.",
    code: [
      "▌ KR-1  on track    7d events: 24",
      "▌ KR-2  drifting    7d events:  4",
      "▌ KR-3  off         7d events:  0",
      "  → reallocate or restate",
    ],
  },
];

export function HowItWorks() {
  return (
    <section id="how" className="border-b border-rule bg-paper-deep/40">
      <div className="mx-auto max-w-page px-6 py-24 lg:px-10 lg:py-32">
        <SectionHeading
          number="03"
          label="The Mechanism"
          title={
            <>
              Three steps. <span className="italic">No new process.</span>{" "}
              No standup to attend.
            </>
          }
          kicker="The product reads the work that already exists. You don't change how your team operates."
        />

        <div className="mt-16 space-y-16 lg:space-y-20">
          {STEPS.map((s) => (
            <div
              key={s.n}
              className="grid grid-cols-1 gap-10 border-t border-rule-strong/70 pt-8 lg:grid-cols-12 lg:gap-12"
            >
              {/* Number + verb column */}
              <div className="lg:col-span-3">
                <div className="font-mono text-[11px] tracking-label text-persimmon">
                  STEP {s.n}
                </div>
                <div className="mt-2 font-display text-[42px] font-semibold leading-none tracking-tighter text-ink">
                  {s.verb}.
                </div>
                <div className="mt-4 font-mono text-[12px] text-muted">
                  {s.timing}
                </div>
              </div>

              {/* Body column */}
              <div className="lg:col-span-5">
                <h3 className="font-display text-[24px] leading-[1.2] tracking-editorial text-ink">
                  {s.title}
                </h3>
                <p className="mt-4 max-w-[55ch] text-[15.5px] leading-[1.65] text-ink-soft">
                  {s.detail}
                </p>
              </div>

              {/* Code excerpt — the artifact */}
              <div className="lg:col-span-4">
                <div className="rounded-none border border-rule-strong/70 bg-paper p-5">
                  <div className="mb-3 flex items-center justify-between">
                    <span className="label-ink !text-muted">trace</span>
                    <span className="font-mono text-[10px] text-muted">
                      live sample
                    </span>
                  </div>
                  <pre className="overflow-x-auto whitespace-pre font-mono text-[12.5px] leading-[1.7] text-ink-soft">
                    {s.code.join("\n")}
                  </pre>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
