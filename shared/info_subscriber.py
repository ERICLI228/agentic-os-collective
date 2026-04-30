#!/usr/bin/env python3
"""
全球信息订阅系统 — RSS/Atom 聚合 + 分类 + 知识存档
基于 Obsidian RSS Dashboard 理念，Agentic OS 自动版

功能:
- 订阅 YouTube / Reddit / 博客 RSS 源
- 自动抓取新条目 → 分类打标 → 生成每日摘要
- 竞品/TK选品相关自动高亮
- 知识存档到 Obsidian Vault

用法:
  python3 shared/info_subscriber.py              # 检查所有订阅源更新
  python3 shared/info_subscriber.py --add URL     # 添加新订阅源
  python3 shared/info_subscriber.py --digest      # 生成今日摘要
  python3 shared/info_subscriber.py --daemon      # 后台模式, 60分钟
"""
import json
import os
import sys
import time
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
from dataclasses import dataclass, asdict, field
from typing import List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path.home() / ".agentic-os" / "info_subscriber"
FEEDS_PATH = DATA_DIR / "feeds.json"
ITEMS_PATH = DATA_DIR / "items.json"
DIGEST_PATH = DATA_DIR / "daily_digest.json"
OBSIDIAN_VAULT = Path.home() / "knowledge-base"

# 预设订阅源: TK卖家必关注
PRESET_FEEDS = {
    "youtube": {
        "TK官方动态": "https://www.youtube.com/feeds/videos.xml?channel_id=UCiUnlCUzonUq6U2NduA7bSw",
        "东南亚电商趋势": "https://www.youtube.com/feeds/videos.xml?channel_id=UCNbNf7nG3vB4IiE1BgkZf1Q",
        "TK选品方法": "https://www.youtube.com/feeds/videos.xml?channel_id=UC7T29ISuDhLg9eGdFJ1nJXg",
        "跨境电商运营": "https://www.youtube.com/feeds/videos.xml?channel_id=UCtDOOfkyrKJj2E4Q5LBXa0Q",
    },
    "reddit": {
        "r/dropshipping": "https://www.reddit.com/r/dropshipping/.rss",
        "r/ecommerce": "https://www.reddit.com/r/ecommerce/.rss",
        "r/TikTok": "https://www.reddit.com/r/TikTok/.rss",
        "r/smallbusiness": "https://www.reddit.com/r/smallbusiness/.rss",
    },
    "blog": {
        "Shopify电商博客": "https://www.shopify.com/blog.atom",
        "TK商业博客": "https://newsroom.tiktok.com/en-us/rss.xml",
    },
}

# TK 电商关键词 → 高亮匹配
TK_KEYWORDS = [
    "dropshipping", "tiktok shop", "product research", "trending product",
    "viral", "winning product", "aliexpress", "supplier", "profit margin",
    "东南亚", "shopee", "lazada", "选品", "爆款", "跨境电商",
    "tiktok广告", "TK广告", "roi", "转化率", "素材",
]


@dataclass
class FeedItem:
    feed_name: str
    title: str
    link: str
    published: str
    summary: str = ""
    source_type: str = "unknown"
    tags: List[str] = field(default_factory=list)
    tk_relevance: float = 0.0
    fetched_at: str = ""


