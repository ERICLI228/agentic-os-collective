#!/usr/bin/env python3
"""P2 测试 - 验证路由校验机制"""
from shared.skill_registry.skill_loader import validate_task_skill

# 测试用例 1：TK 任务被错误调度到 drama 脚本（应该被拦截）
task_id = 'TK-20260423-002'
skill_name = 'water-margin-drama'

print(f"测试：{task_id} → {skill_name}")
ok, reason = validate_task_skill(task_id, skill_name)

if not ok:
    print(f'✅ 路由被正确拦截：{reason}')
    
    # 发送飞书 P0 告警
    from shared.config import config
    import requests
    
    alert_msg = {
        'msg_type': 'text',
        'content': {
            'text': f'🚨 P0 路由错误告警\n任务：{task_id}\n错误：{reason}\n时间：2026-04-23\n状态：已拦截，未执行'
        }
    }
    
    try:
        r = requests.post(config.FEISHU_WEBHOOK_URL, json=alert_msg, timeout=10)
        if r.status_code == 200:
            print('✅ 飞书 P0 告警已发送')
        else:
            print(f'⚠️ 告警发送失败：{r.status_code}')
    except Exception as e:
        print(f'⚠️ 告警发送异常：{e}')
else:
    print(f'❌ 路由校验失败：应该拦截但未拦截')

# 测试用例 2：TK 任务正确调度到 claw-operator（应该通过）
print("\n测试：TK-20260423-002 → claw-operator")
ok, reason = validate_task_skill('TK-20260423-002', 'claw-operator')
if ok:
    print(f'✅ 正确路由通过：{reason}')
else:
    print(f'❌ 错误：{reason}')
