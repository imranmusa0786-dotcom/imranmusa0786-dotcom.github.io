#!/usr/bin/env python3
"""
backfill_images.py — ensure every post has a featured image.

Runs in CI before build. For any post missing an image file (or one still on a
placeholder), it (re)generates via Gemini when GEMINI_API_KEY is present, else
falls back to a branded placeholder. Idempotent: AI images are left untouched.
Run locally with no key to seed placeholders.
"""
import os, json, glob, pathlib
import yaml

import taxonomy
import images as imagelib

ROOT  = pathlib.Path(__file__).parent
CFG   = yaml.safe_load((ROOT / "config.yaml").read_text())
POSTS = ROOT / "content" / "posts"

client = None
key = os.environ.get("GEMINI_API_KEY")
if key:
    try:
        from google import genai
        client = genai.Client(api_key=key)
    except Exception as e:
        print(f"[backfill] no genai client ({e}); placeholders only")


def main():
    changed = 0
    for f in sorted(glob.glob(str(POSTS / "*.json"))):
        p = json.loads(pathlib.Path(f).read_text())
        slug = p["slug"]
        if not p.get("category"):
            cs, cn = taxonomy.classify(p.get("title", ""), p.get("tags", []),
                                       p.get("html", ""))
            p["category"], p["category_name"] = cs, cn
        elif not p.get("category_name"):
            p["category_name"] = taxonomy.name_for(p["category"])

        img_file = imagelib.IMG_DIR / f"{slug}.jpg"
        missing = (not p.get("image")) or (not img_file.exists())
        if not missing:
            continue

        rel, alt, kind = imagelib.ensure_image(p, CFG, client=client, force=False)
        if rel:
            p["image"], p["image_alt"], p["image_kind"] = rel, alt, kind
            pathlib.Path(f).write_text(json.dumps(p, indent=2, ensure_ascii=False))
            changed += 1
            print(f"[backfill] {slug}: {kind}")
    print(f"[backfill] updated {changed} post(s)")


if __name__ == "__main__":
    main()
