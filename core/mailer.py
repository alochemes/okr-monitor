"""Plain-SMTP email sender for the daily OWNER/FINANCE report.

Behavior:
  - If `SMTP_HOST` is set in env, sends via smtplib (TLS on port 587 by
    default). Returns a status dict.
  - If `SMTP_HOST` is empty, returns `{"sent": False, "reason": "..."}` so
    the caller can fall back to file-only mode.
  - Never raises on send failure — returns the failure in the dict so the
    daily report still gets written to disk even if email is broken.

Configuration (in `.env`):
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=you@gmail.com
  SMTP_PASS=<app-password>      # NOT your normal password — use an app-specific one
  SMTP_FROM=alochemes@gmail.com
  REPORT_TO_EMAIL=alochemes@gmail.com
"""

from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from typing import Any


def send_report_email(
    *,
    subject: str,
    body_md: str,
    to_addr: str | None = None,
) -> dict[str, Any]:
    host = os.environ.get("SMTP_HOST", "").strip()
    if not host:
        return {"sent": False, "reason": "SMTP_HOST not set in env; email skipped, report written to file only"}

    try:
        port = int(os.environ.get("SMTP_PORT", "587"))
    except ValueError:
        port = 587
    user = os.environ.get("SMTP_USER", "").strip()
    password = os.environ.get("SMTP_PASS", "")
    from_addr = (os.environ.get("SMTP_FROM") or user or "okr-monitor@localhost").strip()
    to = (to_addr or os.environ.get("REPORT_TO_EMAIL", "")).strip()
    if not to:
        return {"sent": False, "reason": "REPORT_TO_EMAIL not set"}

    # Send markdown as plain-text — most clients render it fine and we
    # avoid the cost/complexity of an HTML converter for v0.
    msg = MIMEText(body_md, _subtype="plain", _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to

    try:
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.ehlo()
            try:
                smtp.starttls()
                smtp.ehlo()
            except smtplib.SMTPException:
                pass    # server doesn't support STARTTLS; proceed plaintext (use port 465 / SMTP_SSL for TLS-only)
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg)
        return {"sent": True, "to": to, "host": host, "port": port,
                "from": from_addr, "subject": subject}
    except Exception as exc:
        return {"sent": False, "reason": f"SMTP send failed: {exc}",
                "host": host, "port": port}
