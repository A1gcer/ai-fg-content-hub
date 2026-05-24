---
id: 2026-05-31-103
title: "AI 幻觉识别指南"
slug: "ai-hallucination-check"
date: 2026-05-31
updated: 2026-05-31
category: AI品控检查
tags: [AI幻觉, 事实核验, 风险控制]
risk: 高
channel: github
status: published
summary: "识别AI幻觉的六个信号与对应核验方法。"
question: "如何判断AI是否在胡编？"
answer: "看来源、看可验证性、看时间和数字一致性，无法核验就不采信。"
audience: "知识工作者"
scenario: "引用AI生成结论前"
review_required: true
canonical_url: "https://a1gcer.github.io/ai-fg-content-hub/guides/ai-hallucination-check/"
license: "CC BY-NC-SA 4.0"
---

# AI 幻觉识别指南

## 常见信号
1. 说得很具体但不给来源
2. 引用"研究表明"但无出处
3. 编造案例与机构
4. 时间线混乱
5. 数字过于精准却无口径
6. 混淆相近概念

## 核验方法
- 关键结论双重来源核验
- 反向提问：请给出原始出处
- 让 AI 自评不确定点
- 无法验证则标注"待确认"
