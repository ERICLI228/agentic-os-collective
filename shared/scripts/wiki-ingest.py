#!/usr/bin/env python3
"""
Wiki Ingest 自动化
用法: python3 wiki-ingest.py <raw-file-path> [--type concept|entity|source]

将 raw/ 中的原始素材编译为 wiki 页面:
1. 读取原始素材
2. 用模板创建 wiki 页面（带 YAML frontmatter + [[wikilinks]]）
3. 更新 wiki/index.md
4. 追加 wiki/log.md
"""

import sys
import os
import re
import json
from datetime import date
from pathlib import Path

KNOWLEDGE_BASE = Path(os.path.expanduser("~/agentic-os-collective/shared/knowledge"))
TEMPLATES_DIR = KNOWLEDGE_BASE / "templates"
RAW_DIR = KNOWLEDGE_BASE / "raw"
WIKI_DIR = KNOWLEDGE_BASE / "wiki"
INDEX_PATH = WIKI_DIR / "index.md"
LOG_PATH = WIKI_DIR / "log.md"


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", s)
    s = s.strip("-")
    return s


def read_index() -> dict:
    pages = {"concept": [], "entity": [], "synthesis": [], "output": []}
    if not INDEX_PATH.exists():
        return pages
    current_type = None
    with open(INDEX_PATH) as f:
        for line in f:
            m = re.match(r"^## (\w+)（(\d+) 篇）", line)
            if m:
                cn_map = {"概念": "concept", "实体": "entity", "综合分析": "synthesis", "最近新增": None, "查询结果": "output"}
                current_type = cn_map.get(m.group(1), m.group(1))
                continue
            m = re.match(r"- \[\[([^\]]+)\]\]", line)
            if m and current_type in pages:
                pages[current_type].append(m.group(1))
    return pages


def update_index(slug: str, title: str, page_type: str, summary: str):
    lines = []
    today = date.today().isoformat()
    found_section = False
    section_headers = {
        "concept": "## 概念",
        "entity": "## 实体",
        "synthesis": "## 综合分析",
        "output": "## 查询结果",
    }
    target_header = section_headers.get(page_type, "## 概念")
    inserted = False

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

            if line.strip() == target_header:
                found_section = True
                continue
            if found_section and not inserted and line.startswith("## "):
                indent = "  " if page_type in ("concept", "entity") else ""
                lines.insert(-1, f"- [[{slug}]] — {summary}\n")
                inserted = True
                found_section = False

    if not inserted:
        lines.append(f"\n{target_header}\n\n- [[{slug}]] — {summary}\n")

    # Update recent additions
    for i, line in enumerate(lines):
        if line.startswith("## 最近新增"):
            # Insert after existing entries
            insert_pos = i + 1
            while insert_pos < len(lines) and lines[insert_pos].startswith("1."):
                # Renumber
                m = re.match(r"(\d+)\.", lines[insert_pos])
                if m:
                    old_num = int(m.group(1))
                    lines[insert_pos] = lines[insert_pos].replace(f"{old_num}.", f"{old_num + 1}.", 1)
                insert_pos += 1
            lines.insert(insert_pos, f"1. [{today}] [[{slug}]]（{page_type}）\n")
            break

    with open(INDEX_PATH, "w") as f:
        f.writelines(lines)


def append_log(action: str, raw_file: str, wiki_file: str, page_type: str, title: str):
    today = date.today().isoformat()
    entry = f"""
## [{today}] ingest | {title}
- **Action**: {action}
- **Raw source**: `{raw_file}`
- **Created**: `{wiki_file}`
- **Type**: {page_type}
- **Summary**: 编译 `{raw_file}` → `wiki/{page_type}s/{wiki_file}`
"""
    with open(LOG_PATH, "a") as f:
        f.write(entry.strip() + "\n\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 wiki-ingest.py <raw-file-path> [--type concept|entity|source]")
        sys.exit(1)

    raw_path = Path(sys.argv[1])
    page_type = "concept"
    if "--type" in sys.argv:
        idx = sys.argv.index("--type")
        if idx + 1 < len(sys.argv):
            page_type = sys.argv[idx + 1]

    if not raw_path.exists():
        print(f"File not found: {raw_path}")
        sys.exit(1)

    content = raw_path.read_text(encoding="utf-8")
    title = raw_path.stem.replace("-", " ").title()
    slug = slugify(title)
    today = date.today().isoformat()

    type_dir = WIKI_DIR / f"{page_type}s"
    type_dir.mkdir(parents=True, exist_ok=True)
    wiki_path = type_dir / f"{slug}.md"

    if wiki_path.exists():
        print(f"⚠ Wiki page already exists: {wiki_path}")
        # Still log it
        append_log("re-ingest", str(raw_path), str(wiki_path), page_type, title)
        print(f"✓ Logged re-ingest for {title}")
        return

    template_path = TEMPLATES_DIR / f"{page_type}.md"
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
        page_content = template.replace("{{title}}", title)
        page_content = page_content.replace("{{date}}", today)
        page_content = page_content.replace("{{source-url-or-path}}", str(raw_path))
        page_content = page_content.replace("{{one-sentence-summary}}", f"Ingested from {raw_path.name}")
    else:
        page_content = f"""---
title: "{title}"
date_created: {today}
date_modified: {today}
summary: "Ingested from {raw_path.name}"
tags: []
type: {page_type}
status: draft
---
# {title}

> Ingested from: `{raw_path}`

{content[:2000]}
"""

    wiki_path.write_text(page_content, encoding="utf-8")
    print(f"✓ Created: {wiki_path}")

    # Update index
    summary = f"Ingested from {raw_path.name}"
    update_index(slug, title, page_type, summary)
    print(f"✓ Updated: {INDEX_PATH}")

    # Update log
    append_log("ingest", str(raw_path), str(wiki_path), page_type, title)
    print(f"✓ Updated: {LOG_PATH}")


if __name__ == "__main__":
    main()
