#!/usr/bin/env python3
"""Build TechShield Tools — static calculators site. No server, no API, no cost."""
import json, pathlib, shutil, datetime, html
import yaml, markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from tools import TOOLS, RESULTS

ROOT = pathlib.Path(__file__).parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
SITE = CFG["site"]
BASE = SITE["url"].rstrip("/")
OUT = ROOT / "_site"

env = Environment(loader=FileSystemLoader(str(ROOT / "templates")),
                  autoescape=select_autoescape(["html"]))

CATNAME = {"finance": "Financial Calculators", "utility": "Everyday Tools"}


def write(path, text):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def ld(obj):
    return json.dumps(obj, ensure_ascii=False)


def org_ld():
    return {"@context": "https://schema.org", "@type": "Organization",
            "name": SITE["name"], "url": BASE + "/",
            "logo": BASE + "/static/og.png"}


def website_ld():
    return {"@context": "https://schema.org", "@type": "WebSite",
            "name": SITE["name"], "url": BASE + "/"}


def breadcrumb_ld(tool):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": CATNAME[tool["cat"]], "item": BASE + "/all/"},
                {"@type": "ListItem", "position": 3, "name": tool["name"], "item": BASE + "/" + tool["slug"] + "/"},
            ]}


def webapp_ld(tool):
    return {"@context": "https://schema.org", "@type": "WebApplication",
            "name": tool["name"], "url": BASE + "/" + tool["slug"] + "/",
            "description": tool["desc"], "applicationCategory": "FinanceApplication",
            "operatingSystem": "Any (web browser)",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}


def faq_ld(tool):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f["q"],
                            "acceptedAnswer": {"@type": "Answer",
                                               "text": _strip(f["a"])}} for f in tool["faqs"]]}


def _strip(s):
    import re
    return re.sub("<[^>]+>", "", s)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    finance = [t for t in TOOLS if t["cat"] == "finance"]
    utility = [t for t in TOOLS if t["cat"] == "utility"]
    for t in TOOLS:
        t["cat_name"] = CATNAME[t["cat"]]
        t.setdefault("results_html", RESULTS)

    calc_tpl = env.get_template("calc.html")
    idx_tpl = env.get_template("index.html")
    all_tpl = env.get_template("all.html")
    page_tpl = env.get_template("page.html")

    # calculator pages
    for t in TOOLS:
        related = [r for r in TOOLS if r["cat"] == t["cat"] and r["slug"] != t["slug"]][:3]
        if len(related) < 3:
            related += [r for r in TOOLS if r["slug"] != t["slug"] and r not in related][:3 - len(related)]
        jl = [webapp_ld(t), breadcrumb_ld(t)]
        if t.get("faqs"):
            jl.append(faq_ld(t))
        write(f"{t['slug']}/index.html", calc_tpl.render(
            site=SITE, tool=t, related=related,
            title=t["title"], desc=t["desc"],
            canonical=f"{BASE}/{t['slug']}/", jsonld=[ld(x) for x in jl]))

    # home
    write("index.html", idx_tpl.render(
        site=SITE, finance=finance, utility=utility,
        title=f"{SITE['name']} — Free Calculators & Everyday Tools",
        desc="Free online calculators for mortgages, loans, compound interest, plus everyday tools like percentage, BMI and unit conversion. Fast, accurate, private.",
        canonical=BASE + "/", jsonld=[ld(website_ld()), ld(org_ld())]))

    # all
    write("all/index.html", all_tpl.render(
        site=SITE, finance=finance, utility=utility,
        title=f"All Calculators & Tools — {SITE['name']}",
        desc="Browse every free calculator and tool on " + SITE["name"] + ": financial calculators and everyday utilities.",
        canonical=BASE + "/all/", jsonld=[ld(website_ld())]))

    # static info pages
    metas = {
        "financial-calculators": ("Financial Calculators — The Complete Guide | " + SITE["name"], "Every free financial calculator explained: mortgages, loans, debt payoff, compound interest, retirement and more — and how to combine them for big money decisions."),
        "about": ("About " + SITE["name"], "About TechShield Tools — free, accurate, private calculators and tools for money and everyday life."),
        "contact": ("Contact — " + SITE["name"], "Contact TechShield Tools with feedback, corrections, or calculator suggestions."),
        "privacy": ("Privacy Policy — " + SITE["name"], "TechShield Tools privacy policy. Calculations run in your browser; your numbers are never sent or stored."),
        "disclaimer": ("Disclaimer — " + SITE["name"], "TechShield Tools disclaimer. Calculators provide general estimates for educational purposes, not professional advice."),
    }
    pages_urls = []
    for slug, (ttl, dsc) in metas.items():
        raw = (ROOT / "pages" / f"{slug}.md").read_text()
        title_line = raw.splitlines()[0].lstrip("# ").strip()
        body = markdown.markdown("\n".join(raw.splitlines()[1:]), extensions=["extra"])
        write(f"{slug}/index.html", page_tpl.render(
            site=SITE, page={"title": title_line, "html": body},
            title=ttl, desc=dsc, canonical=f"{BASE}/{slug}/", jsonld=[ld(website_ld())]))
        pages_urls.append(f"{BASE}/{slug}/")

    # assets
    shutil.copytree(ROOT / "static", OUT / "static", dirs_exist_ok=True)

    # sitemap
    urls = [BASE + "/", BASE + "/all/"] + [f"{BASE}/{t['slug']}/" for t in TOOLS] + pages_urls
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    today = datetime.date.today().isoformat()
    for u in urls:
        pr = "1.0" if u == BASE + "/" else ("0.9" if any(t["slug"] in u for t in TOOLS) else "0.5")
        sm.append(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))

    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")

    # ads.txt — only emitted once a real AdSense publisher ID is set in config.yaml
    pub = str(SITE.get("adsense_publisher_id") or "").strip()
    if pub:
        if not pub.startswith("pub-"):
            pub = "pub-" + pub.replace("pub-", "")
        write("ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
        print(f"  ads.txt written for {pub}")

    host = BASE.split("//", 1)[-1]
    if host and not host.endswith("github.io"):
        write("CNAME", host)

    print(f"Built {len(TOOLS)} tools + {len(pages_urls)} pages + home/all -> {OUT}")


if __name__ == "__main__":
    main()
