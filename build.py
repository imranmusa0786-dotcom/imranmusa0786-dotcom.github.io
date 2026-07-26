#!/usr/bin/env python3
"""
build.py — render all posts + pages into a static site in ./_site

Generates: article pages (with featured image, NewsArticle JSON-LD, related
posts), home, category pages, an archive, static pages, sitemap.xml,
news-sitemap.xml, rss.xml, robots.txt. Canonical + Open Graph/Twitter tags and
Organization/WebSite JSON-LD are emitted site-wide. No server needed.
"""
import json, glob, pathlib, shutil, datetime, re
import yaml, markdown
from urllib.parse import urlparse
from jinja2 import Environment, FileSystemLoader, select_autoescape

import taxonomy

ROOT   = pathlib.Path(__file__).parent
CFG    = yaml.safe_load((ROOT / "config.yaml").read_text())
SITE   = CFG["site"]
CATS   = CFG.get("categories", [])
OUT    = ROOT / "_site"
POSTS  = ROOT / "content" / "posts"
PAGES  = ROOT / "pages"
BASE   = SITE["url"].rstrip("/")

env = Environment(loader=FileSystemLoader(str(ROOT / "templates")),
                  autoescape=select_autoescape(["html"]))


def absu(path):
    return BASE + path if path.startswith("/") else path


def load_posts():
    posts = []
    for f in sorted(glob.glob(str(POSTS / "*.json"))):
        p = json.loads(pathlib.Path(f).read_text())
        p["dt"] = datetime.datetime.fromisoformat(p["date"])
        p["date_human"] = p["dt"].strftime("%B %d, %Y")
        p["url"] = f"/posts/{p['slug']}/"
        # backfill category for legacy posts
        if not p.get("category"):
            cs, cn = taxonomy.classify(p.get("title", ""), p.get("tags", []),
                                       p.get("html", ""))
            p["category"], p["category_name"] = cs, cn
        elif not p.get("category_name"):
            p["category_name"] = taxonomy.name_for(p["category"])
        posts.append(p)
    posts.sort(key=lambda x: x["dt"], reverse=True)
    return posts


def load_pages():
    out = []
    for f in sorted(glob.glob(str(PAGES / "*.md"))):
        raw = pathlib.Path(f).read_text()
        title = raw.splitlines()[0].lstrip("# ").strip()
        body = markdown.markdown("\n".join(raw.splitlines()[1:]))
        slug = pathlib.Path(f).stem
        out.append({"slug": slug, "title": title, "html": body, "url": f"/{slug}/"})
    return out


def related_for(post, posts, n=3):
    same = [p for p in posts if p["slug"] != post["slug"]
            and p["category"] == post["category"]]
    if len(same) < n:
        extra = [p for p in posts if p["slug"] != post["slug"] and p not in same]
        same = same + extra
    return same[:n]


def write(path, text):
    path = OUT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def nav_categories():
    return [{"slug": c["slug"], "name": c["name"], "url": f"/category/{c['slug']}/"}
            for c in CATS]


# ------------------------------------------------------------------ JSON-LD
def org_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "NewsMediaOrganization",
        "name": SITE["name"],
        "url": BASE + "/",
        "logo": {"@type": "ImageObject", "url": absu(SITE.get("logo", "/static/logo.png"))},
        "email": SITE.get("email", ""),
        "description": SITE["tagline"],
    }


def website_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE["name"],
        "url": BASE + "/",
    }


