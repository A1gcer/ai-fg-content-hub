#!/usr/bin/env python3
"""validate-content.py — content/ 内所有文件的 frontmatter 校验"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

ALLOWED_RISK = {"低", "中", "高"}
ALLOWED_STATUS = {"draft", "published", "archived"}
ALLOWED_CATEGORY = {
    "AI基础避坑", "职场交付", "AI品控检查", "AI办公自动化",
    "安全与不背锅", "工具选择", "AI工作流", "真实案例拆解",
}

REQUIRED = [
    "id", "title", "slug", "date", "updated", "category", "tags", "risk",
    "status", "summary", "question", "answer", "audience", "scenario", "review_required",
]

SENSITIVE_PATTERNS = [
    r"app_token\s*:\s*[A-Za-z0-9]{10,}",
    r"table_id\s*:\s*[A-Za-z0-9]{8,}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"sk-[A-Za-z0-9]{20,}",
]

def parse(fpath: Path):
    text = fpath.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return None, text, text
    meta = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():].strip()
    return meta, body, text

def is_date(s):
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", str(s)))

def main():
    errors = []
    ids = {}
    slugs = {}

    for f in sorted(CONTENT_DIR.rglob("*.md")):
        rel = f.relative_to(ROOT)
        meta, body, raw_text = parse(f)
        if meta is None:
            errors.append(f"[{rel}] missing frontmatter")
            continue

        for k in REQUIRED:
            if k not in meta:
                errors.append(f"[{rel}] missing field: {k}")

        _id = str(meta.get("id", "")).strip()
        slug = str(meta.get("slug", "")).strip()
        date = str(meta.get("date", "")).strip()
        updated = str(meta.get("updated", "")).strip()
        category = str(meta.get("category", "")).strip()
        risk = str(meta.get("risk", "")).strip()
        status = str(meta.get("status", "")).strip()
        summary = str(meta.get("summary", "")).strip()
        tags = meta.get("tags", [])

        if _id:
            if _id in ids:
                errors.append(f"[{rel}] duplicate id: {_id} (already used in {ids[_id]})")
            ids[_id] = str(rel)

        if slug:
            if slug in slugs:
                errors.append(f"[{rel}] duplicate slug: {slug} (already used in {slugs[slug]})")
            slugs[slug] = str(rel)

        if not is_date(date):
            errors.append(f"[{rel}] invalid date: {date}")
        if not is_date(updated):
            errors.append(f"[{rel}] invalid updated: {updated}")
        if category not in ALLOWED_CATEGORY:
            errors.append(f"[{rel}] invalid category: {category}")
        if risk not in ALLOWED_RISK:
            errors.append(f"[{rel}] invalid risk: {risk}")
        if status not in ALLOWED_STATUS:
            errors.append(f"[{rel}] invalid status: {status}")
        if not isinstance(tags, list):
            errors.append(f"[{rel}] tags must be a list")
        if len(summary) > 120:
            errors.append(f"[{rel}] summary too long (>120 chars)")
        if len(body.strip()) < 50:
            errors.append(f"[{rel}] body too short (<50 chars)")

        # 敏感信息扫描
        for pat in SENSITIVE_PATTERNS:
            if re.search(pat, raw_text):
                errors.append(f"[{rel}] possible sensitive data leak (matched: {pat})")

    if errors:
        print("❌ Validation errors:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("✅ validate-content: all clear")

if __name__ == "__main__":
    main()
