import type { Metadata } from "next";
import Link from "next/link";
import { Nav } from "@/components/Nav";
import { HealthCheckForm } from "@/components/HealthCheckForm";

export const metadata: Metadata = {
  title: "OKR Health Check — OKR Monitor",
  description:
    "Send us your current OKRs and 30 days of work. We send back a real Friday brief on your real data, plus a flagged-cleanup list, within two business days.",
};

export default function HealthCheckPage() {
  return (
    <main>
      <Nav />

      {/* Editorial header */}
      <section className="border-b border-rule">
        <div className="mx-auto max-w-page px-6 pt-14 pb-12 lg:px-10 lg:pt-20 lg:pb-16">
          <div className="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:gap-12">
            <div className="lg:col-span-7">
              <div className="mb-6 flex items-center gap-3">
                <span className="label">No. 002 / Health Check</span>
                <span className="h-px w-10 bg-persimmon/60" />
                <Link
                  href="/"
                  className="font-sans text-[12px] text-muted hover:text-persimmon transition-colors"
                >
                  ← back to home
                </Link>
              </div>

              <h1 className="display-tight font-display text-[clamp(40px,6vw,72px)] font-semibold leading-[0.96] tracking-tightest text-ink">
                A real brief.
                <span className="block italic font-medium">
                  On your real data.
                </span>
                <span className="block">
                  In{" "}
                  <span className="relative inline-block">
                    two days
                    <span
                      aria-hidden="true"
                      className="absolute inset-x-0 -bottom-1 h-[8px] -skew-x-12 bg-persimmon/30"
                    />
                  </span>
                  .
                </span>
              </h1>

              <p className="mt-7 max-w-[58ch] font-display text-[19px] leading-[1.5] tracking-editorial text-ink-soft">
                Tell us about your OKRs and 30 days of recent work. We
                generate a sample Friday brief on your data, flag any KRs
                that need cleanup before you can measure them, and ship a
                customized 45-minute kickoff agenda. No demo to sit through.
              </p>

              <ul className="mt-8 space-y-2 text-[14.5px] text-muted">
                <li className="flex items-start gap-3">
                  <span className="mt-2 inline-block h-1.5 w-1.5 flex-shrink-0 bg-persimmon" />
                  <span>~15 minutes to fill out · save and return later if needed</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="mt-2 inline-block h-1.5 w-1.5 flex-shrink-0 bg-persimmon" />
                  <span>Free · no card · no obligation to start a pilot</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="mt-2 inline-block h-1.5 w-1.5 flex-shrink-0 bg-persimmon" />
                  <span>You receive a markdown brief and a customized kickoff plan, both yours to keep</span>
                </li>
              </ul>
            </div>

            {/* What you get sidebar */}
            <aside className="lg:col-span-5 lg:pt-2">
              <div className="border border-rule-strong/50 p-6">
                <div className="label-ink mb-3">What lands in your inbox</div>
                <ol className="space-y-4 text-[14px] text-ink-soft">
                  <li className="flex gap-3">
                    <span className="font-mono text-persimmon">01</span>
                    <span>
                      <strong className="text-ink">Verdict.</strong> One paragraph naming the single most important fix before you can run a real pilot.
                    </span>
                  </li>
                  <li className="flex gap-3">
                    <span className="font-mono text-persimmon">02</span>
                    <span>
                      <strong className="text-ink">KR review.</strong> Each candidate KR scored against our 6-rule rubric: pass, cleanup, or rewrite, with a proposed rewrite in our canonical shape.
                    </span>
                  </li>
                  <li className="flex gap-3">
                    <span className="font-mono text-persimmon">03</span>
                    <span>
                      <strong className="text-ink">Sample Friday brief.</strong> A styled mockup of what your weekly brief would read like, populated against your recent work summary.
                    </span>
                  </li>
                  <li className="flex gap-3">
                    <span className="font-mono text-persimmon">04</span>
                    <span>
                      <strong className="text-ink">Cleanup list.</strong> 2–3 specific actions, each with an owner and a deadline before pilot day 7.
                    </span>
                  </li>
                  <li className="flex gap-3">
                    <span className="font-mono text-persimmon">05</span>
                    <span>
                      <strong className="text-ink">Kickoff agenda.</strong> A customized 45-minute plan ready to drop into your calendar.
                    </span>
                  </li>
                </ol>
              </div>
            </aside>
          </div>
        </div>
      </section>

      {/* Form section */}
      <section className="border-b border-rule bg-paper-deep/40">
        <div className="mx-auto max-w-page px-6 py-16 lg:px-10 lg:py-24">
          <HealthCheckForm />
        </div>
      </section>

      {/* Footer mini */}
      <footer className="bg-ink text-paper">
        <div className="mx-auto flex max-w-page flex-col items-start gap-4 px-6 py-10 sm:flex-row sm:items-center sm:justify-between lg:px-10">
          <div className="flex items-baseline gap-3">
            <span className="inline-block h-2 w-2 translate-y-[-2px] bg-persimmon" />
            <span className="font-display text-[18px] font-semibold tracking-editorial">
              OKR Monitor
            </span>
          </div>
          <Link href="/" className="font-sans text-[13px] text-paper/60 hover:text-persimmon transition-colors">
            ← back to home
          </Link>
        </div>
      </footer>
    </main>
  );
}
