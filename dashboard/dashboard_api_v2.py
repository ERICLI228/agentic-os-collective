#!/usr/bin/env python3
"""
Dashboard API v2 - 支持多项目 KPI 聚合与决策处理
增强：日志轮转、决策超时告警
"""
import json
import os
import subprocess
import threading
import time
import requests
try:
    import yaml
except ImportError:
    yaml = None
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, jsonify, request, send_file, abort
from flask_cors import CORS

# 新增：工作流模板和执行详情
TEMPLATES_DIR = Path.home() / "agentic-os-collective/shared/templates"
EXEC_LOGS_DIR = Path.home() / "agentic-os-collective/shared/logs/executions"

# 决策超时设置 (小时)
DECISION_TIMEOUT_HOURS = 24
DECISION_CHECK_INTERVAL = 3600  # 1小时检查一次

app = Flask(__name__)
CORS(app)

WORKSPACE = Path.home() / ".openclaw/workspace"
ACTIVE_DIR = WORKSPACE / "tasks/active"
COMPLETED_DIR = WORKSPACE / "tasks/completed"
PROGRESS_LOG = WORKSPACE / "tasks/progress.txt"
MEMORY_DIR = WORKSPACE / "memory"
TOKEN_BUDGET_FILE = Path.home() / ".openclaw/data/token_budget.json"

# 飞书告警 Webhook (技术研发群)
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/148cb666-4573-4ef6-a03e-a9008b0c972c"

def send_feishu_alert(message: str):
    """发送飞书告警"""
    try:
        payload = {
            "msg_type": "text",
            "content": {"text": f"🤖 Agentic OS 告警\n{message}"}
        }
        requests.post(FEISHU_WEBHOOK, json=payload, timeout=5)
    except Exception as e:
        print(f"飞书告警失败: {e}")

def check_decision_timeouts():
    """检查决策超时 - 后台线程"""
    while True:
        try:
            for task_file in ACTIVE_DIR.glob("*.json"):
                with open(task_file) as f:
                    task = json.load(f)
                
                for dp in task.get('decision_points', []):
                    if dp.get('status') == 'pending':
                        # 检查创建时间
                        created = task.get('created_at', '')
                        if created:
                            try:
                                created_time = datetime.fromisoformat(created.replace('Z', '+00:00'))
                                age_hours = (datetime.now() - created_time.replace(tzinfo=None)).total_seconds() / 3600
                                
                                if age_hours > DECISION_TIMEOUT_HOURS:
                                    msg = f"⏰ 决策超时告警！\n任务: {task['id']}\n决策: {dp.get('question', 'N/A')}\n已等待: {age_hours:.1f}小时"
                                    send_feishu_alert(msg)
                                    print(msg)
                            except:
                                pass
        except Exception as e:
            print(f"决策超时检查失败: {e}")
        
        time.sleep(DECISION_CHECK_INTERVAL)

# 启动决策超时监控线程
timeout_thread = threading.Thread(target=check_decision_timeouts, daemon=True)
timeout_thread.start()

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
    
    # 扫描根目录和项目子目录
    search_dirs = [ACTIVE_DIR]
    for subdir in ['drama', 'tk']:
        sub = ACTIVE_DIR / subdir
        if sub.exists():
            search_dirs.append(sub)
    
    for search_dir in search_dirs:
        for f in search_dir.glob("*.json"):
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
    print(f'DEBUG: task_id={task_id}, decision_id={decision_id}')
    data = request.json
    choice = data.get('decision_type') or data.get('choice')
    print(f'DEBUG: choice={choice}')
    # 搜索所有任务目录
    search_dirs = [ACTIVE_DIR, ACTIVE_DIR / 'drama', ACTIVE_DIR / 'tk']
    task_file = None
    for search_dir in search_dirs:
        tf = search_dir / f"{task_id}.json"
        if tf.exists():
            task_file = tf
            break
    
    if not task_file:
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

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """获取所有任务列表（活跃 + 完成）"""
    tasks = []
    
    # 扫描活跃任务
    if ACTIVE_DIR.exists():
        for task_file in ACTIVE_DIR.glob('*.json'):
            try:
                with open(task_file) as f:
                    task = json.load(f)
                    task['_source'] = 'active'
                    tasks.append(task)
            except Exception as e:
                print(f"Error loading {task_file}: {e}")
    
    # 扫描完成任务
    if COMPLETED_DIR.exists():
        for task_file in COMPLETED_DIR.glob('*.json'):
            try:
                with open(task_file) as f:
                    task = json.load(f)
                    task['_source'] = 'completed'
                    tasks.append(task)
            except Exception as e:
                print(f"Error loading {task_file}: {e}")
    
    # 按更新时间排序
    tasks.sort(key=lambda x: x.get('updated_at', x.get('created_at', '')), reverse=True)
    
    return jsonify({
        'status': 'ok',
        'tasks': tasks,
        'total': len(tasks),
        'active_count': len([t for t in tasks if t.get('_source') == 'active']),
        'completed_count': len([t for t in tasks if t.get('_source') == 'completed'])
    })

