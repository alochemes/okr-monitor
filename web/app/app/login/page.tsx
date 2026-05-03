import type { Metadata } from "next";
import Link from "next/link";
import { Suspense } from "react";

import { LoginForm } from "./login-form";

export const metadata: Metadata = {
  title: "OKR Monitor — sign in",
  description: "Magic-link sign-in for OKR Monitor design partners.",
  robots: { index: false, follow: false },
};

export default function LoginPage() {
  return (
    <main className="min-h-screen bg-v2-bg text-v2-text font-sans">
      <div className="mx-auto flex min-h-screen max-w-page flex-col px-6 py-10 lg:px-10">
        <header className="flex items-center justify-between">
          <Link
            href="/"
            className="font-mono text-[11px] uppercase tracking-[0.22em] text-v2-cyan hover:text-v2-text transition-colors"
          >
            OKR_Monitor
          </Link>
          <Link
            href="/v2"
            className="font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted hover:text-v2-cyan transition-colors"
          >
            ← back to home
          </Link>
        </header>

        <section className="my-auto mx-auto w-full max-w-md">
          <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan">
            [01] _ SIGN_IN
          </div>
          <h1 className="mt-3 font-sans font-medium leading-[1.05] tracking-tighter text-[clamp(28px,4vw,40px)] text-v2-text">
            Welcome back.
          </h1>
          <p className="mt-3 max-w-[44ch] text-[14px] leading-[1.7] text-v2-text-dim">
            We&rsquo;ll email you a magic link. No password to remember,
            no SSO friction.
          </p>

          <Suspense fallback={null}>
            <LoginForm />
          </Suspense>

          <div className="mt-10 border-t border-v2-rule pt-6">
            <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted">
              not yet a design partner?
            </p>
            <Link
              href="/health-check"
              className="mt-2 inline-block font-sans text-[14px] text-v2-cyan hover:text-v2-text transition-colors"
            >
              Get a free OKR Health Check &rarr;
            </Link>
          </div>
        </section>

        <footer className="mt-auto pt-10 font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted">
          © 2026 OKR Monitor
        </footer>
      </div>
    </main>
  );
}
