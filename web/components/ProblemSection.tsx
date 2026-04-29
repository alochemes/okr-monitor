import { SectionHeading } from "./SectionHeading";

const SYMPTOMS = [
  {
    n: "i.",
    line: "Your Monday status meeting is the autopsy.",
    sub: "By the time you're asking 'are we on track?', you've already lost a week.",
  },
  {
    n: "ii.",
    line: "The OKR doc and the work happening are two different documents.",
    sub: "Notion says 'In progress.' GitHub says nothing has touched it in 19 days.",
  },
  {
    n: "iii.",
    line: "By Q-end, the post-mortem is the most honest writing your company does.",
    sub: "Drift could have been seen in week 3. It wasn't visible until week 11.",
  },
];

export function ProblemSection() {
  return (
    <section className="border-b border-rule bg-paper">
      <div className="mx-auto max-w-page px-6 py-24 lg:px-10 lg:py-32">
        <SectionHeading
          number="02"
          label="The Autopsy"
          title={
            <>
              Quarterly check-ins are{" "}
              <span className="italic">a memorial service</span> —
              not a steering wheel.
            </>
          }
          kicker="A short polemic on why your OKRs and your week never match."
        />

        <div className="mt-16 grid grid-cols-1 gap-12 md:grid-cols-3 md:gap-10">
          {SYMPTOMS.map((s) => (
            <article
              key={s.n}
              className="border-t border-rule-strong/70 pt-5"
            >
              <div className="mb-4 font-mono text-[11px] tracking-label text-persimmon">
                {s.n}
              </div>
              <p className="font-display text-[22px] leading-[1.25] tracking-editorial text-ink">
                {s.line}
              </p>
              <p className="mt-4 max-w-[34ch] text-[14.5px] leading-[1.55] text-muted">
                {s.sub}
              </p>
            </article>
          ))}
        </div>

        {/* Pull quote — magazine treatment */}
        <figure className="mt-24 grid grid-cols-1 gap-8 lg:grid-cols-12 lg:gap-12">
          <div className="lg:col-span-3">
            <div className="label">Field note</div>
            <div className="mt-2 text-[13px] text-muted">
              Anonymized · CoS at a Series B fintech, 220 employees.
            </div>
          </div>
          <blockquote className="lg:col-span-9">
            <p className="font-display text-[clamp(28px,3vw,40px)] font-medium italic leading-[1.2] tracking-editorial text-ink">
              &ldquo;Every Monday I spend an hour playing telephone — DMing
              five people to find out if the OKRs we set in January are
              still real. By the time I&rsquo;ve answered the CEO, the
              answer is already two days old.&rdquo;
            </p>
          </blockquote>
        </figure>
      </div>
    </section>
  );
}