# ========== 执行透明性新增端点 ==========

@app.route('/api/templates', methods=['GET'])
def list_templates():
    """获取可用工作流模板"""
    templates = []
    # 优先JSON，备选YAML
    for ext in ['.json', '.yaml', '.yml']:
        if TEMPLATES_DIR.exists():
            for f in TEMPLATES_DIR.glob(f'*{ext}'):
                try:
                    if ext == '.json':
                        with open(f) as fp:
                            data = json.load(fp)
                    elif yaml:
                        with open(f) as fp:
                            data = yaml.safe_load(fp)
                    else:
                        continue
                    templates.append({
                        'id': f.stem,
                        'name': data.get('name', f.stem),
                        'project': data.get('project', 'unknown'),
                        'stages_count': len(data.get('stages', [])),
                        'description': data.get('description', '')
                    })
                except:
                    continue
    return jsonify({'templates': templates})

@app.route('/api/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    """获取指定模板详情"""
    # 优先JSON
    for ext in ['.json', '.yaml', '.yml']:
        template_file = TEMPLATES_DIR / f"{template_id}{ext}"
        if template_file.exists():
            try:
                if ext == '.json':
                    with open(template_file) as f:
                        data = json.load(f)
                elif yaml:
                    with open(template_file) as f:
                        data = yaml.safe_load(f)
                else:
                    continue
                return jsonify(data)
            except:
                continue
    return jsonify({'error': 'Template not found'}), 404

@app.route('/api/tasks/<task_id>/milestone/<milestone_id>', methods=['GET'])



def get_milestone_execution(task_id, milestone_id):
    """获取里程碑执行详情"""
    # 1. 从任务文件读取
    task_file = ACTIVE_DIR / f"{task_id}.json"
    milestone_details = None
    
    if task_file.exists():
        with open(task_file) as f:
            task = json.load(f)
            for m in task.get('milestones', []):
                if m.get('id') == milestone_id:
                    # 合并execution_details
                    details = m.copy()
                    # 尝试读取日志文件
                    log_file = EXEC_LOGS_DIR / f"{task_id}_{milestone_id}.log"
                    if log_file.exists():
                        with open(log_file) as lf:
                            details['log_content'] = lf.read()[:5000]
                    milestone_details = details
                    break
    
    return jsonify({
        'task_id': task_id,
        'milestone_id': milestone_id,
        'milestone': milestone_details
    })

@app.route('/api/tasks/create', methods=['POST'])
def create_task():
    """创建新任务"""
    data = request.json
    template_id = data.get('template')
    project = data.get('project', 'drama')
    title = data.get('title', '新任务')
    description = data.get('description', '')
    
    # 获取模板 - 优先JSON
    template = None
    for ext in ['.json', '.yaml', '.yml']:
        template_file = TEMPLATES_DIR / f"{template_id}{ext}"
        if template_file.exists():
            try:
                if ext == '.json':
                    with open(template_file) as f:
                        template = json.load(f)
                elif yaml:
                    with open(template_file) as f:
                        template = yaml.safe_load(f)
                break
            except:
                continue
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    # 生成任务ID
    task_id = f"{project.upper()}-{datetime.now().strftime('%Y%m%d')}-{len(list(ACTIVE_DIR.glob(f'{project.upper()}-*')))+1:03d}"
    
    # 构建任务结构
    task = {
        'id': task_id,
        'project_id': project,
        'name': title,
        'description': description,
        'template': template_id,
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
            for s in template.get('stages', [])
        ],
        'decision_points': [
            {
                'id': f"DP-{s['id']}",
                'milestone_id': s['id'],
                'question': s.get('question', ''),
                'options': s.get('options', []),
                'status': 'pending' if s.get('decision_point') else 'auto'
            }
            for s in template.get('stages', [])
            if s.get('decision_point')
        ],
        'artifacts': []
    }
    
    # 保存任务到项目子目录
    project_dir = ACTIVE_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # 同时保存到根目录（兼容）和项目子目录
    task_file = ACTIVE_DIR / f"{task_id}.json"
    task_file_project = project_dir / f"{task_id}.json"
    
    for tf in [task_file, task_file_project]:
        with open(tf, 'w') as f:
            json.dump(task, f, ensure_ascii=False, indent=2)
    
    return jsonify({'task_id': task_id, 'task': task})

