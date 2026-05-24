#!/bin/bash
# AIFG → GitHub 同步 (build + commit + push)
# 用法: ./scripts/sync.sh [commit-message]

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

echo "🔄 AIFG Sync Starting..."

# Step 1: Build
bash scripts/build.sh

# Step 2: Check for changes
if git diff --quiet && git diff --cached --quiet; then
  echo "ℹ️ No changes to sync"
else
  # Step 3: Commit
  DATE=$(date +%Y-%m-%d)
  MSG="${1:-chore: AIFG 内容同步 ${DATE}}"
  
  git add -A
  git commit -m "$MSG"
  
  # Step 4: Push
  echo "📤 Pushing to origin..."
  if git push; then
    echo "✅ Pushed successfully"
  else
    echo "⚠️ Push failed. Check remote and auth."
    echo "   Try: gh auth login"
    exit 1
  fi
fi

echo "✅ Sync complete"
