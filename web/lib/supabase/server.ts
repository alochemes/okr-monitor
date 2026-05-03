// Server-side Supabase client. Reads/writes the auth cookies on the
// Next.js request so server components and route handlers can see the
// current user without a round-trip to the browser.
//
// Each call returns a fresh client because Next.js request scopes the
// cookies() store. Don't cache it across requests.

import { type CookieOptions, createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

type CookieToSet = { name: string; value: string; options: CookieOptions };

export async function createClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !anon) {
    throw new Error(
      "Supabase env not configured: set NEXT_PUBLIC_SUPABASE_URL " +
        "and NEXT_PUBLIC_SUPABASE_ANON_KEY in your Vercel project.",
    );
  }
  const cookieStore = await cookies();
  return createServerClient(url, anon, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(toSet: CookieToSet[]) {
        try {
          for (const { name, value, options } of toSet) {
            cookieStore.set(name, value, options);
          }
        } catch {
          // setAll throws when called from a Server Component — those
          // can't mutate cookies. Middleware refreshes the session, so
          // it's safe to swallow here.
        }
      },
    },
  });
}
