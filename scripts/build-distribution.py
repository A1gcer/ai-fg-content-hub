#!/usr/bin/env python3
"""build-distribution.py — 从 content/ 生成四平台分发稿件"""

import json
import re
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DIST_DIR = ROOT / "distribution"

PLATFORMS = ["zhihu", "wechat", "juejin", "xiaohongshu"]

def s(v):
    return "" if v is None else str(v)

def parse_md_file(fpath: Path):
    text = fpath.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text.strip()
    meta = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():].strip()
    return meta, body

def is_post_path(rel_path: Path):
    parts = rel_path.parts
    return (len(parts) >= 4 and parts[0] == "content"
            and re.match(r"^\d{4}$", parts[1]) and re.match(r"^\d{2}$", parts[2]))

def split_sections(body: str):
    sections = {}
    current_heading = None
    current_lines = []
    for line in body.split("\n"):
        if line.startswith("## "):
            if current_heading:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_heading:
        sections[current_heading] = "\n".join(current_lines).strip()
    return sections

def get_id_no(meta):
    _id = s(meta.get("id"))
    m = re.match(r"^\d{4}-\d{2}-\d{2}-(\d+)$", _id)
    return m.group(1) if m else _id

def common_tail():
    return (
        "我把这类问题整理成了「AI不翻车FAQ / AI-FG」。\n\n"
        "GitHub 项目：\n"
        "https://github.com/A1gcer/ai-fg-content-hub\n"
    )

def render_zhihu(meta, sections):
    title = s(meta.get("title"))
    question = s(meta.get("question")) or title
    answer = s(meta.get("answer"))
    why = sections.get("为什么会这样", "")
    how = sections.get("普通人怎么做", "")
    checklist = sections.get("防翻车检查清单", "")
    conclusion = sections.get("结论", "")

    default_why = "1. AI输出偏平均化\n2. 缺少场景约束\n3. 流畅表达会放大可信错觉"
    default_how = "1. 先让AI出初稿\n2. 补充场景与事实\n3. 人工核验后再外发"
    default_checklist = "- [ ] 事实是否核验\n- [ ] 是否包含敏感信息\n- [ ] 是否可直接外发"
    default_conclusion = "AI可做初稿，终稿责任在人。"

    body = "\n".join([
        "# 问题：" + question,
        "",
        "一句话回答：" + answer,
        "",
        "很多人用 AI 的问题，不是不会问，而是把 AI 输出当成\"最终答案\"。",
        "",
        "## 为什么会这样？",
        "",
        why if why else default_why,
        "",
        "## 普通人应该怎么做？",
        "",
        how if how else default_how,
        "",
        "## 防翻车清单",
        "",
        checklist if checklist else default_checklist,
        "",
        "## 总结",
        "",
        conclusion if conclusion else default_conclusion,
        "",
        common_tail(),
        "关键词：AI不翻车FAQ / AI-FG / AI交付质量",
    ])
    return body

def render_wechat(meta, sections):
    title = s(meta.get("title"))
    no = get_id_no(meta)
    answer = s(meta.get("answer"))
    why = sections.get("为什么会这样", "")
    how = sections.get("普通人怎么做", "")
    checklist = sections.get("防翻车检查清单", "")

    default_why = "核心原因通常是：缺少边界、缺少场景、缺少复核。"
    default_how = "建议流程：先边界 -> 再初稿 -> 再复核 -> 再发布。"
    default_checklist = "- [ ] 事实\n- [ ] 数据\n- [ ] 场景\n- [ ] 风险\n- [ ] 责任"

    body = "\n".join([
        "# " + title,
        "",
        "你有没有发现：用了 AI 之后，看起来更快，但真正交付时还是要返工。",
        "",
        "今天这篇是「AI不翻车FAQ」第 " + no + " 篇。",
        "",
        "## 01 先说结论",
        "",
        answer,
        "",
        "## 02 为什么会这样？",
        "",
        why if why else default_why,
        "",
        "## 03 正确做法",
        "",
        how if how else default_how,
        "",
        "## 04 发出去之前，先检查这 5 件事",
        "",
        checklist if checklist else default_checklist,
        "",
        "## 05 最后说一句",
        "",
        "AI 可以帮你把工作推到 70 分，但最后 30 分必须由你判断、适配和复核。",
        "",
        "这是「AI不翻车FAQ」第 " + no + " 篇。",
        "",
        "完整知识库持续整理在 GitHub：",
        "https://github.com/A1gcer/ai-fg-content-hub",
    ])
    return body

