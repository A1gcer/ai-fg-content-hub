#!/usr/bin/env python3
"""Add ## 可复制 Skill section to all existing posts"""

import re
from pathlib import Path

CONTENT_DIR = Path("content/2026/05")

skills_data = {
    "2026-05-24-001": {
        "name": "AI 初稿质检助手",
        "scenario": "用 AI 写周报/方案/邮件时，不确定能否直接外发",
        "constraints": "- 不编造事实和数据\n- 不替我做终稿判断\n- 标注可信度等级",
        "checks": (
            "- [ ] 补充了场景上下文？\n"
            "- [ ] 核验了关键事实？\n"
            "- [ ] 调整了业务术语？\n"
            "- [ ] 确认可直接外发？"
        ),
    },
    "2026-05-25-002": {
        "name": "三轮协作写作助手",
        "scenario": "需要 AI 配合一起写文档/报告，从粗稿到终稿",
        "constraints": (
            "- 每轮必须输出可直接使用的部分\n"
            "- 标注需要我补充的信息\n"
            "- 不能直接出终稿"
        ),
        "checks": (
            "- [ ] 粗稿结构完整？\n"
            "- [ ] 细化阶段补充了场景信息？\n"
            "- [ ] 终稿前人工核验了事实？\n"
            "- [ ] 风险提醒都处理了？"
        ),
    },
    "2026-05-26-003": {
        "name": "场景定制写作助手",
        "scenario": "需要 AI 写一篇具体场景下的内容，但不是万能模板",
        "constraints": (
            "- 必须指定受众/场景/格式\n"
            "- 禁止空话套话\n"
            "- 禁止未经证实的数据"
        ),
        "checks": (
            "- [ ] 指定了受众和场景？\n"
            "- [ ] 字数格式符合预期？\n"
            "- [ ] AI 没自动补充未知数据？\n"
            "- [ ] 语气风格匹配？"
        ),
    },
    "2026-05-27-004": {
        "name": "AI 可信度审计助手",
        "scenario": "AI 回答看起来很顺，但不确定是不是在编",
        "constraints": (
            "- 必须标注不确定点\n"
            "- 结论必须有来源引用\n"
            "- 无法确认的必须写明"
        ),
        "checks": (
            "- [ ] AI 标注了所有不确定点？\n"
            "- [ ] 每个结论都能追溯来源？\n"
            '- [ ] "无法确认"标记都处理了？\n'
            "- [ ] 是否可以直接引用或需进一步验证？"
        ),
    },
    "2026-05-28-005": {
        "name": "AI 信息整理助手",
        "scenario": "需要 AI 整理信息但不做最终决策",
        "constraints": (
            "- 只做整理，不给结论\n"
            "- 标注高风险项\n"
            "- 标注需要专业确认项"
        ),
        "checks": (
            "- [ ] AI 没偷给结论？\n"
            "- [ ] 高风险标记都处理了？\n"
            "- [ ] 需要人工确认的项已标注？\n"
            "- [ ] 不可外发项已隔离？"
        ),
    },
    "2026-05-29-006": {
        "name": "70 分初稿助手",
        "scenario": "需要 AI 出第一版初稿，自己继续修改完善",
        "constraints": (
            "- 只出结构完整、信息清晰的初稿\n"
            "- 不替我做终稿判断\n"
            "- 列出需要我补充的事实"
        ),
        "checks": (
            "- [ ] 初稿结构是否完整？\n"
            "- [ ] 列出的待补充事实是否处理？\n"
            "- [ ] 关键判断是否留给了自己？\n"
            "- [ ] 补充后是否重读了全文？"
        ),
    },
    "2026-05-30-007": {
        "name": "AI 内容可交付化改写助手",
        "scenario": "AI 生成的内容需要改写为可直接交付的版本",
        "constraints": (
            "- 标注需要人工确认的事实\n"
            "- 标注可能引发误解的表达\n"
            "- 标注需要补充的场景信息"
        ),
        "checks": (
            "- [ ] 人工确认事实都处理了？\n"
            "- [ ] 可能误解的表达改掉了？\n"
            "- [ ] 补充了场景化信息？\n"
            "- [ ] 读起来像人写的？"
        ),
    },
}

def get_prompt(content):
    m = re.search(
        r"##\s*可复制\s*Prompt\s*\n+```(?:text)?\s*\n?(.*?)\n?```",
        content, re.DOTALL
    )
    return m.group(1).strip() if m else ""

def get_risk(content):
    m = re.search(r"^risk:\s*(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else "中"

def main():
    for f in sorted(CONTENT_DIR.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        id_m = re.search(r"^id:\s*(2026-\d{2}-\d{2}-\d+)", text, re.MULTILINE)
        if not id_m:
            print(f"SKIP {f.name}: no id")
            continue
        post_id = id_m.group(1)
        if post_id not in skills_data:
            print(f"SKIP {f.name}: no skill data")
            continue

        sk = skills_data[post_id]
        prompt = get_prompt(text)
        risk = get_risk(text)
        risk_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(risk, "⚪")

        skill_section = (
            f"## 可复制 Skill\n\n"
            f"**Skill：** {sk['name']}\n"
            f"**场景：** {sk['scenario']}\n"
            f"**风险等级：** {risk_icon} {risk}\n\n"
            f"**指令：**\n"
            f"```text\n"
            f"{prompt}\n"
            f"```\n\n"
            f"**约束：**\n"
            f"{sk['constraints']}\n\n"
            f"**输出检查：**\n"
            f"{sk['checks']}\n"
        )

        if "## 结论" in text:
            text = text.replace("## 结论", skill_section + "\n## 结论")
        else:
            text += "\n" + skill_section

        f.write_text(text, encoding="utf-8")
        print(f"✅ {f.name}: added Skill '{sk['name']}'")

    print("\nDone.")

if __name__ == "__main__":
    main()
