import Link from "next/link";

export function NavV2() {
  return (
    <header className="border-b border-v2-rule bg-v2-bg/80 backdrop-blur-md sticky top-0 z-30">
      <div className="mx-auto flex max-w-page items-center justify-between px-6 py-4 lg:px-10">
        <Link href="/v2" className="group flex items-center gap-3" aria-label="OKR Monitor">
          {/* Brand mark — small octagon in persimmon, matches central node in 3D scene */}
          <span
            aria-hidden
            className="relative inline-flex h-5 w-5 items-center justify-center"
          >
            <span className="absolute inset-0 rotate-45 bg-persimmon shadow-[0_0_18px_rgba(199,58,20,0.55)]" />
            <span className="absolute inset-1 rotate-45 bg-v2-bg" />
            <span className="relative h-1.5 w-1.5 rotate-45 bg-persimmon" />
          </span>
          <span className="font-sans text-[15px] font-semibold tracking-tight text-v2-text group-hover:text-persimmon transition-colors">
            OKR Monitor
          </span>
          <span className="hidden font-mono text-[10px] tracking-[0.22em] text-v2-muted sm:inline">
            v2 / TECH
          </span>
        </Link>

        <nav className="flex items-center gap-6 text-[13px]">
          <a href="#flow"     className="hidden text-v2-text-dim hover:text-v2-cyan transition-colors sm:inline">How it flows</a>
          <a href="#pricing"  className="hidden text-v2-text-dim hover:text-v2-cyan transition-colors sm:inline">Pricing</a>
          <Link
            href="/health-check"
            className="group inline-flex items-center gap-2 border border-persimmon/60 bg-persimmon/10 px-4 py-2 font-mono text-[12px] tracking-[0.12em] text-persimmon hover:bg-persimmon hover:text-v2-text hover:shadow-[0_0_24px_rgba(199,58,20,0.45)] transition-all"
          >
            REQUEST_HEALTH_CHECK
            <span className="inline-block transition-transform group-hover:translate-x-0.5" aria-hidden>›</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
