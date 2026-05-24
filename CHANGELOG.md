# CHANGELOG

## v2.0 (2026-05-24)

### ✨ 双入口方案升级

- **仓库** → 内容看板（README 仪表盘 + 版本管理）
- **Pages** → 阅读站（MkDocs Material + 自动化部署）

### 🏗️ 结构重组

```
ai-fg-content/
├── content/     ← 原始内容（唯一真相源）
├── data/        ← 自动生成的 JSON 索引（新增）
├── docs/        ← Pages 构建输出（新增）
├── scripts/     ← 自动化脚本（重写）
└── .github/     ← CI/CD 工作流（新增）
```

### 🆕 新增

- `scripts/build-index.py` — 自动生成 data/index.json, tags.json, timeline.json, by-risk.json
- `scripts/build-pages.py` — 从 content/ 生成 docs/ 页面
- `scripts/build.sh` — 一键构建
- `scripts/new-post.sh` — 新文章脚手架
- `scripts/sync.sh` — 构建 + commit + push 一键同步
- `.github/workflows/ci.yml` — PR 前校验 frontmatter 完整性
- `.github/workflows/pages.yml` — 自动部署 GitHub Pages
- `mkdocs.yml` — MkDocs Material 配置
- `CHANGELOG.md` — 版本变更记录

### 📝 规范升级

- 所有 content/ 文件统一标准 frontmatter（id/date/category/tags/risk/status/summary）
- README 改为动态仪表盘，含数据看板 + 最近文章表格 + 快速入口

### 🔧 移除

- `scripts/gen-index.sh` → 替代为 `scripts/build-index.py`
- `scripts/sync.sh` → 重写为完整构建+推送流程
- `templates/` → 保留但不再主动维护（由 SKILL.md 覆盖）

---

## v1.0 (2026-05-23)

初始版本：7篇基础避坑内容 + 基础同步脚本
