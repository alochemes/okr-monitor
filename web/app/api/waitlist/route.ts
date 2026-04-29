// Waitlist capture endpoint.
//
// v0 behavior: append each signup to <repo>/data/waitlist.json so the operator
// can read it locally. On Vercel (read-only filesystem outside /tmp), we fall
// back to logging the entry to stdout — visible in Vercel Function logs.
// Move to a real store (Resend audience, Supabase, Postmark) when traffic
// warrants.

import { NextResponse } from "next/server";
import { promises as fs } from "node:fs";
import path from "node:path";

interface Entry {
  email: string;
  role?: string;
  company?: string;
  source?: string;
  ts: string;
  ua?: string;
  ip?: string;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function repoRoot(): string {
  // app/api/waitlist/route.ts → ../../../.. → repo/web → repo
  return path.resolve(process.cwd(), "..");
}

async function appendToFile(entry: Entry): Promise<{ written: boolean; reason?: string }> {
  try {
    const dataDir = path.join(repoRoot(), "data");
    const file = path.join(dataDir, "waitlist.json");
    await fs.mkdir(dataDir, { recursive: true });

    let existing: Entry[] = [];
    try {
      const raw = await fs.readFile(file, "utf-8");
      existing = JSON.parse(raw);
      if (!Array.isArray(existing)) existing = [];
    } catch {
      existing = [];
    }

    existing.push(entry);
    await fs.writeFile(file, JSON.stringify(existing, null, 2) + "\n", "utf-8");
    return { written: true };
  } catch (err) {
    return { written: false, reason: String(err) };
  }
}

export async function POST(req: Request) {
  let body: { email?: string; role?: string; company?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const email = (body.email ?? "").trim().toLowerCase();
  const role = (body.role ?? "").trim();
  const company = (body.company ?? "").trim();

  if (!email || !EMAIL_RE.test(email) || email.length > 254) {
    return NextResponse.json(
      { error: "Please enter a valid work email." },
      { status: 400 },
    );
  }

  const entry: Entry = {
    email,
    role: role || undefined,
    company: company || undefined,
    source: "landing/waitlist",
    ts: new Date().toISOString(),
    ua: req.headers.get("user-agent") ?? undefined,
    ip:
      req.headers.get("x-forwarded-for") ??
      req.headers.get("x-real-ip") ??
      undefined,
  };

  const result = await appendToFile(entry);
  if (!result.written) {
    // Filesystem unavailable (Vercel prod); log so the entry is recoverable
    // from Vercel Function logs.
    console.log("[waitlist:fallback]", JSON.stringify(entry));
  }

  return NextResponse.json(
    {
      ok: true,
      stored: result.written ? "file" : "log",
    },
    { status: 200 },
  );
}

export async function GET() {
  return NextResponse.json(
    { error: "Method not allowed. POST only." },
    { status: 405 },
  );
}
