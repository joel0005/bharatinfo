import os
import json
import datetime
import requests
import xml.etree.ElementTree as ET
from pathlib import Path

# ── CONFIG ──────────────────────────────────────────────────────────────────
# Reads API key from environment (GitHub Secrets) — falls back to hardcoded for local testing
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "YOUR_NEWSAPI_KEY_HERE")

TODAY     = datetime.date.today().isoformat()
DATE_NICE = datetime.date.today().strftime("%B %d, %Y")

# ── RSS FEEDS PER SUBCATEGORY ─────────────────────────────────────────────
# Primary source — unlimited, no API key needed
RSS_SOURCES = {

    # ── WORLD AI ──────────────────────────────────────────────────────────
    "ai_company": [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://venturebeat.com/category/ai/feed/",
    ],
    "ai_tools": [
        "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
    ],
    "ai_models": [
        "https://www.technologyreview.com/feed/",
        "https://venturebeat.com/category/ai/feed/",
    ],
    "ai_research": [
        "https://www.technologyreview.com/feed/",
        "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    ],
    "ai_policy": [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
    ],

    # ── CORPORATE BUSINESS ────────────────────────────────────────────────
    "corp_india": [
        "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
        "https://www.business-standard.com/rss/home_page_top_stories.rss",
        "https://feeds.bbci.co.uk/news/business/rss.xml",
    ],
    "corp_global": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "https://www.cnbc.com/id/15839069/device/rss/rss.html",
    ],
    "corp_startup": [
        "https://inc42.com/feed/",
        "https://yourstory.com/feed",
        "https://techcrunch.com/feed/",
    ],
    "corp_market": [
        "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "https://www.moneycontrol.com/rss/MCtopnews.xml",
        "https://www.livemint.com/rss/markets",
    ],

    # ── INDIAN POLITICS ───────────────────────────────────────────────────
    "pol_central": [
        "https://feeds.feedburner.com/ndtvnews-india-news",
        "https://www.thehindu.com/news/national/feeder/default.rss",
        "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    ],
    "pol_state": [
        "https://feeds.feedburner.com/ndtvnews-india-news",
        "https://www.thehindu.com/news/states/feeder/default.rss",
        "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    ],
    "pol_policy": [
        "https://www.thehindu.com/news/national/feeder/default.rss",
        "https://www.business-standard.com/rss/politics-and-policy.rss",
        "https://feeds.feedburner.com/ndtvnews-top-stories",
    ],
    "pol_election": [
        "https://feeds.feedburner.com/ndtvnews-india-news",
        "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
        "https://www.thehindu.com/elections/feeder/default.rss",
    ],

    # ── INDIAN STOCKS ─────────────────────────────────────────────────────
    "ins_movers": [
        "https://www.moneycontrol.com/rss/MCtopnews.xml",
        "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
        "https://www.livemint.com/rss/markets",
    ],
    "ins_ipo": [
        "https://www.moneycontrol.com/rss/MCtopnews.xml",
        "https://economictimes.indiatimes.com/markets/ipos/fpos/rssfeeds/2143429.cms",
        "https://inc42.com/feed/",
    ],
    "ins_sectors": [
        "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
        "https://www.moneycontrol.com/rss/MCtopnews.xml",
        "https://www.business-standard.com/rss/markets-106.rss",
    ],
    "ins_general": [
        "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "https://www.livemint.com/rss/markets",
        "https://www.moneycontrol.com/rss/MCtopnews.xml",
    ],

    # ── WORLD STOCKS ──────────────────────────────────────────────────────
    "ws_us": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "https://www.cnbc.com/id/15839069/device/rss/rss.html",
    ],
    "ws_asia": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    ],
    "ws_commodity": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.moneycontrol.com/rss/MCtopnews.xml",
        "https://economictimes.indiatimes.com/markets/commodities/rssfeeds/2146842.cms",
    ],
    "ws_crypto": [
        "https://cointelegraph.com/rss",
        "https://coindesk.com/arc/outboundfeeds/rss/",
        "https://feeds.feedburner.com/CoinDesk",
    ],
}