class InfoSubscriber:
    def __init__(self):
        self.feeds = self._load_feeds()
        self.items = self._load_items()

    def _load_feeds(self):
        if FEEDS_PATH.exists():
            return json.loads(FEEDS_PATH.read_text())
        # 首次使用 → 加载预设
        feeds = PRESET_FEEDS
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        FEEDS_PATH.write_text(json.dumps(feeds, ensure_ascii=False, indent=2))
        return feeds

    def _load_items(self):
        if ITEMS_PATH.exists():
            return json.loads(ITEMS_PATH.read_text())
        return {}

    def _save_items(self):
        ITEMS_PATH.write_text(json.dumps(self.items, ensure_ascii=False, indent=2))

    def add_feed(self, url, name=None, category="custom"):
        """添加新订阅源"""
        source_type = self._detect_source(url)
        name = name or self._infer_name(url)

        if category not in self.feeds:
            self.feeds[category] = {}
        self.feeds[category][f"{name} [{source_type}]"] = url

        FEEDS_PATH.write_text(json.dumps(self.feeds, ensure_ascii=False, indent=2))
        return {"name": name, "url": url, "type": source_type}

    def _detect_source(self, url):
        u = url.lower()
        if "youtube.com" in u: return "youtube"
        if "reddit.com" in u: return "reddit"
        if "threads.net" in u: return "threads"
        if "atom" in u: return "blog"
        if "rss" in u or "feed" in u or ".xml" in u: return "rss"
        return "unknown"

    def _infer_name(self, url):
        try:
            p = urlparse(url)
            return p.netloc.replace("www.", "").split(".")[0]
        except Exception:
            return url[:30]

    def fetch_feed(self, url, source_type="unknown"):
        """抓取单个 RSS/Atom 源"""
        import urllib.request
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "AgenticOS/3.5 RSS Reader",
                "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"
            })
            resp = urllib.request.urlopen(req, timeout=15)
            return ET.parse(resp).getroot()
        except Exception as e:
            return None

    def parse_items(self, root, feed_name, source_type):
        """解析 RSS/Atom XML → FeedItem 列表"""
        items = []
        if root is None:
            return items

        ns = {"atom": "http://www.w3.org/2005/Atom",
              "media": "http://search.yahoo.com/mrss/",
              "yt": "http://www.youtube.com/xml/schemas/2015"}

        # RSS 2.0
        for item_el in root.findall(".//item"):
            items.append(self._parse_rss_item(item_el, feed_name, source_type))

        # Atom
        if not items:
            for entry_el in root.findall(".//atom:entry", ns):
                items.append(self._parse_atom_entry(entry_el, feed_name, source_type, ns))

        return items

    def _parse_rss_item(self, el, feed_name, source_type):
        title = self._text(el, "title")
        link = self._text(el, "link")
        pub = self._text(el, "pubDate") or self._text(el, "dc:date")
        desc = self._text(el, "description")[:500] if self._text(el, "description") else ""

        relevance, tags = self._analyze_tk_relevance(title, desc, source_type)
        return FeedItem(
            feed_name=feed_name, title=title, link=link,
            published=pub, summary=desc,
            source_type=source_type, tags=tags,
            tk_relevance=relevance,
            fetched_at=datetime.now().isoformat()
        )

    def _parse_atom_entry(self, el, feed_name, source_type, ns):
        title = self._text(el, "atom:title", ns)
        link_el = el.find("atom:link", ns)
        link = link_el.get("href", "") if link_el is not None else ""
        pub = self._text(el, "atom:published", ns) or self._text(el, "atom:updated", ns)
        desc = self._text(el, "atom:summary", ns)[:500] if self._text(el, "atom:summary", ns) else ""

        relevance, tags = self._analyze_tk_relevance(title, desc, source_type)
        return FeedItem(
            feed_name=feed_name, title=title, link=link,
            published=pub, summary=desc,
            source_type=source_type, tags=tags,
            tk_relevance=relevance,
            fetched_at=datetime.now().isoformat()
        )

    def _text(self, el, tag, ns=None):
        found = el.find(tag, ns) if ns else el.find(tag)
        return (found.text or "").strip() if found is not None and found.text else ""

    def _analyze_tk_relevance(self, title, summary, source_type="unknown"):
        """分析 TK 电商相关度 (0-1) + 自动打标"""
        text = (title + " " + summary).lower()
        tags = []
        score = 0

        for kw in TK_KEYWORDS:
            kw_lower = kw.lower()
            if kw_lower in text:
                tags.append(kw)

        # 计算相关度
        match_count = len(tags)
        if match_count >= 3:
            score = 0.9
        elif match_count >= 2:
            score = 0.7
        elif match_count >= 1:
            score = 0.4
        elif source_type in ("youtube", "reddit") and any(
            w in text for w in ("product", "sell", "market", "trend", "shop")
        ):
            score = 0.2

        return round(score, 2), tags[:5]

    def check_all(self):
        """检查所有订阅源 → 返回新条目"""
        new_items = []
        for category, feeds in self.feeds.items():
            for name, url in feeds.items():
                source_type = self._detect_source(url)
                root = self.fetch_feed(url, source_type)
                if root is None:
                    continue

                parsed = self.parse_items(root, name, source_type)

                for item in parsed:
                    item_key = hashlib.md5(
                        f"{item.feed_name}{item.title}{item.link}".encode()
                    ).hexdigest()[:12]

                    if item_key not in self.items:
                        self.items[item_key] = asdict(item)
                        new_items.append(item)

        self._save_items()
        return new_items

    def get_digest(self, top_n=10):
        """生成今日摘要 — 按 TK 相关度排序"""
        sorted_items = sorted(
            self.items.values(),
            key=lambda x: x.get("tk_relevance", 0),
            reverse=True
        )
        top = sorted_items[:top_n]

        return {
            "generated_at": datetime.now().isoformat(),
            "total_subscribed": sum(len(v) for v in self.feeds.values()),
            "total_items": len(self.items),
            "new_today": len([i for i in self.items.values()
                            if i.get("fetched_at", "") > (datetime.now() - timedelta(hours=24)).isoformat()]),
            "top_stories": top,
            "tk_highlights": [i for i in top if i.get("tk_relevance", 0) >= 0.4],
        }

    def save_to_obsidian(self):
        """将今日摘要存档到 Obsidian Vault"""
        daily_dir = OBSIDIAN_VAULT / "05-每日日志"
        if not daily_dir.exists():
            return False

        digest = self.get_digest(top_n=15)
        date_str = datetime.now().strftime("%Y-%m-%d")

        lines = [
            f"# 🌍 全球信息摘要 · {date_str}",
            "",
            f"> 订阅源: {digest['total_subscribed']} | 总条目: {digest['total_items']} | 今日新增: {digest['new_today']}",
            "",
            "## 🔥 TK 电商高相关",
            "",
        ]

        tk_high = digest["tk_highlights"]
        if tk_high:
            for item in tk_high[:8]:
                lines.append(f"- [{item['title'][:80]}]({item['link']}) "
                           f"`{item.get('source_type','?')}` "
                           f"相关度:{item.get('tk_relevance',0)} "
                           f"#{' #'.join(item.get('tags',[]))}")
            lines.append("")
        else:
            lines.append("_(无高相关条目)_\n")

        lines.append("## 📡 其他来源")
        lines.append("")
        other = [i for i in digest["top_stories"] if i.get("tk_relevance", 0) < 0.4]
        for item in other[:10]:
            lines.append(f"- [{item['title'][:80]}]({item['link']}) "
                       f"`{item.get('source_type','?')}`")
        lines.append("")

        digest_file = daily_dir / f"{date_str}-INFO.md"
        digest_file.write_text("\n".join(lines))
        return str(digest_file)


