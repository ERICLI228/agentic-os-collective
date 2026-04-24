#!/usr/bin/env python3
"""测试飞书 Webhook 连通性"""
from shared.config import config
import requests

msg = {
    'msg_type': 'text',
    'content': {
        'text': '🧪 Agentic OS 连通性测试：飞书 Webhook 配置成功！\n时间：2026-04-23\n测试类型：P1 验收'
    }
}

try:
    r = requests.post(config.FEISHU_WEBHOOK_URL, json=msg, timeout=10)
    if r.status_code == 200:
        print('✅ 发送成功 - 飞书群已收到测试消息')
    else:
        print(f'❌ 失败：{r.status_code} {r.text}')
except Exception as e:
    print(f'❌ 异常：{e}')
