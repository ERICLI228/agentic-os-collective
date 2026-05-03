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
    "01": {"id": "lutixia_quan_da_zhenguanxi", "title": "鲁提辖拳打镇关西", "chapter": 3, "character": "鲁智深",
            "idx": 0, "dir": "episode_01", "scene_key": "渭州"},
    "02": {"id": "lu_zhishen_daoba_chuiyangliu", "title": "鲁智深倒拔垂杨柳", "chapter": 4, "character": "鲁智深",
            "idx": 1, "dir": "episode_02", "scene_key": "大相国寺菜园"},
    "03": {"id": "linchong_fengxue_shanshenmiao", "title": "林冲风雪山神庙", "chapter": 10, "character": "林冲",
            "idx": 6, "dir": "episode_03", "scene_key": "风雪山神庙"},
    "04": {"id": "songjiang_sha_yanpoxi", "title": "宋江杀阎婆惜", "chapter": 22, "character": "宋江",
            "idx": 10, "dir": "episode_04", "scene_key": "梁山聚义厅"},
    "05": {"id": "likui_yiling_sha_sihu", "title": "李逵沂岭杀四虎", "chapter": 43, "character": "李逵",
            "idx": 9, "dir": "episode_05", "scene_key": "梁山"},
    "06": {"id": "zhiqu_shengchengang", "title": "智取生辰纲", "chapter": 16, "character": "吴用",
            "idx": 8, "dir": "episode_06", "scene_key": "景阳冈"},
    "07": {"id": "wusong_dahu", "title": "武松打虎", "chapter": 23, "character": "武松",
            "idx": 2, "dir": "episode_07", "scene_key": "景阳冈"},
    "08": {"id": "wusong_dousha_ximenqing", "title": "武松斗杀西门庆", "chapter": 27, "character": "武松",
            "idx": 3, "dir": "episode_08", "scene_key": "狮子楼"},
    "09": {"id": "linchong_xueye_shang_liangshan", "title": "林冲雪夜上梁山", "chapter": 11, "character": "林冲",
            "idx": 7, "dir": "episode_09", "scene_key": "梁山"},
    "10": {"id": "huaheshang_danao_wutaishan", "title": "花和尚大闹五台山", "chapter": 4, "character": "鲁智深",
            "idx": 11, "dir": "episode_10", "scene_key": "五台山"},
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

EP_ORDER = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

# 角色名→文件ID映射
CHARACTER_ID_MAP = {
    "武松": "wusong",
    "鲁智深": "luzhishen",
    "林冲": "linchong",
    "宋江": "songjiang",
    "李逵": "likui",
    "吴用": "wuyong",
    "卢俊义": "lujunyi",
    "公孙胜": "gongsunsheng",
    "关胜": "guansheng",
    "秦明": "qinming",
    "呼延灼": "huyanzhuo",
    "花荣": "huarong",
    "柴进": "chaijin",
    "李应": "liying",
    "朱仝": "zhutong",
    "董平": "dongping",
    "张清": "zhangqing",
    "杨志": "yangzhi",
    "徐宁": "xuning",
    "索超": "suochao",
    "戴宗": "daizong",
    "刘唐": "liutang",
    "史进": "shijin",
    "穆弘": "muhong",
    "雷横": "leiheng",
    "李俊": "lijun",
    "阮小二": "ruanxiaoer",
    "张横": "zhangheng",
    "阮小五": "ruanxiaowu",
    "张顺": "zhangshun",
    "阮小七": "ruanxiaoqi",
    "杨雄": "yangxiong",
    "石秀": "shixiu",
    "解珍": "xiezhen",
    "解宝": "jiebao",
    "燕青": "yanqing",
    "朱武": "zhuwu",
    "黄信": "huangxin",
    "孙立": "sunli",
    "宣赞": "xuanzan",
    "郝思文": "haosiwen",
    "韩滔": "hantao",
    "彭玘": "pengqi",
    "单廷珪": "shantinggui",
    "魏定国": "weidingguo",
    "萧让": "xiaorang",
    "裴宣": "peixuan",
    "欧鹏": "oupeng",
    "邓飞": "dengfei",
    "燕顺": "yanshun",
    "杨林": "yanglin",
    "凌振": "lingzhen",
    "蒋敬": "jiangjing",
    "吕方": "lvfang",
    "郭盛": "guosheng",
    "安道全": "andaoquan",
    "皇甫端": "huangfuduan",
    "王英": "wangying",
    "扈三娘": "husanniang",
    "鲍旭": "baoxu",
    "樊瑞": "fanrui",
    "孔明": "kongming",
    "孔亮": "kongliang",
    "项充": "xiangchong",
    "李衮": "ligun",
    "金大坚": "jindajian",
    "马麟": "malin",
    "童威": "tongwei",
    "童猛": "tongmeng",
    "侯健": "houjian",
    "陈达": "chenda",
    "杨春": "yangchun",
    "郑天寿": "zhengtianshou",
    "陶宗旺": "taozongwang",
    "宋清": "songqing",
    "乐和": "yuehe",
    "龚旺": "gongwang",
    "丁得孙": "dingdesun",
    "穆春": "muchun",
    "曹正": "caozheng",
    "宋万": "songwan",
    "杜迁": "duqian",
    "薛永": "xueyong",
    "施恩": "shien",
    "李忠": "lizhong",
    "周通": "zhoutong",
    "汤隆": "tanglong",
    "杜兴": "duxing",
    "邹渊": "zouyuan",
    "邹润": "zourun",
    "朱贵": "zhugui",
    "朱富": "zhufu",
    "蔡福": "caifu",
    "蔡庆": "caiqing",
    "李立": "lili",
    "李云": "liyun",
    "焦挺": "jiaoting",
    "石勇": "shiyong",
    "孙新": "sunxin",
    "顾大嫂": "gudasao",
    "张青": "zhangqing_shop",
    "孙二娘": "sunerniang",
    "王定六": "wangdingliu",
    "郁保四": "yubaosi",
    "白胜": "baisheng",
    "时迁": "shiqian",
    "段景住": "duanjingzhu",
    "晁盖": "chaogai",
}