# ── NEWSAPI BACKUP QUERIES ────────────────────────────────────────────────
NEWSAPI_BACKUP = {
    "ai_company":   ["OpenAI Google DeepMind Anthropic news"],
    "ai_tools":     ["AI tools platform launch"],
    "ai_models":    ["AI model release GPT LLM"],
    "ai_research":  ["AI research paper breakthrough"],
    "ai_policy":    ["AI regulation policy government"],
    "corp_india":   ["India corporate business"],
    "corp_global":  ["global corporate merger acquisition"],
    "corp_startup": ["India startup funding"],
    "corp_market":  ["India economy stock market"],
    "pol_central":  ["India central government Modi"],
    "pol_state":    ["India state government politics"],
    "pol_policy":   ["India government policy scheme"],
    "pol_election": ["India election 2026"],
    "ins_movers":   ["NSE BSE top gainers losers"],
    "ins_ipo":      ["India IPO listing"],
    "ins_sectors":  ["India sector stocks"],
    "ins_general":  ["Sensex Nifty market"],
    "ws_us":        ["S&P 500 Nasdaq Wall Street"],
    "ws_asia":      ["Asia stock market Nikkei"],
    "ws_commodity": ["gold oil crude commodity"],
    "ws_crypto":    ["Bitcoin Ethereum crypto"],
}

# ── CATEGORIES STRUCTURE ──────────────────────────────────────────────────
CATEGORIES = [
    {
        "id": "ai", "label": "World AI", "emoji": "🤖",
        "subs": [
            {"id": "ai_company",  "label": "Company News",     "emoji": "🏢"},
            {"id": "ai_tools",    "label": "Tools & Platforms","emoji": "🛠️"},
            {"id": "ai_models",   "label": "Models",           "emoji": "🧠"},
            {"id": "ai_research", "label": "Research",         "emoji": "🔬"},
            {"id": "ai_policy",   "label": "Policy & Ethics",  "emoji": "⚖️"},
        ],
    },
    {
        "id": "corporate", "label": "Corporate Business", "emoji": "💼",
        "subs": [
            {"id": "corp_india",   "label": "India Business",    "emoji": "🇮🇳"},
            {"id": "corp_global",  "label": "Global Business",   "emoji": "🌍"},
            {"id": "corp_startup", "label": "Startups & Funding","emoji": "🚀"},
            {"id": "corp_market",  "label": "Markets & Economy", "emoji": "📈"},
        ],
    },
    {
        "id": "politics", "label": "Indian Politics", "emoji": "🏛️",
        "subs": [
            {"id": "pol_central",  "label": "Central Govt",   "emoji": "🏟️"},
            {"id": "pol_state",    "label": "State Politics", "emoji": "🗺️"},
            {"id": "pol_policy",   "label": "Policy & Law",   "emoji": "📜"},
            {"id": "pol_election", "label": "Elections",      "emoji": "🗳️"},
        ],
    },
    {
        "id": "instock", "label": "Indian Stocks", "emoji": "📊",
        "subs": [
            {"id": "ins_movers",  "label": "Top Movers",  "emoji": "📈"},
            {"id": "ins_ipo",     "label": "IPO News",    "emoji": "🆕"},
            {"id": "ins_sectors", "label": "Sector News", "emoji": "🏭"},
            {"id": "ins_general", "label": "Market News", "emoji": "📰"},
        ],
    },
    {
        "id": "worldstock", "label": "World Stocks", "emoji": "🌐",
        "subs": [
            {"id": "ws_us",        "label": "US Markets",   "emoji": "🇺🇸"},
            {"id": "ws_asia",      "label": "Asia Markets", "emoji": "🌏"},
            {"id": "ws_commodity", "label": "Commodities",  "emoji": "🛢️"},
            {"id": "ws_crypto",    "label": "Crypto",       "emoji": "₿" },
        ],
    },
]

HEADERS = {"User-Agent": "Mozilla/5.0 BharatInfo/1.0 RSS Reader"}

# ── SPAM / PROMO FILTER ───────────────────────────────────────────────
SPAM_KEYWORDS = [
    "promo code", "promo codes", "coupon code", "coupon codes",
    "discount code", "% off", " off |", "off | ",
    "deals", "deal of the day", "best deals", "amazon deals",
    "% discount", "blackfriday", "black friday", "cyber monday",
    "save up to", "subscription deals", "gift guide", "best gifts",
    "shopping deals", "wirecutter", "review:", "reviewed:",
    "best of ", "buying guide", "discount for",
]

SPAM_URL_PATHS = [
    "/coupon", "/promo", "/deals", "/discount", "/gift-guide",
    "/buying-guide", "/wirecutter", "/review/",
]

def is_spam(article: dict) -> bool:
    """Filter out promo/coupon/deal articles"""
    text = (article.get("title", "") + " " + article.get("description", "")).lower()
    url  = (article.get("url") or "").lower()
    
    for kw in SPAM_KEYWORDS:
        if kw in text:
            return True
    for path in SPAM_URL_PATHS:
        if path in url:
            return True
    return False


