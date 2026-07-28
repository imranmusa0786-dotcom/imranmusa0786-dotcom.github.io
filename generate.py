#!/usr/bin/env python3
"""
generate.py — pull feeds, write ORIGINAL articles with Gemini, gate them
through automated QA, retry on rejection, save passing posts as JSON.

Quality gates (hard rules, before the AI editor even runs):
  * >= min_words words
  * >= min_sources distinct external source links
  * >= min_data_points concrete figures (numbers/stats)
Anything failing is held (never published).

Also: classifies each post into a coverage category, adds 1-2 internal links
to prior related coverage, and generates a related featured image.

Runs on GitHub Actions (see .github/workflows/publish.yml).
Needs env var GEMINI_API_KEY (stored as a GitHub Actions secret).
"""
import os, re, json, glob, pathlib, datetime, html, sys
import yaml, feedparser
from google import genai

import taxonomy
import images as imagelib

ROOT   = pathlib.Path(__file__).parent
CFG    = yaml.safe_load((ROOT / "config.yaml").read_text())
POSTS  = ROOT / "content" / "posts"; POSTS.mkdir(parents=True, exist_ok=True)
SEEN_F = ROOT / "seen.json"
PROMPT = (ROOT / "synthesis_prompt.txt").read_text()

G = CFG["generation"]
GEN_MODEL = G["model"]
QA_MODEL  = G["qa_model"]
MAX_TRY   = G["max_attempts"]
MIN_WORDS = G["min_words"]
MIN_SRC   = G.get("min_sources", 2)
MIN_DATA  = G.get("min_data_points", 1)
N_POSTS   = G.get("posts_per_run", 1)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
seen   = set(json.loads(SEEN_F.read_text())) if SEEN_F.exists() else set()


def slugify(t):
    s = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return s[:70] or "post"


def extract_json(text):
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1).strip()
    return json.loads(text)


def gemini(model, prompt):
    r = client.models.generate_content(model=model, contents=prompt)
    return r.text


# ----------------------------------------------------------------- inputs
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
    uniq, keys = [], set()
    for it in items:
        if it["link"] not in keys:
            keys.add(it["link"]); uniq.append(it)
    return uniq


def build_context(items):
    return "\n\n".join(
        f"- {i['title']}: {i['summary']} (source: {i['link']})" for i in items[:6]
    )


def prior_coverage(limit=12):
    """Recent published posts, for internal-linking context."""
    out = []
    for f in sorted(glob.glob(str(POSTS / "*.json")), reverse=True)[:limit]:
        try:
            p = json.loads(pathlib.Path(f).read_text())
            out.append({"title": p["title"], "url": f"/posts/{p['slug']}/"})
        except Exception:
            continue
    return out


def coverage_block(items):
    if not items:
        return "(none yet)"
    return "\n".join(f'- "{i["title"]}" -> {i["url"]}' for i in items)


def generate_article(lead_title, context, prior):
    p = (PROMPT
         .replace("{{CONTEXT}}", context)
         .replace("{{LEAD}}", lead_title)
         .replace("{{PRIOR}}", coverage_block(prior)))
    return extract_json(gemini(GEN_MODEL, p))


# ----------------------------------------------------------------- QA gates
EXT_LINK_RE = re.compile(r'href=["\'](https?://[^"\']+)["\']', re.I)
DATA_RE     = re.compile(r'(\$\s?\d|\d+\s?%|\b\d[\d,\.]*\b)')


def count_sources(html_str):
    hosts = set()
    for u in EXT_LINK_RE.findall(html_str):
        m = re.match(r'https?://([^/]+)/?', u)
        if m:
            hosts.add(m.group(1).lower().replace("www.", ""))
    return len(hosts)


def count_data_points(html_str):
    text = re.sub("<[^>]+>", " ", html_str)
    return len(DATA_RE.findall(text))


def passes_qa(data, context):
    h = data.get("html", "")
    words = len(re.sub("<[^>]+>", " ", h).split())
    if words < MIN_WORDS:
        return False, f"too thin ({words} words < {MIN_WORDS})"
    src = count_sources(h)
    if src < MIN_SRC:
        return False, f"too few linked sources ({src} < {MIN_SRC})"
    dp = count_data_points(h)
    if dp < MIN_DATA:
        return False, f"no concrete data point ({dp} < {MIN_DATA})"
    if not data.get("title") or len(data["title"]) > 120:
        return False, "missing/overlong title"
    # AI editor gate
    review = gemini(QA_MODEL,
        "You are a STRICT news editor. Here are the SOURCES the writer used:\n"
        f"{context}\n\nHere is the ARTICLE:\n{h}\n\n"
        "Reject it if it is off-topic, thin, clickbait, OR states any fact, "
        "number, quote, or date NOT supported by the sources. "
        'Reply with ONLY JSON: {"publish": true or false, "reason": "short reason"}')
    try:
        v = extract_json(review)
        return bool(v.get("publish")), v.get("reason", "")
    except Exception as e:
        return False, f"QA parse error: {e}"


# ----------------------------------------------------------------- save
def save_post(data):
    today = datetime.date.today().isoformat()
    slug  = f"{today}-{slugify(data['title'])}"
    cat_slug, cat_name = taxonomy.classify(
        data.get("title", ""), data.get("tags", []), data.get("html", ""))
    post = {
        "slug": slug,
        "title": data["title"],
        "html": data["html"],
        "tags": data.get("tags", []),
        "category": cat_slug,
        "category_name": cat_name,
        "meta_description": data.get("meta_description", "")[:155],
        "date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "author": CFG["site"]["author"],
    }
    # featured image (AI, with safe fallback)
    try:
        rel, alt, kind = imagelib.ensure_image(post, CFG, client=client)
        post["image"], post["image_alt"], post["image_kind"] = rel, alt, kind
        post["image_pv"] = imagelib.PROMPT_VERSION
    except Exception as e:
        print(f"  image step error (non-fatal): {e}")
    (POSTS / f"{slug}.json").write_text(
        json.dumps(post, indent=2, ensure_ascii=False))
    return slug


def main():
    stories = gather_stories()
    if not stories:
        print("No new stories this run."); return
    context = build_context(stories)
    prior   = prior_coverage()

    published = 0
    for story in stories[:MAX_TRY]:
        if published >= N_POSTS:
            break
        seen.add(story["link"])
        try:
            data = generate_article(story["title"], context, prior)
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
