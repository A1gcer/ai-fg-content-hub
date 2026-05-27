# AI不翻车FAQ / AI-FG

> 面向职场人的 AI 交付安全与质量控制知识库。
> 不教你玩 AI，教你用 AI 做出能交差的东西。

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-online-brightgreen)](https://a1gcer.github.io/ai-fg-content-hub/)
[![Build](https://github.com/A1gcer/ai-fg-content-hub/actions/workflows/pages.yml/badge.svg)](https://github.com/A1gcer/ai-fg-content-hub/actions)
[![Content License: CC BY-NC-SA 4.0](https://img.shields.io/badge/content-CC%20BY--NC--SA%204.0-lightgrey)](./LICENSE)
[![Code License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](./LICENSE)

---

## 这个项目解决什么问题？

很多人用 AI 之后不是更快，而是：
- 复制了错误答案
- 产出空泛内容
- 泄露公司信息
- 把 AI 初稿当终稿
- 看似省时间，实际返工更多

AI-FG 目标：提供可复用的 FAQ、检查清单、提示词模板和工作流，帮助你把 AI 产出变成交付成果。

## 适合谁？

- 职场新人 / 知识工作者
- 运营、产品、市场、HR、销售
- 小团队负责人
- 想把 AI 用到真实工作交付的人

## 快速入口

- 📖 站点首页：https://a1gcer.github.io/ai-fg-content-hub/
- 🧭 分类浏览：`/categories/`
- 🏷 标签浏览：`/tags/`
- ⚠ 风险分级：`/risk/`
- 📅 时间线：`/timeline/`

---

## 数据看板

<!-- AIFG_META_START -->
| 指标 | 数值 |
|---|---|
| 📝 总文章 | 17 |
| ✅ 已发布 | 17 |
| 📄 草稿 | 0 |
| 🗂 归档 | 0 |
| 📂 分类 | 6 |
| 🏷 标签 | 44 |
<!-- AIFG_META_END -->

*自动更新 · 最后更新: 2026-05-27T00:48:19.707145Z*

---

## 内容源说明

本仓库是「AI不翻车FAQ / AI-FG」的公开知识库和 canonical 内容源。

- 正式内容：`content/`
- 公开站点：[GitHub Pages](https://a1gcer.github.io/ai-fg-content-hub/)
- GEO 文件：`llms.txt`、`llms-full.txt`、`sitemap.xml`
- 平台分发稿：由私有运营仓库 `ai-fg-private-ops` 生成，不在本仓库维护
- 外部分发链接：见 `data/publications.json`

---

---

## 最新内容

<!-- AIFG_POSTS_START -->
| Date | Title | Category | Tags | Risk | Status |
|---|---|---|---|---|---|
| 2026-05-30 | [为什么不建议直接复制AI答案？](./content/2026/05/2026-05-30-007-no-copy.md) | AI品控检查 | AI使用, 交付质量, 职场习惯 | 高 | published |
| 2026-05-29 | [AI到底适合做初稿还是终稿？](./content/2026/05/2026-05-29-006-draft-vs-final.md) | 职场交付 | AI工作流, 效率, 产出质量 | 中 | published |
| 2026-05-28 | [哪些事情不能直接交给AI？](./content/2026/05/2026-05-28-005-dont-ai.md) | 安全与不背锅 | AI安全, 数据隐私, 职场红线 | 高 | published |
| 2026-05-27 | [为什么AI回答越流畅越容易让人误判？](./content/2026/05/2026-05-27-004-fluent-scam.md) | 安全与不背锅 | AI风险, 批判思维, 信息验证 | 高 | published |
| 2026-05-27 | [AI 突然挂了怎么办？一个真实的应急预案](./content/2026/05/2026-05-27-009-ai-outage-plan.md) | AI基础避坑 | 预案, 备份, AI故障 | 高 | published |
| 2026-05-26 | [AI写的东西为什么总是很空？](./content/2026/05/2026-05-26-003-vague.md) | AI品控检查 | AI指令, 提示词, 内容质量 | 中 | published |
| 2026-05-26 | [把Excel直接丢给AI分析，我踩过的坑](./content/2026/05/2026-05-26-008-excel-give-to-ai-analysis.md) | AI办公自动化 | Excel, AI分析, 数据处理 | 中 | published |
| 2026-05-26 | [AI 生成内容交付前检查清单](./content/checklists/ai-output-quality-checklist.md) | AI品控检查 | 检查清单, 交付质量, 人工复核 | 中 | published |
| 2026-05-26 | [AI 敏感信息红线清单](./content/checklists/ai-privacy-risk-checklist.md) | 安全与不背锅 | 隐私, 安全, 红线 | 高 | published |
| 2026-05-26 | [术语：AI交付](./content/glossary/ai-delivery.md) | 职场交付 | 术语, AI交付 | 中 | published |
<!-- AIFG_POSTS_END -->

---

## 内容地图（8 大分类）

1. AI基础避坑
2. 职场交付
3. AI品控检查
4. AI办公自动化
5. 安全与不背锅
6. 工具选择
7. AI工作流
8. 真实案例拆解

---

## 本地运行

```bash
pip install pyyaml mkdocs-material
bash scripts/build.sh
mkdocs serve
```

## 贡献方式

见 [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

- Code: MIT
- Content: CC BY-NC-SA 4.0

详见 [LICENSE](./LICENSE)