@app.route('/api/tasks/<task_id>/execute/<milestone_id>', methods=['POST'])
def execute_milestone(task_id, milestone_id):
    """执行里程碑"""
    task_file = ACTIVE_DIR / f"{task_id}.json"
    if not task_file.exists():
        return jsonify({'error': 'Task not found'}), 404
    
    with open(task_file) as f:
        task = json.load(f)
    
    # 找到对应阶段
    template_id = task.get('template', 'drama_pipeline')
    command = None
    
    # 获取模板
    for ext in ['.json', '.yaml', '.yml']:
        template_file = TEMPLATES_DIR / f"{template_id}{ext}"
        if template_file.exists():
            try:
                if ext == '.json':
                    with open(template_file) as f:
                        template = json.load(f)
                elif yaml:
                    with open(template_file) as f:
                        template = yaml.safe_load(f)
                for s in template.get('stages', []):
                    if s['id'] == milestone_id:
                        command = s.get('command', '').format(task_id=task_id)
                        break
                break
            except:
                continue
    
    if not command:
        return jsonify({'error': 'Command not found in template'}), 400
    
    # 执行命令
    start = datetime.now()
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=600)
    duration = (datetime.now() - start).total_seconds()
    
    # 记录执行详情
    EXEC_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = EXEC_LOGS_DIR / f"{task_id}_{milestone_id}.log"
    with open(log_file, 'w') as f:
        f.write(f"COMMAND: {command}\n")
        f.write(f"DURATION: {duration:.2f}s\n")
        f.write(f"STATUS: {'completed' if result.returncode == 0 else 'failed'}\n")
        f.write("=" * 60 + "\nSTDOUT:\n")
        f.write(result.stdout)
        if result.stderr:
            f.write("\n" + "=" * 60 + "\nSTDERR:\n")
            f.write(result.stderr)
    
    # 更新任务状态
    with open(task_file, 'r+') as f:
        task = json.load(f)
        for m in task.get('milestones', []):
            if m['id'] == milestone_id:
                m['status'] = 'completed' if result.returncode == 0 else 'failed'
                m['execution_details'] = {
                    'command': command,
                    'duration': round(duration, 2),
                    'return_code': result.returncode,
                    'stdout_preview': result.stdout[:1000],
                    'stderr_preview': result.stderr[:500],
                    'log_file': str(log_file)
                }
                break
        
        # 检查是否所有里程碑完成
        if all(m.get('status') == 'completed' for m in task.get('milestones', [])):
            task['status'] = 'completed'
        
        f.seek(0)
        json.dump(task, f, ensure_ascii=False, indent=2)
        f.truncate()
    
    return jsonify({
        'status': 'completed' if result.returncode == 0 else 'failed',
        'duration': duration,
        'returncode': result.returncode,
        'stdout': result.stdout[:500],
        'stderr': result.stderr[:200]
    })

@app.route('/api/insights', methods=['GET'])
def cross_project_insights():
    return jsonify({
        'insights': [
            {'source': 'tk', 'target': 'drama', 'suggestion': '手机壳搜索量+230% → 短剧选题《穿越卖手机壳》', 'action': 'create_task'}
        ]
    })

# 视频输出目录
DRAMA_OUTPUT_DIR = Path.home() / ".openclaw/skills/water-margin-drama/output"
WORKSPACE_DIR = Path.home() / ".openclaw/workspace"

