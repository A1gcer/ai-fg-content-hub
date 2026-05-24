#!/usr/bin/env python3
"""build-sitemap.py — 生成 sitemap.xml + robots.txt"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"

SITE_URL = "https://a1gcer.github.io/ai-fg-content-hub"

def load_json(name):
    p = DATA_DIR / name
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))

def main():
    index = load_json("index.json")
    if not index:
        raise SystemExit("data/index.json not found")

    posts = index["posts"]
    published = [p for p in posts if p["status"] == "published"]

    urls = [(f"{SITE_URL}/", "daily", "1.0")]
    for p in published:
        loc = f"{SITE_URL}/{p['url_path']}"
        lastmod = p.get("updated", p.get("date", ""))
        urls.append((loc, lastmod, "weekly", "0.8"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, *rest in urls:
        lastmod = rest[0] if rest else ""
        changefreq = rest[1] if len(rest) > 1 else "weekly"
        priority = rest[2] if len(rest) > 2 else "0.5"
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod}</lastmod>" if lastmod else "",
            f"    <changefreq>{changefreq}</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    (DOCS_DIR / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://a1gcer.github.io/ai-fg-content-hub/sitemap.xml\n",
        encoding="utf-8",
    )
    print("build-sitemap complete")

if __name__ == "__main__":
    main()
