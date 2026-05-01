#!/usr/bin/env python3
"""Add video_prompts (three-scheme: portrait/scene/cinematic) to visual_bible.json for all characters.
Uses existing character trait data (appearance, personality, scenes) to personalize prompts.
"""
import json, os, sys
from datetime import datetime

VISUAL_BIBLE = os.path.expanduser("~/.agentic-os/character_designs/visual_bible.json")

# ── template helpers ──────────────────────────────────────────────────────

def scheme_1_portrait(char):
    """静态肖像特写: close-up, micro-movements, fixed camera"""
    name = char.get("name", "")
    name_en = name
    basic = char.get("basic_info", {})
    appearance = char.get("appearance", {})
    face = basic.get("face", "distinctive face")
    build = basic.get("build", "")
    color = appearance.get("color_palette", {})
    costume = appearance.get("costume", "ancient Chinese attire")

    prompt = (
        f"A hyperrealistic close-up portrait of {name_en}, "
        f"{face}. "
        f"{'His ' + build + ' physique is subtly outlined by sunlight.' if build else ''} "
        f"Wearing {costume}. "
        f"Slight subtle movements of hair and clothing in a gentle breeze. "
        f"Static camera, fixed shot. Natural cinematic lighting, "
        f"cinematic film grain, 1998 Chinese TV drama aesthetic."
    )
    short = (
        f"A hyperrealistic portrait of {name_en}. "
        f"His/her distinctive features are illuminated by natural light. "
        f"A gentle breeze stirs his/her robes. Fixed camera, cinematic lighting."
    )
    return {
        "title": "静态肖像特写（推荐首选）",
        "desc": f"捕捉{name}的标志性外貌特征，通过微妙的动态和光影营造电影级的庄重感。",
        "prompt": prompt,
        "简练版": short,
        "参数": "Duration: 3-5s, Model: Pollo 2.0 or Sora 2"
    }

def scheme_2_scene(char):
    """经典场景动态: iconic action/reaction, slow-motion"""
    name = char.get("name", "")
    name_en = name
    basic = char.get("basic_info", {})
    personality = char.get("personality", {})
    scene_data = char.get("scenes", [{}])
    costume = (char.get("appearance", {}) or {}).get("costume", "ancient attire")
    build = basic.get("build", "")

    # Pick key details from first scene if available
    first_scene = scene_data[0] if scene_data else {}
    scene_desc = first_scene.get("description", "")
    scene_loc = ""
    if "room" in scene_desc:
        scene_loc = "in an ancient room"
    elif "temple" in scene_desc:
        scene_loc = "in a temple courtyard"
    elif "forest" in scene_desc or "mountain" in scene_desc:
        scene_loc = "on a misty hillside"
    elif "hall" in scene_desc:
        scene_loc = "in a grand hall"
    elif "street" in scene_desc:
        scene_loc = "on an ancient street"
    else:
        scene_loc = "in a dramatic ancient setting"

    # Pick speech style for mood
    speech = personality.get("speech_style", "determined expression")
    emotional = personality.get("emotional_range", "focused and intense")

    prompt = (
        f"{name_en}, {build}, "
        f"wearing {costume}, {scene_loc}. "
        f"{'His ' + scene_desc[:80] if scene_desc else 'His/her expression is ' + emotional}. "
        f"Slow-motion, dynamic camera movement. "
        f"Atmospheric lighting, cinematic film grain, "
        f"1998 Chinese TV drama aesthetic."
    )
    return {
        "title": "经典场景动态",
        "desc": f"还原{name}的标志性场景或动作，强调其{emotional[:20]}的气质。",
        "prompt": prompt,
        "参数": "Duration: 3-5s, Model: Pollo 2.0 or Google Veo 3.1"
    }

def scheme_3_cinematic(char):
    """电影感运镜: slow push-in, depth of field, blurred background"""
    name = char.get("name", "")
    name_en = name
    basic = char.get("basic_info", {})
    personality = char.get("personality", {})
    face = basic.get("face", "distinctive face")
    costume = (char.get("appearance", {}) or {}).get("costume", "robes")
    habits = personality.get("habits", [])
    hab = habits[0] if habits else "gazing into the distance"

    prompt = (
        f"Slow push-in shot towards {name_en}, {face}. "
        f"Wearing {costume}, {hab.lower()}. "
        f"The background is a soft atmospheric blur of an ancient Chinese landscape. "
        f"Slight breeze stirring fabric. Slow-motion, "
        f"cinematic film grain, 1998 Chinese TV drama aesthetic."
    )
    return {
        "title": "电影感运镜",
        "desc": f"通过缓慢的镜头推进聚焦{name}的面部细节和眼神，强化角色气质与命运感。",
        "prompt": prompt,
        "参数": "Duration: 4-6s, Model: Pollo 2.0 or Kling AI"
    }

# ── main ──────────────────────────────────────────────────────────────────