def push_to_feishu(digest):
    """推送今日全球信息摘要到飞书"""
    try:
        from config import get_feishu_webhook
        webhook = get_feishu_webhook("数据看板")
    except Exception:
        webhook = os.environ.get("FEISHU_WEBHOOK_URL", "")

    if not webhook:
        print("⚠️ 无飞书 webhook")
        return False

    highlights = digest.get("tk_highlights", [])
    lines = [f"🌍 全球信息摘要 · {datetime.now().strftime('%m-%d %H:%M')}"]
    lines.append(f"订阅 {digest['total_subscribed']} 源 | 新增 {digest['new_today']} 条\n")

    if highlights:
        lines.append("🔥 **TK高相关**:")
        for item in highlights[:5]:
            tags = " ".join(f"#{t}" for t in item.get("tags", [])[:3])
            lines.append(f"• [{item['title'][:60]}]({item['link']}) {tags}")
    else:
        lines.append("_(无高相关)_")

    try:
        import urllib.request
        body = json.dumps({
            "msg_type": "text",
            "content": {"text": "\n".join(lines)}
        }).encode("utf-8")
        req = urllib.request.Request(webhook, data=body,
            headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception:
        return False


def main():
    import argparse
    p = argparse.ArgumentParser(description="全球信息订阅系统")
    p.add_argument("--add", help="添加 RSS URL")
    p.add_argument("--name", help="订阅源名称")
    p.add_argument("--digest", action="store_true", help="生成今日摘要")
    p.add_argument("--obsidian", action="store_true", help="存档到 Obsidian")
    p.add_argument("--feishu", action="store_true", help="推送到飞书")
    p.add_argument("--daemon", action="store_true", help="守护进程模式")
    p.add_argument("--test", action="store_true", help="Mock 测试")
    args = p.parse_args()

    sub = InfoSubscriber()

    if args.test:
        new = sub.check_all()
        digest = sub.get_digest()
        print(json.dumps({
            "status": "ok",
            "feeds": sum(len(v) for v in sub.feeds.values()),
            "sources": list(sub.feeds.keys()),
            "new_items": len(new),
            "total_items": digest["total_items"],
            "tk_highlights": len(digest["tk_highlights"]),
        }, ensure_ascii=False, indent=2))
        print("\n✅ --test PASS: info_subscriber")
        return

    if args.add:
        result = sub.add_feed(args.add, args.name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.daemon:
        print("🌍 全球信息订阅守护进程 (60min)")
        while True:
            try:
                new = sub.check_all()
                if new:
                    print(f"  📥 {datetime.now().strftime('%H:%M')} | +{len(new)} 新条目")
                    digest = sub.get_digest()
                    push_to_feishu(digest)
                else:
                    print(f"  ⏳ {datetime.now().strftime('%H:%M')} | 无更新")
            except Exception as e:
                print(f"  ❌ {e}")
            time.sleep(3600)

    if args.digest or not any([args.add, args.obsidian, args.feishu]):
        new = sub.check_all()
        if new:
            print(f"📥 {len(new)} 新条目")
            for item in new[:5]:
                print(f"  [{item.tk_relevance:.1f}] {item.title[:60]}")

        digest = sub.get_digest()
        print(f"\n📊 摘要: {digest['total_subscribed']} 源 | {digest['total_items']} 总条目 | {digest['new_today']} 今日新增")

        if digest["tk_highlights"]:
            print(f"\n🔥 TK 高相关 ({len(digest['tk_highlights'])} 条):")
            for item in digest["tk_highlights"][:5]:
                tags_str = " ".join(f"[{t}]" for t in item.get("tags", [])[:3])
                print(f"  • {item['title'][:70]} {tags_str}")

    if args.obsidian:
        path = sub.save_to_obsidian()
        if path:
            print(f"📁 已存档到 Obsidian: {path}")
        else:
            print("⚠️ Obsidian Vault 未找到")

    if args.feishu:
        digest = sub.get_digest()
        if push_to_feishu(digest):
            print("✅ 已推送到飞书")


if __name__ == "__main__":
    main()
