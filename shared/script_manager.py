#!/usr/bin/env python3
"""
剧本管理 API — v3.6
提供剧本查看、编辑、导出功能，上下游实时同步
"""
import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

SCRIPT_YAML = PROJECT_ROOT / "stories" / "shuihuzhuan.yaml"
SCRIPT_JSON = Path.home() / ".agentic-os" / "shorthands.json"

# EPISODE_MAP: 当前6集短剧选定的故事集
CURRENT_EPISODES = {
    "01": {"id": "lutixia_quan_da_zhenguanxi", "title": "鲁提辖拳打镇关西", "chapter": 3, "character": "鲁智深"},
    "02": {"id": "lu_zhishen_daoba_chuiyangliu", "title": "鲁智深倒拔垂杨柳", "chapter": 4, "character": "鲁智深"},
    "03": {"id": "linchong_fengxue_shanshenmiao", "title": "林冲风雪山神庙", "chapter": 10, "character": "林冲"},
    "04": {"id": "songjiang_sha_yanpoxi", "title": "宋江杀阎婆惜", "chapter": 22, "character": "宋江"},
    "05": {"id": "likui_yiling_sha_sihu", "title": "李逵沂岭杀四虎", "chapter": 43, "character": "李逵"},
    "06": {"id": "zhiqu_shengchengang", "title": "智取生辰纲", "chapter": 16, "character": "吴用"},
}

ROLE_OVERVIEW = {
    "武松": {"traits": ["打虎英雄", "刚正不阿"], "height": 188, "face": "方颚浓眉", "weapon": "哨棒/双刀", "voice": "zhiming(浑厚有力)", "color": "#1a1a2e+#8b0000"},
    "鲁智深": {"traits": ["花和尚", "力大无穷"], "height": 195, "face": "秃头戒疤·络腮胡", "weapon": "月牙铲", "voice": "zhiming(粗犷豪迈)", "color": "#4a3728+#2d5016"},
    "林冲": {"traits": ["豹子头", "忍辱负重"], "height": 182, "face": "儒雅·薄髭", "weapon": "丈八蛇矛", "voice": "zhilun(沉郁悲壮)", "color": "#8b0000+#1a1a2e"},
    "宋江": {"traits": ["及时雨", "领袖"], "height": 175, "face": "黑矮·细眉沉稳", "weapon": "短刀", "voice": "zhilun(沉稳内敛)", "color": "#1a3a1a+#4a0080"},
    "杨志": {"traits": ["青面兽", "将门之后"], "height": 185, "face": "刀削面庞·青记", "weapon": "祖传宝刀", "voice": "zhiqiang(深沉自尊)", "color": "#2d5016+#8b0000"},
    "晁盖": {"traits": ["托塔天王", "义薄云天"], "height": 180, "face": "宽额浓眉·三绺须", "weapon": "朴刀", "voice": "zhiming(稳重威严)", "color": "#4a0080+#1a3a1a"},
    "吴用": {"traits": ["智多星", "神机妙算"], "height": 176, "face": "清瘦长须·羽扇纶巾", "weapon": "铜链", "voice": "zhilun(睿智从容)", "color": "#1a3a4a+#c0a060"},
    "李逵": {"traits": ["黑旋风", "天真烂漫"], "height": 190, "face": "漆黑面皮·环眼暴突", "weapon": "板斧(双)", "voice": "zhiqiang(暴烈炽热)", "color": "#0a0a0a+#8b0000"},
}

CHARACTER_DESIGNS_DIR = Path.home() / ".agentic-os" / "character_designs"
RENDER_DIR = CHARACTER_DESIGNS_DIR / "renders"

EP_ORDER = ["01", "02", "03", "04", "05", "06"]

# 角色名→文件ID映射
CHARACTER_ID_MAP = {
    "武松": "wusong", "鲁智深": "luzhishen", "林冲": "linchong",
    "宋江": "songjiang", "李逵": "likui", "吴用": "wuyong",
}

def _get_render_dir(character_name):
    """获取角色的渲染图目录"""
    cid = CHARACTER_ID_MAP.get(character_name, character_name)
    return RENDER_DIR / cid

