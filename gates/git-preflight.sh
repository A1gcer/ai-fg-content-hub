#!/bin/bash
# ============================================================
# AI-FG Git Preflight Gate - 提交前内容合规检查
# 自进化引擎物理门 v1.0
# ============================================================
# 使用方法：提交前手动跑，或在 .git/hooks/pre-commit 中调用
#   bash gates/git-preflight.sh
# ============================================================

set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

REPO_URL=$(git remote get-url origin 2>/dev/null || echo "unknown")
REPO_NAME=$(basename -s .git "$REPO_URL" 2>/dev/null || echo "unknown")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

echo ""
echo "============================================"
echo "🔍 AI-FG Git Preflight Gate"
echo "============================================"
echo "仓库: $REPO_NAME"
echo "分支: $BRANCH"
echo ""

# ---- 规则 1: 识别当前仓库类型 ----
if echo "$REPO_URL" | grep -qi "ai-fg-content-hub"; then
  REPO_TYPE="public"
  echo "✅ 当前是公共仓: ai-fg-content-hub"
elif echo "$REPO_URL" | grep -qi "ai-fg-private-ops"; then
  REPO_TYPE="private"
  echo "✅ 当前是私仓: ai-fg-private-ops"
else
  REPO_TYPE="unknown"
  echo -e "${YELLOW}⚠️  无法识别仓库类型，跳过内容检查${NC}"
fi

# ---- 规则 2: 检查暂存区文件 ----
STAGED=$(git diff --cached --name-only 2>/dev/null || echo "")

if [ -z "$STAGED" ]; then
  # 没有暂存文件，检查是否有未暂存的修改
  UNSTAGED=$(git status --short 2>/dev/null || echo "")
  if [ -z "$UNSTAGED" ]; then
    echo -e "${YELLOW}⚠️  没有检测到任何文件变更${NC}"
    exit 0
  else
    echo -e "${YELLOW}⚠️  有未暂存的文件变更，使用 --all 检查全部变更${NC}"
    STAGED=$(git status --porcelain 2>/dev/null | awk '{print $2}')
  fi
fi

echo "检查文件数: $(echo "$STAGED" | wc -l)"
echo ""

HAS_ERRORS=0

