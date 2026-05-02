// Shared editorial label for /v2 — bracket notation in mono, cyan tint.
// Visual language is "engineering ops console", not "magazine".

interface Props {
  num: string;        // "01"
  label: string;      // "HERO"
  meta?: string;      // optional right-side meta, e.g. "FIG. 1.1"
  className?: string;
}

export function SectionLabelV2({ num, label, meta, className = "" }: Props) {
  return (
    <div className={`flex items-baseline justify-between font-mono ${className}`}>
      <div className="flex items-baseline gap-3 text-[11px] tracking-[0.22em]">
        <span className="text-v2-cyan">[{num}]</span>
        <span className="h-px w-10 self-center bg-v2-cyan/40" aria-hidden />
        <span className="uppercase text-v2-text-dim">{label}</span>
      </div>
      {meta && (
        <span className="text-[10px] tracking-[0.2em] uppercase text-v2-muted">
          {meta}
        </span>
      )}
    </div>
  );
}
