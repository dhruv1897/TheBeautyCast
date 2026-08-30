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
GUIDES_PATH = Path(__file__).resolve().parent / "content" / "guides"


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


# ---------------------------------------------------------------------
# Beauty Room guides
# ---------------------------------------------------------------------
# Each guide is one JSON file in app/content/guides/. The filename is
# irrelevant; the "slug" field inside decides the URL.
#
# TO ADD A GUIDE: copy an existing file, change the slug, title and
# body. It appears on the site immediately. No code changes needed.


def load_guides() -> list[dict]:
    """Return every guide, newest first."""
    if current_app.config.get("DEBUG"):
        return _read_guides()
    return _cached_guides()


@lru_cache(maxsize=1)
def _cached_guides() -> list[dict]:
    return _read_guides()


def _read_guides() -> list[dict]:
    guides = []
    for path in sorted(GUIDES_PATH.glob("*.json")):
        with open(path, "r", encoding="utf-8") as handle:
            guides.append(json.load(handle))
    guides.sort(key=lambda g: g.get("updated", ""), reverse=True)
    return guides


def get_guide(slug: str) -> dict | None:
    """Return a single guide by its slug, or None if it does not exist."""
    for guide in load_guides():
        if guide.get("slug") == slug:
            return guide
    return None


def related_guides(guide: dict, limit: int = 2) -> list[dict]:
    """Resolve a guide's "related" slugs into full guide dictionaries."""
    wanted = guide.get("related", [])
    found = [g for g in load_guides() if g.get("slug") in wanted]

    # Top up with any other guide if the related list is short.
    if len(found) < limit:
        for other in load_guides():
            if other["slug"] != guide["slug"] and other not in found:
                found.append(other)
            if len(found) >= limit:
                break

    return found[:limit]