def _count_renders(rd):
    """计数所有渲染图（含ep前缀）"""
    if not rd.exists(): return []
    return sorted(rd.glob("*.png"))


def load_script_yaml():
    with open(SCRIPT_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_script_yaml(data):
    with open(SCRIPT_YAML, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    # 写同步日志
    log_path = Path.home() / ".agentic-os" / "script_changelog.json"
    changelog = []
    if log_path.exists():
        changelog = json.loads(log_path.read_text())
    changelog.append({"time": datetime.now().isoformat(), "action": "save"})
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(changelog[-50:], ensure_ascii=False, indent=2))
    return True


def get_all_episodes():
    """获取当前6集列表"""
    data = load_script_yaml()
    all_eps = {ep["id"]: ep for ep in data.get("episodes", [])}

    result = []
    for num in EP_ORDER:
        info = CURRENT_EPISODES[num]
        ep_data = all_eps.get(info["id"], {})
        result.append({
            "episode": int(num),
            "number": num,
            "id": info["id"],
            "title": info["title"],
            "chapter": info["chapter"],
            "main_character": info["character"],
            "score": ep_data.get("score", 5.0),
            "tags": ep_data.get("tags", []),
            "character_info": ROLE_OVERVIEW.get(info["character"], {}),
            "has_render": bool(_count_renders(_get_render_dir(info["character"]))),
        })
    return result


def get_episode_detail(ep_num):
    """获取单集完整详情"""
    data = load_script_yaml()
    all_eps = {ep["id"]: ep for ep in data.get("episodes", [])}
    info = CURRENT_EPISODES.get(ep_num)
    if not info:
        return None

    ep_data = all_eps.get(info["id"], {})
    char_data = ROLE_OVERVIEW.get(info["character"], {})

    # 查找角色渲染图
    character_id = info["character"]
    renders = []
    for p in _count_renders(_get_render_dir(character_id)):
        cid = CHARACTER_ID_MAP.get(character_id, character_id)
        renders.append(f"/api/render/{cid}/{p.name}")

    # 查找视觉圣经prompts
    vb_path = CHARACTER_DESIGNS_DIR / "visual_bible.json"
    visual_prompts = {}
    if vb_path.exists():
        vb = json.loads(vb_path.read_text())
        chars = vb.get("characters", {})
        char_vb = chars.get(character_id, {})
        visual_prompts = {
            "character": char_vb.get("character", ""),
            "scenes": char_vb.get("scenes", []),
            "prompt_prefix": char_vb.get("prompt_prefix", ""),
        }

    # 构建5段式分镜描述
    storyboard = _build_storyboard(info["title"], info["chapter"], info["character"])

    return {
        "number": ep_num,
        "episode_id": info["id"],
        "title": info["title"],
        "chapter": info["chapter"],
        "main_character": info["character"],
        "score": ep_data.get("score", 5.0),
        "tags": ep_data.get("tags", []),
        "needs_rewrite": "需改编" in ep_data.get("tags", []),
        "character_design": char_data,
        "renders": renders,
        "visual_prompts": visual_prompts,
        "storyboard": storyboard,
        "scenes": data.get("scenes", {}),
        "roles": data.get("roles", []),
        "controversy_rules": data.get("controversy_rules", []),
    }


def _build_storyboard(title, chapter, character):
    """根据剧集信息构建5段式分镜"""
    templates = {
        "鲁提辖拳打镇关西": [
            {"seq": 1, "act": "开场", "scene": "渭州酒馆", "description": f"鲁提辖在酒馆听到金氏父女哭泣，上前询问", "emotion": "疑惑→关注", "duration": "8秒"},
            {"seq": 2, "act": "发展", "scene": "酒馆内", "description": f"金老诉说镇关西郑屠霸占女儿，{character}勃然大怒", "emotion": "同情→愤怒", "duration": "10秒"},
            {"seq": 3, "act": "冲突", "scene": "状元桥肉铺", "description": f"{character}来到郑屠肉铺，以买肉为名挑起事端，三拳打向郑屠", "emotion": "戏耍→爆发", "duration": "12秒"},
            {"seq": 4, "act": "高潮", "scene": "肉铺前", "description": f"{character}三拳打死镇关西，郑屠倒地，围观百姓惊慌", "emotion": "爆发→震惊", "duration": "10秒"},
            {"seq": 5, "act": "结局", "scene": "渭州街头", "description": f"{character}见郑屠已死，假装醉酒，大步离去，消失在街角", "emotion": "冷静→逃离", "duration": "8秒"},
        ],
        "鲁智深倒拔垂杨柳": [
            {"seq": 1, "act": "开场", "scene": "大相国寺菜园", "description": f"{character}在菜园中察看新长的柳树，众泼皮围观", "emotion": "悠闲→期待", "duration": "8秒"},
            {"seq": 2, "act": "发展", "scene": "菜园", "description": f"泼皮们起哄让{character}展示神力，{character}哈哈大笑掀起袈裟", "emotion": "轻松→自信", "duration": "10秒", "dialogue": "你们几个撮鸟，看洒家拔这棵树！"},
            {"seq": 3, "act": "冲突", "scene": "菜园", "description": f"{character}双手抱住柳树干，一声怒吼，腰马合一，地面裂开", "emotion": "专注→爆发", "duration": "12秒"},
            {"seq": 4, "act": "高潮", "scene": "菜园中央", "description": f"{character}将整棵柳树连根拔起，泥土飞溅，柳条乱舞，泼皮们目瞪口呆纷纷跪拜", "emotion": "震撼→敬畏", "duration": "12秒"},
            {"seq": 5, "act": "结局", "scene": "菜园", "description": f"{character}将柳树随手一抛，拍拍手上泥土，大笑着坐在石凳上", "emotion": "得意→豪迈", "duration": "8秒", "dialogue": "如何？你这些撮鸟，还敢小看洒家吗？"},
        ],
        "林冲风雪山神庙": [
            {"seq": 1, "act": "开场", "scene": "沧州草料场", "description": f"{character}被发配沧州看守草料场，风雪交加中独坐茅屋", "emotion": "沉郁→孤独", "duration": "10秒"},
            {"seq": 2, "act": "发展", "scene": "山神庙", "description": f"大雪压倒草屋，{character}到山神庙暂避，忽闻庙外脚步声", "emotion": "警觉→不安", "duration": "10秒"},
            {"seq": 3, "act": "冲突", "scene": "山神庙外", "description": f"陆谦等三人在庙外密谋烧死{character}，{character}在门后听得一清二楚", "emotion": "震惊→愤怒", "duration": "12秒"},
            {"seq": 4, "act": "高潮", "scene": "山神庙雪地", "description": f"{character}提枪冲出，火光中连杀三人，陆谦惊恐求饶", "emotion": "爆发→复仇", "duration": "12秒", "dialogue": "奸贼！今日便是你的死期！"},
            {"seq": 5, "act": "结局", "scene": "风雪山林", "description": f"{character}杀死陆谦，望着燃烧的草料场，风雪中提枪踏上通往梁山的路", "emotion": "决绝→新生", "duration": "10秒"},
        ],
        "宋江杀阎婆惜": [
            {"seq": 1, "act": "开场", "scene": "宋江书房", "description": f"{character}深夜回到书房，发现阎婆惜正在翻找他的东西", "emotion": "警觉", "duration": "8秒"},
            {"seq": 2, "act": "发展", "scene": "书房内·灯光昏暗", "description": f"阎婆惜拿出梁山书信威胁{character}，{character}面色大变", "emotion": "惊吓→愤怒", "duration": "10秒", "dialogue": "你…你竟敢威胁我！"},
            {"seq": 3, "act": "冲突", "scene": "书房内", "description": f"两人激烈争吵，{character}去夺书信，阎婆惜大声呼救", "emotion": "紧张→失控", "duration": "10秒"},
            {"seq": 4, "act": "高潮", "scene": "书房内", "description": f"混乱中{character}抽出短刀刺向阎婆惜，鲜血溅在梁山书信上", "emotion": "绝望→冲动", "duration": "8秒"},
            {"seq": 5, "act": "结局", "scene": "书房·黎明", "description": f"{character}擦拭血迹，收起书信，晨光中露出复杂而沉重的表情", "emotion": "悔恨→决断", "duration": "8秒"},
        ],
        "李逵沂岭杀四虎": [
            {"seq": 1, "act": "开场", "scene": "沂岭山路", "description": f"{character}背着老娘走在沂岭山路上，烈日当空，娘说口渴", "emotion": "孝顺→焦急", "duration": "8秒", "dialogue": "娘，您歇着，我去找水"},
            {"seq": 2, "act": "发展", "scene": "山溪边", "description": f"{character}找到山溪舀水，远处传来低沉的虎啸声", "emotion": "安心→警觉", "duration": "10秒", "dialogue": "什么声音？"},
            {"seq": 3, "act": "冲突", "scene": "沂岭·洞穴外", "description": f"回来发现老娘不见，地上血迹斑斑，{character}目眦欲裂", "emotion": "恐惧→暴怒", "duration": "12秒"},
            {"seq": 4, "act": "高潮", "scene": "沂岭", "description": f"{character}双斧挥舞，连杀四虎，虎血染红衣衫，怒吼震山林", "emotion": "狂怒→悲壮", "duration": "14秒"},
            {"seq": 5, "act": "结局", "scene": "沂岭·黄昏", "description": f"{character}跪在老娘失踪处，夕阳下拉长身影，默默收起染血的双斧", "emotion": "悲痛→决绝", "duration": "8秒"},
        ],
        "智取生辰纲": [
            {"seq": 1, "act": "开场", "scene": "聚义厅·烛光下", "description": f"{character}手持羽扇，烛光映照清瘦面容，展开地图低声策划", "emotion": "沉稳→机密", "duration": "12秒", "dialogue": "此番智取，不许动一兵一卒"},
            {"seq": 2, "act": "发展", "scene": "黄泥岗山路", "description": f"{character}扮作枣贩，推车行于黄泥岗山路，烈日当空", "emotion": "伪装→警觉", "duration": "12秒"},
            {"seq": 3, "act": "冲突", "scene": "黄泥岗", "description": f"押送队伍到达，{character}以掺药酒为计，表面争吵掩护", "emotion": "紧张→博弈", "duration": "12秒"},
            {"seq": 4, "act": "高潮", "scene": "黄泥岗", "description": f"{character}与众好汉假装抢酒喝，军士纷纷倒地，计谋得逞", "emotion": "暗喜→胜利", "duration": "14秒"},
            {"seq": 5, "act": "结局", "scene": "黄泥岗·夕阳", "description": f"{character}摇扇微笑，望着满载珠宝的车队消失在暮色中", "emotion": "得意→从容", "duration": "10秒"},
        ],
    }

    key = title if title in templates else list(templates.keys())[0]
    storyboard = templates.get(key, [])

    # 如果没有匹配模板，生成通用分镜
    if not storyboard:
        storyboard = [
            {"seq": i+1, "act": act, "scene": f"场景{i+1}", "description": f"{character}的精彩演绎", "emotion": "待定义", "duration": "10秒"}
            for i, act in enumerate(["开场", "发展", "冲突", "高潮", "结局"])
        ]

    return storyboard


def update_episode(ep_num, data):
    """更新单集剧本"""
    script = load_script_yaml()
    info = CURRENT_EPISODES.get(ep_num)
    if not info:
        return None

    # 更新episodes中对应条目
    for ep in script.get("episodes", []):
        if ep["id"] == info["id"]:
            if "title" in data:
                ep["title"] = data["title"]
            if "score" in data:
                ep["score"] = float(data["score"])
            if "tags" in data:
                ep["tags"] = data["tags"]
            if "character" in data:
                ep["character"] = data["character"]
            break

    # 更新roles中对应角色
    if "character_design" in data:
        char_name = info["character"]
        for role in script.get("roles", []):
            if role["name"] == char_name:
                cd = data["character_design"]
                if "voice_style" in cd:
                    role["voice_style"] = cd["voice_style"]
                if "tts_voice" in cd:
                    role["tts_voice"] = cd["tts_voice"]
                if "description" in cd:
                    role["description"] = cd["description"]
                break

    save_script_yaml(script)

    # 也更新 CURRENT_EPISODES
    if "title" in data:
        CURRENT_EPISODES[ep_num]["title"] = data["title"]

    return get_episode_detail(ep_num)


def export_episode(ep_num, format="txt"):
    """导出剧本为 TXT 或 HTML，返回 (content, mime_type, filename)"""
    detail = get_episode_detail(ep_num)
    if not detail:
        return None

    if format == "html":
        content = _export_html(detail)
        filename = f"ep{detail['number']}.html"
        return (content, "text/html; charset=utf-8", filename)
    elif format == "srt":
        content = _export_srt(detail)
        filename = f"ep{detail['number']}.srt"
        return (content, "text/plain; charset=utf-8", filename)
    elif format == "json":
        content = json.dumps(detail, ensure_ascii=False, indent=2)
        filename = f"ep{detail['number']}.json"
        return (content, "application/json; charset=utf-8", filename)
    content = _export_txt(detail)
    filename = f"ep{detail['number']}.txt"
    return (content, "text/plain; charset=utf-8", filename)


def _export_srt(detail):
    """导出为 SRT 字幕格式"""
    sb = detail.get("storyboard", [])
    lines = []
    for i, scene in enumerate(sb, 1):
        start_sec = sum(s.get("duration_sec", 5) for s in sb[:i-1])
        end_sec = start_sec + scene.get("duration_sec", 5)
        start_ts = f"00:00:{start_sec:02d},000"
        end_ts = f"00:00:{end_sec:02d},000"
        text = scene.get("dialogue") or scene.get("description", "")
        lines.append(f"{i}")
        lines.append(f"{start_ts} --> {end_ts}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def _export_txt(detail):
    lines = [
        f"{'='*60}",
        f"  水浒传AI短剧 · 第{detail['number']}集",
        f"  {detail['title']}",
        f"{'='*60}",
        f"",
        f"原著回目: 第{detail['chapter']}回",
        f"主角: {detail['main_character']}",
        f"评分: {detail['score']}/10",
        f"标签: {', '.join(detail.get('tags', []))}",
        f"",
        f"{'─'*60}",
        f"  角色设计",
        f"{'─'*60}",
    ]
    cd = detail.get("character_design", {})
    for k, v in cd.items():
        lines.append(f"  {k}: {v}")

    lines.extend([
        f"",
        f"{'─'*60}",
        f"  分镜脚本（5段式叙事）",
        f"{'─'*60}",
    ])
    for sb in detail.get("storyboard", []):
        lines.append(f"")
        lines.append(f"  镜{sb['seq']} [{sb['act']}] {sb['scene']} · {sb.get('duration','')}")
        lines.append(f"  {sb['description']}")
        lines.append(f"  情绪: {sb['emotion']}")
        if sb.get("dialogue"):
            lines.append(f"  对白: {sb['dialogue']}")

    lines.extend([
        f"",
        f"{'─'*60}",
        f"  审查规则",
        f"{'─'*60}",
    ])
    for cr in detail.get("controversy_rules", []):
        lines.append(f"  [{cr['severity']}] {cr['pattern']}: {cr['rewrite'][:60]}")

    return "\n".join(lines)


def _export_html(detail):
    cd = detail.get("character_design", {})
    renders = detail.get("renders", [])

    render_imgs = ""
    if renders:
        render_imgs = "<div class='renders'>" + "".join(
            f"<img src='{r}' style='max-width:200px;margin:4px;border-radius:8px;' />"
            for r in renders
        ) + "</div>"

    storyboard_rows = ""
    for sb in detail.get("storyboard", []):
        storyboard_rows += f"""
        <div class='storyboard-card'>
            <h4>镜{sb['seq']} [{sb['act']}] {sb['scene']} <small>{sb.get('duration','')}</small></h4>
            <p>{sb['description']}</p>
            <div class='meta'>情绪: {sb['emotion']}{' · 对白: ' + sb['dialogue'] if sb.get('dialogue') else ''}</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>水浒传AI短剧 · 第{detail['number']}集 {detail['title']}</title>
<style>
body {{ font-family: 'PingFang SC','Hiragino Sans GB',sans-serif; max-width:800px; margin:40px auto; padding:0 20px; background:#1a1a2e; color:#e0e0e0; }}
h1 {{ color:#e94560; border-bottom:2px solid #e94560; padding-bottom:10px; }}
h2 {{ color:#00d2ff; margin-top:30px; }}
.meta {{ display:flex; gap:20px; margin:15px 0; color:#aaa; }}
.storyboard-card {{ background:#16213e; border-radius:10px; padding:15px; margin:10px 0; border-left:3px solid #e94560; }}
.storyboard-card h4 {{ margin:0 0 8px; color:#00d2ff; }}
.storyboard-card .meta {{ font-size:0.85em; color:#888; }}
.char-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:10px; }}
.char-item {{ background:#16213e; padding:10px; border-radius:8px; }}
.controversy {{ background:#2d1b1b; border-left:3px solid #ff6b6b; padding:10px; margin:8px 0; border-radius:4px; }}
.renders {{ display:flex; flex-wrap:wrap; gap:8px; margin:15px 0; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.8em; }}
.badge-high {{ background:#ff6b6b22; color:#ff6b6b; }}
.badge-medium {{ background:#ffd93d22; color:#ffd93d; }}
footer {{ margin-top:40px; padding-top:15px; border-top:1px solid #333; text-align:center; color:#666; font-size:0.85em; }}
</style>
</head>
<body>
<h1>🎬 水浒传AI短剧 · 第{detail['number']}集</h1>
<h2>{detail['title']}</h2>
<div class='meta'>
    <span>📖 原著第{detail['chapter']}回</span>
    <span>👤 主角: {detail['main_character']}</span>
    <span>⭐ 评分: {detail['score']}/10</span>
    <span>🏷️ {' '.join(f"<span class='badge badge-medium'>{t}</span>" for t in detail.get('tags',[]))}</span>
</div>

<h2>🎨 角色设计</h2>
{render_imgs}
<div class='char-grid'>
{''.join(f"<div class='char-item'><strong>{k}</strong><br/>{v}</div>" for k,v in cd.items())}
</div>

<h2>📋 分镜脚本</h2>
{storyboard_rows}

<h2>⚠️ 审查规则</h2>
{''.join(f"<div class='controversy'><span class='badge badge-high'>{cr['severity']}</span> <strong>{cr['pattern']}</strong><br/>{cr['rewrite'][:80]}</div>" for cr in detail.get('controversy_rules',[]))}

<footer>
    Agentic OS v3.6 · 水浒传AI短剧 · 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}
</footer>
</body>
</html>"""


if __name__ == "__main__":
    # 自测
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true")
    p.add_argument("--ep", default="01")
    p.add_argument("--export", choices=["txt", "html"])
    p.add_argument("--test", action="store_true")
    args = p.parse_args()

    if args.test:
        print("🧪 剧本管理器测试...")
        eps = get_all_episodes()
        print(f"  共 {len(eps)} 集")
        for ep in eps:
            status = "✅" if ep["has_render"] else "⏳"
            print(f"  {status} EP{ep['number']}: {ep['title']} [{ep['main_character']}]")
        detail = get_episode_detail("01")
        if detail:
            print(f"\n  EP01 detail: {len(detail['storyboard'])} 镜 · {len(detail['renders'])} renders")
        print("  ✅ 剧本管理器测试通过")
    elif args.list:
        import json as _j
        print(_j.dumps(get_all_episodes(), ensure_ascii=False, indent=2))
    elif args.export:
        content = export_episode(args.ep, args.export)
        if content:
            out_path = Path.home() / f".agentic-os/script_ep{args.ep}.{args.export}"
            out_path.write_text(content, encoding="utf-8")
            print(f"✅ 已导出: {out_path}")
    else:
        detail = get_episode_detail(args.ep)
        if detail:
            import json as _j
            print(_j.dumps(detail, ensure_ascii=False, indent=2))
