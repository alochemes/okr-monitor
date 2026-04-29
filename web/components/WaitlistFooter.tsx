import { WaitlistForm } from "./WaitlistForm";

export function WaitlistFooter() {
  return (
    <section
      id="waitlist"
      className="bg-ink text-paper"
    >
      <div className="mx-auto grid max-w-page grid-cols-1 gap-14 px-6 py-24 lg:grid-cols-12 lg:gap-16 lg:px-10 lg:py-32">
        {/* Editorial column */}
        <div className="lg:col-span-5">
          <div className="flex items-center gap-3">
            <span className="font-mono text-[11px] tracking-label text-persimmon">
              07
            </span>
            <span className="h-px w-12 bg-persimmon/60" aria-hidden="true" />
            <span className="font-sans text-[10px] tracking-label text-paper/50 uppercase">
              The Subscription
            </span>
          </div>
          <h2 className="mt-5 font-display text-[clamp(36px,4.5vw,56px)] font-medium leading-[1.04] tracking-tighter text-paper">
            Get a free OKR Health Check.
            <span className="mt-2 block italic font-normal text-paper/70">
              Receive a sample brief on your real OKRs within two business days.
            </span>
          </h2>

          <div className="mt-10 space-y-4 text-[14.5px] leading-relaxed text-paper/70">
            <p>
              You send us your current OKR doc and the team / repo / Slack
              channels you&rsquo;d want connected. We send back a real brief
              — same shape as the Friday brief above, populated against your
              actual work.
            </p>
            <p>
              We do this manually for the first cohort so we learn what
              translates and what doesn&rsquo;t. There is no demo to sit
              through.
            </p>
          </div>
        </div>

        {/* Form column */}
        <div className="lg:col-span-7">
          <WaitlistForm />
        </div>
      </div>

      {/* Footer band */}
      <footer className="border-t border-paper/15">
        <div className="mx-auto flex max-w-page flex-col items-start gap-6 px-6 py-10 sm:flex-row sm:items-center sm:justify-between lg:px-10">
          <div className="flex items-baseline gap-3">
            <span className="inline-block h-2 w-2 translate-y-[-2px] bg-persimmon" aria-hidden="true" />
            <span className="font-display text-[18px] font-semibold tracking-editorial text-paper">
              OKR Monitor
            </span>
            <span className="font-mono text-[10px] tracking-label text-paper/40">
              EST. 2026
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-x-7 gap-y-2 font-sans text-[13px] text-paper/55">
            <a href="mailto:hello@okrmonitor.com" className="hover:text-persimmon transition-colors">
              hello@okrmonitor.com
            </a>
            <a href="https://github.com/alochemes/okr-monitor" className="hover:text-persimmon transition-colors">
              GitHub
            </a>
            <a href="#" className="hover:text-persimmon transition-colors">
              LinkedIn
            </a>
            <a href="#" className="hover:text-persimmon transition-colors">
              Privacy
            </a>
            <a href="#" className="hover:text-persimmon transition-colors">
              Terms
            </a>
          </div>

          <div className="font-mono text-[11px] text-paper/40">
            © 2026 · Issue 001
          </div>
        </div>
      </footer>
    </section>
  );
}
