#!/usr/bin/env python3
"""
Dashboard API v2 - 支持多项目 KPI 聚合与决策处理
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

WORKSPACE = Path.home() / ".openclaw/workspace"
ACTIVE_DIR = WORKSPACE / "tasks/active"
COMPLETED_DIR = WORKSPACE / "tasks/completed"
PROGRESS_LOG = WORKSPACE / "tasks/progress.txt"
MEMORY_DIR = WORKSPACE / "memory"
TOKEN_BUDGET_FILE = Path.home() / ".openclaw/data/token_budget.json"

def load_token_budget():
    try:
        with open(TOKEN_BUDGET_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"drama": {"used": 0, "limit": 400000}, "tk": {"used": 0, "limit": 600000}}

def count_tasks(project_id=None, status=None):
    tasks = []
    if not ACTIVE_DIR.exists():
        return tasks
    for f in ACTIVE_DIR.glob("*.json"):
        try:
            with open(f, 'r') as fp:
                t = json.load(fp)
                if project_id and t.get('project_id') != project_id:
                    continue
                if status and t.get('status') != status:
                    continue
                tasks.append(t)
        except:
            continue
    return tasks

@app.route('/api/dashboard', methods=['GET'])
def dashboard_data():
    project_id = request.args.get('project', 'all')
    budget = load_token_budget()
    
    drama_tasks = len(count_tasks('drama', 'running'))
    tk_tasks = len(count_tasks('tk', 'running'))
    
    pending_decisions = 0
    for t in count_tasks():
        for d in t.get('decision_points', []):
            if d.get('status') == 'pending':
                pending_decisions += 1
    
    data = {
        'kpi': {
            'drama': {'running': drama_tasks, 'budget_used': budget.get('drama', {}).get('used', 0), 'budget_limit': budget.get('drama', {}).get('limit', 400000)},
            'tk': {'running': tk_tasks, 'budget_used': budget.get('tk', {}).get('used', 0), 'budget_limit': budget.get('tk', {}).get('limit', 600000)}
        },
        'alerts': [],
        'pending_decisions': pending_decisions,
        'active_tasks': [t for t in count_tasks() if (project_id == 'all' or t.get('project_id') == project_id)][:20]
    }
    return jsonify(data)

@app.route('/api/decision/<task_id>/<decision_id>', methods=['POST'])
def resolve_decision(task_id, decision_id):
    data = request.json
    choice = data.get('choice')
    task_file = ACTIVE_DIR / f"{task_id}.json"
    
    if not task_file.exists():
        return jsonify({'error': 'Task not found'}), 404
    
    with open(task_file, 'r+') as f:
        task = json.load(f)
        
        # 1. 找到并更新决策点
        decision_question = ""
        decision_updated = False
        for d in task.get('decision_points', []):
            if d.get('id') == decision_id:
                d['status'] = 'resolved'
                d['resolution'] = choice
                d['resolved_at'] = datetime.now().isoformat()
                decision_question = d.get('question', "")
                decision_updated = True
                break
        
        if not decision_updated:
            return jsonify({'error': 'Decision not found'}), 404
        
        # 2. 决策通过时，联动更新对应里程碑
        milestone_updated = False
        if choice == '通过':
            for m in task.get('milestones', []):
                # 规则：决策问题包含"审核"时，自动完成"审核"相关里程碑
                if '审核' in decision_question and '审核' in m.get('name', ''):
                    m['status'] = 'completed'
                    m['completed_at'] = datetime.now().isoformat()
                    milestone_updated = True
                # 如果决策是"剧本筛选"，完成第一个里程碑
                elif '剧本筛选' in decision_question and '剧本' in m.get('name', ''):
                    m['status'] = 'completed'
                    m['completed_at'] = datetime.now().isoformat()
                    milestone_updated = True
                # 如果决策是"角色设计"，完成角色相关里程碑
                elif '角色设计' in decision_question and '角色' in m.get('name', ''):
                    m['status'] = 'completed'
                    m['completed_at'] = datetime.now().isoformat()
                    milestone_updated = True
        
        # 3. 如果所有里程碑都完成了，自动更新任务状态
        if task.get('milestones'):
            all_done = all(m.get('status') == 'completed' for m in task['milestones'])
            if all_done:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
        
        f.seek(0)
        json.dump(task, f, ensure_ascii=False, indent=2)
        f.truncate()
    
    # 4. 创建决策事件文件
    event_file = Path.home() / ".openclaw/workspace/events/decision_received.json"
    event_file.parent.mkdir(parents=True, exist_ok=True)
    with open(event_file, 'w') as ef:
        json.dump({
            'task_id': task_id,
            'decision_id': decision_id,
            'choice': choice,
            'milestone_updated': milestone_updated,
            'timestamp': datetime.now().isoformat()
        }, ef)
    
    return jsonify({
        'status': 'ok', 
        'triggered': True,
        'milestone_updated': milestone_updated,
        'task_status': task.get('status')
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/insights', methods=['GET'])
def cross_project_insights():
    return jsonify({
        'insights': [
            {'source': 'tk', 'target': 'drama', 'suggestion': '手机壳搜索量+230% → 短剧选题《穿越卖手机壳》', 'action': 'create_task'}
        ]
    })

if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    try:
        from shared.config import config
        host = config.API_HOST
        port = config.API_PORT
    except ImportError:
        host = os.environ.get("API_HOST", "127.0.0.1")
        port = int(os.environ.get("API_PORT", "5001"))
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    app.run(host=host, port=port, debug=False)