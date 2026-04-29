"use client";

// Hook for reading a PostHog feature flag as an A/B variant. Captures an
// $experiment_started event the first time a unique visitor is exposed to a
// variant, so the reporting CLI can compute exposures.
//
// Usage:
//   const variant = useExperiment("hero_headline", "control");
//   if (variant === "variant_a") return <H1A />;
//
// If PostHog isn't initialized (no key in env), returns the fallback so
// dev / preview always renders deterministically.

import { useEffect, useState } from "react";
import posthog from "posthog-js";

type AnyVariant = string;

const exposed = new Set<string>();

export function useExperiment<V extends AnyVariant>(
  flagKey: string,
  fallback: V,
): V | string {
  const [variant, setVariant] = useState<V | string>(fallback);

  useEffect(() => {
    if (typeof window === "undefined") return;
    // Wait for posthog to be ready (initialized lazily by the provider).
    const tryRead = () => {
      const ph = (posthog as unknown as { __loaded?: boolean }).__loaded;
      if (!ph) return false;
      const v = posthog.getFeatureFlag(flagKey);
      if (typeof v === "string" && v) {
        setVariant(v);
        if (!exposed.has(flagKey)) {
          exposed.add(flagKey);
          posthog.capture("$experiment_started", {
            $feature_flag: flagKey,
            $feature_flag_response: v,
          });
        }
        return true;
      }
      return false;
    };
    if (tryRead()) return;
    // posthog might still be initializing; poll briefly.
    const id = window.setInterval(() => {
      if (tryRead()) window.clearInterval(id);
    }, 80);
    const stop = window.setTimeout(() => window.clearInterval(id), 3000);
    return () => {
      window.clearInterval(id);
      window.clearTimeout(stop);
    };
  }, [flagKey]);

  return variant;
}
