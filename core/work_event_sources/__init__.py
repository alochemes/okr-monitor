"""Work-event source registry. Each entry maps a source key to its
module + status. See `notion/02_product/04_okr_source_integrations.md`.

Source keys group by sub-category (code / tickets / docs / chat / crm)
to keep the front-end navigation tidy. The grouping is metadata only —
all sources implement the same `poll(slug, *, config, since_days)`
contract.

Status values: see `core/okr_sources/__init__.py`.
"""

from __future__ import annotations

REGISTRY: dict[str, dict[str, str]] = {
    # --- code ---
    "github":         {"name": "GitHub",         "subcat": "code",    "auth": "pat",         "status": "shipped"},
    "gitlab":         {"name": "GitLab",         "subcat": "code",    "auth": "pat",         "status": "stub"},
    "bitbucket":      {"name": "Bitbucket",      "subcat": "code",    "auth": "app_pwd",     "status": "stub"},

    # --- tickets ---
    "linear":         {"name": "Linear",         "subcat": "tickets", "auth": "api_key",     "status": "shipped"},
    "jira":           {"name": "Jira",           "subcat": "tickets", "auth": "atlassian",   "status": "stub"},
    "asana_tasks":    {"name": "Asana (tasks)",  "subcat": "tickets", "auth": "pat",         "status": "stub"},
    "shortcut":       {"name": "Shortcut",       "subcat": "tickets", "auth": "api_token",   "status": "planned"},
    "github_issues":  {"name": "GitHub Issues",  "subcat": "tickets", "auth": "pat",         "status": "stub"},

    # --- docs ---
    "notion_docs":    {"name": "Notion (docs)",  "subcat": "docs",    "auth": "internal_token", "status": "planned"},
    "confluence":     {"name": "Confluence",     "subcat": "docs",    "auth": "atlassian",   "status": "planned"},
    "google_drive":   {"name": "Google Drive",   "subcat": "docs",    "auth": "oauth2",      "status": "planned"},
    "coda_docs":      {"name": "Coda (docs)",    "subcat": "docs",    "auth": "api_token",   "status": "planned"},

    # --- chat ---
    "slack":          {"name": "Slack",          "subcat": "chat",    "auth": "bot_token",   "status": "stub"},
    "teams":          {"name": "Microsoft Teams","subcat": "chat",    "auth": "graph_oauth", "status": "planned"},
    "discord":        {"name": "Discord",        "subcat": "chat",    "auth": "bot_token",   "status": "planned"},

    # --- CRM ---
    "hubspot":        {"name": "HubSpot",        "subcat": "crm",     "auth": "private_app", "status": "stub"},
    "salesforce":     {"name": "Salesforce",     "subcat": "crm",     "auth": "oauth2",      "status": "planned"},
    "pipedrive":      {"name": "Pipedrive",      "subcat": "crm",     "auth": "api_token",   "status": "planned"},
    "attio":          {"name": "Attio",          "subcat": "crm",     "auth": "api_key",     "status": "planned"},
}


SUBCATS = ("code", "tickets", "docs", "chat", "crm")


def list_sources(subcat: str | None = None) -> list[dict[str, str]]:
    out = [{"key": k, **v} for k, v in REGISTRY.items()
           if subcat is None or v["subcat"] == subcat]
    order = {"shipped": 0, "in_progress": 1, "stub": 2, "planned": 3, "deferred": 4}
    return sorted(out, key=lambda x: (order.get(x["status"], 9), x["name"]))