def get_color_palette(character_name):
    role = ROLE_OVERVIEW.get(character_name, {})
    color = role.get("color", "#1a1a2e+#8b0000")
    parts = color.split("+")
    return tuple(parts) if len(parts) == 2 else ("#1a1a2e", "#8b0000")

def _get_render_dir(character_name):
    """获取角色的渲染图目录（直接使用传入名称，不再通过ID映射转换）"""
    return RENDER_DIR / character_name

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
        renders = _count_renders(_get_render_dir(info["character"]))
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
            "has_render": bool(renders),
            "scene_count": len(renders),
            "render_files": [p.name for p in renders],
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
    """v3.8: 工业级分镜数据模型 — timecode, music_cue, dialogue[], shot_type, color_palette, pacing"""
    import json as _json
    ep_data_path = Path(__file__).resolve().parent / "episode_templates.json"
    templates = {}
    if ep_data_path.exists():
        templates = _json.loads(ep_data_path.read_text(encoding="utf-8"))
    key = title if title in templates else list(templates.keys())[0] if templates else None
    storyboard = templates.get(key, []) if key else []
    if not storyboard:
        storyboard = [
            {"seq": i+1, "shot_label": "镜" + str(i+1).zfill(2), "act": act,
             "scene": "场景" + str(i+1), "description": character + "的精彩演绎",
             "timecode": {"start": "00:00", "end": "01:00"},
             "music_cue": "待定义", "shot_type": "中景", "camera_move": "固定",
             "pacing": "normal", "color_palette": "待定义",
             "dialogue": [], "emotion": "待定义", "duration": 60, "performance_notes": []}
            for i, act in enumerate(["开场", "发展", "冲突", "高潮", "结局"])
        ]
    return storyboard


def compute_dialogue_stats(storyboard):
    """v3.8: 计算对白比例统计 — classical vs modern word counts"""
    classical_words = 0
    modern_words = 0
    for shot in storyboard:
        for d in shot.get("dialogue", []):
            text = d.get("text", "")
            wc = len(text.replace(" ", ""))
            if d.get("style") == "classical":
                classical_words += wc
            else:
                modern_words += wc
    total = classical_words + modern_words
    classical_pct = round(classical_words / total * 100) if total > 0 else 0
    modern_pct = round(modern_words / total * 100) if total > 0 else 0
    return {
        "classical_chars": classical_words,
        "modern_chars": modern_words,
        "total_chars": total,
        "classical_pct": classical_pct,
        "modern_pct": modern_pct,
        "ratio_label": "⚔ " + str(classical_pct) + "% 古典 / " + str(modern_pct) + "% 现代"
    }


