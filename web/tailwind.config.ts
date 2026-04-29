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
      },
      animation: {
        rise: 'rise 0.7s cubic-bezier(0.2, 0.7, 0.2, 1) forwards',
        'fade-in': 'fadeIn 0.6s ease-out forwards',
      },
    },
  },
  plugins: [],
} satisfies Config;
