#!/usr/bin/env python3
"""build-index.py — 扫描 content/，生成 data/index.json / tags.json / timeline.json / by-risk.json"""

import json
import re
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DATA_DIR = ROOT / "data"

def parse_file(fpath: Path):
    text = fpath.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text.strip()
    meta = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():].strip()
    return meta, body

def ensure_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [str(v)]

def infer_type(rel: Path):
    parts = rel.parts
    if len(parts) >= 4 and parts[0] == "content" and re.match(r"^\d{4}$", parts[1]) and re.match(r"^\d{2}$", parts[2]):
        return "post", "posts"
    if len(parts) >= 2 and parts[0] == "content":
        return "asset", parts[1]
    return "unknown", "misc"

def make_url_path(meta: dict, rel: Path):
    ctype, section = infer_type(rel)
    slug = meta.get("slug", rel.stem)
    date = str(meta.get("date", ""))
    if ctype == "post":
        yyyy = date[:4] if len(date) >= 4 else "unknown"
        mm = date[5:7] if len(date) >= 7 else "00"
        return f"posts/{yyyy}/{mm}/{slug}/"
    return f"{section}/{slug}/"

def extract_prompt(body: str) -> str:
    """从 body 中提取 ## 可复制 Prompt 区块的内容"""
    m = re.search(r"##\s*可复制\s*Prompt\s*\n+```(?:text)?\s*\n?(.*?)\n?```", body, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""


def scan():
    posts = []
    for f in sorted(CONTENT_DIR.rglob("*.md")):
        rel = f.relative_to(ROOT)
        meta, body = parse_file(f)
        if not meta:
            continue
        tags = ensure_list(meta.get("tags", []))
        ctype, section = infer_type(rel)
        item = {
            "id": str(meta.get("id", "")),
            "title": str(meta.get("title", "")),
            "slug": str(meta.get("slug", f.stem)),
            "date": str(meta.get("date", "")),
            "updated": str(meta.get("updated", meta.get("date", ""))),
            "category": str(meta.get("category", "")),
            "tags": tags,
            "risk": str(meta.get("risk", "中")),
            "channel": str(meta.get("channel", "")),
            "status": str(meta.get("status", "draft")),
            "summary": str(meta.get("summary", "")),
            "question": str(meta.get("question", "")),
            "answer": str(meta.get("answer", "")),
            "audience": str(meta.get("audience", "")),
            "scenario": str(meta.get("scenario", "")),
            "review_required": bool(meta.get("review_required", True)),
            "canonical_url": str(meta.get("canonical_url", "")),
            "license": str(meta.get("license", "CC BY-NC-SA 4.0")),
            "path": str(rel),
            "content_type": ctype,
            "section": section,
            "url_path": make_url_path(meta, rel),
            "word_count": len(re.findall(r"\S+", body)),
            "prompt": extract_prompt(body),
            "body": body,
        }
        posts.append(item)
    return posts

def build_index(items):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    meta = {
        "total": len(items),
        "published": len([x for x in items if x["status"] == "published"]),
        "draft": len([x for x in items if x["status"] == "draft"]),
        "archived": len([x for x in items if x["status"] == "archived"]),
        "categories": len(set([x["category"] for x in items if x["category"]])),
        "tags": len(set([t for x in items for t in x["tags"]])),
        "updated": datetime.utcnow().isoformat() + "Z",
    }
    out = {"meta": meta, "posts": items}
    (DATA_DIR / "index.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

def build_tags(items):
    tags = {}
    for p in items:
        for t in p["tags"]:
            tags.setdefault(t, {"tag": t, "count": 0, "posts": []})
            tags[t]["count"] += 1
            tags[t]["posts"].append(p["id"])
    arr = sorted(tags.values(), key=lambda x: (-x["count"], x["tag"]))
    (DATA_DIR / "tags.json").write_text(json.dumps(arr, ensure_ascii=False, indent=2), encoding="utf-8")

def build_timeline(items):
    timeline = {}
    for p in items:
        d = p.get("date", "")
        m = d[:7] if d else "unknown"
        timeline.setdefault(m, {"month": m, "count": 0, "posts": []})
        timeline[m]["count"] += 1
        timeline[m]["posts"].append(p["id"])
    arr = sorted(timeline.values(), key=lambda x: x["month"], reverse=True)
    (DATA_DIR / "timeline.json").write_text(json.dumps(arr, ensure_ascii=False, indent=2), encoding="utf-8")

def build_risk(items):
    risks = {}
    for p in items:
        r = p.get("risk", "中")
        risks.setdefault(r, {"risk": r, "count": 0, "posts": []})
        risks[r]["count"] += 1
        risks[r]["posts"].append(p["id"])
    arr = sorted(risks.values(), key=lambda x: -x["count"])
    (DATA_DIR / "by-risk.json").write_text(json.dumps(arr, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    items = scan()
    build_index(items)
    build_tags(items)
    build_timeline(items)
    build_risk(items)
    print(f"build-index complete: {len(items)} items")
