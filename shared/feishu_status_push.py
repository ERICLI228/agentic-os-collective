#!/usr/bin/env python3
"""
飞书状态推送 — v3.5 Sprint 0.2
每 30 分钟推送系统状态到飞书「运营指挥部」群
单向推送，无回调按钮（先推后看，驾驶舱就绪后再加交互）

用法:
  python3 shared/feishu_status_push.py          # 推送一次
  python3 shared/feishu_status_push.py --test    # 测试模式（打印 JSON 不发飞书）
  python3 shared/feishu_status_push.py --daemon  # 守护模式（每 30 分钟循环）
"""

import json
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import config


def fetch_status():
    """从本地 task_wizard API 获取状态，失败时降级"""
    import urllib.request
    try:
        req = urllib.request.Request('http://localhost:5001/api/status')
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {
            'tasks': [],
            'total': 0,
            'completed': 0,
            'decision_pending': 0,
            'system_health': 'unreachable',
            'error': str(e)
        }


def build_card(status_data):
    """构建飞书交互卡片 JSON（当前纯展示，无按钮）"""
    total = status_data.get('total', 0)
    completed = status_data.get('completed', 0)
    pending = status_data.get('decision_pending', 0)
    health = status_data.get('system_health', 'unknown')

    # 健康状态图标
    health_icon = {'ok': '🟢', 'degraded': '🟡', 'unreachable': '🔴'}.get(health, '⚪')

    # 任务状态分布
    tasks = status_data.get('tasks', [])
    running = len([t for t in tasks if t.get('status') == 'running'])
    waiting = len([t for t in tasks if t.get('status') in ('waiting_approval', 'waiting_decision')])
    failed = len([t for t in tasks if t.get('status') == 'failed'])

    # 待决策任务列表
    decision_tasks = [t for t in tasks if t.get('decision_pending')]
    decision_text = ''
    if decision_tasks:
        names = ', '.join(f"{t.get('name', '未知')}" for t in decision_tasks[:3])
        decision_text = f"\n⚠️ 待决策: {names}"

    # 卡片 JSON
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"📊 Agentic OS 系统状态 [{health}]"},
                "template": "blue" if health == "ok" else ("red" if health == "unreachable" else "orange")
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**总任务**: {total} | **完成**: {completed} | **进行中**: {running}\n"
                            f"{health_icon} **系统**: {health} | ⚠️ **待决策**: {pending}{decision_text}"
                        )
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "note",
                    "elements": [{
                        "tag": "plain_text",
                        "content": f"⏰ 下次推送: 30 分钟后 | 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    }]
                }
            ]
        }
    }

    # 如果有失败任务，添加警告
    if failed:
        failed_names = ', '.join(t.get('name', '未知') for t in tasks if t.get('status') == 'failed')
        card['card']['elements'].insert(1, {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"❌ **失败 ({failed})**: {failed_names}"
            }
        })
        card['card']['header']['template'] = 'red'

    return card


def send_to_feishu(card_json, channel="运营指挥部"):
    """推送到飞书群"""
    import urllib.request
    webhook_url = config.get_feishu_webhook(channel)
    if not webhook_url:
        print(f"❌ 飞书 Webhook 未配置: {channel}")
        return False

    data = json.dumps(card_json).encode('utf-8')
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get('code') == 0:
                print(f"✅ 已推送到飞书 [{channel}]")
                return True
            else:
                print(f"⚠️ 飞书返回异常: {result}")
                return False
    except Exception as e:
        print(f"❌ 推送失败: {e}")
        return False


def push_once(test_mode=False):
    """执行一次推送"""
    status = fetch_status()
    card = build_card(status)

    if test_mode:
        print("=== 测试模式：飞书卡片 JSON ===")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return True

    return send_to_feishu(card)


def run_daemon(interval_minutes=30):
    """守护模式：定时循环推送"""
    print(f"🔄 飞书状态推送守护模式启动，间隔 {interval_minutes} 分钟")
    while True:
        try:
            push_once()
        except Exception as e:
            print(f"❌ 推送异常: {e}")
        print(f"⏰ 下次推送: {interval_minutes} 分钟后...")
        time.sleep(interval_minutes * 60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='飞书状态推送')
    parser.add_argument('--test', action='store_true', help='测试模式（打印 JSON 不发飞书）')
    parser.add_argument('--daemon', action='store_true', help='守护模式（循环推送）')
    parser.add_argument('--interval', type=int, default=30, help='推送间隔（分钟，默认 30）')
    parser.add_argument('--channel', default='运营指挥部', help='飞书群频道')
    args = parser.parse_args()

    if args.daemon:
        run_daemon(args.interval)
    else:
        push_once(args.test)