def render_juejin(meta, sections):
    title = s(meta.get("title"))
    answer = s(meta.get("answer"))
    why = sections.get("为什么会这样", "")
    how = sections.get("普通人怎么做", "")
    checklist = sections.get("防翻车检查清单", "")
    prompt = sections.get("可复制 Prompt", "")
    conclusion = sections.get("结论", "")

    if prompt:
        prompt_block = prompt
    else:
        prompt_block = "\n".join([
            "```text",
            "请帮我生成一个初稿，但不要替我做最终判断。",
            "输出时标注：",
            "1. 哪些内容是推测",
            "2. 哪些内容需要补充事实",
            "3. 哪些内容不能直接外发",
            "```",
        ])

    default_why = "问题不在模型本身，而在于使用者把「生成」当成「交付」。"
    default_how = "建议流程：明确边界 -> 生成初稿 -> 场景补充 -> 事实核验 -> 人工定稿"
    default_checklist = "- [ ] 事实\n- [ ] 数据\n- [ ] 风险\n- [ ] 场景\n- [ ] 责任"
    default_conclusion = "AI 出稿，人出品质；终稿责任在人。"

    body = "\n".join([
        "# " + title,
        "",
        "## 背景",
        "",
        "很多人把 AI 当成\"一键完成工具\"，但真实工作交付里，这种用法风险很高。",
        "",
        "本文来自「AI不翻车FAQ / AI-FG」项目，目标是把 AI 生成内容变成可交付成果。",
        "",
        "## 一句话结论",
        "",
        answer,
        "",
        "## 问题本质",
        "",
        why if why else default_why,
        "",
        "## 更稳的做法",
        "",
        how if how else default_how,
        "",
        "## 检查清单",
        "",
        checklist if checklist else default_checklist,
        "",
        "## 可复制 Prompt",
        "",
        prompt_block,
        "",
        "## 结论",
        "",
        conclusion if conclusion else default_conclusion,
        "",
        "## 项目链接",
        "",
        "AI不翻车FAQ / AI-FG：",
        "https://github.com/A1gcer/ai-fg-content-hub",
    ])
    return body

