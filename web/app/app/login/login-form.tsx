"use client";

import { useState, useTransition } from "react";
import { useRouter, useSearchParams } from "next/navigation";

import { createClient } from "@/lib/supabase/client";

type Status =
  | { kind: "idle" }
  | { kind: "sending" }
  | { kind: "sent"; email: string }
  | { kind: "error"; message: string };

export function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>({ kind: "idle" });
  const [, startTransition] = useTransition();

  // Where to land after the magic link is verified. Falls back to the
  // dashboard. Middleware sets `next` when it redirects unauthed users
  // here, so the round-trip preserves their intended destination.
  const next = params.get("next") || "/app/dashboard";

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!email) return;
    setStatus({ kind: "sending" });

    let supabase;
    try {
      supabase = createClient();
    } catch (err) {
      setStatus({
        kind: "error",
        message:
          err instanceof Error
            ? err.message
            : "Supabase client not available.",
      });
      return;
    }

    const origin =
      typeof window !== "undefined" ? window.location.origin : "";
    const redirectTo = `${origin}/app/auth/callback?next=${encodeURIComponent(
      next,
    )}`;

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: redirectTo },
    });

    if (error) {
      setStatus({ kind: "error", message: error.message });
      return;
    }
    setStatus({ kind: "sent", email });
    startTransition(() => router.refresh());
  }

  if (status.kind === "sent") {
    return (
      <div
        className="border border-v2-cyan-faint bg-v2-bg-card px-5 py-6 font-sans text-[14px] leading-[1.7] text-v2-text"
        role="status"
        aria-live="polite"
      >
        <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-v2-cyan">
          link_sent
        </p>
        <p className="mt-3">
          Check <strong className="text-v2-text">{status.email}</strong>. The
          link expires in 60 minutes and can be used once.
        </p>
        <button
          type="button"
          onClick={() => setStatus({ kind: "idle" })}
          className="mt-4 font-mono text-[11px] uppercase tracking-[0.16em] text-v2-cyan hover:text-v2-text transition-colors"
        >
          ← use a different email
        </button>
      </div>
    );
  }

  const sending = status.kind === "sending";

  return (
    <form onSubmit={onSubmit} className="mt-8 space-y-5" aria-label="Sign in form">
      <label className="block">
        <span className="block font-mono text-[10px] uppercase tracking-[0.18em] text-v2-muted">
          work_email
        </span>
        <input
          type="email"
          name="email"
          required
          autoComplete="email"
          placeholder="you@yourcompany.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={sending}
          className="mt-2 w-full border border-v2-rule-strong bg-v2-bg-card px-4 py-3 font-sans text-[14px] text-v2-text placeholder:text-v2-muted focus:border-v2-cyan focus:outline-none focus:ring-0 disabled:opacity-50"
        />
      </label>

      <button
        type="submit"
        disabled={sending || !email}
        className="group inline-flex w-full items-center justify-center gap-3 bg-persimmon px-7 py-4 font-sans text-[15px] font-medium tracking-tight text-v2-text transition-all duration-200 hover:translate-y-[-1px] hover:shadow-[0_0_36px_rgba(199,58,20,0.55)] disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0 disabled:hover:shadow-none"
      >
        {sending ? "Sending…" : "Send magic link"}
        {!sending && (
          <span
            className="inline-block transition-transform group-hover:translate-x-1"
            aria-hidden
          >
            →
          </span>
        )}
      </button>

      {status.kind === "error" && (
        <p
          className="font-mono text-[11px] uppercase tracking-[0.16em] text-verdict-off"
          role="alert"
        >
          {status.message}
        </p>
      )}
    </form>
  );
}