def article_jsonld(post):
    img = absu(post["image"]) if post.get("image") else absu(SITE.get("default_image"))
    return {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": post["title"][:110],
        "description": post.get("meta_description", ""),
        "image": [img],
        "datePublished": post["dt"].isoformat(),
        "dateModified": post["dt"].isoformat(),
        "author": {"@type": "Organization", "name": post.get("author", SITE["author"])},
        "publisher": {
            "@type": "NewsMediaOrganization",
            "name": SITE["name"],
            "logo": {"@type": "ImageObject",
                     "url": absu(SITE.get("logo", "/static/logo.png"))},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": absu(post["url"])},
        "articleSection": post.get("category_name", "News"),
    }


def dumps_ld(objs):
    return [json.dumps(o, ensure_ascii=False) for o in objs]


def base_ctx(canonical, desc, og_image=None, og_type="website", jsonld=None):
    return {
        "site": SITE,
        "pages": PAGES_LIST,
        "nav_categories": nav_categories(),
        "canonical": absu(canonical),
        "page_desc": desc,
        "og_image": absu(og_image or SITE.get("default_image")),
        "og_type": og_type,
        "jsonld": dumps_ld(jsonld or [org_jsonld(), website_jsonld()]),
    }


PAGES_LIST = []


def main():
    global PAGES_LIST
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    posts = load_posts()
    PAGES_LIST = load_pages()
    pages = PAGES_LIST

    art_tpl  = env.get_template("article.html")
    idx_tpl  = env.get_template("index.html")
    page_tpl = env.get_template("page.html")
    cat_tpl  = env.get_template("category.html")

    # ---- article pages ----
    for p in posts:
        ctx = base_ctx(p["url"], p.get("meta_description", SITE["tagline"]),
                       og_image=p.get("image"), og_type="article",
                       jsonld=[org_jsonld(), article_jsonld(p)])
        ctx.update({"post": p, "related": related_for(p, posts)})
        write(f"posts/{p['slug']}/index.html", art_tpl.render(**ctx))

    # ---- static pages ----
    for pg in pages:
        ctx = base_ctx(pg["url"], SITE["tagline"])
        ctx.update({"page": pg})
        write(f"{pg['slug']}/index.html", page_tpl.render(**ctx))

    # ---- home (latest 12; rest via archive) ----
    ctx = base_ctx("/", SITE["tagline"])
    ctx.update({"posts": posts[:12], "heading": "Latest News",
                "show_archive_link": len(posts) > 12})
    write("index.html", idx_tpl.render(**ctx))

    # ---- archive (all posts) ----
    ctx = base_ctx("/archive/", f"All articles from {SITE['name']}.")
    ctx.update({"posts": posts, "heading": "Archive — All Articles",
                "show_archive_link": False})
    write("archive/index.html", idx_tpl.render(**ctx))

    # ---- category pages ----
    for c in CATS:
        cposts = [p for p in posts if p["category"] == c["slug"]]
        curl = f"/category/{c['slug']}/"
        ctx = base_ctx(curl, f"{c['name']} news — {SITE['name']}.")
        ctx.update({"category": c, "posts": cposts,
                    "heading": c["name"]})
        write(f"category/{c['slug']}/index.html", cat_tpl.render(**ctx))

    # ---- assets ----
    shutil.copytree(ROOT / "static", OUT / "static", dirs_exist_ok=True)

    # ---- sitemap.xml ----
    urls = [BASE + "/", BASE + "/archive/"]
    urls += [BASE + f"/category/{c['slug']}/" for c in CATS]
    urls += [BASE + p["url"] for p in posts]
    urls += [BASE + pg["url"] for pg in pages]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))

    # ---- news-sitemap.xml (last 2 days) ----
    now = datetime.datetime.now(datetime.timezone.utc)
    fresh = [p for p in posts if (now - p["dt"]).days < 2][:1000]
    ns = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
          '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    for p in fresh:
        ns += [
            "  <url>",
            f"    <loc>{BASE}{p['url']}</loc>",
            "    <news:news>",
            "      <news:publication>",
            f"        <news:name>{_x(SITE['name'])}</news:name>",
            f"        <news:language>{SITE['language']}</news:language>",
            "      </news:publication>",
            f"      <news:publication_date>{p['dt'].isoformat()}</news:publication_date>",
            f"      <news:title>{_x(p['title'])}</news:title>",
            "    </news:news>",
            "  </url>",
        ]
    ns.append("</urlset>")
    write("news-sitemap.xml", "\n".join(ns))

    # ---- rss.xml ----
    rss = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0"><channel>',
           f"<title>{_x(SITE['name'])}</title>",
           f"<link>{BASE}/</link>",
           f"<description>{_x(SITE['tagline'])}</description>"]
    for p in posts[:20]:
        rss += ["<item>",
                f"<title>{_x(p['title'])}</title>",
                f"<link>{BASE}{p['url']}</link>",
                f"<guid>{BASE}{p['url']}</guid>",
                f"<pubDate>{p['dt'].strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>",
                f"<description>{_x(p['meta_description'])}</description>",
                "</item>"]
    rss += ["</channel></rss>"]
    write("rss.xml", "\n".join(rss))

    # ---- robots.txt + optional CNAME ----
    write("robots.txt",
          "User-agent: *\nAllow: /\n"
          f"Sitemap: {BASE}/sitemap.xml\n"
          f"Sitemap: {BASE}/news-sitemap.xml\n")
    host = urlparse(BASE).netloc
    if host and not host.endswith("github.io") and not host.endswith("pages.dev"):
        write("CNAME", host)

    print(f"Built {len(posts)} posts, {len(pages)} pages, {len(CATS)} categories, "
          f"{len(fresh)} in news sitemap -> {OUT}")


def _x(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    main()