def get_episode_detail_rich(ep_num):
    """v3.8: 工业级端点 — 返回完整 timecode+music_cue+dialogue[]+color_palette+pacing"""
    detail = get_episode_detail(ep_num)
    if not detail:
        return None
    stats = compute_dialogue_stats(detail.get("storyboard", []))
    detail["dialogue_stats"] = stats
    return detail


def get_dialogue_stats(ep_num):
    """v3.8: 对白比例统计端点"""
    detail = get_episode_detail(ep_num)
    if not detail:
        return None
    return compute_dialogue_stats(detail.get("storyboard", []))


def get_all_dialogue_stats():
    """v3.8: 全部剧集对白比例统计"""
    episodes = get_all_episodes()
    result = []
    for ep in episodes:
        ep_num = str(ep["episode"]).zfill(2)
        stats = get_dialogue_stats(ep_num)
        result.append({
            "episode": ep_num,
            "title": ep["title"],
            "character": ep["main_character"],
            "stats": stats or {"classical_chars": 0, "modern_chars": 0, "total_chars": 0}
        })
    return result

def build_rewrite_prompt(original_storyboard, ep_title, feedback_type, feedback_desc, params=None):
    """v3.9: Build AI rewrite prompt matching user's example quality — 07 shot industrial script"""
    import json as _json

    sb_text = _json.dumps(original_storyboard, ensure_ascii=False, indent=2)
    orig_len = len(original_storyboard)

    type_hints = {
        "剧情节奏": "以下改写要点：\n1. 原"+str(orig_len)+"镜必须扩展为"+str(orig_len+2)+"镜\n2. 新增1镜'归途/心理转变'过渡段（act='转折'）\n3. 新增1镜环境/气氛渲染（act='开幕'或'插入'）\n4. 冲突段扩展为2镜对峙+高潮，占总时长40%以上\n5. 每镜必须标注 camera_script（推/拉/摇/移/跟/闪回）",
        "剧本质量": "以下改写要点：\n1. description 必须是电影级画面描述（光影/构图/色彩/镜头运动）\n2. music_cue 具体到乐器+情绪（如'风雪底噪+单簧管哀伤主题'）\n3. camera_script 必须有推拉摇移和剪辑节奏描述\n4. 至少1镜包含闪回/回忆/快剪\n5. 终场镜标注 end_credit:true 并附字幕文案",
        "角色形象": "以下改写要点：\n1. 强化主角语言风格一致性（林冲=隐忍刚毅，鲁智深=豪迈粗犷）\n2. classical 风格台词需有文学性但不拗口\n3. 添加 performance_notes 描述微表情和小动作",
        "逻辑一致性": "以下改写要点：\n1. 时间线必须连续无跳跃\n2. 空间逻辑一致\n3. 情节因果递进\n4. 修复不符合原著人物性格的对白",
        "配音": "以下改写要点：\n1. voice_dir 必须明确标注情绪和气声要求\n2. timing_hint 标注停顿/节奏\n3. 对话节奏错落有致，避免连续长句堆砌",
        "其他": "请基于以下反馈进行全面优化：\n"
    }

    hint = type_hints.get(feedback_type, type_hints["其他"])
    desc_line = "\n具体要求: " + feedback_desc if feedback_desc else ""

    system_prompt = """你是一位资深影视编剧和分镜导演，精通中国古典文学改编，尤其擅长《水浒传》人物塑造和戏剧冲突设计。

你的任务是根据用户反馈，重写短剧单集的故事板分镜脚本，产出AI数字漫画短剧可直接使用的工业级脚本。

【核心风格指引】
1. 对白比例：30%半文半白古典风(style='classical') + 70%现代白话(style='modern')
2. 古典台词必须有文学质感但不拗口；现代台词需自然有力量
3. description 必须是电影级画面描述——必须有光影、构图、色彩、镜头运动
4. camera_script 必须详细描述推拉摇移跟、闪回、快切、慢镜等
5. music_cue 必须具体到乐器、情绪和音效

【输出格式】严格的 JSON，每个镜必须15字段齐全。"""

    target_shots = 7 if orig_len <= 5 else (orig_len + 2)
    target_dur = target_shots * 55

    user_prompt = f"""请重写{ep_title}的工业级故事板分镜脚本。

【原始分镜（{orig_len}镜）】
{sb_text}

【反馈意见】
类型: {feedback_type}
{hint}{desc_line}

【必须遵守的输出规范】
1. 总镜头数: {target_shots}镜，总时长控制在{target_dur}秒以内
2. 结构必须包含: 开场→发展→转折→冲突→对峙→高潮→结局（每镜分配5-6个act标签之一）
3. 每镜 description 必须包含:
   - 🎬 景别标注: 如'【远景】''【中景】''【特写】''【大远景】'等
   - 镜头运动方向: 如'镜头推进至中景''旋转镜头''俯拍→水平跟拍'
   - 画面氛围: 光影/色调/天气/时间
4. camera_script 必须描述本镜的所有摄影动作: 推/拉/摇/移/跟/闪回/快切/慢镜
5. dialogue 每条必须包含:
   - speaker: 角色名
   - text: 对白文本（classical风格用半文半白，modern风格用自然白话）
   - style: 'classical' 或 'modern'
   - voice_dir: 演技指导，如'(沧桑气声，气息凝白)' '(拱手，真诚)' '(冷笑)' '(哽咽)'
   - emotion_mark: 情感标签，如'悲怆' '怒极' '隐忍' '平静下的爆发'
   - subtext: 潜台词
   - timing_hint: '停顿3秒' '语速渐快' '声渐低'等节奏标注
6. performance_notes 至少2条：微表情、小动作、走位
7. 冲突段和高潮段必须各有独立完整的情绪弧线
8. end_credit: 最后一镜设为true，包含黑屏字幕文案
9. 至少包含2条 classical 风格对白，至少2条配音导向明确的 voice_dir

【输出JSON示例格式】
{{\"storyboard\": [{{\"seq\":1, \"shot_label\":\"镜01\", \"act\":\"开场\",
\"scene\":\"沧州草料场外·黄昏\",
\"description\":\"🎬 【远景】落日沉入铅灰色云层，沧州大地银装素裹。风雪如刀...\",
\"timecode\":{{\"start\":\"00:00\",\"end\":\"00:45\"}},
\"music_cue\":\"风雪底噪+单簧管哀伤主题\",
\"shot_type\":\"远景\", \"camera_move\":\"推→中景\", \"pacing\":\"slow\",
\"color_palette\":\"铅灰+银白+暗金\",
\"camera_script\":\"远景3秒→慢推至中景8秒→跟拍林冲行走→推至面部特写\",
\"duration\":45, \"emotion\":\"苍凉\",
\"dialogue\":[
  {{\"speaker\":\"林冲\",\"text\":\"人道我林冲是八十万禁军教头，风光无限。\",\"style\":\"classical\",\"voice_dir\":\"沧桑气声，气息凝白\",\"emotion_mark\":\"自嘲/悲凉\",\"subtext\":\"外表风光，内里落魄\",\"timing_hint\":\"缓速\"}},
  {{\"speaker\":\"林冲\",\"text\":\"却不知……这天地间，原无一处可容落魄之人。\",\"style\":\"classical\",\"voice_dir\":\"气声渐弱\",\"emotion_mark\":\"悲怆\",\"subtext\":\"看透自己命运\",\"timing_hint\":\"停顿3秒→声渐低\"}}
],
\"performance_notes\":[\"眯眼迎风时右肩微沉\",\"提枪换手时停顿半秒\"],
\"end_credit\":false}}
]}}

直接输出JSON，不要markdown代码块。"""

    return {"system": system_prompt, "user": user_prompt, "original_sb_len": orig_len}