@app.route('/api/download', methods=['GET'])
def download_file():
    """文件下载 API"""
    filepath = request.args.get('path', '')
    filename = request.args.get('name', '')
    
    if not filepath and not filename:
        return jsonify({'error': 'Missing path or name parameter'}), 400
    
    # 搜索可能存在的文件
    search_dirs = [
        DRAMA_OUTPUT_DIR,
        Path.home() / "drama/output",
        Path.home() / ".openclaw/drama/output",
        WORKSPACE_DIR / "dramas",
        Path.home() / "Downloads"
    ]
    
    # 如果只提供文件名，搜索所有目录
    if filename and not filepath:
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for f in search_dir.rglob(filename):
                if f.is_file() and f.stat().st_size > 1000:  # 忽略测试文件
                    return send_file(f, as_attachment=True)
        return jsonify({'error': f'File not found: {filename}'}), 404
    
    # 如果提供完整路径
    if filepath:
        full_path = Path(filepath)
        if full_path.exists() and full_path.is_file():
            if full_path.stat().st_size < 1000:
                return jsonify({'error': '测试文件无法下载'}), 400
            return send_file(full_path, as_attachment=True)
        
        # 尝试在搜索目录中查找
        for search_dir in search_dirs:
            test_path = search_dir / full_path.name
            if test_path.exists() and test_path.is_file():
                if test_path.stat().st_size < 1000:
                    return jsonify({'error': '测试文件无法下载'}), 400
                return send_file(test_path, as_attachment=True)
    
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    # ========== 第八阶段：智能向导端点 ==========
    
    @app.route('/api/task/wizard/validate-title', methods=['POST'])
    def validate_title():
        """验证任务标题"""
        data = request.json or {}
        title = data.get('title', '')
        
        result = {'valid': True, 'errors': [], 'suggestions': []}
        
        # 长度检查
        if len(title) > 50:
            result['valid'] = False
            result['errors'].append(f"标题过长，不能超过50字符 (当前{len(title)})")
        
        # 特殊字符
        import re
        special_chars = re.findall(r'[!@#$%^&*()_+=\[\]{}|\\,./<>?]', title)
        if special_chars:
            result['valid'] = False
            result['errors'].append(f"包含特殊字符: {''.join(set(special_chars))}")
        
        # 建议
        if not result['errors']:
            if 'drama' in title.lower() or '短剧' in title or '水浒' in title:
                result['suggestions'].append("建议添加 DS- 前缀")
                result['suggestions'].append("格式: DS-[主题]-[YYYYMMDD]-[序号]")
            elif 'tk' in title.lower() or '运营' in title:
                result['suggestions'].append("建议添加 TK- 前缀")
        
        return jsonify(result)
    
    @app.route('/api/task/wizard/recommend', methods=['POST'])
    def recommend_template():
        """智能推荐模板"""
        data = request.json or {}
        topic = data.get('topic', '')
        category = data.get('category', 'drama')
        
        # 知识库
        drama_keywords = ['短剧', '剧本', '视频', '水浒', '武松', '角色', '配音']
        tk_keywords = ['运营', 'tk', 'tiktok', '监控', '爆款', '数据', '3c']
        
        if category == 'drama' or any(k in topic for k in drama_keywords):
            return jsonify({
                'template': 'drama_pipeline',
                'name': 'AI数字短剧制作流水线',
                'description': '水浒传AI数字短剧全自动制作',
                'time_estimate': '30分钟-2小时',
                'best_practices': [
                    '使用结构化剧本格式',
                    '提前设计角色声线',
                    '预留人工审核节点',
                    '视频与音频分离制作'
                ],
                'params': {
                    '剧本筛选': '候选3-5个,质量评分>7.5',
                    '争议检测': '政治/色情/暴力/谣言',
                    '角色设计': '3-5个角色,性格鲜明',
                    '视频生成': '1-3分钟,1080p'
                }
            })
        else:
            return jsonify({
                'template': 'tk_pipeline',
                'name': 'TK东南亚3C运营流水线',
                'description': 'TikTok东南亚5国3C自动运营',
                'time_estimate': '实时-1小时',
                'best_practices': [
                    '关注ASMR/清洁类视频',
                    '定制类产品受欢迎',
                    '美观展示+音乐效果佳'
                ],
                'params': {
                    '品类监控': '每2小时更新',
                    '爆款阈值': '播放量>300万',
                    '数据维度': '播放/点赞/评论'
                }
            })
    
    @app.route('/api/task/wizard/description-guide', methods=['GET'])
    def description_guide():
        """获取描述填写指引"""
        category = request.args.get('category', 'drama')
        if category == 'drama':
            guide = [
                '明确剧本主题（如：复仇、穿越、甜宠）',
                '说明目标受众和风格定位',
                '指定集数和每集时长',
                '列出主要角色和声线要求',
                '标注敏感内容或需改写部分'
            ]
        else:
            guide = [
                '指定运营品类（如：3C配件、美妆）',
                '说明目标市场（印尼/越南/泰国等）',
                '设定爆款判定阈值',
                '明确数据上报频率',
                '指定告警通知群'
            ]
        return jsonify({'guide': guide})
    
    # ========== 第九阶段：全透明流水线 + 决策系统 ==========
    
    @app.route('/api/milestone/<task_id>/<milestone_id>/output', methods=['GET'])
    def get_milestone_output(task_id, milestone_id):
        """获取里程碑产出内容"""
        # 搜索所有任务目录
        search_dirs = [ACTIVE_DIR, ACTIVE_DIR / 'drama', ACTIVE_DIR / 'tk']
        task_file = None
        for search_dir in search_dirs:
            tf = search_dir / f"{task_id}.json"
            if tf.exists():
                task_file = tf
                break
        
        if not task_file:
            return jsonify({'error': 'Task not found'}), 404
        
        with open(task_file) as f:
            task = json.load(f)
        
        for m in task.get('milestones', []):
            if m.get('id') == milestone_id:
                output_content = m.get('execution_details', {}).get('output_content', {})
                return jsonify({
                    'task_id': task_id,
                    'milestone_id': milestone_id,
                    'milestone_name': m.get('name'),
                    'status': m.get('status'),
                    'decision_point': m.get('decision_point', False),
                    'decision_required': m.get('decision_required', False),
                    'decision_options': m.get('decision_options', []),
                    'decision_deadline': m.get('decision_deadline'),
                    'output_content': output_content
                })
        
        return jsonify({'error': 'Milestone not found'}), 404
    
    @app.route('/api/decision/submit', methods=['POST'])
    def submit_decision():
        """提交决策 - 通过/修改/驳回"""
        data = request.json
        task_id = data.get('task_id')
        milestone_id = data.get('milestone_id')
        decision_type = data.get('decision_type')  # approve/modify/reject
        comment = data.get('comment', '')
        
        # 搜索所有任务目录
        search_dirs = [ACTIVE_DIR, ACTIVE_DIR / 'drama', ACTIVE_DIR / 'tk']
        task_file = None
        for search_dir in search_dirs:
            tf = search_dir / f"{task_id}.json"
            if tf.exists():
                task_file = tf
                break
        
        if not task_file:
            return jsonify({'error': 'Task not found'}), 404
        
        with open(task_file, 'r+') as f:
            task = json.load(f)
            
            for m in task.get('milestones', []):
                if m.get('id') == milestone_id:
                    # 记录决策
                    decision_entry = {
                        'decision_type': decision_type,
                        'decision_at': datetime.now().isoformat(),
                        'decision_value': decision_type,
                        'decision_by': 'human',
                        'comment': comment
                    }
                    m.setdefault('decision_history', []).append(decision_entry)
                    
                    # 更新状态
                    if decision_type == 'approve':
                        m['status'] = 'completed'
                        m['decision_status'] = 'approved'
                    elif decision_type == 'modify':
                        m['status'] = 'pending'
                        m['decision_status'] = 'modifying'
                    elif decision_type == 'reject':
                        m['status'] = 'rejected'
                        m['decision_status'] = 'rejected'
                    
                    m['decision_completed_at'] = datetime.now().isoformat()
                    break
            
            # 检查是否所有里程碑完成
            if all(mm.get('status') == 'completed' for mm in task.get('milestones', [])):
                task['status'] = 'completed'
            
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
        
        return jsonify({'status': 'ok', 'decision_type': decision_type})
    
    @app.route('/api/decision/retry', methods=['POST'])
    def retry_milestone():
        """重新执行里程碑（修改后重试）"""
        data = request.json
        task_id = data.get('task_id')
        milestone_id = data.get('milestone_id')
        comment = data.get('comment', '')
        
        # 更新任务状态为 running
        # 搜索所有任务目录
        search_dirs = [ACTIVE_DIR, ACTIVE_DIR / 'drama', ACTIVE_DIR / 'tk']
        task_file = None
        for search_dir in search_dirs:
            tf = search_dir / f"{task_id}.json"
            if tf.exists():
                task_file = tf
                break
        
        if not task_file:
            return jsonify({'error': 'Task not found'}), 404
        
        with open(task_file, 'r+') as f:
            task = json.load(f)
            
            for m in task.get('milestones', []):
                if m.get('id') == milestone_id:
                    m['status'] = 'running'
                    m['retry_comment'] = comment
                    m['retried_at'] = datetime.now().isoformat()
                    break
            
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
        
        return jsonify({'status': 'retry_triggered', 'message': '重新执行已触发'})
    
    @app.route('/api/tasks/<task_id>/pending-decisions', methods=['GET'])
    def get_pending_decisions(task_id):
        """获取任务的待决策里程碑列表"""
        # 搜索所有任务目录
        search_dirs = [ACTIVE_DIR, ACTIVE_DIR / 'drama', ACTIVE_DIR / 'tk']
        task_file = None
        for search_dir in search_dirs:
            tf = search_dir / f"{task_id}.json"
            if tf.exists():
                task_file = tf
                break
        
        if not task_file:
            return jsonify({'error': 'Task not found'}), 404
        
        with open(task_file) as f:
            task = json.load(f)
        
        pending = []
        for m in task.get('milestones', []):
            if m.get('decision_required') and m.get('status') in ['pending', 'pending_decision']:
                output = m.get('execution_details', {}).get('output_content', {})
                pending.append({
                    'milestone_id': m.get('id'),
                    'milestone_name': m.get('name'),
                    'decision_options': m.get('decision_options', []),
                    'decision_deadline': m.get('decision_deadline'),
                    'output_type': output.get('type'),
                    'output_title': output.get('title'),
                    'output_content': output.get('content', '')[:500],
                    'suggestions': output.get('suggestions', []),
                    'artifacts': output.get('artifacts', [])
                })
        
        return jsonify({'task_id': task_id, 'pending_decisions': pending})
    
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # ─────────────── GPT-SoVITS 语音管理 API ───────────────
    VOICES_CONFIG = Path(__file__).resolve().parent.parent / "drama/openclaw/skills/water-margin-drama/character_voices.json"
    AUDIO_OUTPUT_DIR = Path.home() / "GPT-SoVITS/output/drama"
    
    def _read_voices():
        if VOICES_CONFIG.exists():
            with open(VOICES_CONFIG) as f:
                return json.load(f)
        return {"characters": {}, "gpt_sovits_config": {}}
    
    def _write_voices(data):
        VOICES_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        with open(VOICES_CONFIG, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @app.route("/api/voices", methods=["GET"])
    def list_voices():
        data = _read_voices()
        chars = data.get("characters", {})
        result = []
        for cid, c in chars.items():
            ref = c.get("ref_audio", "")
            ready = bool(ref) and bool(c.get("prompt_text"))
            if ref:
                ref_path = os.path.expanduser(ref)
                ready = ready and os.path.exists(ref_path)
            result.append({
                "id": cid, "name": c.get("name", cid),
                "voice_desc": c.get("voice_desc", ""),
                "ready": ready,
                "ref_audio": ref,
                "prompt_text": c.get("prompt_text", ""),
                "has_ref_file": bool(ref) and os.path.exists(os.path.expanduser(ref)) if ref else False,
            })
        return jsonify({"voices": result, "output_dir": str(AUDIO_OUTPUT_DIR)})
    
    @app.route("/api/voices/<char_id>", methods=["GET"])
    def get_voice(char_id):
        data = _read_voices()
        c = data["characters"].get(char_id)
        if not c:
            return jsonify({"error": f"角色 '{char_id}' 不存在"}), 404
        ref = c.get("ref_audio", "")
        return jsonify({**c, "id": char_id, "has_ref_file": bool(ref) and os.path.exists(os.path.expanduser(ref)) if ref else False})
    
    @app.route("/api/voices/<char_id>", methods=["POST"])
    def update_voice(char_id):
        data = _read_voices()
        if char_id not in data.get("characters", {}):
            return jsonify({"error": f"角色 '{char_id}' 不存在"}), 404
        body = request.get_json(silent=True) or {}
        c = data["characters"][char_id]
        for k in ("prompt_text", "prompt_language", "voice_desc"):
            if k in body:
                c[k] = body[k]
        if "ref_audio" in body:
            c["ref_audio"] = body["ref_audio"]
        if "gpt_params" in body:
            c["gpt_params"] = body["gpt_params"]
        _write_voices(data)
        return jsonify({"ok": True, "character": c})
    
    @app.route("/api/voices/<char_id>/upload", methods=["POST"])
    def upload_ref_audio(char_id):
        data = _read_voices()
        if char_id not in data.get("characters", {}):
            return jsonify({"error": f"角色 '{char_id}' 不存在"}), 404
        if "file" not in request.files:
            return jsonify({"error": "缺少 file 字段"}), 400
        f = request.files["file"]
        if f.filename == "":
            return jsonify({"error": "文件名为空"}), 400
        upload_dir = Path.home() / "GPT-SoVITS/output"
        upload_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"ref_{char_id}_{int(time.time())}.wav"
        dest = upload_dir / safe_name
        f.save(str(dest))
        data["characters"][char_id]["ref_audio"] = str(dest)
        _write_voices(data)
        return jsonify({"ok": True, "path": str(dest), "filename": safe_name})
    
    @app.route("/api/voices/<char_id>/tts", methods=["POST"])
    def voice_tts(char_id):
        data = _read_voices()
        c = data["characters"].get(char_id)
        if not c:
            return jsonify({"error": f"角色 '{char_id}' 不存在"}), 404
        body = request.get_json(silent=True) or {}
        text = body.get("text", "")
        if not text:
            return jsonify({"error": "缺少 text 参数"}), 400
        ref = c.get("ref_audio", "")
        pt = c.get("prompt_text", "")
        if not ref or not pt:
            return jsonify({"error": "参考音频或提示文本未配置"}), 400
        ref_path = os.path.expanduser(ref)
        if not os.path.exists(ref_path):
            return jsonify({"error": f"参考音频不存在: {ref_path}"}), 400
        
        sovits_cfg = data.get("gpt_sovits_config", {})
        root = os.path.expanduser(sovits_cfg.get("GPT_SOVITS_ROOT", "~/GPT-SoVITS"))
        
        import sys as _sys
        _sys.path.insert(0, os.path.join(root, "GPT_SoVITS", "GPT_SoVITS"))
        _sys.path.insert(0, os.path.join(root, "GPT_SoVITS"))
        os.environ.update({
            "gpt_path": os.path.expanduser(sovits_cfg.get("gpt_path", "")),
            "sovits_path": os.path.expanduser(sovits_cfg.get("sovits_path", "")),
            "bert_path": os.path.expanduser(sovits_cfg.get("bert_path", "")),
        })
        
        _cwd = os.getcwd()
        try:
            os.chdir(root)
            import inference_webui as w
            import numpy as np
            import soundfile
            
            gen_w = w.change_sovits_weights(os.environ["sovits_path"])
            list(gen_w)
            
            params = dict(c.get("gpt_params", {}))
            params.setdefault("how_to_cut", "不切")
            params.setdefault("top_k", 5)
            params.setdefault("top_p", 0.9)
            params.setdefault("temperature", 0.8)
            params.setdefault("speed", 1.0)
            params.setdefault("sample_steps", 32)
            
            gen = w.get_tts_wav(ref_path, pt, c.get("prompt_language", "Chinese"), text, "Chinese", **params)
            sr, audio = next(gen)
            
            AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            out_name = f"{char_id}_{int(time.time())}.wav"
            out_path = AUDIO_OUTPUT_DIR / out_name
            soundfile.write(str(out_path), np.clip(audio, -32768, 32767).astype(np.int16), sr)
            
            return jsonify({
                "ok": True,
                "filename": out_name,
                "duration": len(audio) / sr,
                "sample_rate": sr,
                "url": f"/api/audio/{out_name}",
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.chdir(_cwd)
    
    @app.route("/api/audio/<filename>")
    def serve_audio(filename):
        p = AUDIO_OUTPUT_DIR / filename
        if not p.exists():
            return jsonify({"error": "文件不存在"}), 404
        return send_file(str(p), mimetype="audio/wav")
    
    @app.route("/api/voices/<char_id>/audio", methods=["GET"])
    def list_char_audio(char_id):
        if not AUDIO_OUTPUT_DIR.exists():
            return jsonify({"files": []})
        files = sorted(AUDIO_OUTPUT_DIR.glob(f"{char_id}_*.wav"), key=os.path.getmtime, reverse=True)
        return jsonify({"files": [{"name": f.name, "url": f"/api/audio/{f.name}", "size": f.stat().st_size} for f in files[:20]]})
    
    app.run(host='0.0.0.0', port=5001, debug=False)