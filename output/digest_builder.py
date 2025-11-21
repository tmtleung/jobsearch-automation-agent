# output/digest_builder.py

from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from .formatter import format_job_line


def build_digest(
    new_jobs: List[Dict[str, Any]],
    all_filtered_jobs: List[Dict[str, Any]],
    total_in_history: int,
    output_path: Path,
) -> None:
    """
    Build the digest markdown file.
    If no new jobs this run:
       → Show the full filtered job list so the digest is still useful.
    """

    lines = []

    # Header
    lines.append("# JobSearch AI Agent 2.0 — Digest\n")
    lines.append(f"**New relevant jobs this run:** {len(new_jobs)}")
    lines.append(f"**Total tracked jobs:** {total_in_history}\n")
    lines.append("---\n")

    # If nothing is new, we show the full list instead of an empty digest
    if len(new_jobs) == 0:
        lines.append("### No new jobs this run.\n")
        lines.append("### Here's the full list of currently relevant jobs:\n")

        for job in all_filtered_jobs:
            lines.append(format_job_line(job))

    else:
        lines.append("### New relevant jobs discovered:\n")
        for job in new_jobs:
            lines.append(format_job_line(job))

    # Write out the digest
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Digest] Built → {output_path}")
