import { SectionLabelV2 } from "./SectionLabelV2";

const STEPS = [
  {
    n: "01",
    verb: "CONNECT",
    title: "Plug the systems where work already happens",
    detail:
      "OAuth into GitHub, Linear or Jira, Slack, and Notion. We import your quarterly OKRs from your existing source — Notion, Asana, Mooncamp, or a CSV. No new process for your team.",
    spec: ["github", "linear", "jira", "slack", "notion"],
    timing: "T+0 → T+4min",
  },
  {
    n: "02",
    verb: "MAP",
    title: "Every event tied to a KR with calibrated confidence",
    detail:
      "OKR-Mapper reads each work event and decides which KR(s) it advances. Confident mappings only — anything below 0.5 confidence is dropped, not faked. Our target: ≥85% precision @ ≥70% recall.",
    spec: ["read_event", "score_vs_kr", "drop_if<0.5", "log_reason"],
    timing: "T+4min → T+10min",
  },
  {
    n: "03",
    verb: "NARRATE",
    title: "Friday at 09:00, a one-page brief writes itself",
    detail:
      "Not a dashboard. A reading. Verdict per KR (on_track / drifting / off), specific commits and tickets cited, one paragraph at the bottom on what to do Monday.",
    spec: ["per_kr_verdict", "cite_events", "exec_summary", "monday_action"],
    timing: "FRI 09:00:00 PT",
  },
];

export function HowItWorksV2() {
  return (
    <section id="flow" className="relative border-b border-v2-rule bg-v2-bg-elev/40">
      <div className="relative mx-auto max-w-page px-6 py-24 lg:px-10 lg:py-32">
        <SectionLabelV2 num="03" label="The mechanism" meta="3 stages · 1 cron" className="mb-10" />

        <h2 className="max-w-[28ch] font-sans font-medium leading-[1.04] tracking-tighter text-[clamp(32px,5vw,56px)] text-v2-text">
          A pipeline that runs while
          <span className="block text-v2-text-dim">you sleep.</span>
        </h2>

        <div className="mt-16 space-y-10">
          {STEPS.map((s, idx) => (
            <article
              key={s.n}
              className="relative grid grid-cols-1 gap-8 border border-v2-rule bg-v2-bg-elev p-7 lg:grid-cols-12 lg:gap-10 lg:p-10"
            >
              {/* Glow corner — top-left */}
              <span
                aria-hidden
                className="absolute -left-px -top-px h-12 w-12 border-l-2 border-t-2 border-v2-cyan"
              />
              {/* Stage badge */}
              <div className="lg:col-span-3">
                <div className="font-mono text-[11px] tracking-[0.22em] text-v2-cyan">
                  STAGE_{s.n}
                </div>
                <div className="mt-2 font-sans text-[44px] font-semibold leading-none tracking-tighter text-v2-text">
                  {s.verb}
                </div>
                <div className="mt-4 font-mono text-[11px] tracking-[0.16em] text-v2-muted">
                  {s.timing}
                </div>
              </div>

              {/* Detail */}
              <div className="lg:col-span-5">
                <h3 className="font-sans text-[22px] leading-[1.3] tracking-tight text-v2-text">
                  {s.title}
                </h3>
                <p className="mt-4 max-w-[55ch] text-[15px] leading-[1.7] text-v2-text-dim">
                  {s.detail}
                </p>
              </div>

              {/* Spec block — looks like a system manifest */}
              <div className="lg:col-span-4">
                <div className="border border-v2-rule bg-v2-bg p-5">
                  <div className="mb-3 flex items-center justify-between">
                    <span className="font-mono text-[10px] tracking-[0.22em] text-v2-muted">
                      SPEC.{s.n}
                    </span>
                    <span className="inline-block h-1.5 w-1.5 rounded-full bg-v2-cyan animate-pulse-v2" />
                  </div>
                  <ul className="space-y-1.5 font-mono text-[12.5px] text-v2-text-dim">
                    {s.spec.map((line) => (
                      <li key={line} className="flex items-baseline gap-2">
                        <span className="text-v2-cyan">→</span>
                        <span>{line}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
