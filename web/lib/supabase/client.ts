// Browser-side Supabase client. Used by client components to start the
// magic-link flow (signInWithOtp) and read the current session.
//
// The cookie-aware @supabase/ssr browser client keeps auth state in sync
// with the server. Do not import this from a server component — use
// `lib/supabase/server.ts` there instead.

import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !anon) {
    throw new Error(
      "Supabase env not configured: set NEXT_PUBLIC_SUPABASE_URL " +
        "and NEXT_PUBLIC_SUPABASE_ANON_KEY in your Vercel project " +
        "(or .env.local for dev).",
    );
  }
  return createBrowserClient(url, anon);
}
