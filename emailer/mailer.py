# emailer/mailer.py

from __future__ import annotations
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import os


def send_digest(digest_path: Path, config: dict):
    """
    Sends the digest markdown file to the configured email recipients.
    Uses Gmail SMTP with app-password authentication.
    """

    email_cfg = config.get("email_notifications", {})
    sender = email_cfg.get("sender")
    recipients = email_cfg.get("recipients", [])
    subject_template = email_cfg.get("subject_template", "JobSearch Digest — {{date}}")

    if not sender or not recipients:
        raise RuntimeError(
            "Missing sender or recipients in email_notifications config."
        )

    # Replace {{date}} in subject
    from datetime import datetime

    subject = subject_template.replace(
        "{{date}}", datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    # Read the digest content
    digest_content = digest_path.read_text()

    # Email setup
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    msg.attach(MIMEText(digest_content, "plain"))

    # Environment variable for Gmail app password
    password = os.environ.get("EMAIL_PASSWORD")
    if not password:
        raise RuntimeError(
            "EMAIL_PASSWORD not set. Export it via: "
            "export EMAIL_PASSWORD='your-16-char-app-password'"
        )

    smtp_host = email_cfg.get("smtp_host", "smtp.gmail.com")
    smtp_port = email_cfg.get("smtp_port", 587)
    use_tls = email_cfg.get("use_tls", True)

    # Send email via Gmail SMTP
    server = smtplib.SMTP(smtp_host, smtp_port)
    if use_tls:
        server.starttls()

    server.login(sender, password)
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()

    print("[Email] Digest sent successfully.")
