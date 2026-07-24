# AutoNews — free automated news site

A zero-cost, hands-off news site for home security / VPN / streaming TV / telecom.
Every 2 hours it reads your RSS feeds, writes an **original** article with Google
Gemini (free tier), runs it through an automated quality gate, and publishes to a
static site on **GitHub Pages** — no server, no monthly bill.

```
GitHub Actions (cron, free)
   → generate.py   pull feeds → Gemini writes original article → QA gate → retry → save post
   → build.py      render posts + pages → HTML + sitemaps + RSS
   → GitHub Pages   deploy (free hosting, free HTTPS)
```

Total cost: **$0/month.** (Optional: a real domain for ~$10/year, see the end.)

---

## What you need (all free, ~20 minutes)

1. A **GitHub account** — https://github.com
2. A **Google Gemini API key** — https://aistudio.google.com/apikey
   (free tier: 1,500 requests/day, no credit card)

---

## Setup — step by step

### 1. Put this project on GitHub
- Create a new **public** repository (public = unlimited free Actions minutes).
- Upload all these files to it (drag-and-drop in the GitHub web UI works, or use git).

### 2. Add your Gemini key as a secret
- In the repo: **Settings → Secrets and variables → Actions → New repository secret**
- Name: `GEMINI_API_KEY`   Value: *(your key from Google AI Studio)*

### 3. Turn on GitHub Pages
- **Settings → Pages → Build and deployment → Source: GitHub Actions**

### 4. Edit `config.yaml`
- Set your `site: name`, `tagline`, `author`, `email`.
- Set `url:` to `https://YOURUSERNAME.github.io/YOUR-REPO` for now
  (find the exact URL under Settings → Pages after the first deploy).
- Add/replace the `feeds:` with the outlets you want to track.
- Also update the email in `pages/contact.md` and `pages/about.md`.

### 5. Launch
- Go to the **Actions** tab → select **Publish news** → **Run workflow**.
- First run builds the site (with the sample post) and deploys it.
- On the schedule after that, it writes and publishes new articles on its own.

That's it. Your site is live and self-updating.

---

## IMPORTANT — start slow (don't get filtered by Google)

A brand-new site that suddenly publishes every 2 hours looks like spam.
For the **first ~4 weeks**, publish 2–3/day, then ramp up:

- Open `.github/workflows/publish.yml`
- Comment out `- cron: "0 */2 * * *"` and use `- cron: "0 */8 * * *"` (3x/day)
- After a month with no issues, switch back to every 2 hours.

The other non-negotiables (already built in): original synthesis (never copied),
the QA gate, and real About / Contact / Editorial / Privacy pages.

---

## Your weekly 10-minute check

- Skim the latest live posts — anything off-topic or wrong? (The QA gate makes
  this rare.) Delete a bad post by removing its file in `content/posts/`.
- Once indexed, add the site to **Google Search Console**, submit
  `sitemap.xml` and `news-sitemap.xml`, and watch **Manual Actions** (must stay empty).
- After ~2–4 weeks of steady posts, optionally add the site in **Google Publisher Center**.

---

## Local test (optional)

```bash
pip install -r requirements.txt
python build.py          # builds _site/ from the sample post (no API key needed)
python -m http.server -d _site 8000   # open http://localhost:8000
```

To test generation locally, set your key first:
```bash
export GEMINI_API_KEY=your_key
python generate.py
```

---

## When you buy a real domain later

1. Buy a `.com` (Cloudflare Registrar, ~$10/yr, at-cost renewal).
2. In `config.yaml`, change `url:` to `https://yourdomain.com`.
   The build auto-writes a `CNAME` file for GitHub Pages.
3. At your registrar, add a DNS record pointing to GitHub Pages
   (a `CNAME` to `YOURUSERNAME.github.io`, or the 4 Pages `A` records).
4. In **Settings → Pages → Custom domain**, enter your domain and enable HTTPS.
5. Re-run the workflow. Done — same site, real domain, still free hosting.

---

## Files

| File | What it does |
|---|---|
| `config.yaml` | The only file you normally edit — site info + feeds + settings |
| `generate.py` | Feeds → Gemini original article → QA gate → retry → save post |
| `build.py` | Renders posts/pages → HTML, sitemaps, RSS into `_site/` |
| `synthesis_prompt.txt` | The instructions that make articles original, not copied |
| `templates/` `static/` | Page layout and styling |
| `pages/` | About, Contact, Editorial Policy, Privacy (required for Google News) |
| `content/posts/` | Generated articles (JSON). Delete the sample after launch. |
| `.github/workflows/publish.yml` | The every-2-hours automation |
