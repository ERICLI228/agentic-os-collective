#!/usr/bin/env python3
"""
Feishu 通知集成 - TK 运营专属

支持 8 个飞书群通知:
- 选品作战室
- 数据看板
- 达人合作
- 订单中心
- 广告优化
- 内容创作
- 客服支持
- 技术研发
"""

import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FeishuNotification:
    channel: str
    title: str
    content: str
    level: str = "info"  # info, warning, error, success
    mention_all: bool = False
    
    def to_feishu_payload(self) -> Dict:
        """转换为飞书 webhook  payload"""
        colors = {
            "info": "blue",
            "warning": "orange",
            "error": "red",
            "success": "green"
        }
        
        content = f"{self.content}"
        if self.mention_all:
            content = f"<at user_id=\"all\">所有人</at>\n{content}"
        
        return {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": self.title
                    },
                    "template": colors.get(self.level, "blue")
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": content
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            }
                        ]
                    }
                ]
            }
        }


class FeishuNotifier:
    """飞书通知器"""
    
    CHANNELS = [
        "选品作战室",
        "数据看板",
        "达人合作",
        "订单中心",
        "广告优化",
        "内容创作",
        "客服支持",
        "技术研发"
    ]
    
    def __init__(self, webhooks: Dict[str, str] = None):
        self.webhooks = webhooks or {}
        self.sent_count = 0
        self.failed_count = 0
    
    def send(self, notification: FeishuNotification, channels: List[str] = None) -> Dict:
        """发送通知到指定频道"""
        channels = channels or ["技术研发"]
        results = {"success": [], "failed": []}
        
        payload = notification.to_feishu_payload()
        
        for channel in channels:
            webhook = self.webhooks.get(channel)
            if not webhook:
                results["failed"].append({"channel": channel, "reason": "webhook not configured"})
                continue
            
            try:
                response = requests.post(webhook, json=payload, timeout=10)
                if response.status_code == 200:
                    results["success"].append(channel)
                    self.sent_count += 1
                else:
                    results["failed"].append({"channel": channel, "reason": f"HTTP {response.status_code}"})
                    self.failed_count += 1
            except Exception as e:
                results["failed"].append({"channel": channel, "reason": str(e)})
                self.failed_count += 1
        
        return results
    
    def send_hot_product(self, product: Dict) -> Dict:
        """发送爆款产品通知"""
        notification = FeishuNotification(
            channel="选品作战室",
            title="🔥 发现爆款产品",
            content=f"**{product.get('name', 'Unknown')}**\n\n"
                   f"📊 播放量：{product.get('view_count', 0):,}\n"
                   f"🛒 品类：{product.get('category', 'Unknown')}\n"
                   f"🌍 市场：{product.get('market', 'Unknown')}\n"
                   f"📈 互动率：{product.get('engagement_rate', 0)}%",
            level="success"
        )
        return self.send(notification, ["选品作战室", "数据看板"])
    
    def send_low_stock(self, product: Dict) -> Dict:
        """发送库存预警通知"""
        notification = FeishuNotification(
            channel="订单中心",
            title="⚠️ 库存预警",
            content=f"**{product.get('name', 'Unknown')}**\n\n"
                   f"📦 当前库存：{product.get('stock', 0)}\n"
                   f"⚠️ 阈值：{product.get('threshold', 10)}\n"
                   f"请及时补货！",
            level="warning",
            mention_all=True
        )
        return self.send(notification, ["订单中心"])
    
    def send_error(self, title: str, error: str, channel: str = "技术研发") -> Dict:
        """发送错误通知"""
        notification = FeishuNotification(
            channel=channel,
            title=f"❌ {title}",
            content=f"**错误详情:**\n```\n{error}\n```",
            level="error"
        )
        return self.send(notification, [channel])
    
    def send_daily_report(self, report: Dict) -> Dict:
        """发送日报"""
        content = f"**TK 东南亚 5 国 3C 运营日报**\n\n"
        content += f"📅 日期：{report.get('date', 'Unknown')}\n\n"
        content += f"📊 **核心指标**\n"
        content += f"• 总销售额：${report.get('total_sales', 0):,.2f}\n"
        content += f"• 总订单：{report.get('total_orders', 0)}\n"
        content += f"• 总播放：{report.get('total_views', 0):,}\n"
        content += f"• 转化率：{report.get('conversion_rate', 0)}%\n\n"
        content += f"🔥 **爆款产品**: {len(report.get('hot_products', []))} 个\n"
        content += f"⚠️ **库存预警**: {len(report.get('low_stock_items', []))} 个"
        
        notification = FeishuNotification(
            channel="数据看板",
            title="📊 每日运营报告",
            content=content,
            level="info"
        )
        return self.send(notification, self.CHANNELS)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "sent": self.sent_count,
            "failed": self.failed_count,
            "success_rate": f"{self.sent_count / (self.sent_count + self.failed_count) * 100:.1f}%" if (self.sent_count + self.failed_count) > 0 else "N/A"
        }


def main():
    """测试入口"""
    import argparse
    parser = argparse.ArgumentParser(description="Feishu 通知集成")
    parser.add_argument("command", choices=["test", "hot-product", "low-stock", "error", "daily-report", "stats"])
    parser.add_argument("--channel", default="技术研发", help="目标频道")
    parser.add_argument("--webhook", help="Webhook URL")
    args = parser.parse_args()
    
    webhooks = {}
    if args.webhook:
        webhooks[args.channel] = args.webhook
    
    notifier = FeishuNotifier(webhooks)
    
    if args.command == "test":
        notification = FeishuNotification(
            channel=args.channel,
            title="🧪 测试通知",
            content="这是一条测试消息",
            level="info"
        )
        result = notifier.send(notification, [args.channel])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "hot-product":
        product = {
            "name": "无线蓝牙耳机",
            "view_count": 3500000,
            "category": "3C",
            "market": "TH",
            "engagement_rate": 5.2
        }
        result = notifier.send_hot_product(product)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "low-stock":
        product = {
            "name": "快充充电器",
            "stock": 5,
            "threshold": 10
        }
        result = notifier.send_low_stock(product)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "error":
        result = notifier.send_error("测试错误", "这是一个测试错误消息", args.channel)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "stats":
        print(json.dumps(notifier.get_stats(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
