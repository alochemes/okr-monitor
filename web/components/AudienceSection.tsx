import { SectionHeading } from "./SectionHeading";

const FOR = [
  "Chiefs of Staff at Series A–C SaaS, 50–500 people.",
  "Heads of Operations who already write the Friday update by hand.",
  "VPs of Engineering who want to know if the work matches the roadmap.",
];

const NOT_FOR = [
  "Pre-seed companies without an OKR practice yet.",
  "1,000+ employee enterprises with a six-month procurement cycle.",
  "Teams hand-updating Excel for OKR tracking — not yet.",
];

export function AudienceSection() {
  return (
    <section className="border-b border-rule bg-paper-deep/40">
      <div className="mx-auto max-w-page px-6 py-24 lg:px-10 lg:py-28">
        <SectionHeading
          number="06"
          label="Who this is for"
          title={
            <>
              Built for the person who writes the
              <span className="italic"> Friday update</span>.
            </>
          }
        />

        <div className="mt-16 grid grid-cols-1 gap-12 md:grid-cols-2 md:gap-16">
          <div>
            <div className="label-ink mb-4">For you, if</div>
            <ul className="space-y-5">
              {FOR.map((line, i) => (
                <li key={i} className="flex items-start gap-4">
                  <span className="mt-2 inline-block h-2 w-2 flex-shrink-0 bg-persimmon" aria-hidden="true" />
                  <span className="font-display text-[19px] leading-[1.45] tracking-editorial text-ink">
                    {line}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <div className="label-ink mb-4">Not yet, if</div>
            <ul className="space-y-5">
              {NOT_FOR.map((line, i) => (
                <li key={i} className="flex items-start gap-4">
                  <span className="mt-2 inline-block h-2 w-2 flex-shrink-0 border border-ink-soft" aria-hidden="true" />
                  <span className="font-display text-[19px] leading-[1.45] tracking-editorial text-muted">
                    {line}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
