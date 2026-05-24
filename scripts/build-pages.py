#!/usr/bin/env python3
"""build-pages.py — 从 data/index.json 生成 docs/ 页面"""

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"

def load_json(name):
    p = DATA_DIR / name
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def sort_by_date_desc(items):
    return sorted(items, key=lambda x: x.get("date", ""), reverse=True)

def post_link(p, depth=0):
    prefix = "../" * depth
    return f"{prefix}{p['url_path']}"

def build_home(posts, meta):
    risk_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}
    lines = [
        "# AI不翻车FAQ / AI-FG", "",
        "> 面向职场人的 AI 交付安全与质量控制知识库。", "",
        "## 数据看板", "",
        f"- 总文章：{meta['total']}",
        f"- 已发布：{meta['published']}",
        f"- 草稿：{meta['draft']}",
        f"- 归档：{meta['archived']}",
        f"- 分类：{meta['categories']}",
        f"- 标签：{meta['tags']}", "",
        "## 最新内容", "",
        "| Date | Title | Category | Risk |",
        "|---|---|---|---|",
    ]
    for p in sort_by_date_desc(posts)[:10]:
        icon = risk_icon.get(p["risk"], "⚪")
        lines.append(f"| {p['date']} | [{p['title']}]({post_link(p,0)}) | {p['category']} | {icon} {p['risk']} |")
    lines += [
        "", "## 核心页面", "",
        "- [分类](categories/)",
        "- [标签](tags/)",
        "- [时间线](timeline/)",
        "- [风险](risk/)", "",
        f"*更新于 {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*",
    ]
    write(DOCS_DIR / "index.md", "\n".join(lines))

def build_categories(posts):
    cats = {}
    for p in posts:
        cats.setdefault(p["category"], []).append(p)
    lines = ["# 分类浏览", ""]
    for c in sorted(cats.keys()):
        lines.append(f"## {c}（{len(cats[c])}）\n")
        for p in sort_by_date_desc(cats[c]):
            lines.append(f"- [{p['title']}]({post_link(p,1)}) · {p['date']}")
        lines.append("")
    write(DOCS_DIR / "categories" / "index.md", "\n".join(lines))

def build_tags(posts):
    tags = {}
    for p in posts:
        for t in p["tags"]:
            tags.setdefault(t, []).append(p)
    lines = ["# 标签浏览", ""]
    for t in sorted(tags.keys()):
        lines.append(f"## {t}（{len(tags[t])}）\n")
        for p in sort_by_date_desc(tags[t]):
            lines.append(f"- [{p['title']}]({post_link(p,1)})")
        lines.append("")
    write(DOCS_DIR / "tags" / "index.md", "\n".join(lines))

def build_timeline(posts):
    m = {}
    for p in posts:
        k = p["date"][:7] if p["date"] else "unknown"
        m.setdefault(k, []).append(p)
    lines = ["# 时间线", ""]
    for month in sorted(m.keys(), reverse=True):
        lines.append(f"## {month}（{len(m[month])}）\n")
        for p in sort_by_date_desc(m[month]):
            lines.append(f"- [{p['title']}]({post_link(p,1)})")
        lines.append("")
    write(DOCS_DIR / "timeline" / "index.md", "\n".join(lines))

def build_risk(posts):
    r = {}
    for p in posts:
        r.setdefault(p["risk"], []).append(p)
    icon = {"高": "🔴", "中": "🟡", "低": "🟢"}
    lines = ["# 按风险浏览", ""]
    for risk in ["高", "中", "低"]:
        arr = r.get(risk, [])
        if not arr:
            continue
        lines.append(f"## {icon[risk]} {risk}（{len(arr)}）\n")
        for p in sort_by_date_desc(arr):
            lines.append(f"- [{p['title']}]({post_link(p,1)})")
        lines.append("")
    write(DOCS_DIR / "risk" / "index.md", "\n".join(lines))

def render_post_page(p):
    import json as _json
    jsonld = ""
    if p.get("question") and p.get("answer"):
        jsonld = f"""
<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[{{
    "@type":"Question",
    "name":{_json.dumps(p["question"], ensure_ascii=False)},
    "acceptedAnswer":{{
      "@type":"Answer",
      "text":{_json.dumps(p["answer"], ensure_ascii=False)}
    }}
  }}]
}}
</script>""".strip()
    lines = [
        f"# {p['title']}", "",
        f"> 分类：{p['category']} ｜ 风险：{p['risk']} ｜ 日期：{p['date']}", "",
        f"**一句话答案：** {p.get('answer', '')}", "",
        p["body"], "",
        "## 复核提醒", "",
        "- AI 可做初稿，终稿责任在人",
        "- 关键事实必须人工核查",
        "- 涉及敏感信息请勿上传公共 AI 工具", "",
    ]
    if jsonld:
        lines.append(jsonld)
    return "\n".join(lines)

def build_content_pages(items):
    for p in items:
        if p["status"] != "published":
            continue
        out = DOCS_DIR / p["url_path"] / "index.md"
        write(out, render_post_page(p))

def build_awesome(posts):
    lines = ["# Awesome AI不翻车", "", "## AI误区", ""]
    for p in posts:
        if "误区" in p["title"] or "为什么" in p["title"]:
            lines.append(f"- [{p['title']}](./{post_link(p,0)})")
    lines += ["", "## 检查清单", "",
              "- [AI 生成内容交付前检查清单](checklists/ai-output-quality-checklist/)",
              "- [AI 敏感信息红线清单](checklists/ai-privacy-risk-checklist/)"]
    write(DOCS_DIR / "awesome-ai-fg.md", "\n".join(lines))

if __name__ == "__main__":
    index = load_json("index.json")
    if not index:
        raise SystemExit("data/index.json not found")
    items = index["posts"]
    published = [x for x in items if x["status"] == "published"]
    build_home(published, index["meta"])
    build_categories(published)
    build_tags(published)
    build_timeline(published)
    build_risk(published)
    build_content_pages(items)
    build_awesome(published)
    print("build-pages complete")
