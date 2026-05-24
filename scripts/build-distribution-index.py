#!/usr/bin/env python3
"""build-distribution-index.py — 从 content/ frontmatter 生成 distribution.json 看板"""

import json
import re
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DATA_DIR = ROOT / "data"

PLATFORMS = ["zhihu", "wechat", "juejin"]
STATUSES = ["pending", "drafted", "published", "archived"]

def s(v):
    return "" if v is None else str(v)

def parse_md(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return None
    return yaml.safe_load(m.group(1)) or {}

def is_post(rel: Path):
    parts = rel.parts
    return (len(parts) >= 4 and parts[0] == "content"
            and re.match(r"^\d{4}$", parts[1]) and re.match(r"^\d{2}$", parts[2]))

def main():
    posts = []
    metrics = {p: {k: 0 for k in STATUSES} for p in PLATFORMS}
    links_filled = {p: 0 for p in PLATFORMS}
    published_total = {p: 0 for p in PLATFORMS}

    for f in sorted(CONTENT_DIR.rglob("*.md")):
        rel = f.relative_to(ROOT)
        if not is_post(rel):
            continue
        meta = parse_md(f)
        if meta is None:
            continue

        _id = s(meta.get("id"))
        title = s(meta.get("title"))
        date = s(meta.get("date"))
        slug = s(meta.get("slug"))
        status = s(meta.get("status"))

        sync = meta.get("sync", {}) if isinstance(meta.get("sync"), dict) else {}
        urls = meta.get("urls", {}) if isinstance(meta.get("urls"), dict) else {}

        month = date[:7] if len(date) >= 7 else "unknown-00"
        base_name = f"{_id}-{slug}.md"

        dist_paths = {
            "zhihu": f"distribution/zhihu/{month}/{base_name}",
            "wechat": f"distribution/wechat/{month}/{base_name}",
            "juejin": f"distribution/juejin/{month}/{base_name}",
        }

        for p in PLATFORMS:
            st = s(sync.get(p, "pending"))
            if st not in STATUSES:
                st = "pending"
            metrics[p][st] += 1

            if st == "published":
                published_total[p] += 1
                if s(urls.get(p, "")).strip():
                    links_filled[p] += 1

        posts.append({
            "id": _id,
            "title": title,
            "date": date,
            "slug": slug,
            "status": status,
            "path": str(rel),
            "sync": {p: s(sync.get(p, "pending")) for p in PLATFORMS},
            "urls": {p: s(urls.get(p, "")) for p in PLATFORMS},
            "distribution_paths": dist_paths
        })

    total_posts = len(posts)
    platform_stats = {}
    for p in PLATFORMS:
        pub = published_total[p]
        pub_with_url = sum(
            1 for x in posts
            if x["sync"][p] == "published" and x["urls"][p] != ""
        )
        platform_stats[p] = {
            "pending": metrics[p]["pending"],
            "drafted": metrics[p]["drafted"],
            "published": metrics[p]["published"],
            "archived": metrics[p]["archived"],
            "links_filled": links_filled[p],
            "link_fill_rate": round(links_filled[p] / total_posts * 100, 2) if total_posts else 0.0,
            "published_with_url_rate": round(pub_with_url / pub * 100, 2) if pub else 0.0,
        }

    out = {
        "meta": {
            "updated": datetime.utcnow().isoformat() + "Z",
            "total_posts": total_posts
        },
        "platforms": platform_stats,
        "posts": posts
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "distribution.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"build-distribution-index complete: {total_posts} posts")

if __name__ == "__main__":
    main()
