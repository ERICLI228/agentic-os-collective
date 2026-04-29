#!/usr/bin/env python3
"""
智能任务创建向导 API
包含智能推荐、内容引导、参数建议
"""
import json
import yaml
import re
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

WORKSPACE = Path.home() / "agentic-os-collective"
KNOWLEDGE_FILE = WORKSPACE / "shared/knowledge/best_practices.yaml"
TEMPLATES_DIR = WORKSPACE / "shared/templates"
ACTIVE_DIR = Path.home() / ".openclaw/workspace/tasks/active"

def load_knowledge():
    """加载知识库"""
    try:
        with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except:
        return {}

def validate_title(title: str) -> dict:
    """验证任务标题"""
    result = {'valid': True, 'errors': [], 'suggestions': []}
    
    # 长度检查
    if len(title) > 50:
        result['valid'] = False
        result['errors'].append(f"标题过长，不能超过50字符 (当前{len(title)})")
    
    # 特殊字符检查
    special_chars = re.findall(r'[!@#$%^&*()_+=\[\]{}|\\,./<>?]', title)
    if special_chars:
        result['valid'] = False
        result['errors'].append(f"包含特殊字符: {''.join(set(special_chars))}")
    
    # 建议生成
    if not result['errors']:
        if 'drama' in title.lower() or '短剧' in title or '武松' in title or '水浒' in title:
            result['suggestions'].append("建议添加 DS- 前缀")
            result['suggestions'].append("格式: DS-[主题]-[YYYYMMDD]-[序号]")
        elif 'tk' in title.lower() or 'tiktok' in title or '运营' in title:
            result['suggestions'].append("建议添加 TK- 前缀")
            result['suggestions'].append("格式: TK-[地区]-[品类]-[YYYYMMDD]-[序号]")
    
    return result

def recommend_template(topic: str, category: str) -> dict:
    """根据主题推荐模板"""
    knowledge = load_knowledge()
    
    # 关键词匹配
    drama_keywords = ['短剧', '剧本', '视频', '水浒', '武松', '潘金莲', '角色', '配音']
    tk_keywords = ['运营', 'tk', 'tiktok', '监控', '爆款', '数据', '分析', '3c', '品类']
    
    if category == 'drama' or any(k in topic for k in drama_keywords):
        best_practice = knowledge.get('short剧制作最佳实践', {})
        return {
            'template': 'drama_pipeline',
            'name': 'AI数字短剧制作流水线',
            'description': best_practice.get('描述', '水浒传AI数字短剧全自动制作'),
            'time_estimate': best_practice.get('时间预估', '30分钟-2小时'),
            'best_practices': best_practice.get('最佳实践', []),
            'common_issues': best_practice.get('常见问题', []),
            'params': best_practice.get('建议参数', {})
        }
    else:
        best_practice = knowledge.get('TK运营最佳实践', {})
        return {
            'template': 'tk_pipeline', 
            'name': 'TK东南亚3C运营流水线',
            'description': best_practice.get('描述', 'TikTok东南亚5国3C自动运营'),
            'time_estimate': best_practice.get('时间预估', '实时-1小时'),
            'best_practices': best_practice.get('最佳实践', []),
            'common_issues': best_practice.get('常见问题', []),
            'params': best_practice.get('建议参数', {})
        }

def get_description_guide(category: str) -> list:
    """获取描述填写指引"""
    if category == 'drama':
        return [
            '明确剧本主题（如：复仇、穿越、甜宠）',
            '说明目标受众和风格定位',
            '指定集数和每集时长',
            '列出主要角色和声线要求',
            '标注敏感内容或需改写部分'
        ]
    else:
        return [
            '指定运营品类（如：3C配件、 美妆）',
            '说明目标市场（印尼/越南/泰国等）',
            '设定爆款判定阈值',
            '明确数据上报频率',
            '指定告警通知群'
        ]

# ========== API 端点 ==========

@app.route('/api/task/wizard/validate-title', methods=['POST'])
def api_validate_title():
    data = request.json
    return jsonify(validate_title(data.get('title', '')))

@app.route('/api/task/wizard/recommend', methods=['POST'])
def api_recommend():
    data = request.json
    topic = data.get('topic', '')
    category = data.get('category', 'drama')
    return jsonify(recommend_template(topic, category))

