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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)