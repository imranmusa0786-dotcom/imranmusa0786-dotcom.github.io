#!/usr/bin/env python3
"""taxonomy.py — classify a post into one coverage category by keyword score."""
import re, pathlib, yaml

ROOT = pathlib.Path(__file__).parent
_CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
CATEGORIES = _CFG.get("categories", [])
_BY_SLUG = {c["slug"]: c for c in CATEGORIES}


def classify(title="", tags=None, html=""):
    """Return (slug, name) of the best-matching category."""
    tags = tags or []
    hay = " ".join([title] + list(tags) + [re.sub("<[^>]+>", " ", html)]).lower()
    best, best_score = None, 0
    for cat in CATEGORIES:
        score = 0
        for kw in cat["keywords"]:
            # weight title/tag hits a bit higher
            score += hay.count(kw)
        if score > best_score:
            best, best_score = cat, score
    if best is None:
        best = CATEGORIES[0] if CATEGORIES else {"slug": "news", "name": "News"}
    return best["slug"], best["name"]


def name_for(slug):
    c = _BY_SLUG.get(slug)
    return c["name"] if c else "News"
