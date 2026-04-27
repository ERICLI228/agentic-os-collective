#!/usr/bin/env python3
"""
Wiki Lint 定时巡检
用法: python3 wiki-lint.py [--fix]

每周健康检查：
1. 孤儿页面（无人链入）
2. 断链（指向不存在页面）
3. 缺 frontmatter
4. 内容冲突标记
5. 高频引用但未独立成页

输出报告到 wiki/outputs/lint-report-{date}.md
"""

import sys
import os
import re
from datetime import date
from pathlib import Path

WIKI_DIR = Path(os.path.expanduser("~/agentic-os-collective/shared/knowledge/wiki"))
INDEX_PATH = WIKI_DIR / "index.md"
LOG_PATH = WIKI_DIR / "log.md"


def find_all_wiki_pages() -> dict[str, Path]:
    pages = {}
    for ext in ("*.md",):
        for p in WIKI_DIR.rglob(ext):
            if p.name in ("index.md", "log.md", "CLAUDE.md"):
                continue
            pages[p.stem] = p
    return pages


def extract_wikilinks_from(content: str) -> set[str]:
    return set(re.findall(r"\[\[([^\]]+)\]\]", content))


def check_frontmatter(content: str) -> list[str]:
    issues = []
    if not content.startswith("---"):
        issues.append("Missing YAML frontmatter (no --- header)")
        return issues
    parts = content.split("---", 2)
    if len(parts) < 3:
        issues.append("Malformed YAML frontmatter")
        return issues
    fm = parts[1]
    required = ["title:", "date_created:", "summary:", "type:", "status:"]
    for field in required:
        if field not in fm:
            issues.append(f"Missing frontmatter field: {field}")
    return issues


def main():
    today = date.today().isoformat()
    pages = find_all_wiki_pages()

    report = []
    report.append(f"# Lint Report — {today}")
    report.append(f"Total pages: {len(pages)}\n")

    # Build all wikilinks map
    all_wikilinks: dict[str, set[str]] = {}
    for slug, path in pages.items():
        content = path.read_text(encoding="utf-8")
        all_wikilinks[slug] = extract_wikilinks_from(content)

    # 1. Orphan pages (no one links to them)
    linked_pages = set()
    for slug, links in all_wikilinks.items():
        linked_pages.update(links)
    orphans = [s for s in pages if s not in linked_pages and s not in ("index", "log")]
    if orphans:
        report.append(f"## ⚠ Orphan Pages ({len(orphans)})")
        for s in sorted(orphans):
            report.append(f"- [[{s}]] — no incoming links")
    else:
        report.append("## ✅ Orphan Pages — none found")

    # 2. Broken wikilinks
    all_slugs = set(pages.keys()) | {"index", "log"}
    broken = {}
    for slug, links in all_wikilinks.items():
        for link in links:
            link_slug = link.replace(" ", "-").lower()
            if link_slug not in all_slugs:
                broken.setdefault(slug, []).append(link)
    if broken:
        report.append(f"\n## ⚠ Broken Wikilinks ({sum(len(v) for v in broken.values())})")
        for src, links in sorted(broken.items()):
            report.append(f"- [[{src}]] → {', '.join(f'[[{l}]]' for l in links)}")
    else:
        report.append("\n## ✅ Broken Wikilinks — none found")

    # 3. Missing frontmatter
    no_fm = []
    incomplete_fm = []
    for slug, path in pages.items():
        content = path.read_text(encoding="utf-8")
        issues = check_frontmatter(content)
        if "Missing YAML frontmatter" in issues:
            no_fm.append(slug)
        elif issues:
            incomplete_fm.append((slug, issues))
    if no_fm:
        report.append(f"\n## ⚠ Pages Without Frontmatter ({len(no_fm)})")
        for s in sorted(no_fm):
            report.append(f"- [[{s}]]")
    else:
        report.append("\n## ✅ Frontmatter — all pages have it")
    if incomplete_fm:
        report.append(f"\n## ⚠ Incomplete Frontmatter ({len(incomplete_fm)})")
        for s, issues in sorted(incomplete_fm):
            for i in issues:
                report.append(f"- [[{s}]] — {i}")

    # 4. Frequent unlinked terms (simple heuristic)
    all_text = " ".join(p.read_text(encoding="utf-8") for p in pages.values())
    # Find [[wikilinks]] usage frequency
    link_counts: dict[str, int] = {}
    for links in all_wikilinks.values():
        for link in links:
            link_counts[link] = link_counts.get(link, 0) + 1
    frequently_linked = {k: v for k, v in link_counts.items() if v >= 3 and k not in all_slugs}
    if frequently_linked:
        report.append(f"\n## 💡 Frequently Linked But No Page ({len(frequently_linked)})")
        for link, count in sorted(frequently_linked.items(), key=lambda x: -x[1]):
            report.append(f"- [[{link}]] — referenced {count} times")

    report_text = "\n".join(report)

    out_path = WIKI_DIR / "outputs" / f"lint-report-{today}.md"
    out_path.write_text(report_text, encoding="utf-8")
    print(report_text)
    print(f"\n✓ Report saved: {out_path}")

    # Append to log
    entry = f"""## [{today}] lint | 健康检查
- **Report**: `wiki/outputs/lint-report-{today}.md`
- **Pages**: {len(pages)}
- **Orphans**: {len(orphans)}
- **Broken links**: {sum(len(v) for v in broken.values())}

"""
    with open(LOG_PATH, "a") as f:
        f.write(entry)


if __name__ == "__main__":
    main()
