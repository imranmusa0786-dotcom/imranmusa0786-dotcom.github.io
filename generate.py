#!/usr/bin/env python3
"""
generate.py — pull feeds, write ORIGINAL articles with Gemini, gate them
through automated QA, retry on rejection, save passing posts as JSON.

Runs on GitHub Actions every 2 hours (see .github/workflows/publish.yml).
Needs env var GEMINI_API_KEY (stored as a GitHub Actions secret).
"""
import os, re, json, glob, pathlib, datetime, html, sys
import yaml, feedparser
from google import genai

ROOT   = pathlib.Path(__file__).parent
CFG    = yaml.safe_load((ROOT / "config.yaml").read_text())
POSTS  = ROOT / "content" / "posts"; POSTS.mkdir(parents=True, exist_ok=True)
SEEN_F = ROOT / "seen.json"
PROMPT = (ROOT / "synthesis_prompt.txt").read_text()

GEN_MODEL = CFG["generation"]["model"]
QA_MODEL  = CFG["generation"]["qa_model"]
MAX_TRY   = CFG["generation"]["max_attempts"]
MIN_WORDS = CFG["generation"]["min_words"]
N_POSTS   = CFG["generation"].get("posts_per_run", 1)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
seen   = set(json.loads(SEEN_F.read_text())) if SEEN_F.exists() else set()


def slugify(t):
    s = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return s[:70] or "post"


def extract_json(text):
    """Gemini sometimes wraps JSON in ```json fences — strip them."""
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1).strip()
    return json.loads(text)


def gemini(model, prompt):
    r = client.models.generate_content(model=model, contents=prompt)
    return r.text


def gather_stories():
    items = []
    for feed in CFG["feeds"]:
        try:
            parsed = feedparser.parse(feed)
        except Exception as e:
            print(f"  feed error {feed}: {e}"); continue
        for e in parsed.entries[:6]:
            link = getattr(e, "link", "")
            if link and link not in seen:
                items.append({
                    "title": html.unescape(getattr(e, "title", "")),
                    "summary": re.sub("<[^>]+>", " ", getattr(e, "summary", ""))[:600],
                    "link": link,
                })
    # de-dupe by link, keep order (freshest-ish first)
    uniq, keys = [], set()
    for it in items:
        if it["link"] not in keys:
            keys.add(it["link"]); uniq.append(it)
    return uniq


def build_context(items):
    return "\n\n".join(
        f"- {i['title']}: {i['summary']} (source: {i['link']})" for i in items[:6]
    )


def generate_article(lead_title, context):
    p = PROMPT.replace("{{CONTEXT}}", context).replace("{{LEAD}}", lead_title)
    return extract_json(gemini(GEN_MODEL, p))


def passes_qa(data, context):
    # 1) cheap hard rules
    words = len(re.sub("<[^>]+>", " ", data.get("html", "")).split())
    if words < MIN_WORDS:
        return False, f"too thin ({words} words)"
    if not data.get("title") or len(data["title"]) > 120:
        return False, "missing/overlong title"
    # 2) AI editor gate
    review = gemini(QA_MODEL,
        "You are a STRICT news editor. Here are the SOURCES the writer used:\n"
        f"{context}\n\nHere is the ARTICLE:\n{data['html']}\n\n"
        "Reject it if it is off-topic, thin, clickbait, OR states any fact, "
        "number, quote, or date NOT supported by the sources. "
        'Reply with ONLY JSON: {"publish": true or false, "reason": "short reason"}')
    try:
        v = extract_json(review)
        return bool(v.get("publish")), v.get("reason", "")
    except Exception as e:
        return False, f"QA parse error: {e}"


def save_post(data):
    today = datetime.date.today().isoformat()
    slug  = f"{today}-{slugify(data['title'])}"
    post = {
        "slug": slug,
        "title": data["title"],
        "html": data["html"],
        "tags": data.get("tags", []),
        "meta_description": data.get("meta_description", "")[:155],
        "date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "author": CFG["site"]["author"],
    }
    (POSTS / f"{slug}.json").write_text(json.dumps(post, indent=2, ensure_ascii=False))
    return slug


def main():
    stories = gather_stories()
    if not stories:
        print("No new stories this run."); return
    context = build_context(stories)

    published = 0
    for story in stories[:MAX_TRY]:
        if published >= N_POSTS:
            break
        seen.add(story["link"])  # never retry the same story next run
        try:
            data = generate_article(story["title"], context)
            ok, reason = passes_qa(data, context)
        except Exception as e:
            print(f"  attempt error, next story: {e}"); continue
        if not ok:
            print(f"  REJECTED, retrying next story: {reason}"); continue
        slug = save_post(data)
        print(f"  PUBLISHED: {slug}"); published += 1

    SEEN_F.write_text(json.dumps(sorted(seen), indent=2))
    if published == 0:
        print("No story passed QA this run — slot skipped (safer than junk).")


if __name__ == "__main__":
    main()
