import { SectionHeading } from "./SectionHeading";

const TIERS = [
  {
    name: "Pilot",
    price: "$0",
    cadence: "60 days",
    blurb: "Prove it on your real data.",
    features: [
      "All integrations enabled",
      "Up to 200 contributors",
      "One Slack workspace",
      "Founder-led onboarding",
      "Decide before you pay",
    ],
    cta: "Apply for a pilot",
    emphasis: false,
  },
  {
    name: "Starter",
    price: "$299",
    cadence: "/month",
    blurb: "For teams under 50.",
    features: [
      "Up to 50 contributors",
      "GitHub + 1 ticket source",
      "Weekly Friday brief",
      "Slack delivery",
      "Email support",
    ],
    cta: "Choose Starter",
    emphasis: false,
  },
  {
    name: "Team",
    price: "$899",
    cadence: "/month",
    blurb: "For most companies.",
    features: [
      "Up to 50 contributors",
      "All integrations",
      "Daily 7 PM exec digest",
      "OKR drift alerts",
      "Slack + email + dashboard",
    ],
    cta: "Choose Team",
    emphasis: true,
  },
  {
    name: "Scale",
    price: "$2,499",
    cadence: "/month",
    blurb: "Multi-team, audit-grade.",
    features: [
      "Up to 200 contributors",
      "SSO + audit log",
      "Per-team briefs",
      "Custom KR scoring",
      "DPA, SOC 2 reports",
    ],
    cta: "Talk to founders",
    emphasis: false,
  },
];

export function Pricing() {
  return (
    <section id="pricing" className="border-b border-rule bg-paper">
      <div className="mx-auto max-w-page px-6 py-24 lg:px-10 lg:py-32">
        <SectionHeading
          number="05"
          label="Pricing"
          title={
            <>
              Pay when you&rsquo;re convinced.{" "}
              <span className="italic">Not before.</span>
            </>
          }
          kicker="No demo gating, no annual prepay, no haggling on procurement."
        />

        <div className="mt-16 grid grid-cols-1 border-t border-rule-strong/70 sm:grid-cols-2 lg:grid-cols-4">
          {TIERS.map((t, i) => (
            <article
              key={t.name}
              className={`relative flex flex-col px-6 py-8 lg:px-7 lg:py-10 ${
                i !== 0 ? "border-t border-rule sm:border-l sm:border-t-0 sm:border-l-rule" : ""
              } ${
                i === 2 ? "sm:border-t lg:border-t-0" : ""
              } ${
                t.emphasis
                  ? "bg-ink text-paper sm:!border-l-ink lg:!border-l-rule"
                  : ""
              }`}
            >
              {t.emphasis && (
                <span className="absolute -top-3 left-6 inline-block bg-persimmon px-2 py-1 font-mono text-[10px] font-semibold tracking-label text-paper">
                  Most pilots land here
                </span>
              )}

              <div className={`label !text-persimmon ${t.emphasis ? "!text-persimmon" : ""}`}>
                {t.name}
              </div>

              <div className="mt-3 flex items-baseline gap-2">
                <span
                  className={`font-display text-[44px] font-semibold leading-none tracking-tightest ${
                    t.emphasis ? "text-paper" : "text-ink"
                  }`}
                >
                  {t.price}
                </span>
                <span
                  className={`font-mono text-[13px] ${
                    t.emphasis ? "text-paper/60" : "text-muted"
                  }`}
                >
                  {t.cadence}
                </span>
              </div>

              <p
                className={`mt-3 font-display italic text-[16px] leading-snug ${
                  t.emphasis ? "text-paper/80" : "text-ink-soft"
                }`}
              >
                {t.blurb}
              </p>

              <ul className="mt-7 flex-1 space-y-2.5 text-[14px]">
                {t.features.map((f) => (
                  <li
                    key={f}
                    className={`flex items-start gap-2 ${
                      t.emphasis ? "text-paper/85" : "text-ink-soft"
                    }`}
                  >
                    <span
                      className={`mt-2 inline-block h-px w-2 ${
                        t.emphasis ? "bg-paper/40" : "bg-rule-strong/60"
                      }`}
                      aria-hidden="true"
                    />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>

              <a
                href="#waitlist"
                className={`mt-8 inline-flex items-center gap-1.5 self-start border-b pb-0.5 font-sans text-[14px] transition-colors ${
                  t.emphasis
                    ? "border-paper text-paper hover:border-persimmon hover:text-persimmon"
                    : "border-ink-soft text-ink-soft hover:border-persimmon hover:text-persimmon"
                }`}
              >
                {t.cta}
                <span aria-hidden="true">→</span>
              </a>
            </article>
          ))}
        </div>

        <div className="mt-10 max-w-[68ch] text-[14px] leading-relaxed text-muted">
          Per-contributor counts mean active people committing, ticketing, or
          messaging during the billing month — not seats. If your team grows
          past a tier, we move you up at the next month start. We don&rsquo;t
          charge mid-month for a single new hire.
        </div>
      </div>
    </section>
  );
}
