// Static SVG of the same composition as <DataFlow3D />.
// Renders for: mobile (<768px), users with prefers-reduced-motion, no-WebGL.
// Same color palette + same nodes as the live scene so the brand feel is identical.

const SOURCES = [
  { label: "GITHUB",  x: 110, y: 110 },
  { label: "LINEAR",  x: 530, y: 110 },
  { label: "SLACK",   x: 110, y: 410 },
  { label: "NOTION",  x: 530, y: 410 },
];

export function DataFlowFallbackSVG({ className = "" }: { className?: string }) {
  const cx = 320;
  const cy = 260;

  return (
    <svg
      viewBox="0 0 640 520"
      className={className}
      role="img"
      aria-label="Diagram of OKR Monitor connecting GitHub, Linear, Slack, and Notion to a central dashboard node"
    >
      {/* Boundary "system" arc — wireframe sphere stand-in */}
      <defs>
        <radialGradient id="boundaryGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="rgba(0,217,255,0.0)" />
          <stop offset="80%" stopColor="rgba(0,217,255,0.08)" />
          <stop offset="100%" stopColor="rgba(0,217,255,0.0)" />
        </radialGradient>
        <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%"   stopColor="rgba(199,58,20,0.55)" />
          <stop offset="60%"  stopColor="rgba(199,58,20,0.12)" />
          <stop offset="100%" stopColor="rgba(199,58,20,0.0)" />
        </radialGradient>
      </defs>

      {/* Faint grid */}
      <g opacity="0.25">
        {[0, 80, 160, 240, 320, 400, 480, 560].map((x) => (
          <line key={`vx-${x}`} x1={x} x2={x} y1="0" y2="520" stroke="#1A1F2E" strokeWidth="1" />
        ))}
        {[0, 80, 160, 240, 320, 400, 480].map((y) => (
          <line key={`hy-${y}`} x1="0" x2="640" y1={y} y2={y} stroke="#1A1F2E" strokeWidth="1" />
        ))}
      </g>

      {/* Boundary halo */}
      <circle cx={cx} cy={cy} r="220" fill="url(#boundaryGrad)" />
      <circle cx={cx} cy={cy} r="220" fill="none" stroke="#1A1F2E" strokeWidth="1" strokeDasharray="2 6" opacity="0.6" />
      <circle cx={cx} cy={cy} r="160" fill="none" stroke="#1A1F2E" strokeWidth="1" strokeDasharray="2 8" opacity="0.4" />

      {/* Curved data streams from each source to center */}
      {SOURCES.map((s) => {
        // Quadratic Bezier with a control point pulled toward center & up
        const ctrlX = (s.x + cx) / 2;
        const ctrlY = ((s.y + cy) / 2) - 30;
        return (
          <g key={`stream-${s.label}`}>
            <path
              d={`M ${s.x} ${s.y} Q ${ctrlX} ${ctrlY} ${cx} ${cy}`}
              fill="none"
              stroke="#00D9FF"
              strokeWidth="1"
              opacity="0.4"
            />
            {/* tracer dot — single position (not animated in fallback) */}
            <circle cx={ctrlX} cy={ctrlY + 4} r="3" fill="#00D9FF">
              <animate
                attributeName="opacity"
                values="0.3;1;0.3"
                dur="2.6s"
                repeatCount="indefinite"
                begin={`${SOURCES.indexOf(s) * 0.4}s`}
              />
            </circle>
          </g>
        );
      })}

      {/* Central node — glowing octagon */}
      <circle cx={cx} cy={cy} r="60" fill="url(#centerGlow)" />
      <polygon
        points={`${cx-26},${cy} ${cx-18},${cy-18} ${cx},${cy-26} ${cx+18},${cy-18} ${cx+26},${cy} ${cx+18},${cy+18} ${cx},${cy+26} ${cx-18},${cy+18}`}
        fill="#0B0E18"
        stroke="#C73A14"
        strokeWidth="1.5"
      />
      <polygon
        points={`${cx-13},${cy} ${cx-9},${cy-9} ${cx},${cy-13} ${cx+9},${cy-9} ${cx+13},${cy} ${cx+9},${cy+9} ${cx},${cy+13} ${cx-9},${cy+9}`}
        fill="#C73A14"
      >
        <animate attributeName="opacity" values="1;0.55;1" dur="2.4s" repeatCount="indefinite" />
      </polygon>
      <text
        x={cx}
        y={cy + 56}
        textAnchor="middle"
        className="font-mono"
        fontFamily="JetBrains Mono, ui-monospace, monospace"
        fontSize="10"
        fill="#C73A14"
        letterSpacing="2"
      >
        DASHBOARD
      </text>

      {/* Source plinths */}
      {SOURCES.map((s) => (
        <g key={`node-${s.label}`}>
          {/* Subtle halo */}
          <rect
            x={s.x - 50}
            y={s.y - 16}
            width="100"
            height="32"
            fill="none"
            stroke="#00D9FF"
            strokeWidth="1"
            opacity="0.15"
          />
          {/* Plinth */}
          <rect
            x={s.x - 44}
            y={s.y - 12}
            width="88"
            height="24"
            fill="#101522"
            stroke="#2A3142"
            strokeWidth="1"
          />
          {/* Status dot */}
          <circle cx={s.x - 32} cy={s.y} r="2.5" fill="#00D9FF">
            <animate attributeName="opacity" values="1;0.4;1" dur="1.8s" repeatCount="indefinite" />
          </circle>
          {/* Label */}
          <text
            x={s.x + 6}
            y={s.y + 4}
            fontFamily="JetBrains Mono, ui-monospace, monospace"
            fontSize="11"
            fill="#E6EAF2"
            letterSpacing="2"
          >
            {s.label}
          </text>
        </g>
      ))}

      {/* Bottom-left coordinate read-out — engineering touch */}
      <text x="16" y="500" fontFamily="JetBrains Mono, ui-monospace, monospace" fontSize="9" fill="#6E7691" letterSpacing="2">
        SYS · NODES 4 · STREAMS 4 · STATUS NOMINAL
      </text>
    </svg>
  );
}
