import type { Metadata } from "next";
import Link from "next/link";
import { NavV2 } from "@/components/v2/NavV2";
import { HeroV2 } from "@/components/v2/HeroV2";
import { ProblemSectionV2 } from "@/components/v2/ProblemSectionV2";
import { HowItWorksV2 } from "@/components/v2/HowItWorksV2";
import { IntegrationsStripV2 } from "@/components/v2/IntegrationsStripV2";

export const metadata: Metadata = {
  title: "OKR Monitor — connect every part of your business to one brief",
  description:
    "A live data-flow that ingests work events from GitHub, Linear/Jira, Slack, and Notion, maps them to your KRs, and writes a one-page Friday exec brief.",
};

export default function V2Page() {
  return (
    <main className="min-h-screen bg-v2-bg text-v2-text">
      <NavV2 />
      <HeroV2 />
      <ProblemSectionV2 />
      <HowItWorksV2 />
      <IntegrationsStripV2 />

      <footer className="border-t border-v2-rule bg-v2-bg-elev/40">
        <div className="mx-auto grid max-w-page grid-cols-1 gap-8 px-6 py-14 lg:grid-cols-12 lg:gap-10 lg:px-10">
          <div className="lg:col-span-5">
            <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan">
              [05] _ NEXT
            </div>
            <h2 className="mt-3 font-sans font-medium leading-[1.05] tracking-tighter text-[clamp(28px,4vw,42px)] text-v2-text">
              See your own data in a brief.
            </h2>
            <p className="mt-4 max-w-[48ch] text-[14.5px] leading-[1.7] text-v2-text-dim">
              Send us your current OKRs and 30 days of work events. We&rsquo;ll
              return a real Friday brief on your real data &mdash; plus a
              flagged-cleanup list &mdash; within two business days.
            </p>
            <div className="mt-7">
              <Link
                href="/health-check"
                className="group inline-flex items-center gap-3 bg-persimmon px-7 py-4 font-sans text-[15px] font-medium tracking-tight text-v2-text transition-all duration-200 hover:translate-y-[-1px] hover:shadow-[0_0_36px_rgba(199,58,20,0.55)]"
              >
                Get a free OKR Health Check
                <span
                  className="inline-block transition-transform group-hover:translate-x-1"
                  aria-hidden
                >
                  →
                </span>
              </Link>
            </div>
          </div>

          <div className="lg:col-span-4 lg:col-start-9">
            <div className="font-mono text-[10px] tracking-[0.22em] text-v2-muted">
              SYSTEM_META
            </div>
            <dl className="mt-4 space-y-2.5 font-mono text-[11px] tracking-[0.14em] text-v2-text-dim">
              {[
                ["build", "v2.2026.05"],
                ["ingest", "github · linear · jira · slack · notion"],
                ["delivery", "fri 09:00 pt"],
                ["data", "stays in your tenant · no training"],
              ].map(([k, v]) => (
                <div key={k} className="flex items-baseline justify-between gap-6">
                  <dt className="uppercase text-v2-muted">{k}</dt>
                  <dd className="text-right text-v2-text-dim">{v}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>

        <div className="border-t border-v2-rule">
          <div className="mx-auto flex max-w-page flex-wrap items-baseline justify-between gap-y-2 px-6 py-5 font-mono text-[10px] tracking-[0.18em] text-v2-muted lg:px-10">
            <span className="uppercase">© 2026 OKR Monitor</span>
            <Link
              href="/"
              className="hover:text-v2-cyan transition-colors uppercase"
            >
              ← editorial / v1
            </Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
