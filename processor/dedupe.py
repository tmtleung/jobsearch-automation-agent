# processor/deduper.py

from __future__ import annotations
from typing import List, Dict, Any, Tuple


def dedupe_jobs(
    new_jobs: List[Dict[str, Any]], history: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Deduplicate jobs based on (title, company, location).
    A job is "new or updated" if it doesn't exactly match existing history.
    """

    key = lambda j: (
        j.get("title", "").strip().lower(),
        j.get("company", "").strip().lower(),
        j.get("location", "").strip().lower(),
    )

    # Convert history to dict for fast lookup
    history_dict = {key(j): j for j in history}

    new_or_updated = []

    for job in new_jobs:
        k = key(job)

        if k not in history_dict:
            # Completely new job
            new_or_updated.append(job)
            history_dict[k] = job
        else:
            # Existing job — check if significant fields changed
            old = history_dict[k]
            if job.get("url") != old.get("url") or job.get(
                "days_since_posted"
            ) != old.get("days_since_posted"):
                new_or_updated.append(job)
                history_dict[k] = job

    # Rebuild history as a list
    updated_history = list(history_dict.values())

    return new_or_updated, updated_history
