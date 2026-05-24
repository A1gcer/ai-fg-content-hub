#!/usr/bin/env python3
"""build-readme.py — 从 data/index.json 更新 README.md 的看板表格"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
INDEX = ROOT / "data" / "index.json"

def replace_block(text, start_tag, end_tag, new_inner):
    pattern = re.compile(re.escape(start_tag) + r".*?" + re.escape(end_tag), re.DOTALL)
    block = f"{start_tag}\n{new_inner}\n{end_tag}"
    return pattern.sub(block, text)

def main():
    if not README.exists() or not INDEX.exists():
        raise SystemExit("README or data/index.json missing")

    raw = README.read_text(encoding="utf-8")
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    meta = idx["meta"]
    posts = sorted(idx["posts"], key=lambda x: x.get("date", ""), reverse=True)[:10]

    meta_inner = "\n".join([
        "| 指标 | 数值 |",
        "|---|---|",
        f"| 📝 总文章 | {meta['total']} |",
        f"| ✅ 已发布 | {meta['published']} |",
        f"| 📄 草稿 | {meta['draft']} |",
        f"| 🗂 归档 | {meta['archived']} |",
        f"| 📂 分类 | {meta['categories']} |",
        f"| 🏷 标签 | {meta['tags']} |",
    ])

    table_lines = [
        "| Date | Title | Category | Tags | Risk | Status |",
        "|---|---|---|---|---|---|",
    ]
    for p in posts:
        title = p["title"].replace("|", " ")
        tags = ", ".join(p["tags"][:3])
        table_lines.append(
            f"| {p['date']} | [{title}](./{p['path']}) | {p['category']} | {tags} | {p['risk']} | {p['status']} |"
        )
    table_inner = "\n".join(table_lines)

    raw = replace_block(raw, "<!-- AIFG_META_START -->", "<!-- AIFG_META_END -->", meta_inner)
    raw = replace_block(raw, "<!-- AIFG_POSTS_START -->", "<!-- AIFG_POSTS_END -->", table_inner)
    raw = re.sub(r"\*自动更新 · 最后更新: .*?\*", f"*自动更新 · 最后更新: {meta['updated']}*", raw)
    README.write_text(raw, encoding="utf-8")
    print("build-readme complete")

if __name__ == "__main__":
    main()
