"""
Shared utilities for Phase 1.

Logging setup, file I/O helpers, slug generation, and date parsing.
"""

import logging
import json
import re
from datetime import datetime
from pathlib import Path

from rich.logging import RichHandler

from src.phase1.config import LOG_LEVEL


def setup_logging(name: str = "phase1") -> logging.Logger:
    """Configure and return a logger with Rich formatting."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )
    logger = logging.getLogger(name)
    return logger


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def ensure_directory(path: Path) -> Path:
    """Create directory if it doesn't exist. Returns the path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: dict | list, filepath: Path) -> None:
    """Save data as JSON to filepath."""
    ensure_directory(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def load_json(filepath: Path) -> dict | list:
    """Load JSON data from filepath."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_text(text: str, filepath: Path) -> None:
    """Save text content to filepath."""
    ensure_directory(filepath.parent)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)


def load_text(filepath: Path) -> str:
    """Load text content from filepath."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def parse_date(date_str: str) -> str:
    """
    Try to parse a date string into ISO 8601 format (YYYY-MM-DD).
    Returns the original string if parsing fails.
    """
    date_formats = [
        "%d %b %Y",        # 07 May 2026
        "%d %B %Y",        # 07 May 2026
        "%b %d, %Y",       # May 07, 2026
        "%B %d, %Y",       # May 07, 2026
        "%d-%m-%Y",        # 07-05-2026
        "%d/%m/%Y",        # 07/05/2026
        "%Y-%m-%d",        # 2026-05-07
        "%m/%d/%Y",        # 05/07/2026
        "%d %b, %Y",       # 07 May, 2026
    ]
    date_str = date_str.strip()
    for fmt in date_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str


def get_today_iso() -> str:
    """Return today's date in ISO 8601 format."""
    return datetime.now().strftime("%Y-%m-%d")
