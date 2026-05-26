#!/usr/bin/env python3
"""build-pages.py — 从 data/index.json 生成 docs/ 页面"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

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
    lines.append("")
    lines.append(gen_jsonld_home(meta))
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
    lines.append(gen_jsonld_collection("分类浏览", f"共{len(cats)}个分类，{len(published)}篇文章", "categories/"))
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
    lines.append(gen_jsonld_collection("标签浏览", f"共{len(tags)}个标签", "tags/"))
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
    lines.append(gen_jsonld_collection("时间线", f"共{len(m)}个月，{len(published)}篇文章", "timeline/"))
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
    lines.append(gen_jsonld_collection("按风险浏览", f"高{len(r.get('高',[]))}篇 / 中{len(r.get('中',[]))}篇 / 低{len(r.get('低',[]))}篇", "risk/"))
    write(DOCS_DIR / "risk" / "index.md", "\n".join(lines))

def gen_jsonld_collection(title: str, description: str, url_path: str) -> str:
    site_url = "https://a1gcer.github.io/ai-fg-content-hub"
    cp = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": f"{site_url}/{url_path}",
        "isPartOf": {
            "@type": "WebSite",
            "name": "AI不翻车FAQ / AI-FG",
            "url": site_url
        }
    }
    return f"\n<script type=\"application/ld+json\">\n{json.dumps(cp, indent=2, ensure_ascii=False)}\n</script>"

def gen_jsonld_article(p) -> str:
    """生成 Article + (可选 FAQPage) 双层 JSON-LD"""
    site_url = "https://a1gcer.github.io/ai-fg-content-hub"
    page_url = f"{site_url}/{p['url_path']}"

    # Base Article schema
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["title"],
        "description": p.get("summary", p.get("answer", "")),
        "datePublished": p.get("date", ""),
        "dateModified": p.get("updated", p.get("date", "")),
        "author": {
            "@type": "Person",
            "name": "A1gcer"
        },
        "publisher": {
            "@type": "Person",
            "name": "A1gcer"
        },
        "about": {
            "@type": "Thing",
            "name": p.get("category", "AI交付")
        },
        "keywords": ", ".join(p.get("tags", [])),
        "url": page_url,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": page_url
        }
    }
    graphs = [article]

    # BreadcrumbList
    section = p.get("section", p["url_path"].split("/")[0])
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": site_url},
            {"@type": "ListItem", "position": 2, "name": section, "item": f"{site_url}/{section}/"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": page_url},
        ]
    }
    graphs.append(breadcrumb)

    # FAQPage if question+answer exist
    if p.get("question") and p.get("answer"):
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{
                "@type": "Question",
                "name": p["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": p["answer"]
                }
            }]
        }
        graphs.append(faq)

    # Render as @graph
    return f"""
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graphs}, indent=2, ensure_ascii=False)}
</script>""".strip()


def gen_jsonld_home(meta) -> str:
    site_url = "https://a1gcer.github.io/ai-fg-content-hub"
    ws = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "AI不翻车FAQ / AI-FG",
        "description": "面向职场人的 AI 交付安全与质量控制知识库",
        "url": site_url,
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint", "urlTemplate": f"{site_url}/?s={{search_term_string}}"},
            "query-input": "required name=search_term_string"
        }
    }
    return f"<script type=\"application/ld+json\">\n{json.dumps(ws, indent=2, ensure_ascii=False)}\n</script>"


def render_post_page(p):
    jsonld = gen_jsonld_article(p)
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
    lines.append(gen_jsonld_collection("Awesome AI不翻车", "精选推荐的高质量AI使用内容", "awesome-ai-fg"))
    write(DOCS_DIR / "awesome-ai-fg.md", "\n".join(lines))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") if s else ""

def build_prompts(posts):
    """生成卡片式 Skill 库页面（Skill > Prompt，兼容旧 Prompt 数据）"""
    risk_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}
    risk_tag = {"高": "tag-risk-high", "中": "tag-risk-mid", "低": "tag-risk-low"}
    cards = []
    for p in posts:
        skill = p.get("skill", {})
        prompt = skill.get("instruction", "") or p.get("prompt", "")
        if not prompt:
            continue
        skill_name = skill.get("name", "")
        skill_scenario = skill.get("scenario", "")
        skill_constraints = skill.get("constraints", "")
        skill_checks = skill.get("checks", "")
        risk = skill.get("risk", p.get("risk", "中"))
        # Clean emoji prefix from risk if present
        risk_clean = re.sub(r"[🔴🟡🟢⚪]", "", risk).strip() or risk
        risk_html = risk_icon.get(risk_clean, "⚪")
        tag_html = risk_tag.get(risk_clean, "")
        escaped_prompt = esc(prompt)
        escaped_constraints = esc(skill_constraints)
        escaped_checks = esc(skill_checks)

        cards.append(f"""
<div class="prompt-card">
  <div class="prompt-card-header">
    <h3>\U0001f9e0 {skill_name if skill_name else p['title']}</h3>
    <div class="prompt-card-meta">
      <span>\U0001f4c2 {p.get('category', '通用')}</span>
      <span><span class="tag {tag_html}">{risk_html} {risk_clean}</span></span>
    </div>
  </div>
  <div class="prompt-card-body">
    <div class="skill-scenario">\U0001f3af 场景：{esc(skill_scenario)}</div>
    <details open="open">
      <summary>\U0001f4cb 可复制 Skill（一键复制）</summary>
      <pre><code>{escaped_prompt}

--- 约束 ---
{escaped_constraints if escaped_constraints else '无'}

--- 输出检查 ---
{escaped_checks if escaped_checks else '无'}</code></pre>
    </details>
  </div>
  <div class="prompt-card-footer">
    <a href="{post_link(p,1)}">\U0001f449 查看完整解答</a>
  </div>
</div>""")

    html = f"""# \U0001f4cb AI不翻车 Skill 库

> 每个 Skill 都是一个可复用的 AI 解决方案，包含场景、指令、约束和检查清单。

<div class="prompt-grid">
{"".join(cards)}
</div>

---

*共 {len(cards)} 个 Skill · 更新于 {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*
"""
    write(DOCS_DIR / "prompts" / "index.md", html)
    print(f"build-prompts: {len(cards)} skills")


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
    build_prompts(published)
    print("build-pages complete")