@app.route('/api/task/wizard/description-guide', methods=['GET'])
def api_description_guide():
    category = request.args.get('category', 'drama')
    return jsonify({'guide': get_description_guide(category)})

@app.route('/api/task/wizard/knowledge', methods=['GET'])
def api_knowledge():
    """获取完整知识库"""
    return jsonify(load_knowledge())

@app.route('/api/task/wizard/create', methods=['POST'])
def api_create_task():
    """创建任务（向导模式）"""
    data = request.json
    
    title = data.get('title', '')
    description = data.get('description', '')
    category = data.get('category', 'drama')
    template = data.get('template', 'drama_pipeline' if category == 'drama' else 'tk_pipeline')
    
    # 验证标题
    validation = validate_title(title)
    if not validation['valid']:
        return jsonify({'error': validation['errors'][0]}), 400
    
    # 生成任务ID
    prefix = 'DS' if category == 'drama' else 'TK'
    date_str = datetime.now().strftime('%Y%m%d')
    existing = len(list(ACTIVE_DIR.glob(f'{prefix}{date_str}*')))
    task_id = f'{prefix}-{date_str}-{existing+1:03d}'
    
    # 加载模板
    template_file = TEMPLATES_DIR / f'{template}.json'
    if template_file.exists():
        with open(template_file) as f:
            template_data = json.load(f)
    else:
        template_data = {'stages': []}
    
    # 构建任务
    task = {
        'id': task_id,
        'project_id': category,
        'name': title,
        'description': description,
        'template': template,
        'priority': 'P1',
        'status': 'created',
        'created_at': datetime.now().isoformat(),
        'milestones': [
            {
                'id': s['id'],
                'name': s['name'],
                'status': 'pending',
                'executor': s.get('executor', 'OpenClaw'),
                'expected_artifacts': s.get('expected_artifacts', [])
            }
            for s in template_data.get('stages', [])
        ],
        'decision_points': [],
        'artifacts': []
    }
    
    # 保存任务
    task_file = ACTIVE_DIR / f'{task_id}.json'
    with open(task_file, 'w') as f:
        json.dump(task, f, ensure_ascii=False, indent=2)
    
    return jsonify({'task_id': task_id, 'task': task})

# ========== V3.5 新增：系统状态 + 决策接口 ==========

def _load_all_tasks():
    """加载所有活跃任务"""
    tasks = []
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    for f in sorted(ACTIVE_DIR.glob('*.json')):
        try:
            with open(f) as fh:
                tasks.append(json.load(fh))
        except Exception:
            pass
    return tasks


@app.route('/api/status', methods=['GET'])
def api_status():
    """系统状态总览 — v3.5 新增"""
    tasks = _load_all_tasks()
    tasks_list = []
    decision_pending_count = 0
    for t in tasks:
        status = t.get('status', 'unknown')
        is_pending = status in ('waiting_approval', 'waiting_decision')
        if is_pending:
            decision_pending_count += 1
        tasks_list.append({
            'id': t.get('id'),
            'name': t.get('name'),
            'status': status,
            'decision_pending': is_pending,
            'priority': t.get('priority', 'P1'),
            'created_at': t.get('created_at', ''),
            'milestones': [
                {'id': m.get('id', ''), 'name': m.get('title', m.get('name', '')), 'status': m.get('status', 'pending')}
                for m in t.get('milestones', [])
            ]
        })

    # 里程碑状态（从任务中提取决策点）
    milestones = []
    for t in tasks:
        for dp in t.get('decision_points', []):
            milestones.append({
                'task_id': t.get('id'),
                'ms': dp.get('id', dp.get('milestone_id', '')),
                'name': dp.get('name', ''),
                'decision_point': True,
                'locked': dp.get('status') != 'approved'
            })

    # 系统健康检查
    health_checks = {
        'api': 'ok',
        'database': 'ok',
        'knowledge': 'ok' if (WORKSPACE / 'shared/knowledge/best_practices.yaml').exists() else 'missing'
    }
    system_health = 'ok' if all(v == 'ok' for v in health_checks.values()) else 'degraded'

    return jsonify({
        'tasks': tasks_list,
        'total': len(tasks_list),
        'completed': len([t for t in tasks_list if t['status'] == 'completed']),
        'decision_pending': decision_pending_count,
        'milestones': milestones,
        'system_health': system_health,
        'health_checks': health_checks,
        'timestamp': datetime.now().isoformat()
    })


