# AI不翻车FAQ · 内容看板

> 我不教你玩AI，我教你用AI做出能交差的东西。
>
> — AI防翻车教练

---

## 📊 数据看板

<!-- AIFG_META_START -->
| 指标 | 数值 |
|------|------|
| 📝 总文章 | — |
| ✅ 已发布 | — |
| 📄 草稿 | — |
| 📂 分类 | — |
<!-- AIFG_META_END -->

*自动更新 · 最后更新: —*

---

## 📝 最近内容

<!-- AIFG_TABLE_START -->
| Date | Title | Category | Tags | Risk | Status |
|------|-------|----------|------|------|--------|
<!-- AIFG_TABLE_END -->

---

## 🔍 快速入口

| 入口 | 链接 | 用途 |
|------|------|------|
| 📖 阅读站 | [GitHub Pages](https://a1gcer.github.io/ai-fg-content) | 对外展示、分类检索 |
| 📂 分类浏览 | [categories/](docs/categories/) | 按8大类归档 |
| 🏷️ 标签聚合 | [tags/](data/tags.json) | 按标签交叉检索 |
| 📅 时间线 | [timeline/](data/timeline.json) | 按日期回顾 |
| ⚠️ 风险等级 | [risk/](data/by-risk.json) | 按风险筛选内容 |

---

## 🚀 使用方式

```bash
# 本地构建
bash scripts/build.sh

# 构建 + 同步到 GitHub
bash scripts/sync.sh "chore: 5/24 内容更新"
```

---

## 📂 目录结构

```
ai-fg-content/
├── content/              # 原始内容（唯一真相源）
│   └── YYYY/MM/          # 按日期归档
├── data/                 # 自动生成的索引（JSON）
├── docs/                 # GitHub Pages 目录
├── templates/            # 内容模板
├── scripts/              # 自动化脚本
│   ├── build.sh          # 全量构建
│   ├── sync.sh           # 构建+推送
│   ├── new-post.sh       # 新文章脚手架
│   ├── build-index.py    # 索引生成器
│   └── build-pages.py    # 页面生成器
├── .github/workflows/    # CI/CD
│   ├── ci.yml            # 代码质量校验
│   └── pages.yml         # Pages 自动部署
├── mkdocs.yml            # MkDocs 配置
├── README.md             # ← 你在这里
└── CHANGELOG.md
```

---

## 🏷️ 八大分类

1. [基础避坑](content/2026/05/) · 认知纠偏
2. 职场交付 · 输出质量
3. AI品控检查 · 质检方法论
4. AI办公自动化 · 效率工具
5. 安全与不背锅 · 红线
6. 工具选择 · 选型指南
7. AI工作流 · SOP设计
8. 真实案例拆解 · 复现分析

---

## 🧭 双入口方案

- **GitHub 仓库** (这里) → 内容看板 + 版本管理 + 协作
- **GitHub Pages** ([阅读站](https://a1gcer.github.io/ai-fg-content)) → 分类检索 + 全文搜索 + 对外展示

---

## 📜 许可

内容采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可。
