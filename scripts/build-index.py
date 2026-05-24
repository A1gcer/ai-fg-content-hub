#!/usr/bin/env python3
"""Build content indexes: data/index.json, data/tags.json, data/timeline.json"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

def parse_frontmatter(text):
    """Parse YAML-like frontmatter between --- markers"""
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not m:
        return {}, text
    header = m.group(1)
    body = text[m.end():]
    meta = {}
    for line in header.strip().split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip()
            # Parse array values
            if val.startswith('[') and val.endswith(']'):
                val = [v.strip().strip('"\'') for v in val[1:-1].split(',')]
            else:
                val = val.strip('"\'')
            meta[key] = val
    return meta, body.strip()

def scan_content():
    posts = []
    for fpath in sorted(CONTENT_DIR.rglob("*.md")):
        if "template" in fpath.name.lower():
            continue
        text = fpath.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if not meta.get("id"):
            continue
        rel_path = fpath.relative_to(CONTENT_DIR.parent)
        posts.append({
            "id": meta.get("id"),
            "title": meta.get("title", ""),
            "date": meta.get("date", ""),
            "category": meta.get("category", ""),
            "tags": meta.get("tags", []),
            "risk": meta.get("risk", ""),
            "channel": meta.get("channel", ""),
            "status": meta.get("status", "draft"),
            "summary": meta.get("summary", ""),
            "feishu_id": meta.get("feishu_id", ""),
            "path": str(rel_path),
            "word_count": len(body),
        })
    return posts

def build_index(posts):
    """Build data/index.json"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    index = {
        "meta": {
            "total": len(posts),
            "published": len([p for p in posts if p["status"] == "published"]),
            "draft": len([p for p in posts if p["status"] == "draft"]),
            "categories": len(set(p["category"] for p in posts)),
            "tags": len(set(t for p in posts for t in (p["tags"] if isinstance(p["tags"], list) else [p["tags"]]))),
            "updated": datetime.utcnow().isoformat() + "Z",
        },
        "posts": posts,
    }
    (DATA_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2))
    print(f"✅ data/index.json — {len(posts)} posts")

def build_tags(posts):
    """Build data/tags.json"""
    tags = {}
    for p in posts:
        tag_list = p["tags"] if isinstance(p["tags"], list) else [p["tags"]]
        for tag in tag_list:
            tag = tag.strip()
            if tag not in tags:
                tags[tag] = {"tag": tag, "count": 0, "posts": []}
            tags[tag]["count"] += 1
            tags[tag]["posts"].append(p["id"])
    
    tag_list = sorted(tags.values(), key=lambda x: -x["count"])
    (DATA_DIR / "tags.json").write_text(json.dumps(tag_list, ensure_ascii=False, indent=2))
    print(f"✅ data/tags.json — {len(tag_list)} tags")

def build_timeline(posts):
    """Build data/timeline.json"""
    timeline = {}
    for p in posts:
        date = p.get("date", "")
        month = date[:7] if date else "unknown"
        if month not in timeline:
            timeline[month] = {"month": month, "count": 0, "posts": []}
        timeline[month]["count"] += 1
        timeline[month]["posts"].append(p["id"])
    
    result = sorted(timeline.values(), key=lambda x: x["month"], reverse=True)
    (DATA_DIR / "timeline.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"✅ data/timeline.json — {len(result)} months")

def build_risk_index(posts):
    """Build data/by-risk.json"""
    levels = {}
    for p in posts:
        level = p.get("risk", "未知")
        if level not in levels:
            levels[level] = {"risk": level, "count": 0, "posts": []}
        levels[level]["count"] += 1
        levels[level]["posts"].append(p["id"])
    
    result = sorted(levels.values(), key=lambda x: -x["count"])
    (DATA_DIR / "by-risk.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"✅ data/by-risk.json — {len(result)} risk levels")

def generate_readme_table(posts):
    """Generate the recent posts table for README"""
    headers = ["Date", "Title", "Category", "Tags", "Risk", "Status"]
    rows = []
    for p in posts[:10]:  # Last 10
        tags = ", ".join(p["tags"][:3]) if isinstance(p["tags"], list) else str(p["tags"])
        risk_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(p["risk"], "⚪")
        status_icon = {"published": "✅", "draft": "📝", "复盘": "📊"}.get(p["status"], "📄")
        rows.append(f"| {p['date']} | [{p['title']}]({p['path']}) | {p['category']} | {tags} | {risk_icon} {p['risk']} | {status_icon} {p['status']} |")
    
    return "\n".join(rows)

if __name__ == "__main__":
    posts = scan_content()
    if not posts:
        print("⚠️ No posts found in content/")
        sys.exit(0)
    
    build_index(posts)
    build_tags(posts)
    build_timeline(posts)
    build_risk_index(posts)
    
    # Generate README table for use in rebuild-readme.sh
    table = generate_readme_table(posts)
    meta = {
        "total": len(posts),
        "published": len([p for p in posts if p["status"] == "published"]),
        "draft": len([p for p in posts if p["status"] == "draft"]),
        "categories": len(set(p["category"] for p in posts)),
    }
    (DATA_DIR / "readme-meta.json").write_text(json.dumps({"table": table, **meta}))
    print(f"\n📊 Stats: {meta['total']} total · {meta['published']} published · {meta['draft']} drafts · {meta['categories']} categories")
    print("✅ Build complete")
