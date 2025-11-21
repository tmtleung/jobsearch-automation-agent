# output/formatter.py

from __future__ import annotations
from typing import Dict, Any


def _format_posted_suffix(job: Dict[str, Any]) -> str:
    """
    Adds the (Posted X days ago) suffix to each job line.
    """
    # Normalized integer version
    if "days_since_posted" in job:
        days = job["days_since_posted"]

        if days == 0:
            human = "today"
        elif days == 1:
            human = "1 day ago"
        else:
            human = f"{days} days ago"

        return f" (Posted {human})"

    # Fallback raw text version if present
    raw = job.get("posted_age_raw")
    if raw:
        return f" (Posted {raw})"

    return ""


def format_job_line(job: Dict[str, Any]) -> str:
    """
    Build a single markdown line for a job.
    Example:
       - [Senior Manufacturing Test Engineer](URL) — Zoox — Foster City, CA (Posted 3 days ago)
    """
    title = job.get("title", "").strip()
    company = job.get("company", "").strip()
    location = job.get("location", "").strip()
    url = job.get("url", "").strip()

    posted = _format_posted_suffix(job)

    return f"- [{title}]({url}) — {company} — {location}{posted}"
