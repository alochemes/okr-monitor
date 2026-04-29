"use client";

import { useState } from "react";
import { trackEvent } from "./PostHogProvider";

type Status = "idle" | "submitting" | "success" | "error";

export function WaitlistForm() {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [company, setCompany] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [message, setMessage] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("submitting");
    setMessage(null);

    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, role, company }),
      });
      const data = await res.json();
      if (!res.ok) {
        setStatus("error");
        setMessage(data?.error ?? "Something broke. Try again in a moment.");
        return;
      }
      setStatus("success");
      setMessage(
        "You're on the list. We'll reach out within two business days."
      );
      // Conversion event — the primary metric for landing-page experiments.
      trackEvent("waitlist_signup", {
        has_role: Boolean(role),
        has_company: Boolean(company),
      });
      setEmail("");
      setRole("");
      setCompany("");
    } catch {
      setStatus("error");
      setMessage("Network error. Try again in a moment.");
    }
  }

  if (status === "success") {
    return (
      <div className="border border-paper/20 bg-paper/5 p-6">
        <div className="label !text-persimmon">Confirmed</div>
        <p className="mt-3 font-display text-[20px] leading-[1.4] tracking-editorial text-paper">
          {message}
        </p>
        <p className="mt-3 text-[13.5px] text-paper/70">
          Want to skip the line? Reply to the confirmation with the OKR doc
          you currently use and the date your quarter ends. We&rsquo;ll
          prioritize companies with active quarters.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4" noValidate>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="label !text-paper/60">Work email</span>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@company.com"
            className="mt-2 block w-full border-b border-paper/30 bg-transparent px-0 py-3 font-mono text-[15px] text-paper placeholder:text-paper/30 focus:border-persimmon focus:outline-none"
          />
        </label>
        <label className="block">
          <span className="label !text-paper/60">Your title</span>
          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="Chief of Staff"
            className="mt-2 block w-full border-b border-paper/30 bg-transparent px-0 py-3 font-mono text-[15px] text-paper placeholder:text-paper/30 focus:border-persimmon focus:outline-none"
          />
        </label>
      </div>

      <label className="block">
        <span className="label !text-paper/60">Company</span>
        <input
          type="text"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="Acme, Inc · Series B · 142 employees"
          className="mt-2 block w-full border-b border-paper/30 bg-transparent px-0 py-3 font-mono text-[15px] text-paper placeholder:text-paper/30 focus:border-persimmon focus:outline-none"
        />
      </label>

      <div className="flex flex-col items-start gap-4 pt-3 sm:flex-row sm:items-center sm:justify-between">
        <button
          type="submit"
          disabled={status === "submitting"}
          className="group inline-flex items-center gap-2 bg-paper px-7 py-3.5 font-sans text-[15px] font-medium tracking-tight text-ink transition-all duration-200 hover:bg-persimmon hover:text-paper hover:translate-y-[-1px] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {status === "submitting" ? "Sending…" : "Get my Health Check"}
          <span className="inline-block transition-transform group-hover:translate-x-1" aria-hidden="true">
            →
          </span>
        </button>
        <p className="font-mono text-[11px] text-paper/55">
          We answer within 2 business days · No spam, no list-rental.
        </p>
      </div>

      {status === "error" && message && (
        <p className="text-[13px] text-persimmon">{message}</p>
      )}
    </form>
  );
}
