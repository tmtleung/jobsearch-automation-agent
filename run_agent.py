# run_agent.py

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

from scrapers.linkedin_scraper import scrape_linkedin
from processor.filters import filter_jobs
from processor.relevance_classifier import classify_jobs
from processor.dedupe import dedupe_jobs
from output.digest_builder import build_digest
from utils.logger import init_logger


def load_config():
    try:
        with open("config/config.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in config/config.json: {e}")
    except FileNotFoundError:
        raise RuntimeError("Missing config/config.json")


def load_history(path: Path) -> list:
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text())
    except Exception:
        return []


def save_history(path: Path, history: list):
    # Ensure the directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, indent=2))


def main():
    logger = init_logger()
    logger.info("=== JobSearch AI Agent 2.0 Started ===")

    # Load configuration
    config = load_config()

    # Prepare paths
    history_path = Path("history/job_history.json")
    digest_path = Path("outputs/latest_digest.md")

    # Load job history
    history = load_history(history_path)

    # SCRAPE
    logger.info("Scraping LinkedIn...")
    linkedin_jobs = scrape_linkedin(config)
    logger.info(f"LinkedIn returned {len(linkedin_jobs)} jobs.")

    # PROCESS
    logger.info(f"Processing {len(linkedin_jobs)} scraped jobs...")
    filtered = filter_jobs(linkedin_jobs, config)
    logger.info(f"Filtered down to {len(filtered)} jobs.")

    classified = classify_jobs(filtered, config)
    logger.info(f"Classified {len(classified)} jobs.")

    # DEDUPE
    deduped, updated_history = dedupe_jobs(classified, history)
    logger.info(f"After dedupe: {len(deduped)} new or updated jobs.")

    # SAVE DIGEST (always show full filtered list)
    build_digest(
        new_jobs=deduped,
        all_filtered_jobs=classified,
        total_in_history=len(updated_history),
        output_path=digest_path,
    )

    logger.info(f"Digest saved → {digest_path}")

    # UPDATE HISTORY
    save_history(history_path, updated_history)

    # EMAIL
    if config.get("email_notifications", {}).get("enabled", False):
        from emailer.mailer import send_digest

        logger.info("Sending email digest...")
        try:
            send_digest(digest_path, config)
            logger.info("Email sent successfully.")
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
    else:
        logger.info("Email sending disabled in config.")

    logger.info("=== JobSearch AI Agent 2.0 Complete ===")


if __name__ == "__main__":
    main()
