#!/usr/bin/env python3
"""Build Markdown pages from content/ into docs/ for GitHub Pages"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
CONTENT_PARENT = Path(__file__).resolve().parent.parent

def load_data(name):
    fpath = DATA_DIR / name
    if not fpath.exists():
        print(f"⚠️ data/{name} not found. Run build-index.py first.")
        return None
    return json.loads(fpath.read_text(encoding="utf-8"))

def write_doc(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def build_homepage(posts, meta):
    """Build docs/index.md"""
    lines = [
        "---",
        "layout: home",
        "title: AI不翻车FAQ",
        "description: 职场人用AI做出能交差的成果",
        "---",
        "",
        "# AI不翻车FAQ 📖",
        "",
        "> 我不教你玩AI，我教你用AI做出能交差的东西。",
        "",
        "## 📊 数据看板",
        "",
        f"- **总文章**: {meta['total']}",
        f"- **已发布**: {meta['published']}",
        f"- **草稿**: {meta['draft']}",
        f"- **分类**: {meta['categories']} 个",
        "",
        "## 📝 最新内容",
        "",
        "| Date | Title | Category | Risk | Status |",
        "|------|-------|----------|------|--------|",
    ]
    for p in posts[:10]:
        risk_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(p["risk"], "⚪")
        status_icon = {"published": "✅", "draft": "📝"}.get(p["status"], "📄")
        lines.append(f"| {p['date']} | [{p['title']}](../{p['path']}) | {p['category']} | {risk_icon} {p['risk']} | {status_icon} {p['status']} |")
    
    lines += [
        "",
        "---",
        "",
        "### 🔍 快速入口",
        "",
        "- [📂 按分类浏览](categories/)",
        "- [🏷️ 按标签浏览](tags/)",
        "- [📅 时间线](timeline/)",
        "- [⚠️ 按风险等级](risk/)",
        "",
        "---",
        f"*更新于: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*",
    ]
    write_doc(DOCS_DIR / "index.md", "\n".join(lines))
    print("✅ docs/index.md")

def build_categories(posts):
    """Build docs/categories/index.md"""
    cats = {}
    for p in posts:
        c = p["category"]
        if c not in cats:
            cats[c] = []
        cats[c].append(p)
    
    lines = [
        "---",
        "layout: page",
        "title: 分类浏览",
        "---",
        "",
        "# 📂 分类浏览",
        "",
    ]
    for cat in sorted(cats.keys()):
        items = cats[cat]
        lines += [f"## {cat} ({len(items)}篇)", ""]
        for p in items:
            lines.append(f"- [{p['title']}](../../{p['path']}) — {p['date']}")
        lines.append("")
    
    write_doc(DOCS_DIR / "categories" / "index.md", "\n".join(lines))
    print("✅ docs/categories/index.md")

def build_tags_page(tags):
    lines = [
        "---",
        "layout: page",
        "title: 标签浏览",
        "---",
        "",
        "# 🏷️ 标签浏览",
        "",
    ]
    for t in tags:
        lines.append(f"### {t['tag']} ({t['count']}篇)")
        lines.append("")
        for pid in t["posts"]:
            lines.append(f"- `{pid}`")
        lines.append("")
    
    write_doc(DOCS_DIR / "tags" / "index.md", "\n".join(lines))
    print("✅ docs/tags/index.md")

def build_timeline_page(timeline):
    lines = [
        "---",
        "layout: page",
        "title: 时间线",
        "---",
        "",
        "# 📅 时间线",
        "",
    ]
    for t in timeline:
        lines.append(f"### {t['month']} ({t['count']}篇)")
        lines.append("")
        for pid in t["posts"]:
            lines.append(f"- `{pid}`")
        lines.append("")
    
    write_doc(DOCS_DIR / "timeline" / "index.md", "\n".join(lines))
    print("✅ docs/timeline/index.md")

def build_risk_page(risks):
    lines = [
        "---",
        "layout: page",
        "title: 风险等级",
        "---",
        "",
        "# ⚠️ 按风险等级浏览",
        "",
    ]
    risk_order = {"高": "🔴", "中": "🟡", "低": "🟢"}
    for r in risks:
        icon = risk_order.get(r["risk"], "⚪")
        lines.append(f"### {icon} {r['risk']} ({r['count']}篇)")
        lines.append("")
        for pid in r["posts"]:
            lines.append(f"- `{pid}`")
        lines.append("")
    
    write_doc(DOCS_DIR / "risk" / "index.md", "\n".join(lines))
    print("✅ docs/risk/index.md")

if __name__ == "__main__":
    index = load_data("index.json")
    if not index:
        import sys; sys.exit(1)
    
    posts = index["posts"]
    meta = index["meta"]
    
    tags = load_data("tags.json")
    timeline = load_data("timeline.json")
    risks = load_data("by-risk.json")
    
    build_homepage(posts, meta)
    build_categories(posts)
    if tags: build_tags_page(tags)
    if timeline: build_timeline_page(timeline)
    if risks: build_risk_page(risks)
    
    print("\n✅ Pages build complete — output in docs/")
