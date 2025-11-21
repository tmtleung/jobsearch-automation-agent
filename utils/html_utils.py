# utils/html_utils.py

from __future__ import annotations
from typing import Optional
from bs4 import BeautifulSoup


def extract_text_safe(html_fragment: str) -> str:
    """
    Safely extracts visible text from a partial HTML snippet.
    Handles None, empty strings, or malformed HTML.
    """
    if not html_fragment:
        return ""
    try:
        soup = BeautifulSoup(html_fragment, "html.parser")
        return soup.get_text(" ", strip=True)
    except Exception:
        return ""


def strip_tags(html: str) -> str:
    """
    Removes all HTML tags and returns plain text.
    """
    return extract_text_safe(html)


def safe_soup(html: str) -> Optional[BeautifulSoup]:
    """
    Safely create a BeautifulSoup object without breaking the scraper.
    Returns None on failure.
    """
    if not html:
        return None

    try:
        return BeautifulSoup(html, "html.parser")
    except Exception:
        return None


def find_first(soup: BeautifulSoup, selectors: list) -> Optional[str]:
    """
    Try multiple CSS selectors and return the first match's text.
    This is extremely useful for messy websites with inconsistent markup.
    """
    if soup is None:
        return None

    for sel in selectors:
        tag = soup.select_one(sel)
        if tag:
            return tag.get_text(strip=True)

    return None
