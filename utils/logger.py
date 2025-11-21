# utils/logger.py

from __future__ import annotations
import logging
from datetime import datetime
from pathlib import Path


def init_logger() -> logging.Logger:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    log_path = logs_dir / f"agent_{timestamp}.log"

    logger = logging.getLogger("jobsearch_agent")
    logger.setLevel(logging.INFO)

    # Clear previous handlers if reloading
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatting
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
