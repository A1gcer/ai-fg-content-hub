#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_draft_saved.py — 校验 draft_saved 状态与字段一致性

规则:
- status=draft_saved 时必须有 draft_path
- status=published 时必须有合法 url
- status=draft_saved 时不应已有 url（警告）
- 非法状态值报错

用法: python3 scripts/validate_draft_saved.py <feishu_export.csv> [repo_root]
"""

import csv
import re
import sys
from pathlib import Path

# 按飞书导出列名修改这里
COL = {
    "content_id": "content_id",
    "platform_status": "xiaohongshu_status",
    "draft_path": "xiaohongshu_draft_path",
    "url": "xiaohongshu_url",
    "error": "xiaohongshu_error"
}

ALLOWED_STATUS = {
    "pending", "drafted", "review_passed", "queued",
    "publishing", "draft_saved", "published", "failed", "archived"
}

def is_url(x: str) -> bool:
    return bool(re.match(r"^https?://", (x or "").strip()))

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/validate_draft_saved.py <feishu_export.csv> [repo_root]")
        sys.exit(1)

    csv_path = Path(sys.argv[1]).resolve()
    repo_root = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else Path.cwd()

    if not csv_path.exists():
        print(f"❌ CSV 不存在: {csv_path}")
        sys.exit(1)

    errors = []
    warns = []
    total = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            cid = (row.get(COL["content_id"]) or "").strip()
            st = (row.get(COL["platform_status"]) or "").strip()
            draft_path = (row.get(COL["draft_path"]) or "").strip()
            url = (row.get(COL["url"]) or "").strip()

            row_tag = f"[row={total}, content_id={cid or '-'}]"

            if st and st not in ALLOWED_STATUS:
                errors.append(f"{row_tag} 非法状态: {st}")

            # 规则1：draft_saved 必须有 draft_path
            if st == "draft_saved":
                if not draft_path:
                    errors.append(f"{row_tag} status=draft_saved 但 draft_path 为空")
                else:
                    p = (repo_root / draft_path).resolve()
                    if not p.exists():
                        warns.append(f"{row_tag} draft_path 不存在: {draft_path}")

                # draft_saved 不应已有最终发布 URL
                if url:
                    warns.append(f"{row_tag} status=draft_saved 但已有 url，建议确认是否应改为 published")

            # 规则2：published 必须有合法 url
            if st == "published":
                if not url:
                    errors.append(f"{row_tag} status=published 但 url 为空")
                elif not is_url(url):
                    errors.append(f"{row_tag} status=published 但 url 非法: {url}")

            # 规则3：failed 建议有 error
            if st == "failed":
                err = (row.get(COL["error"]) or "").strip()
                if not err:
                    warns.append(f"{row_tag} status=failed 但 error 为空（建议补充）")

    if warns:
        print("\n⚠️ 警告:")
        for w in warns:
            print(" -", w)

    if errors:
        print("\n❌ 校验失败:")
        for e in errors:
            print(" -", e)
        print(f"\n结果: failed, total={total}, errors={len(errors)}, warns={len(warns)}")
        sys.exit(1)

    print(f"\n✅ 校验通过: total={total}, errors=0, warns={len(warns)}")

if __name__ == "__main__":
    main()
