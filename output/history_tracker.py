# output/history_tracker.py

from __future__ import annotations
from typing import Any, Dict, List
import json
from pathlib import Path


def load_history(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {"jobs": []}

    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"jobs": []}


def update_history(
    history: Dict[str, Any], new_jobs: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Adds new jobs to history.
    """
    hist_list = history.get("jobs", [])
    hist_list.extend(new_jobs)
    history["jobs"] = hist_list
    return history
