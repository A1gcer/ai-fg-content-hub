# AI-FG Content Hub — 目录概要

> **仓库:** [github.com/A1gcer/ai-fg-content-hub](https://github.com/A1gcer/ai-fg-content-hub)
> **Pages:** https://a1gcer.github.io/ai-fg-content-hub/
> **版本:** v1.3.0 | **跟踪文件:** 79 | **内容:** 15篇 | **分发包:** 28份

```
ai-fg-content-hub/
│
├── 根配置文件
│   ├── SKILL.md                  ← AI-FG 技能定义
│   ├── SKILL_DISTRIBUTION.md     ← 一源三写分发规范
│   ├── DAILY_WORKFLOW.md         ← 日更SOP
│   ├── CHANGELOG.md              ← 版本历史
│   ├── ROADMAP.md                ← 路线图
│   ├── CONTRIBUTING.md           ← 贡献指南
│   ├── SECURITY.md               ← 安全策略
│   ├── LICENSE                   ← CC BY-NC-SA 4.0 + MIT
│   ├── README.md                 ← 项目首页（含数据看板+同步看板）
│   ├── .env.example              ← 环境变量模板
│   └── mkdocs.yml                ← MkDocs 配置
│
├── content/                      ← 唯一真相源（15篇）
│   ├── 2026/05/                  ← 7篇 FAQ（全部 published）
│   │   ├── 2026-05-24-001-misuse.md          ← 普通人用AI最大的误区
│   │   ├── 2026-05-25-002-efficiency.md      ← AI效率反而没提高
│   │   ├── 2026-05-26-003-vague.md           ← AI内容为什么空泛
│   │   ├── 2026-05-27-004-fluent-scam.md     ← AI越流畅越容易误判
│   │   ├── 2026-05-28-005-dont-ai.md         ← 哪些事不能交给AI
│   │   ├── 2026-05-29-006-draft-vs-final.md  ← AI适合初稿还是终稿
│   │   └── 2026-05-30-007-no-copy.md          ← 为什么不建议复制AI答案
│   ├── checklists/
│   │   ├── ai-output-quality-checklist.md     ← 交付前检查清单
│   │   └── ai-privacy-risk-checklist.md       ← 隐私红线清单
│   ├── guides/
│   │   └── ai-hallucination-check.md          ← AI幻觉识别指南
│   ├── prompts/
│   │   └── index.md                           ← Prompt模板库
│   ├── methodology/
│   │   └── ai-fg.md                           ← AI-FG方法论
│   └── glossary/
│       ├── ai-hallucination.md                ← 术语：AI幻觉
│       ├── ai-delivery.md                     ← 术语：AI交付
│       └── human-review.md                    ← 术语：人工复核
│
├── distribution/                 ← 28份分发包（CI自动生成，人工发布）
│   ├── zhihu/2026-05/       ×7   ← 知乎风格：问答式（1000-1800字）
│   ├── wechat/2026-05/      ×7   ← 公众号风格：系列式（1200-2000字）
│   ├── juejin/2026-05/      ×7   ← 掘金风格：方法式（1500-2500字）
│   └── xiaohongshu/2026-05/ ×7   ← 小红书风格：钩子式（300-800字）
│
├── scripts/                     ← 15个脚本
│   ├── 构建链
│   │   ├── build.sh                              ← 一键全量构建
│   │   ├── build-index.py                        ← 扫描content→data/index.json
│   │   ├── build-pages.py                        ← 从data/生成docs/页面
│   │   ├── build-distribution.py                 ← 四平台分发稿生成
│   │   ├── build-distribution-index.py           ← 同步看板数据
│   │   ├── build-readme.py                       ← 更新README看板
│   │   ├── build-llms.py                         ← llms.txt生成
│   │   └── build-sitemap.py                      ← sitemap.xml+robots.txt
│   ├── 校验
│   │   ├── validate-content.py                   ← frontmatter完整性校验
│   │   ├── validate-distribution.py              ← sync/urls字段校验
│   │   └── validate_draft_saved.py               ← 发布前状态一致性检查
│   ├── 运维
│   │   ├── sync.sh                               ← 构建+提交+推送
│   │   ├── new-post.sh                           ← 新文章脚手架
│   │   ├── backfill_urls_from_feishu_export.py   ← 飞书CSV→GitHub回填
│   │   └── fix_draft_saved_to_published_all.py   ← 批量状态修复（4平台）
│
├── .github/
│   ├── workflows/               ← 4个CI
│   │   ├── pages.yml            ← Pages自动部署
│   │   ├── ci.yml               ← 基础构建验证
│   │   ├── distribution-ci.yml  ← PR时校验分发字段
│   │   └── link-check.yml       ← 外链定期检查
│   └── ISSUE_TEMPLATE/          ← 3个模板
│       ├── bug_report.yml
│       ├── content_request.yml
│       └── case_submission.yml
│
├── config/
│   └── feishu_field_map.json    ← 飞书发布中台字段映射（含4平台）
│
├── templates/
│   └── post.md                  ← 新文章frontmatter模板
│
├── data/                        * 自动生成（含index.json/distribution.json/tags.json等）
├── docs/                        * 自动生成（含llms.txt/sitemap.xml/静态页面）
└── site/                        * 自动生成（MkDocs构建输出）
```

---

## 核心能力矩阵

| 能力 | 状态 | 说明 |
|------|------|------|
| 一源三写 | ✅ | content/ → 4平台分发稿自动生成 |
| 小红书发布 | ✅ v1.3.0 | 手动复制→草稿箱保存→发布 |
| 飞书中台 | ✅ 字段映射就绪 | 含51字段，4平台完整映射 |
| 状态机 | ✅ | pending→drafted→review_passed→draft_saved→published |
| GitHub回填 | ✅ | 飞书CSV导出 → 批量写回frontmatter |
| Pages站点 | ✅ 已上线 | https://a1gcer.github.io/ai-fg-content-hub |
| CI/CD | ✅ | 4个workflow，构建/校验/部署/分发 |

---

## 日常操作

```bash
# 生成分发包
bash scripts/build.sh

# 查看小红书稿件（复制到平台草稿箱）
cat distribution/xiaohongshu/2026-05/2026-05-24-001-ai-biggest-misuse.md

# 发布后回填GitHub
python3 scripts/backfill_urls_from_feishu_export.py ./feishu_export.csv
```
