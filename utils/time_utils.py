# utils/time_utils.py

from __future__ import annotations
from datetime import datetime


def now_str() -> str:
    """
    Returns a standard timestamp string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_only() -> str:
    return datetime.now().strftime("%Y-%m-%d")
