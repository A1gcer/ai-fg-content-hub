---
id: 2026-05-31-102
title: "AI 敏感信息红线清单"
slug: "ai-privacy-risk-checklist"
date: 2026-05-26
updated: 2026-05-26
category: 安全与不背锅
tags: [隐私, 安全, 红线]
risk: 高
channel: github
status: published
summary: "列出不应直接上传给公共AI工具的信息类型。"
question: "哪些敏感信息不能发给AI？"
answer: "客户数据、合同条款、财务明细、内部战略、个人隐私、密钥等都不应直接上传。"
audience: "全体职场人"
scenario: "向公共大模型输入业务资料前"
review_required: true
canonical_url: "https://a1gcer.github.io/ai-fg-content-hub/checklists/ai-privacy-risk-checklist/"
license: "CC BY-NC-SA 4.0"
---

# AI 敏感信息红线清单

以下信息不应直接上传至公共 AI 工具：

- [ ] 客户姓名、联系方式、交易细节
- [ ] 合同全文、报价明细、法务条款
- [ ] 财务报表、未公开经营数据
- [ ] 公司战略、并购、融资计划
- [ ] 员工隐私信息（身份证、手机号、住址）
- [ ] API Key、Token、账号密码
- [ ] 未发布产品规划与技术细节

## 替代做法
1. 脱敏后再输入
2. 只输入结构，不输入原文
3. 对高敏内容优先使用企业私有模型
