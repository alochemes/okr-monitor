import type { Config } from "tailwindcss";

export default {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Editorial paper-and-ink palette. One accent: persimmon.
        paper: "#FAF7F2",
        "paper-deep": "#F2EDE4",
        ink: "#0F0E0C",
        "ink-soft": "#1F1D1A",
        muted: "#6B6862",
        rule: "#D9D2C4",
        "rule-strong": "#1F1D1A",
        persimmon: {
          DEFAULT: "#C73A14",
          dark: "#A52E0F",
          ink: "#5A1A07",
        },
        verdict: {
          on: "#1F6F44",
          drift: "#A66A00",
          off: "#9C2A1A",
        },
        // v2 — high-tech "engineering ops console" palette. Isolated
        // namespace so editorial / and tech /v2 can coexist without
        // either palette polluting the other.
        v2: {
          bg: "#06070A",
          "bg-elev": "#0B0E18",
          "bg-card": "#101522",
          "bg-card-2": "#161C2E",
          text: "#E6EAF2",
          "text-dim": "#A5ADBE",
          muted: "#6E7691",
          rule: "#1A1F2E",
          "rule-strong": "#2A3142",
          cyan: {
            DEFAULT: "#00D9FF",
            dim: "#0099B8",
            faint: "#1A4A5C",
          },
        },
      },
      fontFamily: {
        display: ['var(--font-display)', 'Georgia', 'serif'],
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      letterSpacing: {
        tightest: '-0.045em',
        tighter: '-0.02em',
        editorial: '-0.015em',
        label: '0.18em',
      },
      maxWidth: {
        page: '1280px',
        prose: '68ch',
      },
      keyframes: {
        rise: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        // v2 — slow, ambient pulse for the central node + status dots.
        pulse_v2: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.55', transform: 'scale(0.92)' },
        },
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(200%)' },
        },
      },
      animation: {
        rise: 'rise 0.7s cubic-bezier(0.2, 0.7, 0.2, 1) forwards',
        'fade-in': 'fadeIn 0.6s ease-out forwards',
        'pulse-v2': 'pulse_v2 2.4s ease-in-out infinite',
        'scan': 'scan 8s linear infinite',
      },
    },
  },
  plugins: [],
} satisfies Config;
