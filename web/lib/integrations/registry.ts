// TypeScript mirror of core/okr_sources, core/work_event_sources, and
// core/kpi_sources Python registries. Drift between the two is a bug.
// The eventual CI step (Sprint 1) parses both files and fails the build
// on mismatch.
//
// When you add a Python registry entry, also add it here with the same
// status. The status values are:
//   shipped     — fully implemented, in production use
//   in_progress — partially implemented, behind a feature flag
//   stub        — module exists with clear docs; raises on call
//   planned     — listed for visibility; no module yet
//   deferred    — explicitly out of scope until further notice

export type IntegrationStatus =
  | "shipped"
  | "in_progress"
  | "stub"
  | "planned"
  | "deferred";

export type IntegrationCategory = "okr-sources" | "work-events" | "kpi-sources";

export type WorkEventSubcat = "code" | "tickets" | "docs" | "chat" | "crm";

export type IntegrationEntry = {
  key: string;
  name: string;
  category: IntegrationCategory;
  subcat?: WorkEventSubcat;
  auth: string;
  status: IntegrationStatus;
};

export const OKR_SOURCES: IntegrationEntry[] = [
  { key: "notion",      name: "Notion",       category: "okr-sources", auth: "internal_token", status: "shipped" },
  { key: "monday",      name: "Monday.com",   category: "okr-sources", auth: "api_token",      status: "stub" },
  { key: "asana",       name: "Asana Goals",  category: "okr-sources", auth: "pat",            status: "stub" },
  { key: "mooncamp",    name: "Mooncamp",     category: "okr-sources", auth: "api_key",        status: "stub" },
  { key: "coda",        name: "Coda",         category: "okr-sources", auth: "api_token",      status: "stub" },
  { key: "csv",         name: "CSV / paste",  category: "okr-sources", auth: "none",           status: "stub" },
  { key: "lattice",     name: "Lattice",      category: "okr-sources", auth: "oauth2",         status: "planned" },
  { key: "workboard",   name: "Workboard",    category: "okr-sources", auth: "pat",            status: "planned" },
  { key: "google_docs", name: "Google Docs",  category: "okr-sources", auth: "oauth2+llm",     status: "deferred" },
];

export const WORK_EVENT_SOURCES: IntegrationEntry[] = [
  // code
  { key: "github",        name: "GitHub",          category: "work-events", subcat: "code",    auth: "pat",          status: "shipped" },
  { key: "gitlab",        name: "GitLab",          category: "work-events", subcat: "code",    auth: "pat",          status: "stub" },
  { key: "bitbucket",     name: "Bitbucket",       category: "work-events", subcat: "code",    auth: "app_pwd",      status: "stub" },
  // tickets
  { key: "linear",        name: "Linear",          category: "work-events", subcat: "tickets", auth: "api_key",      status: "shipped" },
  { key: "jira",          name: "Jira",            category: "work-events", subcat: "tickets", auth: "atlassian",    status: "stub" },
  { key: "asana_tasks",   name: "Asana (tasks)",   category: "work-events", subcat: "tickets", auth: "pat",          status: "stub" },
  { key: "github_issues", name: "GitHub Issues",   category: "work-events", subcat: "tickets", auth: "pat",          status: "stub" },
  { key: "shortcut",      name: "Shortcut",        category: "work-events", subcat: "tickets", auth: "api_token",    status: "planned" },
  // docs
  { key: "notion_docs",   name: "Notion (docs)",   category: "work-events", subcat: "docs",    auth: "internal_token", status: "planned" },
  { key: "confluence",    name: "Confluence",      category: "work-events", subcat: "docs",    auth: "atlassian",    status: "planned" },
  { key: "google_drive",  name: "Google Drive",    category: "work-events", subcat: "docs",    auth: "oauth2",       status: "planned" },
  { key: "coda_docs",     name: "Coda (docs)",     category: "work-events", subcat: "docs",    auth: "api_token",    status: "planned" },
  // chat
  { key: "slack",         name: "Slack",           category: "work-events", subcat: "chat",    auth: "bot_token",    status: "stub" },
  { key: "teams",         name: "Microsoft Teams", category: "work-events", subcat: "chat",    auth: "graph_oauth",  status: "planned" },
  { key: "discord",       name: "Discord",         category: "work-events", subcat: "chat",    auth: "bot_token",    status: "planned" },
  // crm
  { key: "hubspot",       name: "HubSpot",         category: "work-events", subcat: "crm",     auth: "private_app",  status: "stub" },
  { key: "salesforce",    name: "Salesforce",      category: "work-events", subcat: "crm",     auth: "oauth2",       status: "planned" },
  { key: "pipedrive",     name: "Pipedrive",       category: "work-events", subcat: "crm",     auth: "api_token",    status: "planned" },
  { key: "attio",         name: "Attio",           category: "work-events", subcat: "crm",     auth: "api_key",      status: "planned" },
];

export const KPI_SOURCES: IntegrationEntry[] = [
  { key: "datadog",   name: "Datadog",   category: "kpi-sources", auth: "api+app_keys",    status: "stub" },
  { key: "mixpanel",  name: "Mixpanel",  category: "kpi-sources", auth: "service_account", status: "stub" },
  { key: "amplitude", name: "Amplitude", category: "kpi-sources", auth: "api+secret",      status: "planned" },
  { key: "posthog",   name: "PostHog",   category: "kpi-sources", auth: "api_key",         status: "planned" },
  { key: "grafana",   name: "Grafana",   category: "kpi-sources", auth: "api_token",       status: "planned" },
];

export const ALL_INTEGRATIONS: IntegrationEntry[] = [
  ...OKR_SOURCES,
  ...WORK_EVENT_SOURCES,
  ...KPI_SOURCES,
];

const STATUS_ORDER: Record<IntegrationStatus, number> = {
  shipped: 0,
  in_progress: 1,
  stub: 2,
  planned: 3,
  deferred: 4,
};

export function sortByStatus(entries: IntegrationEntry[]): IntegrationEntry[] {
  return [...entries].sort((a, b) => {
    const s = STATUS_ORDER[a.status] - STATUS_ORDER[b.status];
    return s !== 0 ? s : a.name.localeCompare(b.name);
  });
}

export const STATUS_LABEL: Record<IntegrationStatus, string> = {
  shipped: "🟢 connected",
  in_progress: "🟡 in progress",
  stub: "🟠 not yet built",
  planned: "⚪ planned",
  deferred: "⚫ deferred",
};

// Sub-category metadata for the UI navigation.
export const WORK_EVENT_SUBCATS: { key: WorkEventSubcat; name: string; q: string }[] = [
  { key: "code",    name: "Code",          q: "Q18 — where does code live?" },
  { key: "tickets", name: "Tickets",       q: "Q19 — where do tickets live?" },
  { key: "docs",    name: "Docs",          q: "Q20 — where do docs live?" },
  { key: "chat",    name: "Async chat",    q: "Q21 — what's your chat tool?" },
  { key: "crm",     name: "Customer pipeline", q: "Q22 — what's your CRM?" },
];
