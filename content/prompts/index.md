---
id: 2026-05-31-104
title: "AI-FG Prompt 模板库"
slug: "prompt-templates"
date: 2026-05-31
updated: 2026-05-31
category: AI工作流
tags: [Prompt, 模板, 复用]
risk: 中
channel: github
status: published
summary: "面向职场交付的可复用 Prompt 模板库。"
question: "如何搭建可复用Prompt模板库？"
answer: "按任务类型沉淀固定模板，并把复核点写进模板。"
audience: "职场人, 团队"
scenario: "周报、纪要、方案、风险复核"
review_required: true
canonical_url: "https://a1gcer.github.io/ai-fg-content-hub/prompts/prompt-templates/"
license: "CC BY-NC-SA 4.0"
---

# AI-FG Prompt 模板库

## 1. 周报模板
```text
请根据本周工作内容生成周报初稿，结构：
1) 本周完成
2) 数据与结果
3) 风险与问题
4) 下周计划
请标注：需要我补充的事实。
```

## 2. 会议纪要模板
```text
请将以下会议记录整理为纪要：
- 决策事项
- 待办事项（负责人+截止日期）
- 风险点
- 待确认项
```

## 3. 风险复核模板
```text
请审核以下内容，输出：
1) 事实风险
2) 隐私风险
3) 误导风险
4) 不建议直接外发段落
```
