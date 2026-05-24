#!/usr/bin/env python3
"""backfill_urls_from_feishu_export.py
从飞书导出 CSV 回填 content/*.md 的 sync/urls/distribution_date frontmatter
用法: python3 scripts/backfill_urls_from_feishu_export.py ./feishu_export.csv
"""

import csv
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

PLATFORMS = ["zhihu", "wechat", "juejin", "xiaohongshu"]

# CSV列名映射（按飞书导出列名调整）
CSV_COL_MAP = {
    "content_id": "content_id",
    "zhihu_url": "zhihu_url",
    "wechat_url": "wechat_url",
    "juejin_url": "juejin_url",
    "xiaohongshu_url": "xiaohongshu_url"
}

def parse_md(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return None, text
    meta = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return meta, body

def dump_md(path: Path, meta: dict, body: str):
    fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip()
    content = f"---\n{fm}\n---\n\n{body.lstrip()}"
    path.write_text(content, encoding="utf-8")

def load_csv(csv_path: Path):
    rows = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cid = (r.get(CSV_COL_MAP["content_id"]) or "").strip()
            if not cid:
                continue
            rows[cid] = {
                "zhihu": (r.get(CSV_COL_MAP["zhihu_url"]) or "").strip(),
                "wechat": (r.get(CSV_COL_MAP["wechat_url"]) or "").strip(),
                "juejin": (r.get(CSV_COL_MAP["juejin_url"]) or "").strip(),
                "xiaohongshu": (r.get(CSV_COL_MAP["xiaohongshu_url"]) or "").strip()
            }
    return rows

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/backfill_urls_from_feishu_export.py <csv_path>")
        sys.exit(1)

    csv_path = Path(sys.argv[1]).resolve()
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        sys.exit(1)

    data = load_csv(csv_path)
    if not data:
        print("No valid rows in CSV")
        sys.exit(1)

    updated = 0
    matched = 0

    for md in CONTENT_DIR.rglob("*.md"):
        meta, body = parse_md(md)
        if meta is None:
            continue

        cid = str(meta.get("id", "")).strip()
        if not cid or cid not in data:
            continue

        matched += 1
        urls = data[cid]

        if not isinstance(meta.get("sync"), dict):
            meta["sync"] = {}
        if not isinstance(meta.get("urls"), dict):
            meta["urls"] = {}

        changed = False
        any_published = False

        for p in PLATFORMS:
            old_url = str(meta["urls"].get(p, "") or "").strip()
            new_url = urls.get(p, "").strip()

            if new_url and new_url != old_url:
                meta["urls"][p] = new_url
                meta["sync"][p] = "published"
                changed = True
                any_published = True
            else:
                if p not in meta["sync"]:
                    meta["sync"][p] = "pending"
                    changed = True
                if p not in meta["urls"]:
                    meta["urls"][p] = old_url if old_url else ""
                    changed = True
                if meta["sync"].get(p) == "published":
                    any_published = True

        if any_published and not meta.get("distribution_date"):
            meta["distribution_date"] = datetime.utcnow().strftime("%Y-%m-%d")
            changed = True

        if changed:
            dump_md(md, meta, body)
            updated += 1
            print(f"Updated: {md.relative_to(ROOT)}")

    print(f"\nDone. matched={matched}, updated={updated}")

if __name__ == "__main__":
    main()
