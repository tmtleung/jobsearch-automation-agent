# output/email_sender.py

from __future__ import annotations

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict


def send_email_digest(digest_path: str, config: Dict[str, any]):
    """
    Sends the daily digest via SMTP using credentials stored in environment variables.
    This avoids storing sensitive passwords in config.json.
    """

    email_cfg = config.get("email_settings", {})
    if not email_cfg.get("enabled", False):
        print("[Email] Email disabled in config; skipping.")
        return

    sender = email_cfg.get("sender", "")
    recipients = email_cfg.get("recipients", [])
    smtp_host = email_cfg.get("smtp_host", "")
    smtp_port = email_cfg.get("smtp_port", 587)
    use_tls = email_cfg.get("use_tls", True)

    if not sender or not recipients:
        raise ValueError("Missing sender or recipients in email_settings.")

    # Load password from environment — NEVER store credentials in config
    email_password = os.getenv("EMAIL_PASSWORD")
    if not email_password:
        raise ValueError(
            "EMAIL_PASSWORD not set in environment. "
            "Set it with: export EMAIL_PASSWORD='your-app-password'"
        )

    # Read digest content
    try:
        with open(digest_path, "r", encoding="utf-8") as f:
            digest_text = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read digest: {e}")

    # Build subject line
    subject_template = email_cfg.get("subject_template", "JobSearch Digest — {{date}}")
    today = datetime.now().strftime("%Y-%m-%d")
    subject = subject_template.replace("{{date}}", today)

    # Build email message
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    msg.attach(MIMEText(digest_text, "plain"))

    # Send email
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if use_tls:
                server.starttls()
            server.login(sender, email_password)
            server.sendmail(sender, recipients, msg.as_string())
        print("[Email] Digest sent successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}")
