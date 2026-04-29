import type { Metadata } from "next";
import { Fraunces, Inter, JetBrains_Mono } from "next/font/google";
import { PostHogProvider } from "@/components/PostHogProvider";
import "./globals.css";

const display = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
  weight: ["400", "500", "600", "700", "900"],
  style: ["normal", "italic"],
  display: "swap",
});

const sans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  weight: ["400", "500", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "OKR Monitor — connect goals to the work",
  description:
    "Every Friday, a one-page exec brief naming which OKRs are on track, which are drifting, and exactly which work is — and isn't — moving the needle.",
  openGraph: {
    title: "OKR Monitor — connect goals to the work",
    description:
      "Every Friday, a one-page exec brief naming which OKRs are on track, which are drifting, and exactly which work is — and isn't — moving the needle.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${display.variable} ${sans.variable} ${mono.variable}`}
    >
      <body className="bg-paper text-ink font-sans antialiased selection:bg-persimmon selection:text-paper">
        <PostHogProvider>{children}</PostHogProvider>
      </body>
    </html>
  );
}
