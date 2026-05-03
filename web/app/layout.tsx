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

const PAGE_TITLE = "OKR Monitor — connect goals to the work";
const PAGE_DESC =
  "OKR drift, surfaced the day it starts — not the week it ends. A live scoreboard you can check anytime, and a one-page Friday brief that anchors Monday standup.";

export const metadata: Metadata = {
  title: PAGE_TITLE,
  description: PAGE_DESC,
  icons: {
    icon: "/logo-icon.svg",
  },
  openGraph: {
    title: PAGE_TITLE,
    description: PAGE_DESC,
    type: "website",
    images: [{ url: "/og.svg", width: 1200, height: 630, alt: "OKR Monitor" }],
  },
  twitter: {
    card: "summary_large_image",
    title: PAGE_TITLE,
    description: PAGE_DESC,
    images: ["/og.svg"],
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
