// Auth gate for /app/* routes (everything that requires a signed-in
// design partner). Login and the magic-link callback are exempt.
//
// Two responsibilities:
//   1. Refresh the Supabase session cookie on every request so the
//      server components downstream see a valid auth state without
//      the browser having to bounce through /auth/callback.
//   2. Redirect unauthenticated users from /app/dashboard (and any
//      future /app/* route) to /app/login.

import { NextRequest, NextResponse } from "next/server";
import { type CookieOptions, createServerClient } from "@supabase/ssr";

type CookieToSet = { name: string; value: string; options: CookieOptions };

const PUBLIC_APP_PATHS = new Set<string>(["/app/login", "/app/auth/callback"]);

export async function middleware(req: NextRequest) {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  // If Supabase isn't configured (e.g. local dev without a project),
  // don't black-hole the app. Let the page render so the operator can
  // demo /app/dashboard with the snapshot. Production must set the env.
  if (!url || !anon) {
    return NextResponse.next();
  }

  const res = NextResponse.next({ request: { headers: req.headers } });

  const supabase = createServerClient(url, anon, {
    cookies: {
      getAll() {
        return req.cookies.getAll();
      },
      setAll(toSet: CookieToSet[]) {
        for (const { name, value, options } of toSet) {
          res.cookies.set({ name, value, ...options });
        }
      },
    },
  });

  // getUser revalidates the session against the auth server; safer than
  // getSession (which trusts the cookie blindly).
  const { data: { user } } = await supabase.auth.getUser();

  const path = req.nextUrl.pathname;
  const inAppArea = path.startsWith("/app");
  const isPublic = PUBLIC_APP_PATHS.has(path);

  if (inAppArea && !isPublic && !user) {
    const login = req.nextUrl.clone();
    login.pathname = "/app/login";
    login.searchParams.set("next", path);
    return NextResponse.redirect(login);
  }

  return res;
}

export const config = {
  // Run on every /app/* path so session cookies stay fresh and the gate
  // applies. Static assets, _next, and the marketing routes are skipped.
  matcher: ["/app/:path*"],
};
