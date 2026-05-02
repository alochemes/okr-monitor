"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { useEffect, useState } from "react";
import { trackEvent } from "@/components/PostHogProvider";
import { DataFlowFallbackSVG } from "./DataFlowFallbackSVG";
import { SectionLabelV2 } from "./SectionLabelV2";

// Lazy-load the 3D scene so the LCP element (the headline) paints first.
// SSR off because Three.js touches `window` at import time.
const DataFlow3D = dynamic(
  () => import("./DataFlow3D").then((m) => m.DataFlow3D),
  { ssr: false, loading: () => <DataFlowFallbackSVG className="h-full w-full" /> },
);

// Decide whether to render the live 3D scene or the static fallback.
// Mobile (<768px), reduced-motion, no-WebGL all get the fallback.
function useShouldRender3D() {
  const [enabled, setEnabled] = useState(false);
  useEffect(() => {
    if (typeof window === "undefined") return;
    const isWide = window.matchMedia("(min-width: 768px)").matches;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let webgl = false;
    try {
      const c = document.createElement("canvas");
      webgl = !!(c.getContext("webgl2") || c.getContext("webgl"));
    } catch {
      webgl = false;
    }
    setEnabled(isWide && !reduced && webgl);
  }, []);
  return enabled;
}

export function HeroV2() {
  const render3D = useShouldRender3D();

  return (
    <section className="relative overflow-hidden border-b border-v2-rule">
      {/* Blueprint grid background */}
      <div
        aria-hidden
        className="absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage:
            "linear-gradient(to right, #2A3142 1px, transparent 1px), linear-gradient(to bottom, #2A3142 1px, transparent 1px)",
          backgroundSize: "80px 80px",
        }}
      />
      {/* Vignette glow from the center to give the 3D scene atmosphere */}
      <div
        aria-hidden
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(60% 50% at 70% 40%, rgba(199,58,20,0.10), rgba(0,217,255,0.04) 45%, transparent 75%)",
        }}
      />

      <div className="relative mx-auto max-w-page px-6 pt-16 pb-20 lg:px-10 lg:pt-24 lg:pb-32">
        <SectionLabelV2 num="01" label="Hero" meta="rev. 2026.001" className="mb-8" />

        <div className="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:items-center lg:gap-10">
          {/* Headline column */}
          <div className="lg:col-span-7">
            {/* Status row — the "live system" cue */}
            <div className="reveal reveal-1 mb-6 flex flex-wrap items-center gap-x-6 gap-y-2 font-mono text-[11px] tracking-[0.18em] text-v2-text-dim">
              <span className="inline-flex items-center gap-2">
                <span className="inline-block h-2 w-2 rounded-full bg-v2-cyan animate-pulse-v2" aria-hidden />
                <span className="uppercase">SYSTEM_ONLINE</span>
              </span>
              <span className="text-v2-muted">·</span>
              <span className="uppercase">30 AGENTS</span>
              <span className="text-v2-muted">·</span>
              <span className="uppercase">5 SOURCES</span>
              <span className="text-v2-muted">·</span>
              <span className="uppercase">FRI 09:00 PT</span>
            </div>

            <h1 className="reveal reveal-2 text-v2-text font-sans font-semibold leading-[0.94] tracking-tightest text-[clamp(48px,8vw,98px)]">
              Connect every part of
              <br />
              your business to{" "}
              <span className="relative inline-block">
                one
                <span
                  aria-hidden
                  className="absolute -inset-x-1 -bottom-1 h-[10px] -skew-x-12 bg-persimmon/35"
                />
              </span>{" "}
              brief.
            </h1>

            <p className="reveal reveal-3 mt-8 max-w-[58ch] text-[19px] leading-[1.55] text-v2-text-dim">
              Every Friday, a one-page exec brief naming which OKRs are on
              track, which are drifting, and exactly which work is — and
              isn&rsquo;t — moving the needle. Connected to the systems
              where work already happens.
            </p>

            <div className="reveal reveal-4 mt-10 flex flex-wrap items-center gap-x-6 gap-y-4">
              <Link
                href="/health-check"
                onClick={() => trackEvent("hero_cta_click", { variant: "v2", destination: "/health-check" })}
                className="group relative inline-flex items-center gap-3 bg-persimmon px-7 py-4 font-sans text-[15px] font-medium tracking-tight text-v2-text transition-all duration-200 hover:translate-y-[-1px] hover:shadow-[0_0_36px_rgba(199,58,20,0.55)]"
              >
                <span className="absolute inset-0 -z-10 bg-persimmon blur-md opacity-30 group-hover:opacity-60 transition-opacity" aria-hidden />
                Get a free OKR Health Check
                <span className="inline-block transition-transform group-hover:translate-x-1" aria-hidden>→</span>
              </Link>
              <a
                href="#brief"
                className="group inline-flex items-center gap-2 border border-v2-rule-strong px-5 py-3 font-mono text-[12px] tracking-[0.14em] text-v2-text-dim hover:border-v2-cyan hover:text-v2-cyan transition-colors"
              >
                VIEW_SAMPLE_BRIEF
                <span className="inline-block transition-transform group-hover:translate-x-0.5" aria-hidden>›</span>
              </a>
            </div>

            {/* Live source readout — bottom anchor for the column */}
            <div className="reveal reveal-5 mt-14 grid max-w-md grid-cols-2 gap-x-6 gap-y-2 border-t border-v2-rule pt-5 font-mono text-[11px] tracking-[0.14em] text-v2-text-dim">
              {[
                ["EVENTS_24H", "412"],
                ["MAPPED",     "98.3%"],
                ["DRIFT_FOUND", "3 KRs"],
                ["BRIEF_SENT",  "FRI 09:00:14"],
              ].map(([k, v]) => (
                <div key={k} className="flex items-baseline justify-between">
                  <span className="text-v2-muted">{k}</span>
                  <span className="text-v2-cyan">{v}</span>
                </div>
              ))}
            </div>
          </div>

          {/* 3D scene column */}
          <div className="reveal reveal-3 relative lg:col-span-5">
            <div className="aspect-square w-full max-h-[640px]">
              {render3D ? (
                <DataFlow3D className="h-full w-full" />
              ) : (
                <DataFlowFallbackSVG className="h-full w-full" />
              )}
            </div>
            {/* Caption strip beneath the scene */}
            <div className="mt-3 flex items-baseline justify-between font-mono text-[10px] tracking-[0.2em] text-v2-muted">
              <span>FIG_01 — DATA_FLOW_SCHEMATIC</span>
              <span>4 SOURCES → 1 DASHBOARD</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom marquee — engineering ticker */}
      <div className="border-t border-v2-rule bg-v2-bg-elev/60">
        <div className="mx-auto max-w-page px-6 py-3 lg:px-10">
          <div className="flex flex-wrap items-center gap-x-6 gap-y-1 font-mono text-[10px] tracking-[0.16em] text-v2-muted">
            <span className="text-v2-cyan">●</span>
            <span className="uppercase">ingest_github</span>
            <span>›</span>
            <span className="uppercase">map_to_kr</span>
            <span>›</span>
            <span className="uppercase">verdict_per_kr</span>
            <span>›</span>
            <span className="uppercase">narrate_brief</span>
            <span>›</span>
            <span className="uppercase">deliver_friday_09:00</span>
          </div>
        </div>
      </div>
    </section>
  );
}