def parse_ai_storyboard(ai_response_text):
    """v3.9: Parse AI response JSON, validate 15 fields per shot"""
    import json as _json

    text = ai_response_text.strip()
    for marker in ("```json", "```"):
        if marker in text:
            parts = text.split(marker)
            text = parts[1].split("```")[0].strip() if len(parts) > 1 else text

    data = _json.loads(text)
    storyboard = data.get("storyboard", data if isinstance(data, list) else [])

    required_fields = ["seq", "shot_label", "act", "scene", "description",
                       "timecode", "music_cue", "shot_type", "camera_move",
                       "pacing", "color_palette", "duration", "emotion",
                       "dialogue", "performance_notes"]

    validated = []
    errors = []
    for i, shot in enumerate(storyboard):
        missing = [f for f in required_fields if f not in shot]
        if missing:
            errors.append("Shot " + str(i+1) + " missing: " + str(missing))
            continue
        if not isinstance(shot.get("dialogue"), list):
            shot["dialogue"] = []
        if not isinstance(shot.get("performance_notes"), list):
            shot["performance_notes"] = []
        tc = shot.get("timecode", {})
        if not isinstance(tc, dict) or "start" not in tc or "end" not in tc:
            shot["timecode"] = {"start": "00:00", "end": "01:00"}
        if not shot.get("camera_script"):
            shot["camera_script"] = shot.get("camera_move", "") + " 中景"
        for d in shot.get("dialogue", []):
            d.setdefault("emotion_mark", "")
            d.setdefault("subtext", "")
            d.setdefault("timing_hint", "")
        shot.setdefault("end_credit", False)
        validated.append(shot)

    return {"storyboard": validated, "errors": errors}


