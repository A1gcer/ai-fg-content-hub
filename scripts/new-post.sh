#!/bin/bash
# new-post.sh — 新文章脚手架
set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONTENT_DIR="$REPO_DIR/content"

if [ $# -lt 1 ]; then
  echo "Usage: ./scripts/new-post.sh \"Title\" [category]"
  exit 1
fi

TITLE="$1"
CATEGORY="${2:-AI基础避坑}"

TODAY=$(date +%Y-%m-%d)
YEAR=$(date +%Y)
MONTH=$(date +%m)

mkdir -p "$CONTENT_DIR/$YEAR/$MONTH"
EXISTING=$(ls "$CONTENT_DIR/$YEAR/$MONTH/"*.md 2>/dev/null | wc -l | tr -d ' ')
NEXT=$((EXISTING + 1))
NUM=$(printf "%03d" $NEXT)

SLUG=$(echo "$TITLE" | sed 's/[^a-zA-Z0-9\u4e00-\u9fff]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | tr '[:upper:]' '[:lower:]')
FILE="$CONTENT_DIR/$YEAR/$MONTH/${TODAY}-${NUM}-${SLUG}.md"

cat > "$FILE" << EOF
---
id: ${TODAY}-$(printf "%03d" $NEXT)
title: "${TITLE}"
slug: "${SLUG}"
date: ${TODAY}
updated: ${TODAY}
category: ${CATEGORY}
tags: []
risk: 中
channel: github
status: draft
summary: ""
question: ""
answer: ""
audience: ""
scenario: ""
review_required: true
canonical_url: ""
license: "CC BY-NC-SA 4.0"
---

# ${TITLE}

## 一句话答案


## 适用场景


## 为什么会这样


## 怎么做


## 检查清单


## 结论
EOF

echo "Created: $FILE"
