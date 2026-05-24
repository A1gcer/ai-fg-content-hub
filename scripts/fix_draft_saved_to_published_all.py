#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_draft_saved_to_published_all.py — 四平台批量修复

规则：某平台 *_status == draft_saved 且 *_url 是合法链接，
则自动改为 published，并补 *_publish_time（若为空）。

用法: python3 scripts/fix_draft_saved_to_published_all.py <input.csv> [output.csv]
"""

import csv
import re
import sys
from pathlib import Path
from datetime import datetime

PLATFORMS = ["zhihu", "wechat", "juejin", "xiaohongshu"]

COL_MAP = {
    "zhihu": {
        "status": "zhihu_status",
        "url": "zhihu_url",
        "publish_time": "zhihu_publish_time",
    },
    "wechat": {
        "status": "wechat_status",
        "url": "wechat_url",
        "publish_time": "wechat_publish_time",
    },
    "juejin": {
        "status": "juejin_status",
        "url": "juejin_url",
        "publish_time": "juejin_publish_time",
    },
    "xiaohongshu": {
        "status": "xiaohongshu_status",
        "url": "xiaohongshu_url",
        "publish_time": "xiaohongshu_publish_time",
    },
}

def is_url(x: str) -> bool:
    return bool(re.match(r"^https?://", (x or "").strip()))

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/fix_draft_saved_to_published_all.py <input.csv> [output.csv]")
        sys.exit(1)

    in_csv = Path(sys.argv[1]).resolve()
    out_csv = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else in_csv.with_name(in_csv.stem + ".fixed.csv")

    if not in_csv.exists():
        print(f"❌ 文件不存在: {in_csv}")
        sys.exit(1)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_rows = 0
    changed_rows = 0
    changed_cells = 0
    per_platform_changed = {p: 0 for p in PLATFORMS}

    with in_csv.open("r", encoding="utf-8-sig", newline="") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames or []

        for p in PLATFORMS:
            pt_col = COL_MAP[p]["publish_time"]
            if pt_col not in fieldnames:
                fieldnames.append(pt_col)

        rows = []
        for row in reader:
            total_rows += 1
            row_changed = False

            for p in PLATFORMS:
                st_col = COL_MAP[p]["status"]
                url_col = COL_MAP[p]["url"]
                pt_col = COL_MAP[p]["publish_time"]

                st = (row.get(st_col) or "").strip()
                url = (row.get(url_col) or "").strip()

                if st == "draft_saved" and is_url(url):
                    row[st_col] = "published"
                    if not (row.get(pt_col) or "").strip():
                        row[pt_col] = now_str
                    row_changed = True
                    changed_cells += 1
                    per_platform_changed[p] += 1

            if row_changed:
                changed_rows += 1

            rows.append(row)

    with out_csv.open("w", encoding="utf-8-sig", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("✅ 修复完成")
    print(f"- 总行数: {total_rows}")
    print(f"- 变更行数: {changed_rows}")
    print(f"- 变更单元格(状态): {changed_cells}")
    print(f"- 各平台变更: {per_platform_changed}")
    print(f"- 输出文件: {out_csv}")

if __name__ == "__main__":
    main()
