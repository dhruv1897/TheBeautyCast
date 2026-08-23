"""
Shared helpers used by more than one controller.

Right now this loads the editable site copy. Anything reusable that is
not a database model and not a route belongs in here.
"""

import json
from functools import lru_cache
from pathlib import Path

from flask import current_app

CONTENT_PATH = Path(__file__).resolve().parent / "content" / "site.json"


def load_content() -> dict:
    """Read app/content/site.json and return it as a dictionary.

    In debug mode the file is read on every request, so you can edit the
    text and just refresh the browser. In production it is cached.
    """
    if current_app.config.get("DEBUG"):
        return _read_content_file()
    return _cached_content()


@lru_cache(maxsize=1)
def _cached_content() -> dict:
    return _read_content_file()


def _read_content_file() -> dict:
    with open(CONTENT_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def clean(value: str | None, limit: int = 500) -> str:
    """Trim a form value and cap its length."""
    return (value or "").strip()[:limit]


def as_int(value: str | None) -> int | None:
    """Turn a form string into an int, or None if it is not a number."""
    try:
        return int(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None
