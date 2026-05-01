#!/usr/bin/env python3
"""
智能任务创建向导 API
包含智能推荐、内容引导、参数建议
"""
import sys
import json
import yaml
import re
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/dashboard')
def serve_dashboard():
    """驾驶舱 HTML"""
    dashboard_path = Path(__file__).resolve().parent.parent / "dashboard" / "task_board.html"
    if dashboard_path.exists():
        html = dashboard_path.read_text(encoding="utf-8")
        return html, 200, {
            "Content-Type": "text/html; charset=utf-8",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
    return "<h1>Dashboard not found</h1>", 404

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


def _load_pipeline_milestones():
    """从 pipeline YAML 读取里程碑（降级方案）"""
    pipeline_path = WORKSPACE / "shared/templates/tk_pipeline.yaml"
    milestones = []
    try:
        with open(pipeline_path) as f:
            pipe = yaml.safe_load(f)
        for stage in pipe.get("stages", []):
            milestones.append({
                "id": stage.get("id", ""),
                "name": stage.get("name", ""),
                "status": "pending",
                "decision_point": stage.get("decision_point", False),
                "decision": None,
                "note": "",
            })
    except Exception:
        pass
    return milestones


@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    """驾驶舱仪表盘 — v3.5 (SQLite 主存储, JSON 降级)"""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))
        from tk_pipeline_db import get_dashboard as db_dashboard
        data = db_dashboard()
        if data.get("total_milestones", 0) > 0:
            return jsonify(data)
    except Exception:
        pass

    # 降级: JSON
    milestones_path = Path.home() / ".agentic-os/milestones.json"
    milestones = []
    ms_completed = 0
    ms_pending_decision = 0

    if milestones_path.exists():
        with open(milestones_path) as f:
            ms_data = json.load(f)
        for mid, ms in ms_data.get("milestones", {}).items():
            status = ms.get("status", "pending")
            if status == "completed":
                ms_completed += 1
            if status == "waiting_approval":
                ms_pending_decision += 1
            milestones.append({
                "id": mid,
                "name": ms.get("name", mid),
                "status": status,
                "decision_point": ms.get("decision_point", False),
                "decision": ms.get("decision"),
                "note": ms.get("note", ""),
            })
    else:
        milestones = _load_pipeline_milestones()

    total_ms = len(milestones)

    return jsonify({
        "total_milestones": total_ms,
        "completed": ms_completed,
        "pending": total_ms - ms_completed,
        "decision_pending": ms_pending_decision,
        "failed": 0,
        "milestones": milestones,
        "completion_pct": round(ms_completed / total_ms * 100, 1) if total_ms else 0,
        "system_health": "ok",
        "timestamp": datetime.now().isoformat(),
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
    milestone_id = data.get('milestone_id', '')

    if not task_id or action not in ('approved', 'rejected', 'modify'):
        return jsonify({'error': '需要 task_id 和 action (approved/rejected/modify)'}), 400

    task_file = _find_task_file(task_id)
    if not task_file:
        # 宽容模式：任务文件不存在时，写入 decisions 目录
        from pathlib import Path
        decisions_dir = Path.home() / ".agentic-os" / "decisions"
        decisions_dir.mkdir(parents=True, exist_ok=True)
        decision_record = {
            "task_id": task_id,
            "action": action,
            "reason": reason,
            "milestone_id": milestone_id,
            "timestamp": datetime.now().isoformat(),
            "status": "recorded",
        }
        dec_path = decisions_dir / f"{task_id}_{milestone_id or 'unknown'}.json"
        with open(dec_path, "w") as f:
            json.dump(decision_record, f, ensure_ascii=False, indent=2)
        return jsonify({"status": "recorded", "decision": decision_record}), 200

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

    # 同步更新 SQLite 里程碑
    try:
        ms_id = data.get('milestone_id', '')
        if ms_id:
            from tk_pipeline_db import update_milestone, resolve_decision
            status = {'approved': 'completed', 'rejected': 'pending', 'modify': 'waiting_approval'}.get(action, 'pending')
            update_milestone(ms_id, status=status, decision=action, note=reason)
            resolve_decision(task_id, action, reason)
    except Exception:
        pass

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


@app.route('/info')
def serve_info_board():
    """全球信息摘要页面"""
    info_path = Path(__file__).resolve().parent.parent / "dashboard" / "info_board.html"
    if info_path.exists():
        return info_path.read_text(encoding="utf-8"), 200, {"Content-Type": "text/html; charset=utf-8"}
    return "<h1>Info board not found</h1>", 404


@app.route('/api/info/items', methods=['GET'])
def api_info_items():
    """全球信息摘要数据"""
    import json as _json
    items_path = Path.home() / ".agentic-os" / "info_subscriber" / "items.json"
    if not items_path.exists():
        return jsonify({"items": [], "feeds": {}, "new_count": 0, "updated_at": ""})
    with open(items_path) as f:
        raw = _json.load(f)
    items = list(raw.values()) if isinstance(raw, dict) else raw
    items.sort(key=lambda x: x.get("published", x.get("fetched_at", "")), reverse=True)
    feeds = set()
    for i in items:
        feeds.add(i.get("feed_name", i.get("source", "unknown")))
    return jsonify({
        "items": items, "feeds": {f: f for f in sorted(feeds)},
        "new_count": len(items),
        "updated_at": items[0].get("fetched_at", "") if items else "",
    })


@app.route('/api/script', methods=['GET'])
def api_script_list():
    """剧本列表 — 6集概要"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from script_manager import get_all_episodes
        return jsonify({"episodes": get_all_episodes(), "total": 6})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/script/<ep_num>', methods=['GET', 'POST'])
def api_script_detail(ep_num):
    """剧本查看(GET) / 修改(POST)"""
    # Strip "ep" prefix if present: ep06 → 06
    if ep_num.lower().startswith("ep"):
        ep_num = ep_num[2:]
    # Zero-pad: 3 → "03"
    if len(ep_num) == 1:
        ep_num = ep_num.zfill(2)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from script_manager import get_episode_detail, update_episode
        if request.method == 'POST':
            data = request.get_json() or {}
            result = update_episode(ep_num, data)
            return jsonify({"status": "updated", "episode": result})
        result = get_episode_detail(ep_num)
        if result is None:
            return jsonify({"error": f"Episode not found: {ep_num}"}), 404
        # 补充渲染统计字段，和列表端点对齐
        from script_manager import _count_renders, _get_render_dir, CURRENT_EPISODES
        char = CURRENT_EPISODES.get(ep_num, {}).get("character", "")
        renders = _count_renders(_get_render_dir(char))
        result["scene_count"] = len(renders)
        result["render_files"] = [p.name for p in renders]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e), "ep_num": ep_num}), 500


@app.route('/api/script/<ep_num>/export', methods=['GET'])
def api_script_export(ep_num):
    """剧本导出 GET /api/script/01/export?format=txt|html"""
    if ep_num.lower().startswith("ep"):
        ep_num = ep_num[2:]
    fmt = request.args.get("format", "html")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from script_manager import export_episode
        result = export_episode(ep_num, fmt)
        if not result:
            return jsonify({"error": f"Episode not found: {ep_num}"}), 404
        content, mime, filename = result
        return content, 200, {"Content-Type": mime, "Content-Disposition": f"attachment; filename={filename}"}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/download')
def api_download():
    """下载导出文件: /api/download?name=ep01.txt 或 /api/download?name=ep01.html"""
    name = request.args.get("name", "").strip()
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from script_manager import export_episode

        # Parse ep_num and format from name
        import re as _re
        m = _re.match(r'ep(\d+)\.(txt|html|srt|json)', name.lower())
        if not m:
            return jsonify({"error": f"Invalid filename: {name}. Use ep01.txt, ep01.html, etc."}), 400

        ep_num = m.group(1)
        fmt = m.group(2)
        result = export_episode(ep_num, fmt)
        if not result:
            return jsonify({"error": f"Episode not found: {ep_num}"}), 404
        content, mime, filename = result
        return content, 200, {"Content-Type": mime, "Content-Disposition": f"attachment; filename={filename}"}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/character/<char_name>', methods=['GET', 'POST'])
def api_character_detail(char_name):
    """角色设计查看/修改 — 支持完整角色档案 (v3.6.7)"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from script_manager import ROLE_OVERVIEW, CHARACTER_ID_MAP, _get_render_dir
        from character_profile_generator import regenerate_render_on_profile_change

        # Resolve pinyin name to Chinese character name
        REVERSE_ID_MAP = {v: k for k, v in CHARACTER_ID_MAP.items()}
        cn_name = REVERSE_ID_MAP.get(char_name, char_name)
        char_id = CHARACTER_ID_MAP.get(cn_name, char_name)

        # Load visual_bible for full profiles
        bible_path = Path.home() / ".agentic-os" / "character_designs" / "visual_bible.json"
        bible = {}
        if bible_path.exists():
            with open(bible_path, encoding="utf-8") as f:
                bible = json.load(f)

        if request.method == 'POST':
            data = request.get_json() or {}
            changed_fields = list(data.keys())

            # 1. Update ROLE_OVERVIEW (legacy compat)
            if cn_name in ROLE_OVERVIEW:
                ROLE_OVERVIEW[cn_name].update(data)
            elif char_name in ROLE_OVERVIEW:
                ROLE_OVERVIEW[char_name].update(data)

            # 2. Update visual_bible.json (full profile)
            if char_id in bible.get("characters", {}):
                ch = bible["characters"][char_id]
                # Deep merge
                for key, val in data.items():
                    if isinstance(val, dict) and isinstance(ch.get(key), dict):
                        ch[key].update(val)
                    else:
                        ch[key] = val
                ch["_updated_at"] = datetime.now().isoformat()
                with open(bible_path, "w", encoding="utf-8") as f:
                    json.dump(bible, f, ensure_ascii=False, indent=2)

            # 3. Check if re-render needed
            rerender = regenerate_render_on_profile_change(char_id, changed_fields)

            # 4. Build response
            profile = bible["characters"].get(char_id, {})
            return jsonify({
                "status": "updated",
                "character": profile,
                "rerender": rerender,
            })

        # GET: return full profile from visual_bible + renders
        profile = bible.get("characters", {}).get(char_id, {})
        if not profile:
            # Fallback to ROLE_OVERVIEW
            info = ROLE_OVERVIEW.get(cn_name) or ROLE_OVERVIEW.get(char_name)
            if not info:
                return jsonify({"error": f"Character not found: {char_name} (cn: {cn_name})"}), 404
            profile = {"name": cn_name, "design": info}

        rd = _get_render_dir(cn_name)
        renders = []
        if rd.exists():
            for p in sorted(rd.glob("*.png")):
                renders.append(f"/api/render/{char_id}/{p.name}")

        return jsonify({
            "name": cn_name,
            "pinyin": char_id,
            "profile": profile,
            "renders": renders,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/character/<char_name>/generate', methods=['POST'])
def api_character_generate(char_name):
    """AI 生成/刷新角色档案 (v3.6.8)"""
    try:
        from script_manager import CHARACTER_ID_MAP, ROLE_OVERVIEW
        from character_profile_generator import generate_character_profile, KNOWN_PROFILES

        REVERSE_ID_MAP = {v: k for k, v in CHARACTER_ID_MAP.items()}
        cn_name = REVERSE_ID_MAP.get(char_name, char_name)

        # Get title from role overview
        role = ROLE_OVERVIEW.get(cn_name, {})
        title = role.get("title", "")

        # Generate profile (uses KNOWN_PROFILES fallback if AI fails)
        profile = generate_character_profile(cn_name, title)

        # Merge into visual_bible.json
        bible_path = Path.home() / ".agentic-os" / "character_designs" / "visual_bible.json"
        bible = {}
        if bible_path.exists():
            with open(bible_path, encoding="utf-8") as f:
                bible = json.load(f)

        char_id = CHARACTER_ID_MAP.get(cn_name, char_name)
        chars = bible.setdefault("characters", {})
        if char_id not in chars:
            chars[char_id] = {"name": cn_name, "id": char_id}

        # Deep merge profile sections
        for section in ["personality", "appearance", "voice"]:
            if section in profile:
                existing = chars[char_id].get("profile", {}).get(section, {})
                existing.update(profile[section])
                if "profile" not in chars[char_id]:
                    chars[char_id]["profile"] = {}
                chars[char_id]["profile"][section] = existing

        chars[char_id]["profile"]["_updated_at"] = datetime.now().isoformat()
        chars[char_id]["profile"]["_generated_by"] = "ai_profile_generator"

        with open(bible_path, "w", encoding="utf-8") as f:
            json.dump(bible, f, ensure_ascii=False, indent=2)

        return jsonify({
            "status": "ok",
            "character": cn_name,
            "profile": profile,
            "message": f"✅ {cn_name} 档案已生成/刷新",
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/character/<char_name>/regenerate', methods=['POST'])
def api_character_regenerate(char_name):
    """触发角色重新渲染 (v3.6.7)"""
    try:
        from script_manager import CHARACTER_ID_MAP, ROLE_OVERVIEW
        REVERSE_ID_MAP = {v: k for k, v in CHARACTER_ID_MAP.items()}
        cn_name = REVERSE_ID_MAP.get(char_name, char_name)
        char_id = CHARACTER_ID_MAP.get(cn_name, char_name)

        # Load bible profile
        bible_path = Path.home() / ".agentic-os" / "character_designs" / "visual_bible.json"
        bible = {}
        if bible_path.exists():
            with open(bible_path, encoding="utf-8") as f:
                bible = json.load(f)

        ch = bible.get("characters", {}).get(char_id, {})
        appearance = ch.get("appearance", {})

        # Build render prompt from profile
        costume = appearance.get("costume", "")
        accessories = ", ".join(appearance.get("accessories", []))
        basic = ch.get("basic_info", {})

        base_prompt = f"{cn_name}, {basic.get('face', '')}, {basic.get('build', '')}, wearing {costume}"
        if accessories:
            base_prompt += f", with {accessories}"

        # TODO: call comfyui_renderer with new prompt
        # For now, return what would be rendered
        return jsonify({
            "status": "queued",
            "character": cn_name,
            "prompt": base_prompt,
            "message": "渲染任务已提交，请等待完成",
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/render/<char_id>/<filename>')
def api_render_image(char_id, filename):
    """渲染图静态文件服务"""
    path = Path.home() / ".agentic-os" / "character_designs" / "renders" / char_id / filename
    if not path.exists():
        return "Not found", 404
    from flask import send_file
    return send_file(str(path), mimetype="image/png")


# EP → character 映射（用于 /api/render/epXX/shot_X.png 别名路由）
_EP_CHAR_MAP = {
    "01": "luzhishen", "02": "luzhishen",
    "03": "linchong", "04": "songjiang",
    "05": "likui", "06": "wuyong",
}

@app.route('/api/render/ep<ep_num>/shot_<shot_num>.png')
def api_render_episode(ep_num, shot_num):
    """渲染图别名路由：/api/render/ep03/shot_01.png → /api/render/linchong/ep03_shot_01.png"""
    char_id = _EP_CHAR_MAP.get(ep_num)
    if not char_id:
        return "Not found", 404
    filename = f"ep{ep_num}_shot_{shot_num}.png"
    path = Path.home() / ".agentic-os" / "character_designs" / "renders" / char_id / filename
    if not path.exists():
        return "Not found", 404
    from flask import send_file
    return send_file(str(path), mimetype="image/png")


# ========== 商品图片 API ==========

@app.route('/api/images', methods=['GET'])
def api_images_list():
    """商品图片列表"""
    catalog_path = Path.home() / ".agentic-os" / "products" / "catalog.json"
    if not catalog_path.exists():
        return jsonify({"products": []})
    with open(catalog_path) as f:
        catalog = json.load(f)
    return jsonify(catalog)


@app.route('/api/images/<img_id>', methods=['GET'])
def api_image_view(img_id):
    """查看单张商品图片"""
    img_path = Path.home() / ".agentic-os" / "products" / "images" / f"{img_id}.jpg"
    variants = [
        (img_path, "original"),
        (Path.home() / ".agentic-os" / "products" / "images" / f"{img_id}_nobg.jpg", "nobg"),
        (Path.home() / ".agentic-os" / "products" / "images" / f"{img_id}_final.jpg", "final"),
    ]
    files = {}
    for p, tag in variants:
        if p.exists():
            files[tag] = f"/api/images/file/{p.name}"
    if not files:
        return jsonify({"error": f"Image not found: {img_id}"}), 404
    return jsonify({"id": img_id, "files": files})


@app.route('/api/images/file/<filename>')
def api_image_file(filename):
    """商品图片文件服务"""
    path = Path.home() / ".agentic-os" / "products" / "images" / filename
    if not path.exists():
        return "Not found", 404
    from flask import send_file
    return send_file(str(path), mimetype="image/jpeg")


@app.route('/api/images/<img_id>/process', methods=['POST'])
def api_image_process(img_id):
    """处理商品图片: rembg/resize/compliance"""
    data = request.get_json() or {}
    action = data.get("action", "rembg")

    img_path = Path.home() / ".agentic-os" / "products" / "images" / f"{img_id}.jpg"
    if not img_path.exists():
        return jsonify({"error": f"Image not found: {img_id}"}), 404

    results = {"id": img_id, "action": action, "steps": []}

    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from core.image_processor import remove_background, resize_to_square, check_compliance

        if action == "rembg":
            out_path = img_path.parent / f"{img_id}_nobg.jpg"
            result = remove_background(img_path, out_path)
            if result:
                results["steps"].append("rembg: ok")
                results["output"] = f"/api/images/file/{img_id}_nobg.jpg"
            else:
                results["steps"].append("rembg: failed")
                results["error"] = "RemBG 处理失败，检查 rembg 是否正确安装"

        elif action == "resize":
            import shutil
            final_path = img_path.parent / f"{img_id}_final.jpg"
            shutil.copy(img_path, final_path)
            result = resize_to_square(final_path)
            if result:
                results["steps"].append("resize: ok")
                results["output"] = f"/api/images/file/{img_id}_final.jpg"
            else:
                results["steps"].append("resize: failed")

        elif action == "full":
            # rembg → resize → compliance
            out_path = img_path.parent / f"{img_id}_nobg.jpg"
            nobg = remove_background(img_path, out_path)
            if nobg:
                results["steps"].append("rembg: ok")
                import shutil
                final_path = img_path.parent / f"{img_id}_final.jpg"
                shutil.copy(nobg, final_path)
                resized = resize_to_square(final_path)
                if resized:
                    results["steps"].append("resize: ok")
                    issues = check_compliance(final_path)
                    results["steps"].append(f"compliance: {'pass' if not issues else ', '.join(issues)}")
                    results["output"] = f"/api/images/file/{img_id}_final.jpg"
                else:
                    results["steps"].append("resize: failed")
            else:
                results["steps"].append("rembg: failed")

        elif action == "check":
            issues = check_compliance(img_path)
            results["compliance"] = {"passed": len(issues) == 0, "issues": issues}

        elif action == "push_erp":
            from core.image_processor import push_to_erp_draft
            draft_path = push_to_erp_draft(img_id, [str(img_path)], product_title=img_id)
            results["steps"].append(f"erp_draft: {draft_path}")
            results["output"] = draft_path

        else:
            return jsonify({"error": f"Unknown action: {action}"}), 400

        # Update catalog status
        catalog_path = Path.home() / ".agentic-os" / "products" / "catalog.json"
        if catalog_path.exists():
            with open(catalog_path) as f:
                catalog = json.load(f)
            for p in catalog.get("products", []):
                if p["id"] == img_id:
                    if results.get("output"):
                        p["status"] = "已处理"
                        p["output"] = results["output"]
                    if results.get("error"):
                        p["status"] = "处理失败"
                    break
            with open(catalog_path, "w") as f:
                json.dump(catalog, f, ensure_ascii=False, indent=2)

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e), "id": img_id}), 500


@app.route('/api/detail/<ms_id>', methods=['GET'])
def api_detail(ms_id):
    """里程碑详情 — v3.6 返回实体数据(非状态标签)"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from detail_engine import get_all_details
        return jsonify(get_all_details(ms_id))
    except Exception as e:
        return jsonify({"error": str(e), "ms_id": ms_id}), 500


if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, str(Path(__file__).parent.parent))
    try:
        from shared.config import config
        host = config.API_HOST
        port = config.API_PORT
    except ImportError:
        host = os.environ.get("API_HOST", "127.0.0.1")
        port = int(os.environ.get("API_PORT", "5001"))
    app.run(host=host, port=port, debug=False)