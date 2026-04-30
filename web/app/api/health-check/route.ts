// Health Check intake — the lead-magnet capture endpoint.
//
// Accepts a structured intake matching scripts/run_okr_health_check.py's
// expected YAML shape. Persists to <repo>/data/health_checks/<slug>/intake.json
// locally so the operator can run the generator manually.
//
// Vercel filesystem fallback: when running in production (read-only fs
// outside /tmp), logs the entry to stdout for recovery from Function logs.

import { NextResponse } from "next/server";
import { promises as fs } from "node:fs";
import path from "node:path";

interface KrCandidate {
  text: string;
}

interface IntakePayload {
  // Identity
  email: string;
  full_name?: string;
  company_name: string;
  // Company context
  company_size?: number;
  stage?: string;
  industry?: string;
  buyer_role?: string;
  quarter_end?: string;
  // OKR practice
  has_okrs?: boolean;
  okr_tool?: string;
  biggest_frustration?: string;
  // 5-in-5 exercise
  candidate_objective?: string;
  candidate_krs?: KrCandidate[];
  // Recent work narrative
  recent_work_summary?: string;
  // Win definition
  pilot_win_definition?: string;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function repoRoot(): string {
  return path.resolve(process.cwd(), "..");
}

function slugify(s: string): string {
  return (
    s
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_|_$/g, "")
      .slice(0, 60) || "unnamed"
  );
}

function toIntakeYamlShape(p: IntakePayload): Record<string, unknown> {
  // Maps the form payload into the same shape scripts/run_okr_health_check.py
  // expects when it loads data/health_checks/<slug>/intake.yaml.
  return {
    company: {
      name: p.company_name,
      size: p.company_size,
      stage: p.stage,
      industry: p.industry,
      buyer_role: p.buyer_role,
    },
    submitter: {
      email: p.email,
      full_name: p.full_name,
    },
    current_okr_practice: {
      has_okrs: Boolean(p.has_okrs),
      tool: p.okr_tool,
      biggest_frustration: p.biggest_frustration,
    },
    five_in_five: {
      objective: p.candidate_objective,
      candidate_krs: (p.candidate_krs ?? []).map((k) => k.text).filter(Boolean),
    },
    pilot_specifics: {
      quarter_end: p.quarter_end,
      pilot_win_definition: p.pilot_win_definition,
    },
    recent_work_summary: p.recent_work_summary,
    submitted_at: new Date().toISOString(),
    source: "web/health-check-form",
  };
}

async function persistLocally(
  slug: string,
  payload: Record<string, unknown>,
): Promise<{ written: boolean; path?: string; reason?: string }> {
  try {
    const dir = path.join(repoRoot(), "data", "health_checks", slug);
    await fs.mkdir(dir, { recursive: true });
    const file = path.join(dir, "intake.json");
    await fs.writeFile(file, JSON.stringify(payload, null, 2) + "\n", "utf-8");
    return { written: true, path: file };
  } catch (err) {
    return { written: false, reason: String(err) };
  }
}

export async function POST(req: Request) {
  let body: IntakePayload;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const email = (body.email ?? "").trim().toLowerCase();
  const company = (body.company_name ?? "").trim();
  if (!email || !EMAIL_RE.test(email) || email.length > 254) {
    return NextResponse.json(
      { error: "Please enter a valid work email." },
      { status: 400 },
    );
  }
  if (!company) {
    return NextResponse.json(
      { error: "Company name is required." },
      { status: 400 },
    );
  }

  const slug = slugify(company);
  const yamlShape = toIntakeYamlShape({
    ...body,
    email,
    company_name: company,
  });

  const persisted = await persistLocally(slug, yamlShape);
  if (!persisted.written) {
    console.log("[health-check:fallback]", JSON.stringify(yamlShape));
  }

  return NextResponse.json(
    {
      ok: true,
      stored: persisted.written ? "file" : "log",
      slug,
      next_step:
        "We'll generate your Health Check within 2 business days and send it to the email above.",
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
