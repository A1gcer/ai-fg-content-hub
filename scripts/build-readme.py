#!/usr/bin/env python3
"""build-readme.py — 从 data/index.json 更新 README.md（含全网同步看板）"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
INDEX = ROOT / "data" / "index.json"
DIST = ROOT / "data" / "distribution.json"

def replace_block(text, start_tag, end_tag, new_inner):
    pattern = re.compile(re.escape(start_tag) + r".*?" + re.escape(end_tag), re.DOTALL)
    block = f"{start_tag}\n{new_inner}\n{end_tag}"
    return pattern.sub(block, text)

def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def build_meta_block(meta):
    return "\n".join([
        "| 指标 | 数值 |",
        "|---|---|",
        f"| 📝 总文章 | {meta.get('total', 0)} |",
        f"| ✅ 已发布 | {meta.get('published', 0)} |",
        f"| 📄 草稿 | {meta.get('draft', 0)} |",
        f"| 🗂 归档 | {meta.get('archived', 0)} |",
        f"| 📂 分类 | {meta.get('categories', 0)} |",
        f"| 🏷 标签 | {meta.get('tags', 0)} |",
    ])

def build_latest_table(posts):
    posts = sorted(posts, key=lambda x: x.get("date", ""), reverse=True)[:10]
    lines = [
        "| Date | Title | Category | Tags | Risk | Status |",
        "|---|---|---|---|---|---|"
    ]
    for p in posts:
        title = (p.get("title", "") or "").replace("|", " ")
        tags = ", ".join((p.get("tags") or [])[:3])
        path = p.get("path", "")
        lines.append(
            f"| {p.get('date','')} | [{title}](./{path}) "
            f"| {p.get('category','')} | {tags} | {p.get('risk','')} | {p.get('status','')} |"
        )
    return "\n".join(lines)

def build_sync_block(dist):
    if not dist:
        return "\n".join([
            "| 平台 | 已发布 | 待发布 | 草稿 | 回链完整率(已发) |",
            "|---|---:|---:|---:|---:|",
            "| 知乎 | 0 | 0 | 0 | 0% |",
            "| 公众号 | 0 | 0 | 0 | 0% |",
            "| 掘金 | 0 | 0 | 0 | 0% |",
        ])

    p = dist.get("platforms", {})

    def row(name, key):
        x = p.get(key, {})
        return (
            f"| {name} | {x.get('published', 0)} | {x.get('pending', 0)} "
            f"| {x.get('drafted', 0)} | {x.get('published_with_url_rate', 0)}% |"
        )

    return "\n".join([
        "| 平台 | 已发布 | 待发布 | 草稿 | 回链完整率(已发) |",
        "|---|---:|---:|---:|---:|",
        row("📕 知乎", "zhihu"),
        row("📘 公众号", "wechat"),
        row("📗 掘金", "juejin"),
    ])

def main():
    if not README.exists():
        raise SystemExit("README.md not found")
    idx = load_json(INDEX)
    if not idx:
        raise SystemExit("data/index.json not found")

    dist = load_json(DIST)

    raw = README.read_text(encoding="utf-8")
    meta_block = build_meta_block(idx["meta"])
    table_block = build_latest_table(idx["posts"])
    sync_block = build_sync_block(dist)

    raw = replace_block(raw, "<!-- AIFG_META_START -->", "<!-- AIFG_META_END -->", meta_block)
    raw = replace_block(raw, "<!-- AIFG_POSTS_START -->", "<!-- AIFG_POSTS_END -->", table_block)
    raw = replace_block(raw, "<!-- AIFG_SYNC_START -->", "<!-- AIFG_SYNC_END -->", sync_block)
    raw = re.sub(r"\*自动更新 · 最后更新: .*?\*", f"*自动更新 · 最后更新: {idx['meta'].get('updated', '-')}*", raw)
    README.write_text(raw, encoding="utf-8")
    print("build-readme complete")

if __name__ == "__main__":
    main()
