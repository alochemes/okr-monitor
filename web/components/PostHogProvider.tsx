"use client";

// Wraps the app in PostHog. Loads only in the browser, only when
// NEXT_PUBLIC_POSTHOG_KEY is present, so dev / preview environments without
// the key are no-ops (no warnings, no missing-feature-flag noise).

import { useEffect, useState, type ReactNode } from "react";
import posthog from "posthog-js";

type Status = "idle" | "ready" | "skipped";

let initialized = false;

export function PostHogProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<Status>("idle");

  useEffect(() => {
    if (initialized) {
      setStatus("ready");
      return;
    }
    const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;
    if (!key) {
      setStatus("skipped");
      return;
    }
    posthog.init(key, {
      api_host:
        process.env.NEXT_PUBLIC_POSTHOG_HOST ?? "https://us.i.posthog.com",
      capture_pageview: true,
      capture_pageleave: true,
      // Don't auto-capture every click; we want intentional events.
      autocapture: false,
      persistence: "localStorage+cookie",
      // Bootstrap with feature flags so first-paint variants don't flicker.
      bootstrap: {
        featureFlags: {},
      },
    });
    initialized = true;
    setStatus("ready");
  }, []);

  // Status is exposed via data attribute for debugging in dev tools.
  return <div data-posthog={status}>{children}</div>;
}

// Helper exported for direct use in components without re-imports.
export function trackEvent(name: string, properties?: Record<string, unknown>) {
  if (typeof window === "undefined") return;
  if (!initialized) return;
  posthog.capture(name, properties);
}
