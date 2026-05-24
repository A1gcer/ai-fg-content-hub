#!/bin/bash
# sync.sh — 构建 + 提交 + 推送
set -e

bash scripts/build.sh

if ! git diff --quiet || ! git diff --cached --quiet; then
  MSG="${1:-chore: sync AI-FG $(date +%Y-%m-%d)}"
  git add -A
  git commit -m "$MSG"
  git push
  echo "Pushed."
else
  echo "No changes."
fi
