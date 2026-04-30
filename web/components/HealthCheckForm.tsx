"use client";

import { useState } from "react";
import { trackEvent } from "./PostHogProvider";

type Status = "idle" | "submitting" | "success" | "error";

interface KrRow {
  id: string;
  text: string;
}

const SECTIONS = ["Identity", "Company", "OKRs", "5-in-5", "Win"] as const;

let _krCounter = 0;
function newRow(): KrRow {
  _krCounter += 1;
  return { id: `kr-${_krCounter}`, text: "" };
}

export function HealthCheckForm() {
  // Identity
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");

  // Company
  const [companyName, setCompanyName] = useState("");
  const [companySize, setCompanySize] = useState("");
  const [stage, setStage] = useState("");
  const [industry, setIndustry] = useState("");
  const [buyerRole, setBuyerRole] = useState("");
  const [quarterEnd, setQuarterEnd] = useState("");

  // OKR practice
  const [hasOkrs, setHasOkrs] = useState<boolean>(true);
  const [okrTool, setOkrTool] = useState("");
  const [biggestFrustration, setBiggestFrustration] = useState("");

  // 5-in-5
  const [candidateObjective, setCandidateObjective] = useState("");
  const [candidateKrs, setCandidateKrs] = useState<KrRow[]>(() => [
    newRow(),
    newRow(),
    newRow(),
    newRow(),
    newRow(),
  ]);

  // Recent work + win
  const [recentWorkSummary, setRecentWorkSummary] = useState("");
  const [pilotWinDefinition, setPilotWinDefinition] = useState("");

  const [status, setStatus] = useState<Status>("idle");
  const [serverMessage, setServerMessage] = useState<string | null>(null);
  const [slug, setSlug] = useState<string | null>(null);

  function updateKr(id: string, value: string) {
    setCandidateKrs((rows) =>
      rows.map((r) => (r.id === id ? { ...r, text: value } : r)),
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("submitting");
    setServerMessage(null);

    const payload = {
      email,
      full_name: fullName || undefined,
      company_name: companyName,
      company_size: companySize ? Number(companySize) : undefined,
      stage: stage || undefined,
      industry: industry || undefined,
      buyer_role: buyerRole || undefined,
      quarter_end: quarterEnd || undefined,
      has_okrs: hasOkrs,
      okr_tool: okrTool || undefined,
      biggest_frustration: biggestFrustration || undefined,
      candidate_objective: candidateObjective || undefined,
      candidate_krs: candidateKrs
        .filter((r) => r.text.trim())
        .map((r) => ({ text: r.text.trim() })),
      recent_work_summary: recentWorkSummary || undefined,
      pilot_win_definition: pilotWinDefinition || undefined,
    };

    try {
      const res = await fetch("/api/health-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) {
        setStatus("error");
        setServerMessage(data?.error ?? "Something broke. Try again.");
        return;
      }
      setStatus("success");
      setSlug(data?.slug ?? null);
      trackEvent("health_check_submitted", {
        company: companyName,
        kr_count: payload.candidate_krs.length,
      });
    } catch {
      setStatus("error");
      setServerMessage("Network error. Try again in a moment.");
    }
  }

  if (status === "success") {
    return (
      <div className="mx-auto max-w-2xl border border-rule-strong/40 bg-paper p-10">
        <div className="label">Confirmed</div>
        <h2 className="mt-3 font-display text-[34px] font-medium leading-tight tracking-tighter text-ink">
          You&rsquo;re in. We&rsquo;re on it.
        </h2>
        <p className="mt-5 max-w-[55ch] text-[15.5px] leading-relaxed text-ink-soft">
          Your Health Check brief will land in <code className="font-mono text-persimmon">{email}</code>{" "}
          within two business days. We do these manually for the first
          cohort so we can learn what translates and what doesn&rsquo;t —
          expect a real markdown brief, not a templated email.
        </p>
        <div className="mt-7 border-t border-rule pt-5 text-[14px] text-muted">
          <p>Reference for our team:</p>
          <p className="mt-1 font-mono">slug: <span className="text-ink-soft">{slug ?? "—"}</span></p>
        </div>
        <p className="mt-6 text-[14px] text-muted">
          Want to skip the line? Reply to the confirmation email with the
          OKR doc you currently use. Companies with active quarters get
          prioritized.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="mx-auto max-w-3xl space-y-12" noValidate>
      <div>
        <div className="label mb-3">Step 01 · Identity</div>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <Field label="Work email *" required>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@company.com"
              className={inputClass}
            />
          </Field>
          <Field label="Your name">
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Andrew Lochemes"
              className={inputClass}
            />
          </Field>
        </div>
      </div>

      <div>
        <div className="label mb-3">Step 02 · Company</div>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <Field label="Company name *" required>
            <input
              type="text"
              required
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder="Acme Inc"
              className={inputClass}
            />
          </Field>
          <Field label="Headcount">
            <input
              type="number"
              min="1"
              value={companySize}
              onChange={(e) => setCompanySize(e.target.value)}
              placeholder="142"
              className={inputClass}
            />
          </Field>
          <Field label="Stage">
            <select
              value={stage}
              onChange={(e) => setStage(e.target.value)}
              className={inputClass}
            >
              <option value="">—</option>
              <option>Pre-seed</option>
              <option>Seed</option>
              <option>Series A</option>
              <option>Series B</option>
              <option>Series C</option>
              <option>Later</option>
            </select>
          </Field>
          <Field label="Industry / what you sell">
            <input
              type="text"
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              placeholder="SaaS — RevOps tooling"
              className={inputClass}
            />
          </Field>
          <Field label="Your title">
            <input
              type="text"
              value={buyerRole}
              onChange={(e) => setBuyerRole(e.target.value)}
              placeholder="Chief of Staff"
              className={inputClass}
            />
          </Field>
          <Field label="Current quarter end">
            <input
              type="date"
              value={quarterEnd}
              onChange={(e) => setQuarterEnd(e.target.value)}
              className={inputClass}
            />
          </Field>
        </div>
      </div>

      <div>
        <div className="label mb-3">Step 03 · Current OKR practice</div>
        <Field label="Do you currently run OKRs?">
          <div className="mt-1 flex gap-6">
            <label className="flex items-center gap-2 text-[15px] text-ink-soft">
              <input
                type="radio"
                name="has_okrs"
                checked={hasOkrs}
                onChange={() => setHasOkrs(true)}
                className="accent-persimmon"
              />
              Yes
            </label>
            <label className="flex items-center gap-2 text-[15px] text-ink-soft">
              <input
                type="radio"
                name="has_okrs"
                checked={!hasOkrs}
                onChange={() => setHasOkrs(false)}
                className="accent-persimmon"
              />
              Not yet / sort of
            </label>
          </div>
        </Field>
        <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">
          <Field label="Where do they live?">
            <input
              type="text"
              value={okrTool}
              onChange={(e) => setOkrTool(e.target.value)}
              placeholder="Notion / Asana / Mooncamp / CSV"
              className={inputClass}
            />
          </Field>
        </div>
        <Field label="What frustrates you most about your current OKR process?" className="mt-6">
          <textarea
            value={biggestFrustration}
            onChange={(e) => setBiggestFrustration(e.target.value)}
            rows={3}
            placeholder="We set them in January and by April nobody remembers what KR-3 was."
            className={`${inputClass} resize-none`}
          />
        </Field>
      </div>

      <div>
        <div className="label mb-3">Step 04 · 5-in-5 exercise</div>
        <p className="mt-2 max-w-[60ch] text-[14.5px] leading-relaxed text-muted">
          Pick one Objective for the current quarter. Set a 5-minute timer.
          Write 5 candidate Key Results. Don&rsquo;t edit, don&rsquo;t debate.
          Fast and rough. We&rsquo;ll refine together in the kickoff.
        </p>
        <Field label="Objective for this quarter" className="mt-6">
          <input
            type="text"
            value={candidateObjective}
            onChange={(e) => setCandidateObjective(e.target.value)}
            placeholder="Become the default ops tool for $50M+ RevOps teams"
            className={inputClass}
          />
        </Field>
        <div className="mt-6 space-y-3">
          {candidateKrs.map((r, i) => (
            <div key={r.id} className="flex items-center gap-3">
              <span className="font-mono text-[12px] tracking-label text-persimmon w-8">
                KR-{i + 1}
              </span>
              <input
                type="text"
                value={r.text}
                onChange={(e) => updateKr(r.id, e.target.value)}
                placeholder={
                  i === 0
                    ? "Land 5 enterprise pilots by end of quarter"
                    : "[Verb] [metric] from [baseline] to [target] by [date]"
                }
                className={inputClass}
              />
            </div>
          ))}
        </div>
      </div>

      <div>
        <div className="label mb-3">Step 05 · Win definition + recent work</div>
        <Field label="What does a clear win look like in 60 days?">
          <textarea
            value={pilotWinDefinition}
            onChange={(e) => setPilotWinDefinition(e.target.value)}
            rows={3}
            placeholder="Cancel the Monday standup. The brief replaces it. CEO forwards the brief to the board prep deck."
            className={`${inputClass} resize-none`}
          />
        </Field>
        <Field label="Recent work summary (last 30 days)" className="mt-6">
          <textarea
            value={recentWorkSummary}
            onChange={(e) => setRecentWorkSummary(e.target.value)}
            rows={6}
            placeholder={`Engineering: shipped redis pipeline tuning, 18 commits on dashboard surface
Sales: pilot conversations with 3 prospects (no closes)
Marketing: 2 blog posts published
Customer Success: ran churn analysis (results private)`}
            className={`${inputClass} font-mono text-[13.5px] resize-none`}
          />
        </Field>
      </div>

      <div className="border-t border-rule pt-8 flex flex-col items-start gap-5 sm:flex-row sm:items-center sm:justify-between">
        <button
          type="submit"
          disabled={status === "submitting"}
          className="group inline-flex items-center gap-2 bg-ink text-paper px-7 py-3.5 font-sans text-[15px] font-medium tracking-tight transition-all duration-200 hover:bg-persimmon hover:translate-y-[-1px] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {status === "submitting" ? "Sending…" : "Submit my Health Check"}
          <span
            className="inline-block transition-transform group-hover:translate-x-1"
            aria-hidden="true"
          >
            →
          </span>
        </button>
        <p className="font-mono text-[11px] text-muted max-w-[44ch]">
          We answer within 2 business days · No spam, no list-rental, no
          third-party sharing.
        </p>
      </div>

      {status === "error" && serverMessage && (
        <p className="text-[14px] text-persimmon">{serverMessage}</p>
      )}
    </form>
  );
}

const inputClass =
  "mt-2 block w-full border-b border-rule-strong/40 bg-transparent px-0 py-2.5 text-[15px] text-ink placeholder:text-muted focus:border-persimmon focus:outline-none";

function Field({
  label,
  children,
  className = "",
  required = false,
}: {
  label: string;
  children: React.ReactNode;
  className?: string;
  required?: boolean;
}) {
  return (
    <label className={`block ${className}`}>
      <span className={`label-ink ${required ? "after:content-['_*'] after:text-persimmon" : ""}`}>
        {label}
      </span>
      {children}
    </label>
  );
}