def rewrite_episode_to_json(ep_title, storyboard):
    """v3.9: Write AI rewrite result back to episode_templates.json"""
    import json as _json

    ep_data_path = Path(__file__).resolve().parent / "episode_templates.json"
    templates = {}
    if ep_data_path.exists():
        templates = _json.loads(ep_data_path.read_text(encoding="utf-8"))

    if not isinstance(storyboard, list):
        storyboard = storyboard.get("storyboard", [])

    templates[ep_title] = storyboard
    ep_data_path.write_text(_json.dumps(templates, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(storyboard)


def get_version_history(ep_title=None):
    """v3.10: 读取 _version_history 版本变更记录"""
    import json as _json
    ep_data_path = Path(__file__).resolve().parent / "episode_templates.json"
    if not ep_data_path.exists():
        return []
    data = _json.loads(ep_data_path.read_text(encoding="utf-8"))
    history = data.get("_version_history", [])
    if ep_title:
        history = [h for h in history if h.get("episode") == ep_title]
    return sorted(history, key=lambda h: h.get("timestamp", ""), reverse=True)


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


def _dialogue_to_text(dialogue):
    """v3.9: 兼容 string 和 array 两种 dialogue 格式"""
    if isinstance(dialogue, list):
        return " ".join(
            f"{d.get('speaker','')}: {d.get('text','')}"
            for d in dialogue
        )
    if isinstance(dialogue, str):
        return dialogue
    return ""


def _export_srt(detail):
    """v3.11.2: 导出为 SRT 字幕格式 — 每条对白独立时间码"""
    sb = detail.get("storyboard", [])
    dialogue_entries = []
    for shot_i, shot in enumerate(sb):
        tc = shot.get("timecode", {})
        start_str = tc.get("start", "00:00")
        end_str = tc.get("end", "01:00")
        dialogue_lines = shot.get("dialogue", [])
        if isinstance(dialogue_lines, list):
            for dl in dialogue_lines:
                speaker = dl.get("speaker", "")
                text = dl.get("text", "")
                if text:
                    dialogue_entries.append({
                        "start": start_str,
                        "end": end_str,
                        "text": f"{speaker}: {text}" if speaker else text
                    })
        elif isinstance(dialogue_lines, str) and dialogue_lines.strip():
            dialogue_entries.append({"start": start_str, "end": end_str, "text": dialogue_lines})
    lines = []
    for idx, entry in enumerate(dialogue_entries, 1):
        lines.append(str(idx))
        lines.append(f"{entry['start']},000 --> {entry['end']},000")
        lines.append(entry['text'])
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
        lines.append(f"  镜{sb['seq']} [{sb['act']}] {sb.get('shot_label','')} · {sb.get('duration','')}")
        lines.append(f"  {sb['description']}")
        lines.append(f"  情绪: {sb['emotion']}")
        if sb.get("dialogue"):
            dia_lines = sb["dialogue"]
            if isinstance(dia_lines, list):
                for dl in dia_lines:
                    speaker = dl.get("speaker", "")
                    text = dl.get("text", "")
                    style = dl.get("style", "")
                    tag = "⚔" if style == "classical" else "💬"
                    lines.append(f"  {tag} {speaker}: {text}")
                    if dl.get("voice_dir"):
                        lines.append(f"    🎤 voice: {dl['voice_dir']}")
                    if dl.get("emotion_mark"):
                        lines.append(f"    😶 emotion: {dl['emotion_mark']}")
            else:
                lines.append(f"  对白: {_dialogue_to_text(dia_lines)}")

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
            <div class='meta'>情绪: {sb['emotion']}{' · 对白: ' + _dialogue_to_text(sb['dialogue']) if sb.get('dialogue') else ''}</div>
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
