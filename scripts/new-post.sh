#!/bin/bash
# 新文章脚手架
# 用法: ./scripts/new-post.sh "问题标题" "分类" "渠道"

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONTENT_DIR="$REPO_DIR/content"

if [ $# -lt 1 ]; then
  echo "用法: ./scripts/new-post.sh \"标题\" [分类] [渠道]"
  echo "示例: ./scripts/new-post.sh \"怎么用AI写周报\" \"职场交付\" \"gongzhonghao\""
  exit 1
fi

TITLE="$1"
CATEGORY="${2:-基础避坑}"
CHANNEL="${3:-xiaohongshu}"

# 生成日期和序号
TODAY=$(date +%Y-%m-%d)
YEAR=$(date +%Y)
MONTH=$(date +%m)

# 计算下一序号
mkdir -p "$CONTENT_DIR/$YEAR/$MONTH"
EXISTING=$(ls "$CONTENT_DIR/$YEAR/$MONTH/"*.md 2>/dev/null | wc -l)
NEXT=$((EXISTING + 1))
NUM=$(printf "%03d" $NEXT)

SLUG=$(echo "$TITLE" | sed 's/[^a-zA-Z0-9\u4e00-\u9fff]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | tr '[:upper:]' '[:lower:]')
SLUG=$(echo "$SLUG" | sed 's/-\+/-/g')
FILENAME="${TODAY}-${NUM}-${SLUG}.md"
FILEPATH="$CONTENT_DIR/$YEAR/$MONTH/$FILENAME"

cat > "$FILEPATH" << EOF
---
id: ${TODAY}-$(printf "%03d" $NEXT)
title: "${TITLE}"
date: ${TODAY}
category: ${CATEGORY}
tags: []
risk: 中
channel: ${CHANNEL}
status: draft
summary: ""
feishu_id: ""
---

# ${TITLE}


EOF

echo "✅ 新文章已创建: $FILEPATH"
