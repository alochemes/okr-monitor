import { NarrativeMock } from "./NarrativeMock";

export function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-rule">
      <div className="mx-auto max-w-page px-6 pb-20 pt-12 lg:px-10 lg:pb-28 lg:pt-20">
        <div className="grid grid-cols-1 gap-14 lg:grid-cols-12 lg:gap-12">
          {/* Editorial left column */}
          <div className="lg:col-span-7">
            <div className="reveal reveal-1 mb-6 flex items-center gap-3">
              <span className="label">No. 001 / Editorial</span>
              <span className="h-px w-10 bg-persimmon/60" />
              <span className="label-ink !text-muted">April 2026</span>
            </div>

            <h1 className="reveal reveal-2 display-tight font-display text-[clamp(52px,8.4vw,108px)] font-semibold leading-[0.92] tracking-tightest text-ink">
              Stop guessing
              <span className="block italic font-medium">which OKRs</span>
              <span className="block">
                are{" "}
                <span className="relative inline-block">
                  real
                  <span
                    aria-hidden="true"
                    className="absolute inset-x-0 -bottom-1 h-[10px] -skew-x-12 bg-persimmon/30"
                  />
                </span>
                .
              </span>
            </h1>

            <p className="reveal reveal-3 mt-8 max-w-[52ch] font-display text-[20px] leading-[1.5] tracking-editorial text-ink-soft sm:text-[22px]">
              Every Friday at 9 AM, a one-page exec brief lands in your inbox
              naming which KRs are on track, which are drifting, and exactly
              which commits, tickets, and conversations moved them.
            </p>

            <div className="reveal reveal-4 mt-10 flex flex-wrap items-center gap-x-8 gap-y-4">
              <a href="#waitlist" className="btn-primary">
                Get a free OKR Health Check
                <span className="arrow" aria-hidden="true">→</span>
              </a>
              <a href="#how" className="btn-ghost">
                Read sample brief
              </a>
            </div>

            {/* Tiny credit / data line */}
            <div className="reveal reveal-5 mt-12 flex flex-wrap items-baseline gap-x-8 gap-y-2 border-t border-rule pt-5 text-[13px] text-muted">
              <span>
                <span className="font-mono text-ink-soft">30</span> background
                agents
              </span>
              <span>
                <span className="font-mono text-ink-soft">5</span> integrations
                day-one
              </span>
              <span>
                <span className="font-mono text-ink-soft">{"<"}30 min</span> to
                first brief
              </span>
            </div>
          </div>

          {/* Hero asset — printed memo, the proof */}
          <div className="reveal reveal-3 lg:col-span-5 lg:pt-2">
            <div className="relative">
              {/* Caption above */}
              <div className="mb-4 flex items-center justify-between">
                <span className="label">Sample · Brief 17.26</span>
                <span className="font-mono text-[10px] text-muted">FIG. 1</span>
              </div>
              <NarrativeMock />
              {/* Caption below */}
              <div className="mt-4 flex items-baseline justify-between">
                <span className="font-mono text-[11px] text-muted">
                  generated automatically every Friday 09:00 PT
                </span>
                <span className="font-mono text-[11px] text-muted">
                  ¶ 1.1 / 4.2
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom marquee — wedge moments */}
      <div className="border-t border-rule bg-paper-deep/50">
        <div className="mx-auto max-w-page px-6 py-3 text-[11px] uppercase tracking-label text-muted lg:px-10">
          <div className="flex flex-wrap items-center gap-x-8 gap-y-1">
            <span className="font-mono text-ink-soft">●</span>
            <span>connect github / linear / jira / slack / notion</span>
            <span className="font-mono">·</span>
            <span>map every commit + ticket + thread to a KR</span>
            <span className="font-mono">·</span>
            <span>read one page friday morning</span>
            <span className="font-mono">·</span>
            <span>act on monday</span>
          </div>
        </div>
      </div>
    </section>
  );
}