def render_xiaohongshu(meta, sections):
    """
    小红书风格：
    - 痛点开头（钩子）
    - 3个核心点（短句）
    - 可执行动作（3步）
    - 互动结尾 + 话题标签
    建议控制在 300~800 字
    """
    title = s(meta.get("title"))
    answer = s(meta.get("answer"))
    summary = s(meta.get("summary"))
    risk = s(meta.get("risk", "中"))
    question = s(meta.get("question")) or title

    why = sections.get("为什么会这样", "")
    how = sections.get("普通人怎么做", "")
    checklist = sections.get("防翻车检查清单", "")
    conclusion = sections.get("结论", "")

    def extract_bullets(text, max_n=3):
        lines = [x.strip() for x in text.splitlines() if x.strip()]
        bullets = []
        for ln in lines:
            if ln.startswith(("- ", "* ", "1.", "2.", "3.", "4.", "5.", "1、", "2、", "3、", "①", "②", "③")):
                bullets.append(ln.lstrip("-* ").strip())
            elif re.match(r"^\d+[\.、]\s*", ln):
                bullets.append(re.sub(r"^\d+[\.、]\s*", "", ln))
            if len(bullets) >= max_n:
                break
        return bullets

    why_points = extract_bullets(why, 3)
    if len(why_points) < 3:
        why_points = [
            "把 AI 当\"终稿机器\"，而不是\"初稿助手\"",
            "只看表达流畅，不做事实核验",
            "没有固定工作流，每次都从头来"
        ]

    how_steps = extract_bullets(how, 3)
    if len(how_steps) < 3:
        how_steps = [
            "先让 AI 出 70 分初稿",
            "补真实场景 + 关键事实",
            "发出前做 5 分钟复核"
        ]

    risk_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(risk, "⚪")

    quick_check = extract_bullets(checklist, 3)
    if len(quick_check) < 3:
        quick_check = ["事实对不对", "有没有敏感信息", "能不能直接发"]

    tail = conclusion if conclusion else "AI 可以提速，但终稿责任一定在人。"

    text = f"""# {title}

你是不是也遇到过：
AI 写得很顺，但一发出去就容易翻车？😅

先说结论👇
{answer or summary or "AI 适合做初稿，不适合直接当终稿。"} {risk_icon}

为什么会这样（3点）：
1) {why_points[0]}
2) {why_points[1]}
3) {why_points[2]}

普通人可直接照做（3步）：
✅ {how_steps[0]}
✅ {how_steps[1]}
✅ {how_steps[2]}

发之前快检 30 秒：
- {quick_check[0]}
- {quick_check[1]}
- {quick_check[2]}

{tail}

你现在最容易踩坑的是哪一步？
评论区告诉我，我按你的场景给你一版可直接用模板。

#AI不翻车FAQ #AI办公 #AI提效 #提示词 #职场效率 #AI避坑 #内容创作
"""
    return text.strip() + "\n"

def build_file(platform, meta, content, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fm = {
        "source_id": s(meta.get("id")),
        "source_title": s(meta.get("title")),
        "platform": platform,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "status": "drafted"
    }
    frontmatter = "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip() + "\n---\n\n"
    out_path.write_text(frontmatter + content, encoding="utf-8")

def main():
    count = 0
    generated = []

    for fpath in sorted(CONTENT_DIR.rglob("*.md")):
        rel = fpath.relative_to(ROOT)
        if not is_post_path(rel):
            continue

        meta, body = parse_md_file(fpath)
        if not meta:
            continue
        if s(meta.get("status")) == "archived":
            continue

        date = s(meta.get("date"))
        slug = s(meta.get("slug")) or fpath.stem
        post_id = s(meta.get("id"))
        month = date[:7] if len(date) >= 7 else "unknown-00"

        sections = split_sections(body)

        zhihu_text = render_zhihu(meta, sections)
        wechat_text = render_wechat(meta, sections)
        juejin_text = render_juejin(meta, sections)
        xiaohongshu_text = render_xiaohongshu(meta, sections)

        base_name = f"{post_id}-{slug}.md"

        out_zhihu = DIST_DIR / "zhihu" / month / base_name
        out_wechat = DIST_DIR / "wechat" / month / base_name
        out_juejin = DIST_DIR / "juejin" / month / base_name
        out_xhs = DIST_DIR / "xiaohongshu" / month / base_name

        build_file("zhihu", meta, zhihu_text, out_zhihu)
        build_file("wechat", meta, wechat_text, out_wechat)
        build_file("juejin", meta, juejin_text, out_juejin)
        build_file("xiaohongshu", meta, xiaohongshu_text, out_xhs)

        generated.append({
            "id": post_id,
            "title": s(meta.get("title")),
            "date": date,
            "slug": slug,
            "files": {
                "zhihu": str(out_zhihu.relative_to(ROOT)),
                "wechat": str(out_wechat.relative_to(ROOT)),
                "juejin": str(out_juejin.relative_to(ROOT)),
                "xiaohongshu": str(out_xhs.relative_to(ROOT))
            }
        })
        count += 1

    data_dir = ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "distribution-drafts.json").write_text(
        json.dumps({"updated": datetime.utcnow().isoformat() + "Z", "count": count, "items": generated},
                   ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"build-distribution complete: {count} posts -> {len(PLATFORMS)} platforms")

if __name__ == "__main__":
    main()
