#!/bin/bash
# ============================================================
# 安装 AI-FG Git Preflight Hook
# 将物理门注册为 git pre-commit hook
# ============================================================

echo "=== 安装 AI-FG Git Preflight Hooks ==="

# 公共仓
if [ -d "/home/node/.openclaw/workspace/ai-fg-github" ]; then
  HOOK="/home/node/.openclaw/workspace/ai-fg-github/.git/hooks/pre-commit"
  cat > "$HOOK" << 'HOOK'
#!/bin/bash
# AI-FG Preflight Gate - 自动注册
bash gates/git-preflight.sh
if [ $? -ne 0 ]; then
  echo "⛔ 提交被 git-preflight 拦截，请先修复违规内容"
  exit 1
fi
HOOK
  chmod +x "$HOOK"
  echo "✅ 公共仓 pre-commit hook 已安装"
fi

# 私仓
if [ -d "/home/node/.openclaw/workspace/ai-fg-private-ops" ]; then
  HOOK="/home/node/.openclaw/workspace/ai-fg-private-ops/.git/hooks/pre-commit"
  cat > "$HOOK" << 'HOOK'
#!/bin/bash
# AI-FG Private Ops Preflight Gate - 自动注册
bash gates/git-preflight.sh
if [ $? -ne 0 ]; then
  echo "⛔ 提交被 git-preflight 拦截"
  exit 1
fi
HOOK
  chmod +x "$HOOK"
  echo "✅ 私仓 pre-commit hook 已安装"
fi

echo ""
echo "=== 完成 ==="
echo "之后每次 git commit 都会自动触发内容合规检查"
echo "可通过 git commit --no-verify 跳过（不推荐）"
