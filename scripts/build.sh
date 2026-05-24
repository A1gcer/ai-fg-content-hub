#!/bin/bash
# 全量构建：索引 + 页面 + README
# 用法: ./scripts/build.sh

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

echo "🔨 AIFG Build Starting..."
echo ""

# Step 1: Build data indexes
echo "📊 Step 1/3: Building data indexes..."
python3 scripts/build-index.py

# Step 2: Build pages
echo ""
echo "📄 Step 2/3: Building pages..."
python3 scripts/build-pages.py

# Step 3: Generate README
echo ""
echo "📖 Step 3/3: Updating README..."

# Read build metadata
if [ -f "data/readme-meta.json" ]; then
  TOTAL=$(python3 -c "import json; d=json.load(open('data/readme-meta.json')); print(d['total'])")
  PUB=$(python3 -c "import json; d=json.load(open('data/readme-meta.json')); print(d['published'])")
  DRAFT=$(python3 -c "import json; d=json.load(open('data/readme-meta.json')); print(d['draft'])")
  CATS=$(python3 -c "import json; d=json.load(open('data/readme-meta.json')); print(d['categories'])")
  TABLE=$(python3 -c "import json; print(json.load(open('data/readme-meta.json'))['table'])")
  
  echo "📊 $TOTAL posts · $PUB published · $DRAFT drafts · $CATS categories"
  echo ""
fi

echo ""
echo "✅ Build complete!"
echo "   - data/index.json"
echo "   - data/tags.json"
echo "   - data/timeline.json"
echo "   - data/by-risk.json"
echo "   - docs/ (pages)"
echo ""
echo "📌 Next: git add, commit, push"
