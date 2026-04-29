import Link from "next/link";

export function Nav() {
  return (
    <header className="border-b border-rule">
      <div className="mx-auto flex max-w-page items-center justify-between px-6 py-5 lg:px-10">
        <Link
          href="/"
          className="group flex items-baseline gap-2"
          aria-label="OKR Monitor home"
        >
          <span className="inline-block h-2 w-2 translate-y-[-1px] bg-persimmon" aria-hidden="true" />
          <span className="font-display text-[19px] font-semibold tracking-editorial text-ink group-hover:text-persimmon transition-colors">
            OKR Monitor
          </span>
          <span className="ml-1 hidden font-sans text-[10px] tracking-label text-muted sm:inline">
            ISSUE 001
          </span>
        </Link>

        <nav className="flex items-center gap-7 text-[14px] text-ink-soft">
          <a href="#how" className="hidden hover:text-persimmon transition-colors sm:inline">
            How it works
          </a>
          <a href="#pricing" className="hidden hover:text-persimmon transition-colors sm:inline">
            Pricing
          </a>
          <a href="#waitlist" className="btn-primary !py-2 !px-4 !text-[13px]">
            Get a brief
            <span className="arrow" aria-hidden="true">→</span>
          </a>
        </nav>
      </div>
    </header>
  );
}
