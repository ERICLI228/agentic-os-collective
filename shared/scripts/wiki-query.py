#!/usr/bin/env python3
"""
Wiki Query 闭环
用法: python3 wiki-query.py <output-slug> "<title>" "<answer-text>"

将 AI 的回答保存到 wiki/outputs/，自动更新 index.md 和 log.md。

AI 在回答知识库问题后自动调用此脚本：
  回答完 → 提取页面列表 → python3 wiki-query.py "what-is-x" "问题标题" "回答内容"
"""

import sys
import os
import re
from datetime import date
from pathlib import Path

WIKI_DIR = Path(os.path.expanduser("~/agentic-os-collective/shared/knowledge/wiki"))
INDEX_PATH = WIKI_DIR / "index.md"
LOG_PATH = WIKI_DIR / "log.md"


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", s)
    s = s.strip("-")
    return s


def extract_wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", text)


def update_index(slug: str, title: str, summary: str, pages_consulted: list[str]):
    today = date.today().isoformat()
    lines = []
    with open(INDEX_PATH) as f:
        for line in f:
            if line.startswith("date_modified:"):
                line = f"date_modified: {today}\n"
            if line.startswith("total_pages:"):
                m = re.search(r"\d+", line)
                if m:
                    total = int(m.group()) + 1
                    line = f"total_pages: {total}\n"
            lines.append(line)

    # Add to outputs section
    for i, line in enumerate(lines):
        if line.startswith("## 最近新增"):
            insert_pos = i + 1
            while insert_pos < len(lines) and lines[insert_pos].startswith("1."):
                m = re.match(r"(\d+)\.", lines[insert_pos])
                if m:
                    lines[insert_pos] = lines[insert_pos].replace(f"{m.group(1)}.", f"{int(m.group(1)) + 1}.", 1)
                insert_pos += 1
            lines.insert(insert_pos, f"1. [{today}] [[{slug}]]（output）\n")
            break

    with open(INDEX_PATH, "w") as f:
        f.writelines(lines)


def append_log(slug: str, title: str, pages: list[str]):
    today = date.today().isoformat()
    entry = f"""## [{today}] query | {title}
- **Saved**: `wiki/outputs/{slug}.md`
- **Pages consulted**: {", ".join(pages) if pages else "none"}
- **Summary**: AI query result saved to wiki outputs

"""
    with open(LOG_PATH, "a") as f:
        f.write(entry)


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 wiki-query.py <slug> <title> <answer-text>")
        print("  Or: python3 wiki-query.py --read <query>")
        sys.exit(1)

    slug = sys.argv[1]
    title = sys.argv[2]
    answer_text = sys.argv[3]
    today = date.today().isoformat()

    pages = extract_wikilinks(answer_text)
    summary = answer_text.split("\n")[0][:100] if answer_text.strip() else title

    out_dir = WIKI_DIR / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"

    if out_path.exists():
        print(f"⚠ Overwriting existing: {out_path}")

    frontmatter = f"""---
title: "{title}"
date_created: {today}
date_modified: {today}
summary: "{summary}"
type: output
status: final
pages_consulted:
"""
    for p in pages:
        frontmatter += f'  - "{p}"\n'
    frontmatter += "---\n\n"

    content = frontmatter + f"# {title}\n\n" + answer_text.strip() + "\n"

    out_path.write_text(content, encoding="utf-8")
    print(f"✓ Saved: {out_path}")

    update_index(slug, title, summary, pages)
    print(f"✓ Updated: {INDEX_PATH}")

    append_log(slug, title, pages)
    print(f"✓ Updated: {LOG_PATH}")


if __name__ == "__main__":
    main()
