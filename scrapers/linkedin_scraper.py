# scrapers/linkedin_scraper.py

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
import random
import re

SEARCH_URL = "https://www.linkedin.com/jobs/search/"


def _parse_posted_age(raw: str) -> int | None:
    """
    Convert LinkedIn 'posted' text into an approximate days-since-posted integer.
    Examples:
      'Just posted'      -> 0
      '1 hour ago'       -> 0
      '20 hours ago'     -> 0
      '3 days ago'       -> 3
      '2 weeks ago'      -> 14
      '1 month ago'      -> 30
      '30+ days ago'     -> 30
    """
    if not raw:
        return None

    s = raw.strip().lower()

    # Normal "just posted" / "today" style
    if "just posted" in s or "today" in s:
        return 0

    # Hours / minutes → treat as 0 days
    if "hour" in s or "minute" in s:
        return 0

    # 30+ days ago
    if "30+ days" in s:
        return 30

    # Generic "X days ago"
    m = re.search(r"(\d+)\s+day", s)
    if m:
        return int(m.group(1))

    # "X weeks ago"
    m = re.search(r"(\d+)\s+week", s)
    if m:
        return int(m.group(1)) * 7

    # "X months ago" → rough 30-day month
    m = re.search(r"(\d+)\s+month", s)
    if m:
        return int(m.group(1)) * 30

    return None


def scrape_linkedin(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Stable LinkedIn scraper (public HTML version)
    - Single broad search: "Engineer"
    - Location: California, United States
    - Max ~200 results (8 pages)
    - Extracts title, company, location, url, and posting age.
    """

    headers = {"User-Agent": "Mozilla/5.0"}

    keywords = "Engineer"
    location = "California, United States"

    all_jobs: List[Dict[str, Any]] = []
    max_pages = 8  # ≈ 200 jobs
    results_per_page = 25

    for page in range(max_pages):
        start = page * results_per_page

        page_url = (
            f"{SEARCH_URL}"
            f"?keywords={keywords}"
            f"&location={location.replace(' ', '%20')}"
            f"&f_TPR=r604800"
            f"&start={start}"
        )

        print(f"[LinkedIn] Fetching page {page+1}/{max_pages}")

        try:
            resp = requests.get(page_url, headers=headers, timeout=10)
        except Exception as e:
            print(f"[LinkedIn] ERROR fetching page: {e}")
            break

        if resp.status_code != 200:
            print(f"[LinkedIn] HTTP {resp.status_code} — stopping.")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        # Find all job cards
        cards = soup.find_all("div", class_="base-card")
        if not cards:
            print("[LinkedIn] No more job cards — stopping.")
            break

        for card in cards:
            title_tag = card.find("h3", class_="base-search-card__title")
            company_tag = card.find("h4", class_="base-search-card__subtitle")
            location_tag = card.find("span", class_="job-search-card__location")
            link_tag = card.find("a", class_="base-card__full-link")

            # Posting age can be in <time> or in listdate spans
            time_tag = card.find("time")
            listdate_tag = card.find("span", class_="job-search-card__listdate")
            listdate_new_tag = card.find(
                "span", class_="job-search-card__listdate--new"
            )

            posted_raw = None
            if time_tag and time_tag.get_text(strip=True):
                posted_raw = time_tag.get_text(strip=True)
            elif listdate_tag and listdate_tag.get_text(strip=True):
                posted_raw = listdate_tag.get_text(strip=True)
            elif listdate_new_tag and listdate_new_tag.get_text(strip=True):
                posted_raw = listdate_new_tag.get_text(strip=True)

            days_since = _parse_posted_age(posted_raw)

            title = title_tag.get_text(strip=True) if title_tag else ""
            company = company_tag.get_text(strip=True) if company_tag else ""
            location = location_tag.get_text(strip=True) if location_tag else ""
            url = link_tag.get("href", "") if link_tag else ""

            if url:
                url = url.split("?")[0]

            if title and url:
                job: Dict[str, Any] = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": url,
                    "source": "linkedin",
                }

                # Add posting age info (optional but very nice to have)
                if posted_raw:
                    job["posted_age_raw"] = posted_raw
                if days_since is not None:
                    job["days_since_posted"] = days_since

                all_jobs.append(job)

        time.sleep(random.uniform(0.4, 0.8))

    # Deduplicate
    deduped = {
        (j["title"], j["company"], j.get("location", ""), j["url"]): j for j in all_jobs
    }

    print(f"[LinkedIn] Total deduped jobs: {len(deduped)}")

    return list(deduped.values())
