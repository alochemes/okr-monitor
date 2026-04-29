// Editorial section heading — numbered, all-caps label + display headline.

interface Props {
  number: string;        // "02"
  label: string;         // "THE AUTOPSY"
  title: React.ReactNode; // headline
  kicker?: string;       // small italic credit/byline
  className?: string;
}

export function SectionHeading({
  number,
  label,
  title,
  kicker,
  className = "",
}: Props) {
  return (
    <div className={`max-w-prose ${className}`}>
      <div className="mb-5 flex items-center gap-3">
        <span className="font-mono text-[11px] tracking-label text-persimmon">
          {number}
        </span>
        <span className="h-px w-12 bg-persimmon/60" aria-hidden="true" />
        <span className="label-ink">{label}</span>
      </div>
      <h2 className="display-tight font-display text-[clamp(34px,5vw,58px)] font-medium leading-[1.02] tracking-tighter text-ink">
        {title}
      </h2>
      {kicker && (
        <p className="mt-3 font-display italic text-[15px] text-muted">
          {kicker}
        </p>
      )}
    </div>
  );
}