def main():
    with open(VISUAL_BIBLE) as f:
        bible = json.load(f)

    chars = bible["characters"]
    added = 0
    skipped = 0

    canonical_ranks = {
        "songjiang": 1, "lujunyi": 2, "wuyong": 3, "gongsunsheng": 4,
        "guansheng": 5, "linchong": 6, "qinming": 7, "huyanzhuo": 8,
        "huarong": 9, "chaiijin": 10, "liying": 11, "zhutong": 12,
        "luzhishen": 13, "wusong": 14, "dongping": 15, "zhangqing_feishi": 16,
        "yangzhi": 17, "xuning": 18, "suochao": 19, "daizong": 20,
        "liutang": 21, "likui": 22, "shijin": 23, "muhong": 24,
        "leiheng": 25, "lijun": 26, "ruanxiaoer": 27, "zhangheng": 28,
        "ruanxiaowu": 29, "zhangshun": 30, "ruanxiaoqi": 31, "yangxiong": 32,
        "shixiu": 33, "xiezhen": 34, "jiebao": 35, "yanqing": 36,
        "zhuwu": 37, "huangxin": 38, "sunli": 39, "xuanzan": 40,
        "haosiwen": 41, "hantao": 42, "pengqi": 43, "shantinggui": 44,
        "weidingguo": 45, "xiaorang": 46, "peixuan": 47, "oupeng": 48,
        "dengfei": 49, "yanshun": 50, "yanglin_hs": 51, "lingzhen": 52,
        "jiangjing": 53, "lvfang": 54, "guosheng": 55, "andaoquan": 56,
        "huangfuduan": 57, "wangying": 58, "husanniang": 59, "baoxu": 60,
        "fanrui": 61, "kongming": 62, "kongliang": 63, "xiangchong": 64,
        "ligun": 65, "jindajian": 66, "malin": 67, "tongwei": 68,
        "tongmeng": 69, "mengkang": 70, "houjian": 71, "chenda": 72,
        "yangchun": 73, "zhengtianshou": 74, "taozongwang": 75,
        "songqing": 76, "yuehe": 77, "gongwang": 78, "dingdesun": 79,
        "muchun": 80, "caozheng": 81, "songwan": 82, "duqian": 83,
        "xueyong": 84, "shien": 85, "lizhong": 86, "zhoutong": 87,
        "tanglong": 88, "duxing": 89, "zouyuan": 90, "zourun": 91,
        "zhugui": 92, "zhufu": 93, "caifu": 94, "caiqing": 95,
        "lili": 96, "liyun": 97, "jiaoting": 98, "shiyong": 99,
        "sunxin": 100, "gudashao": 101, "zhangqing_caiyuan": 102,
        "sunerniang": 103, "wangdingliu": 104, "yubaosi": 105,
        "baisheng": 106, "shiqian": 107, "duanjingzhu": 108,
        "chaogai": 109,
    }

    for cid, char in chars.items():
        name = char.get("name", cid)
        # Skip if video_prompts already exists
        if "video_prompts" in char and char["video_prompts"]:
            skipped += 1
            continue

        # Ensure basic fields exist
        if "basic_info" not in char:
            char["basic_info"] = {
                "height": "不详", "build": "均匀", "face": f"{name}的特色面容", "age": "不详"
            }
        if "appearance" not in char:
            char["appearance"] = {
                "costume": "古代装束", "color_palette": {"primary": "#888", "secondary": "#666", "accent": "#444"},
                "design_notes": f"{name}的基础设计"
            }
        if "personality" not in char:
            char["personality"] = {
                "core_traits": ["特征不明"],
                "emotional_range": "平静",
                "speech_style": "平常语气",
                "catchphrases": [],
                "habits": []
            }
        if "scenes" not in char or not char["scenes"]:
            rank_info = f"star rank {canonical_ranks.get(cid, '?')}"
            char["scenes"] = [{"shot": "shot_01", "description": f"{name} at {rank_info}", "prompt": f"A portrait of {name}", "negative_prompt": ""}]

        video_prompts = {
            "方案一": scheme_1_portrait(char),
            "方案二": scheme_2_scene(char),
            "方案三": scheme_3_cinematic(char),
        }
        char["video_prompts"] = video_prompts
        added += 1

    bible["_video_prompts_added"] = datetime.now().isoformat()
    bible["_video_prompts_summary"] = {
        "total": len(chars),
        "added": added,
        "skipped_existing": skipped,
        "schema": "three-scheme portrait/scene/cinematic"
    }

    with open(VISUAL_BIBLE, "w", encoding="utf-8") as f:
        json.dump(bible, f, indent=2, ensure_ascii=False)

    print(f"✅ Done: {added} characters got video_prompts, {skipped} skipped (already had)")
    print(f"   File: {VISUAL_BIBLE}")


if __name__ == "__main__":
    main()