# ---- 公共仓红线检查 ----
if [ "$REPO_TYPE" = "public" ]; then

  # 红线 1: distribution/ 不得出现在公共仓
  if echo "$STAGED" | grep -q "^distribution/"; then
    echo -e "${RED}❌ [致命] 公共仓禁止包含 distribution/ 文件！${NC}"
    echo "   这些文件属于私仓 ai-fg-private-ops"
    echo "   提交文件:"
    echo "$STAGED" | grep "^distribution/" | sed 's/^/      /'
    HAS_ERRORS=1
  fi

  # 红线 2: config/feishu_field_map.json 不得在公共仓
  if echo "$STAGED" | grep -q "^config/feishu_field_map\.json$"; then
    echo -e "${RED}❌ [致命] 公共仓禁止包含 feishu_field_map.json！${NC}"
    echo "   真实配置属于私仓 ai-fg-private-ops"
    HAS_ERRORS=1
  fi

  # 红线 3: 私仓脚本不得在公共仓
  PRIVATE_SCRIPTS="build-distribution.py|build-distribution-index.py|validate-distribution.py|validate_draft_saved.py|fix_draft_saved_to_published_all.py|backfill_urls_from_feishu_export.py"
  if echo "$STAGED" | grep -E "^scripts/($PRIVATE_SCRIPTS)$"; then
    echo -e "${RED}❌ [致命] 公共仓禁止包含分发/回填脚本！${NC}"
    echo "   这些脚本属于私仓 ai-fg-private-ops"
    echo "$STAGED" | grep -E "^scripts/($PRIVATE_SCRIPTS)" | sed 's/^/      /'
    HAS_ERRORS=1
  fi

  # 红线 4: distribution-ci workflow
  if echo "$STAGED" | grep -q "\.github/workflows/distribution-ci\.yml"; then
    echo -e "${RED}❌ [致命] 公共仓禁止包含 distribution-ci.yml！${NC}"
    HAS_ERRORS=1
  fi

  # 红线 5: 私仓目录结构
  PRIVATE_DIRS="drafts/|analytics/|feishu/"
  if echo "$STAGED" | grep -E "^($PRIVATE_DIRS)"; then
    echo -e "${RED}❌ [致命] 公共仓禁止包含私仓目录！${NC}"
    echo "$STAGED" | grep -E "^($PRIVATE_DIRS)" | sed 's/^/      /'
    HAS_ERRORS=1
  fi

  # 红线 6: .env / *.csv / *.xlsx
  if echo "$STAGED" | grep -qE "\.env$|\.csv$|\.xlsx$"; then
    echo -e "${RED}❌ [致命] 公共仓禁止包含配置文件或数据文件！${NC}"
    echo "$STAGED" | grep -E "\.env$|\.csv$|\.xlsx$" | sed 's/^/      /'
    HAS_ERRORS=1
  fi

  # 红线 7: check content/ 没有草稿状态
  CONTENT_FILES=$(echo "$STAGED" | grep "^content/" || true)
  if [ -n "$CONTENT_FILES" ]; then
    for f in $CONTENT_FILES; do
      if [ -f "$f" ]; then
        STATUS=$(grep -E "^status:" "$f" 2>/dev/null | head -1 | awk '{print $2}')
        if [ "$STATUS" = "draft" ] || [ "$STATUS" = "pending" ] || [ -z "$STATUS" ]; then
          echo -e "${RED}❌ [警告] 内容文件状态不是 published：${NC}"
          echo "   $f → status: ${STATUS:-未设置}"
          echo -e "${YELLOW}   公共仓只允许 status: published 的内容${NC}"
          HAS_ERRORS=1
        fi
      fi
    done
  fi
fi

# ---- 私仓警告（不拦截，仅提示） ----
if [ "$REPO_TYPE" = "private" ]; then
  # 检查是否有敏感文件要提交
  if echo "$STAGED" | grep -qE "\.env$"; then
    echo -e "${YELLOW}⚠️  注意：你在提交 .env 文件到私仓${NC}"
    echo "   确认不是带真实密钥的 .env"
  fi

  if echo "$STAGED" | grep -q "\.csv$"; then
    echo -e "${YELLOW}ℹ️   注意：CSV 文件将被提交到私仓${NC}"
  fi
fi

# ---- 检查 commit message 格式 ----
COMMIT_MSG_FILE=".git/COMMIT_EDITMSG"
if [ -f "$COMMIT_MSG_FILE" ]; then
  COMMIT_MSG=$(head -1 "$COMMIT_MSG_FILE" 2>/dev/null || echo "")
  if echo "$COMMIT_MSG" | grep -qiE "^fixup!|^wip|^tmp|^test"; then
    echo -e "${YELLOW}⚠️  Commit message 是临时性前缀 (fixup!/wip/tmp)${NC}"
    echo "   确认真的想 commit 吗？"
  fi
fi

echo ""
echo "============================================"

if [ "$HAS_ERRORS" -eq 1 ]; then
  echo -e "${RED}❌ GIT PREFLIGHT 未通过 — 拦截提交${NC}"
  echo ""
  echo "处理方法："
  echo "  1. 把违规文件移到正确的仓库"
  echo "  2. 使用 git reset HEAD <文件> 取消暂存"
  echo "  3. 修复后重新提交"
  echo ""
  echo "  如果是误报，用 --no-verify 跳过（不推荐）"
  echo "============================================"
  exit 1
else
  echo -e "${GREEN}✅ GIT PREFLIGHT 通过${NC}"
  echo "============================================"
  exit 0
fi
