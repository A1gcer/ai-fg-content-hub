#!/usr/bin/env python3
"""build-llms.py — 生成 llms.txt / llms-full.txt"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"

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

    # llms.txt (brief)
    brief = [
        "# AI-FG: AI delivery safety & quality knowledge base",
        "",
        "> Essential docs & guides for turning AI output into deliverable work.",
        "",
        "## Core",
        "",
    ]
    for p in published[:5]:
        brief.append(f"- [{p['title']}](https://a1gcer.github.io/ai-fg-content-hub/{p['url_path']})")
    brief.append("")
    (DOCS_DIR / "llms.txt").write_text("\n".join(brief), encoding="utf-8")

    # llms-full.txt
    full = [
        "# AI-FG: Full content",
        "",
        "This document contains all published AI-FG content for LLM consumption.",
        "",
    ]
    for p in published:
        full.append(f"## {p['title']}")
        full.append(f"URL: https://a1gcer.github.io/ai-fg-content-hub/{p['url_path']}")
        if p.get("summary"):
            full.append(f"Summary: {p['summary']}")
        if p.get("body"):
            full.append("")
            full.append(p["body"])
        full.append("---\n")
    (DOCS_DIR / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")

    print(f"build-llms complete: {len(published)} published docs")

if __name__ == "__main__":
    main()
