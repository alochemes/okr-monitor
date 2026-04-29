const INTEGRATIONS = [
  { name: "GitHub",  meta: "commits, PRs, reviews" },
  { name: "Linear",  meta: "issues, projects, cycles" },
  { name: "Jira",    meta: "issues, sprints, epics" },
  { name: "Slack",   meta: "channels, threads, messages" },
  { name: "Notion",  meta: "OKR docs, project pages" },
];

export function IntegrationsStrip() {
  return (
    <section className="border-b border-rule bg-paper">
      <div className="mx-auto max-w-page px-6 py-20 lg:px-10 lg:py-24">
        <div className="grid grid-cols-1 gap-10 lg:grid-cols-12 lg:gap-12">
          <div className="lg:col-span-3">
            <div className="flex items-center gap-3">
              <span className="font-mono text-[11px] tracking-label text-persimmon">
                04
              </span>
              <span className="h-px w-10 bg-persimmon/60" aria-hidden="true" />
            </div>
            <h2 className="mt-4 font-display text-[34px] font-medium leading-[1.05] tracking-tighter text-ink">
              Where work
              <span className="block italic">actually happens.</span>
            </h2>
          </div>

          <div className="lg:col-span-9">
            <ul className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5">
              {INTEGRATIONS.map((src, i) => (
                <li
                  key={src.name}
                  className={`group border-t border-rule-strong/70 ${
                    i % 2 === 1 ? "border-l border-l-rule sm:border-l-0" : ""
                  } ${
                    i !== 0 ? "sm:border-l sm:border-l-rule" : ""
                  } px-4 py-7`}
                >
                  <div className="font-display text-[26px] font-medium tracking-tighter text-ink transition-colors group-hover:text-persimmon">
                    {src.name}
                  </div>
                  <div className="mt-2 font-mono text-[11px] leading-relaxed text-muted">
                    {src.meta}
                  </div>
                </li>
              ))}
            </ul>

            <p className="mt-8 max-w-[60ch] text-[14.5px] leading-relaxed text-muted">
              OAuth scopes are minimum-required. Slack is opt-in per channel.
              No customer data leaves your tenant for training.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
