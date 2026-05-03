// Magic-link callback. Supabase appends `?code=<otp>` (or `?token_hash`)
// to the redirect URL set in signInWithOtp. We exchange the code for a
// session cookie on the server, then bounce the user to their original
// destination (`?next=…`) or the dashboard.
//
// No-op safety: if Supabase env is missing, we redirect home instead of
// 500'ing — matches the middleware's "don't black-hole the app" posture.

import { NextRequest, NextResponse } from "next/server";

import { createClient } from "@/lib/supabase/server";

export async function GET(req: NextRequest) {
  const { searchParams, origin } = req.nextUrl;
  const code = searchParams.get("code");
  const next = searchParams.get("next") || "/app/dashboard";

  // Defensive: only follow same-origin "next" paths so this can't be
  // weaponized as an open redirect.
  const safeNext = next.startsWith("/") && !next.startsWith("//")
    ? next
    : "/app/dashboard";

  if (!code) {
    return NextResponse.redirect(`${origin}/app/login?error=missing_code`);
  }

  try {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (error) {
      return NextResponse.redirect(
        `${origin}/app/login?error=${encodeURIComponent(error.message)}`,
      );
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : "auth_unavailable";
    return NextResponse.redirect(
      `${origin}/app/login?error=${encodeURIComponent(message)}`,
    );
  }

  return NextResponse.redirect(`${origin}${safeNext}`);
}
