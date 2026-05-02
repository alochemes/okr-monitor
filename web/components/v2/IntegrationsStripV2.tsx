import { SectionLabelV2 } from "./SectionLabelV2";

const INTEGRATIONS = [
  { name: "GitHub", scope: "repo:read", events: "push · pr · review" },
  { name: "Linear", scope: "issues:read", events: "issue · cycle" },
  { name: "Jira",   scope: "issues:read", events: "issue · sprint" },
  { name: "Slack",  scope: "channels:history", events: "thread · msg" },
  { name: "Notion", scope: "page:read", events: "doc · update" },
];

export function IntegrationsStripV2() {
  return (
    <section className="relative border-b border-v2-rule">
      <div className="relative mx-auto max-w-page px-6 py-20 lg:px-10 lg:py-24">
        <SectionLabelV2 num="04" label="Sources online" meta="MIN_SCOPE · OAUTH" className="mb-10" />

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-12">
          <div className="lg:col-span-3">
            <h2 className="font-sans font-medium leading-[1.05] tracking-tighter text-[clamp(28px,4vw,42px)] text-v2-text">
              Where work
              <span className="block text-v2-cyan">already happens.</span>
            </h2>
          </div>

          <div className="lg:col-span-9">
            {/* Integration chips — glowing port-style */}
            <ul className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
              {INTEGRATIONS.map((src) => (
                <li
                  key={src.name}
                  className="group relative border border-v2-rule bg-v2-bg-elev px-5 py-6 hover:border-v2-cyan hover:shadow-[0_0_24px_rgba(0,217,255,0.18)] transition-all"
                >
                  {/* Status dot */}
                  <span
                    aria-hidden
                    className="absolute right-4 top-4 inline-block h-1.5 w-1.5 rounded-full bg-v2-cyan animate-pulse-v2 shadow-[0_0_10px_rgba(0,217,255,0.55)]"
                  />
                  <div className="font-sans text-[20px] font-semibold tracking-tight text-v2-text group-hover:text-v2-cyan transition-colors">
                    {src.name}
                  </div>
                  <div className="mt-3 space-y-1 font-mono text-[10px] tracking-[0.16em] text-v2-muted">
                    <div>{src.scope}</div>
                    <div className="text-v2-text-dim">{src.events}</div>
                  </div>
                </li>
              ))}
            </ul>

            <p className="mt-8 max-w-[60ch] text-[14px] leading-relaxed text-v2-text-dim">
              <span className="font-mono text-v2-cyan">// </span>
              OAuth scopes are minimum-required. Slack is opt-in per channel.
              No customer data leaves your tenant for training.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