def _find_task_file(task_id: str):
    """按 task_id 查找任务文件（文件名可能与 id 不同）"""
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    # 先试精确匹配
    exact = ACTIVE_DIR / f'{task_id}.json'
    if exact.exists():
        return exact
    # 再遍历所有 JSON 文件匹配 id 字段
    for f in ACTIVE_DIR.glob('*.json'):
        try:
            with open(f) as fh:
                data = json.load(fh)
                if data.get('id') == task_id:
                    return f
        except Exception:
            pass
    return None


@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    """驾驶舱仪表盘 — v3.5 新增（CommandCenter.vue 的数据接口）"""
    status_data = api_status().get_json()
    tasks_data = api_list_tasks().get_json()

    # 补充 milestones 数据
    milestones_path = Path.home() / ".agentic-os/milestones.json"
    milestones = []
    if milestones_path.exists():
        with open(milestones_path) as f:
            ms_data = json.load(f)
        for mid, ms in ms_data.get("milestones", {}).items():
            milestones.append({
                "id": mid,
                "name": ms.get("name", mid),
                "status": ms.get("status", "pending"),
                "decision_point": ms.get("decision_point", False),
                "decision": ms.get("decision"),
            })

    return jsonify({
        "total": status_data.get("total", 0),
        "running": len([t for t in status_data.get("tasks", []) if t.get("status") == "running"]),
        "completed": status_data.get("completed", 0),
        "pending": len([t for t in status_data.get("tasks", []) if t.get("status") == "pending"]),
        "failed": len([t for t in status_data.get("tasks", []) if t.get("status") == "failed"]),
        "decision_pending": status_data.get("decision_pending", 0),
        "tasks": tasks_data.get("tasks", []),
        "milestones": milestones,
        "system_health": status_data.get("system_health", "unknown"),
        "timestamp": status_data.get("timestamp", ""),
    })


@app.route('/api/decision', methods=['POST'])
def api_decision():
    """人工审批接口 — v3.5 新增

    请求体:
    {
        "task_id": "TK-20260429-001",
        "action": "approved" | "rejected" | "modify",
        "reason": "可选备注"
    }
    """
    data = request.json
    task_id = data.get('task_id', '')
    action = data.get('action', '')
    reason = data.get('reason', '')

    if not task_id or action not in ('approved', 'rejected', 'modify'):
        return jsonify({'error': '需要 task_id 和 action (approved/rejected/modify)'}), 400

    task_file = _find_task_file(task_id)
    if not task_file:
        return jsonify({'error': f'任务 {task_id} 不存在'}), 404

    with open(task_file) as f:
        task = json.load(f)

    # 更新状态
    if action == 'approved':
        task['human_approved'] = True
        task['decision_status'] = 'approved'
        task['status'] = 'approved' if task.get('status') == 'waiting_approval' else task.get('status')
    elif action == 'rejected':
        task['human_approved'] = False
        task['decision_status'] = 'rejected'
        task['status'] = 'rejected'
    else:  # modify
        task['decision_status'] = 'modify_requested'
        task['status'] = 'waiting_modification'

    task['decision_at'] = datetime.now().isoformat()
    task['decision_reason'] = reason
    task['decision_by'] = 'human'

    with open(task_file, 'w') as f:
        json.dump(task, f, ensure_ascii=False, indent=2)

    return jsonify({
        'task_id': task_id,
        'action': action,
        'status': task['status'],
        'human_approved': task.get('human_approved'),
        'timestamp': datetime.now().isoformat()
    })


# 兼容旧版 task_wizard 入口
@app.route('/api/tasks', methods=['GET'])
def api_list_tasks():
    """任务列表（兼容别名，指向 /api/status）"""
    return api_status()


if __name__ == '__main__':
    from shared.config import config
    app.run(host=config.API_HOST, port=config.API_PORT, debug=False)