# ── RSS FETCH ─────────────────────────────────────────────────────────────
def fetch_rss(url: str) -> list:
    try:
        resp = requests.get(url, timeout=12, headers=HEADERS)
        if resp.status_code != 200:
            return []
        root = ET.fromstring(resp.content)
        ns = {}
        # handle both RSS and Atom
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        articles = []
        for item in items[:8]:
            def g(tag, atom_tag=None):
                v = item.findtext(tag)
                if not v and atom_tag:
                    v = item.findtext(atom_tag)
                return (v or "").strip()

            title = g("title", "{http://www.w3.org/2005/Atom}title")
            link  = g("link",  "{http://www.w3.org/2005/Atom}link")
            desc  = g("description", "{http://www.w3.org/2005/Atom}summary")
            pub   = g("pubDate", "{http://www.w3.org/2005/Atom}updated")

            # clean HTML from description
            import re
            desc = re.sub(r"<[^>]+>", "", desc)[:220].strip()

            # try to get image from media:content or enclosure
            image = ""
            media = item.find("{http://search.yahoo.com/mrss/}content")
            if media is not None:
                image = media.get("url", "")
            if not image:
                enc = item.find("enclosure")
                if enc is not None and "image" in (enc.get("type") or ""):
                    image = enc.get("url", "")

            if title and link and "[Removed]" not in title:
                article = {
                    "title":       title,
                    "description": desc,
                    "url":         link,
                    "source":      url.split("/")[2].replace("www.", "").replace("feeds.feedburner.com/", ""),
                    "image":       image,
                    "publishedAt": pub,
                }
                # skip promo/coupon spam
                if is_spam(article):
                    continue
                articles.append(article)
        return articles
    except Exception as e:
        print(f"      RSS error {url}: {e}")
        return []


# ── NEWSAPI BACKUP ────────────────────────────────────────────────────────
_newsapi_used = 0
_newsapi_limit = 80   # stay under daily limit

def fetch_newsapi(queries: list) -> list:
    global _newsapi_used
    articles = []
    seen = set()
    for q in queries:
        if _newsapi_used >= _newsapi_limit:
            break
        url = (
            "https://newsapi.org/v2/everything"
            f"?q={requests.utils.quote(q)}"
            f"&language=en&sortBy=publishedAt&pageSize=8"
            f"&apiKey={NEWS_API_KEY}"
        )
        try:
            resp = requests.get(url, timeout=12)
            _newsapi_used += 1
            if resp.status_code == 429:
                print("      NewsAPI limit reached — skipping rest")
                break
            if resp.status_code != 200:
                continue
            for a in resp.json().get("articles", []):
                title = (a.get("title") or "").strip()
                if not title or "[Removed]" in title or title in seen:
                    continue
                seen.add(title)
                article = {
                    "title":       title,
                    "description": (a.get("description") or "").strip()[:220],
                    "url":         a.get("url", ""),
                    "source":      a.get("source", {}).get("name", "Unknown"),
                    "image":       a.get("urlToImage", ""),
                    "publishedAt": a.get("publishedAt", ""),
                }
                if is_spam(article):
                    continue
                articles.append(article)
        except Exception as e:
            print(f"      NewsAPI error: {e}")
    return articles


# ── FETCH FOR ONE SUBCATEGORY ─────────────────────────────────────────────
def fetch_sub(sub_id: str) -> list:
    seen = set()
    articles = []

    # 1. Try RSS feeds first
    for rss_url in RSS_SOURCES.get(sub_id, []):
        for a in fetch_rss(rss_url):
            if a["title"] not in seen:
                seen.add(a["title"])
                articles.append(a)

    # 2. If less than 5 articles, top up with NewsAPI
    if len(articles) < 5 and NEWS_API_KEY != "YOUR_NEWSAPI_KEY_HERE":
        backup = fetch_newsapi(NEWSAPI_BACKUP.get(sub_id, []))
        for a in backup:
            if a["title"] not in seen:
                seen.add(a["title"])
                articles.append(a)

    # sort newest first (best effort — pubDate formats vary)
    articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
    return articles[:10]


