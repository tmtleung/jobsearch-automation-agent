# processor/filters.py

from __future__ import annotations
from typing import Any, Dict, List


def filter_jobs(
    jobs: List[Dict[str, Any]], config: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Public-safe generic filtering logic.

    The filtering rules are:
    - Title contains ANY keyword from config (case-insensitive)
    - Location contains ANY location keyword from config (case-insensitive)
    - Posting age <= filters.max_post_age_days
    """

    # Pull config fields
    title_keywords = [kw.lower() for kw in config["scrapers"]["linkedin"]["keywords"]]
    location_keywords = [
        kw.lower() for kw in config["scrapers"]["linkedin"]["location_keywords"]
    ]
    max_age = config["filters"]["max_post_age_days"]

    filtered = []

    for job in jobs:
        title = job.get("title", "").lower()
        location = job.get("location", "").lower()
        age = job.get("days_since_posted")

        # Title keyword filter
        if title_keywords and not any(kw in title for kw in title_keywords):
            continue

        # Location keyword filter (optional)
        if location_keywords:
            if not any(loc_kw in location for loc_kw in location_keywords):
                continue

        # Age filter
        if age is not None and age > max_age:
            continue

        filtered.append(job)

    return filtered
