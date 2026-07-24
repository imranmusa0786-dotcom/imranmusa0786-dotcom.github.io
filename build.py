#!/usr/bin/env python3
"""
build.py — render all posts + pages into a static site in ./_site
Generates: article pages, index, static pages, sitemap.xml,
news-sitemap.xml (Google News, last 2 days only), rss.xml, robots.txt.
No server needed — GitHub Pages / Cloudflare Pages serves the folder.
"""
import json, glob, pathlib, shutil, datetime, re
import yaml, markdown
from urllib.parse import urlparse
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT   = pathlib.Path(__file__).parent
CFG    = yaml.safe_load((ROOT / "config.yaml").read_text())
SITE   = CFG["site"]
OUT    = ROOT / "_site"
POSTS  = ROOT / "content" / "posts"
PAGES  = ROOT / "pages"

env = Environment(loader=FileSystemLoader(str(ROOT / "templates")),
                  autoescape=select_autoescape(["html"]))

def load_posts():
    posts = []
    for f in sorted(glob.glob(str(POSTS / "*.json"))):
        p = json.loads(pathlib.Path(f).read_text())
        p["dt"] = datetime.datetime.fromisoformat(p["date"])
        p["date_human"] = p["dt"].strftime("%B %d, %Y")
        p["url"] = f"/posts/{p['slug']}/"
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

def write(path, text):
    path = OUT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    posts = load_posts()
    pages = load_pages()
    base_url = SITE["url"].rstrip("/")

    art_tpl  = env.get_template("article.html")
    idx_tpl  = env.get_template("index.html")
    page_tpl = env.get_template("page.html")

    # article pages
    for p in posts:
        write(f"posts/{p['slug']}/index.html",
              art_tpl.render(site=SITE, post=p, pages=pages))

    # static pages
    for pg in pages:
        write(f"{pg['slug']}/index.html",
              page_tpl.render(site=SITE, page=pg, pages=pages))

    # home
    write("index.html", idx_tpl.render(site=SITE, posts=posts, pages=pages))

    # assets
    shutil.copytree(ROOT / "static", OUT / "static", dirs_exist_ok=True)

    # ---- sitemap.xml (all URLs) ----
    urls = [base_url + "/"] + [base_url + p["url"] for p in posts] \
           + [base_url + pg["url"] for pg in pages]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))

    # ---- news-sitemap.xml (Google News: articles from the last 2 days) ----
    now = datetime.datetime.now(datetime.timezone.utc)
    fresh = [p for p in posts if (now - p["dt"]).days < 2][:1000]
    ns = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
          '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    for p in fresh:
        ns += [
            "  <url>",
            f"    <loc>{base_url}{p['url']}</loc>",
            "    <news:news>",
            "      <news:publication>",
            f"        <news:name>{SITE['name']}</news:name>",
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
           f"<link>{base_url}/</link>",
           f"<description>{_x(SITE['tagline'])}</description>"]
    for p in posts[:20]:
        rss += ["<item>",
                f"<title>{_x(p['title'])}</title>",
                f"<link>{base_url}{p['url']}</link>",
                f"<pubDate>{p['dt'].strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>",
                f"<description>{_x(p['meta_description'])}</description>",
                "</item>"]
    rss += ["</channel></rss>"]
    write("rss.xml", "\n".join(rss))

    # ---- robots.txt + optional CNAME ----
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n")
    host = urlparse(base_url).netloc
    if host and not host.endswith("github.io") and not host.endswith("pages.dev"):
        write("CNAME", host)   # custom domain -> GitHub Pages picks this up

    print(f"Built {len(posts)} posts, {len(pages)} pages, "
          f"{len(fresh)} in news sitemap -> {OUT}")

def _x(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

if __name__ == "__main__":
    main()
