# processor/relevance_classifier.py

from __future__ import annotations
from typing import Any, Dict, List


def classify_jobs(
    jobs: List[Dict[str, Any]], config: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Rule-based classification into:
    - manufacturing
    - ai_research
    - other
    """
    filters = config.get("search_filters", {})

    mf_cfg = filters.get("manufacturing_engineering", {})
    ai_cfg = filters.get("ai_research", {})

    mf_keywords = [k.lower() for k in mf_cfg.get("keywords", [])]
    ai_keywords = [k.lower() for k in ai_cfg.get("keywords", [])]

    classified = []

    for job in jobs:
        title = job.get("title", "").lower()
        desc = job.get("description", "").lower()

        role_type = "other"

        # Manufacturing logic
        if any(k in title for k in mf_keywords) or any(k in desc for k in mf_keywords):
            role_type = "manufacturing"

        # AI research logic
        if any(k in title for k in ai_keywords) or any(k in desc for k in ai_keywords):
            role_type = "ai_research"

        job["role_type"] = role_type
        classified.append(job)

    return classified
