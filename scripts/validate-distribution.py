#!/usr/bin/env python3
"""validate-distribution.py — 校验 content/ 内文章的分发字段"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

PLATFORMS = ["zhihu", "wechat", "juejin"]
ALLOWED_SYNC = {"pending", "drafted", "published", "archived"}

def s(v):
    return "" if v is None else str(v)

def parse_md(fpath: Path):
    text = fpath.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return None
    return yaml.safe_load(m.group(1)) or {}

def is_post(rel: Path):
    parts = rel.parts
    return (len(parts) >= 4 and parts[0] == "content"
            and re.match(r"^\d{4}$", parts[1]) and re.match(r"^\d{2}$", parts[2]))

def is_valid_url(url: str):
    if url == "":
        return True
    return bool(re.match(r"^https?://", url))

def main():
    errors = []

    for f in sorted(CONTENT_DIR.rglob("*.md")):
        rel = f.relative_to(ROOT)
        if not is_post(rel):
            continue

        meta = parse_md(f)
        if meta is None:
            continue

        sync = meta.get("sync", None)
        urls = meta.get("urls", None)

        if not isinstance(sync, dict):
            errors.append(f"[{rel}] missing or invalid 'sync' (dict required)")
            continue
        if not isinstance(urls, dict):
            errors.append(f"[{rel}] missing or invalid 'urls' (dict required)")
            continue

        for p in PLATFORMS:
            if p not in sync:
                errors.append(f"[{rel}] sync.{p} missing")
            if p not in urls:
                errors.append(f"[{rel}] urls.{p} missing")

        for p in PLATFORMS:
            st = s(sync.get(p))
            url = s(urls.get(p))

            if st not in ALLOWED_SYNC:
                errors.append(f"[{rel}] sync.{p} invalid value: {st}")

            if not is_valid_url(url):
                errors.append(f"[{rel}] urls.{p} invalid url: {url}")

            if st == "published" and url == "":
                errors.append(f"[{rel}] sync.{p}=published but urls.{p} is empty")

        _id = s(meta.get("id"))
        date = s(meta.get("date"))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            errors.append(f"[{rel}] missing or invalid date")
        dd = s(meta.get("distribution_date", ""))
        if dd and not re.match(r"^\d{4}-\d{2}-\d{2}$", dd):
            errors.append(f"[{rel}] invalid distribution_date: {dd}")

    if errors:
        print("❌ Distribution validation failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("✅ Distribution fields valid")

if __name__ == "__main__":
    main()