# ── MAIN ─────────────────────────────────────────────────────────────────
def main():
    output = {"date": TODAY, "date_nice": DATE_NICE, "categories": []}

    import re
    from urllib.parse import urlparse

    def normalize_title(t):
        t = re.sub(r'[^\w\s]', '', (t or '').lower()).strip()
        t = re.sub(r'\s+', ' ', t)
        return t[:60]

    def get_url_slug(url):
        try:
            path = urlparse(url).path.strip('/')
            parts = [p for p in path.split('/') if p][-2:]
            return '/'.join(parts).lower()[:80]
        except:
            return (url or '').lower()

    # First pass: fetch all articles for all subcategories
    # Second pass: distribute uniquely with priority order
    all_subs = []  # list of (cat, sub, articles)
    for cat in CATEGORIES:
        print(f"\n{cat['emoji']} {cat['label']}")
        for sub in cat["subs"]:
            print(f"  → {sub['label']} … ", end="", flush=True)
            arts = fetch_sub(sub["id"])
            print(f"got {len(arts)} raw articles")
            all_subs.append((cat, sub, arts))

    # Now distribute — give each subcategory unique articles
    # Strategy: round-robin assignment to ensure no category is empty
    print(f"\n📊 Distributing articles uniquely across {len(all_subs)} subcategories...")

    seen_titles = set()
    seen_urls = set()
    seen_slugs = set()
    seen_images = set()

    # Track which articles each sub has after dedup
    sub_articles = {sub_id: [] for cat, sub, arts in all_subs for sub_id in [sub["id"]]}

    def is_dup(a):
        nt = normalize_title(a.get("title", ""))
        u  = (a.get("url") or "").strip()
        s  = get_url_slug(u) if u else ""
        i  = (a.get("image") or "").strip()
        if not nt: return True
        if nt in seen_titles: return True
        if u and u in seen_urls: return True
        if s and s in seen_slugs: return True
        if i and i in seen_images: return True
        return False

    def mark_seen(a):
        nt = normalize_title(a.get("title", ""))
        u  = (a.get("url") or "").strip()
        s  = get_url_slug(u) if u else ""
        i  = (a.get("image") or "").strip()
        seen_titles.add(nt)
        if u: seen_urls.add(u)
        if s: seen_slugs.add(s)
        if i: seen_images.add(i)

    # Round-robin: in each round, each subcategory gets ONE article
    # Repeat until each sub has up to 10 articles
    for round_num in range(15):  # max 15 articles per sub
        for cat, sub, arts in all_subs:
            if len(sub_articles[sub["id"]]) >= 10:
                continue
            # find the first non-duplicate article from this sub's pool
            for a in arts:
                if a in sub_articles[sub["id"]]:
                    continue
                if is_dup(a):
                    continue
                sub_articles[sub["id"]].append(a)
                mark_seen(a)
                break

    # Build output
    for cat in CATEGORIES:
        cat_out = {
            "id": cat["id"], "label": cat["label"],
            "emoji": cat["emoji"], "subs": []
        }
        for sub in cat["subs"]:
            arts = sub_articles[sub["id"]]
            print(f"  ✓ {sub['label']}: {len(arts)} unique articles")
            cat_out["subs"].append({
                "id": sub["id"], "label": sub["label"],
                "emoji": sub["emoji"], "articles": arts,
            })
        output["categories"].append(cat_out)

    out_dir = Path("docs")
    out_dir.mkdir(exist_ok=True)

    (out_dir / "today.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / f"{TODAY}.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    # ── AUTO-DELETE archive files older than 2 days ──────────────────
    cutoff = datetime.date.today() - datetime.timedelta(days=2)
    for f in out_dir.glob("*.json"):
        if f.name in ("today.json", "archive.json"):
            continue
        # filename like 2026-04-30.json
        try:
            file_date = datetime.date.fromisoformat(f.stem)
            if file_date < cutoff:
                f.unlink()
                print(f"🗑  Deleted old archive: {f.name}")
        except ValueError:
            pass

    # update archive index — keep only last 2 days
    archive = []
    for f in sorted(out_dir.glob("*.json"), reverse=True):
        if f.name in ("today.json", "archive.json"):
            continue
        try:
            file_date = datetime.date.fromisoformat(f.stem)
            archive.append({
                "date": file_date.isoformat(),
                "date_nice": file_date.strftime("%B %d, %Y")
            })
        except ValueError:
            pass
    archive_file = out_dir / "archive.json"
    archive_file.write_text(
        json.dumps(archive[:3], indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n✅  Done! Saved docs/today.json + docs/{TODAY}.json")
    print(f"📅  Archive: {len(archive)} day(s) kept (today + 2 days max)")
    print(f"📡  NewsAPI requests used: {_newsapi_used}")


if __name__ == "__main__":
    main()
