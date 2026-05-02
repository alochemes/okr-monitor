import { SectionLabelV2 } from "./SectionLabelV2";

const SYMPTOMS = [
  {
    code: "ERR_001",
    line: "monday standup is the autopsy",
    sub: "Asking 'are we on track?' on day 7 means the answer is already a week old.",
  },
  {
    code: "ERR_002",
    line: "okr doc and work happen in two places",
    sub: "Notion says 'In progress.' GitHub says nothing has touched it in 19 days.",
  },
  {
    code: "ERR_003",
    line: "drift visible only at quarter-end",
    sub: "By the time the post-mortem starts, the quarter is gone.",
  },
];

export function ProblemSectionV2() {
  return (
    <section className="relative border-b border-v2-rule">
      <div
        aria-hidden
        className="absolute inset-0 opacity-[0.06]"
        style={{
          backgroundImage:
            "linear-gradient(to right, #2A3142 1px, transparent 1px), linear-gradient(to bottom, #2A3142 1px, transparent 1px)",
          backgroundSize: "80px 80px",
        }}
      />
      <div className="relative mx-auto max-w-page px-6 py-24 lg:px-10 lg:py-32">
        <SectionLabelV2 num="02" label="Failure modes" className="mb-10" />

        <h2 className="text-v2-text font-sans font-medium leading-[1.04] tracking-tighter text-[clamp(32px,5vw,56px)] max-w-[24ch]">
          Quarterly check-ins are{" "}
          <span className="text-persimmon">a memorial service</span> —
          not a steering wheel.
        </h2>

        {/* Three terminal-card "errors" */}
        <div className="mt-14 grid grid-cols-1 gap-px bg-v2-rule sm:grid-cols-3">
          {SYMPTOMS.map((s) => (
            <article
              key={s.code}
              className="relative bg-v2-bg-elev p-7 lg:p-8 group"
            >
              {/* Status pip */}
              <span
                aria-hidden
                className="absolute right-6 top-6 inline-block h-1.5 w-1.5 rounded-full bg-persimmon shadow-[0_0_12px_rgba(199,58,20,0.6)] animate-pulse-v2"
              />
              <div className="font-mono text-[11px] tracking-[0.22em] text-persimmon">
                {s.code}
              </div>
              <p className="mt-4 text-v2-text font-sans text-[20px] leading-[1.3] tracking-tight">
                {s.line}
              </p>
              <p className="mt-4 text-[13.5px] leading-[1.6] text-v2-text-dim font-mono">
                <span className="text-v2-muted">// </span>
                {s.sub}
              </p>
            </article>
          ))}
        </div>

        {/* Quote in monospace terminal style */}
        <figure className="mt-20 grid grid-cols-1 gap-8 lg:grid-cols-12 lg:gap-12">
          <div className="lg:col-span-3">
            <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan">
              FIELD_NOTE.001
            </div>
            <div className="mt-2 font-mono text-[11px] text-v2-muted">
              CoS / Series B fintech / 220 employees
            </div>
          </div>
          <blockquote className="lg:col-span-9">
            <div className="border-l-2 border-v2-cyan/60 pl-7">
              <p className="text-v2-text font-sans text-[clamp(22px,2.6vw,34px)] leading-[1.3] tracking-tight">
                &ldquo;Every Monday I spend an hour playing telephone — DMing
                five people to find out if the OKRs we set in January are
                still real. By the time I&rsquo;ve answered the CEO, the
                answer is already two days old.&rdquo;
              </p>
            </div>
          </blockquote>
        </figure>
      </div>
    </section>
  );
}
