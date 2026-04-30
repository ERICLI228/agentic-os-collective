#!/usr/bin/env python3
"""
角色档案生成器 v1.0 — 基于 name + title 自动生成完整的角色小传
调用 CODING/GLM API 生成 personality/appearance/background 等内容

用法:
  python3 character_profile_generator.py 武松 "行者·打虎英雄"
  python3 character_profile_generator.py --all  # 为所有角色生成
"""
from __future__ import annotations
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

# ── 加载 .env ──
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

BIBLE_PATH = Path.home() / ".agentic-os" / "character_designs" / "visual_bible.json"

# ── 模型路由: CODING 免费额度 ──
MODEL = os.getenv("CHAR_GEN_MODEL", "coding/")

# ── 已知角色预设（AI 生成失败时的 fallback） ──
KNOWN_PROFILES = {
    "武松": {
        "core_traits": ["勇猛刚直", "嫉恶如仇", "重情重义", "嗜酒豪爽"],
        "emotional_range": "外刚内柔，对兄弟情深义重，对仇人冷酷无情",
        "speech_style": "粗犷豪迈，声音洪亮，喜用江湖切口",
        "catchphrases": ["俺武松行不更名，坐不改姓！", "酒来！今日定要喝个痛快！", "你这厮，吃俺一拳！"],
        "habits": ["每日必饮酒，无酒不欢", "走路虎虎生风，自带威压", "说话时习惯拍案而起"],
    },
    "鲁智深": {
        "core_traits": ["豪爽直率", "嫉恶如仇", "粗中有细", "扶弱抑强"],
        "emotional_range": "外表粗犷豪放，内心慈悲为怀，路见不平必拔刀相助",
        "speech_style": "声如洪钟，说话直来直去，不喜拐弯抹角",
        "catchphrases": ["洒家姓鲁，名智深，绰号花和尚！", "呔！你这鸟人，吃洒家一拳！", "酒肉穿肠过，佛祖心中留！"],
        "habits": ["大口吃肉大碗喝酒，僧人戒律一概不理", "遇到不平事，先动手后动脑", "高兴时仰天大笑，声震屋瓦"],
    },
    "林冲": {
        "core_traits": ["隐忍克制", "武艺超群", "忠厚老实", "被逼至绝处方爆发"],
        "emotional_range": "长期忍辱负重，内心悲愤压抑，爆发时如雷霆万钧",
        "speech_style": "言辞克制有礼，但字字含恨，悲壮沉郁",
        "catchphrases": ["林冲一生清白，奈何奸臣当道！", "八十万禁军教头，竟落得如此下场！", "今日林冲便要讨个公道！"],
        "habits": ["独处时习惯性抚摸丈八蛇矛", "眉头常锁，若有所思", "饮酒时沉默不语，一饮而尽"],
    },
    "宋江": {
        "core_traits": ["仗义疏财", "深谋远虑", "重视兄弟情义", "被逼时可下狠手"],
        "emotional_range": "表面温厚仁和，内心城府极深，被逼到绝境时会突然致命",
        "speech_style": "谦和有礼，措辞谨慎，说话时善于观察对方反应",
        "catchphrases": ["宋江不才，愿为各位哥哥效犬马之劳！", "替天行道，乃我梁山本分！", "兄弟们的情义，宋江铭记于心！"],
        "habits": ["说话时习惯拱手作揖", "遇事先想后果，再定行动", "独处时常面露忧色"],
    },
    "李逵": {
        "core_traits": ["暴烈凶猛", "天真烂漫", "极度孝顺", "对宋江绝对忠诚"],
        "emotional_range": "情绪极端，高兴时手舞足蹈，愤怒时如疯虎，悲伤时嚎啕大哭",
        "speech_style": "嗓门极大，说话直白粗鲁，常大喊大叫",
        "catchphrases": ["铁牛在此！谁敢过来！", "哥哥说有，铁牛就去杀！", "娘啊！儿来迟了！"],
        "habits": ["遇事第一反应是动手而不是动嘴", "见到哥哥宋江就咧嘴傻笑", "赤膊上阵，不爱穿铠甲"],
    },
    "吴用": {
        "core_traits": ["足智多谋", "沉着冷静", "善用人心", "文雅中暗藏狡黠"],
        "emotional_range": "始终从容不迫，胜券在握时微微一笑，局势不利时反而更冷静",
        "speech_style": "语速平缓，措辞文雅，说话时习惯摇羽扇，每句话都暗藏机锋",
        "catchphrases": ["此事不难，吴某已有一计。", "兵不厌诈，且看我安排。", "天时地利人和，缺一不可。"],
        "habits": ["思考时习惯轻摇羽扇", "下棋布局，以棋喻事", "笑时嘴角微扬，从不大笑"],
    },
    "杨志": {
        "core_traits": ["骄傲自尊", "刚毅不屈", "重视荣誉", "落魄但不失尊严"],
        "emotional_range": "表面冷峻，内心极度骄傲，落魄后压抑着不甘与愤懑",
        "speech_style": "言辞简洁有力，不爱多说，但每句话都掷地有声",
        "catchphrases": ["俺乃杨家将后人，岂能受你这泼皮辱没！", "祖传宝刀在此，不识货的滚开！", "杨志宁可饿死，不折尊严！"],
        "habits": ["习惯性摩挲祖传宝刀刀柄", "站姿笔挺，军人习惯不改", "被激怒时咬牙忍住的微表情"],
    },
    "晁盖": {
        "core_traits": ["仗义疏财", "善于谋略", "天生的领袖魅力", "从容不迫"],
        "emotional_range": "沉稳大气，对兄弟慷慨大方，面对危险时愈发冷静",
        "speech_style": "声音洪亮，措辞大气，说话时不怒自威",
        "catchphrases": ["晁某一生仗义，各位兄弟的事就是我的事！", "十万贯生辰纲，取之何妨！", "梁山聚义，替天行道！"],
        "habits": ["说话时习惯性捋胡须", "做决定前目光扫视众人", "大笑时声如洪钟"],
    },
}


def generate_character_profile(name: str, title: str, source_material: str = "水浒传") -> dict:
    """
    根据角色名和称号，生成完整的角色档案

    Args:
        name: 角色名（如"武松"）
        title: 称号（如"行者·打虎英雄"）
        source_material: 来源IP

    Returns:
        完整的角色档案字典
    """
    # 1. 先查已知预设（快速 fallback）
    if name in KNOWN_PROFILES:
        return _build_profile(name, title, KNOWN_PROFILES[name])

    # 2. 尝试 AI 生成
    ai_result = _ai_generate(name, title, source_material)
    if ai_result:
        return _build_profile(name, title, ai_result)

    # 3. 完全失败：返回基础骨架
    return _build_profile(name, title, {
        "core_traits": ["待补充"],
        "emotional_range": "待补充",
        "speech_style": "待补充",
        "catchphrases": ["待补充"],
        "habits": ["待补充"],
    })


def _build_profile(name: str, title: str, personality_data: dict) -> dict:
    """从 personality 数据构建完整档案"""
    from script_manager import ROLE_OVERVIEW
    existing = ROLE_OVERVIEW.get(name, {})

    color = existing.get("color", "#1a1a2e+#8b0000")
    parts = color.split("+")

    return {
        "personality": {
            "core_traits": personality_data.get("core_traits", []),
            "emotional_range": personality_data.get("emotional_range", ""),
            "speech_style": personality_data.get("speech_style", ""),
            "catchphrases": personality_data.get("catchphrases", []),
            "habits": personality_data.get("habits", []),
        },
        "appearance": {
            "costume": existing.get("face", "宋代武者装扮"),
            "accessories": [existing.get("weapon", "")] if existing.get("weapon") else [],
            "color_palette": {
                "primary": parts[0] if len(parts) > 0 else "#1a1a2e",
                "secondary": parts[1] if len(parts) > 1 else "#8b0000",
                "accent": parts[2] if len(parts) > 2 else "#d4a574",
            },
        },
        "voice": {
            "nls_speaker": existing.get("voice", "").split("(")[0] or "zhiming",
            "description": existing.get("voice", ""),
            "sample_text": f"{name}在此！{title}！",
        },
    }


def _ai_generate(name: str, title: str, source: str) -> Optional[dict]:
    """调用 AI API 生成角色档案"""
    try:
        from openai import OpenAI

        prompt = f"""你是资深影视角色设计师，专攻古典文学IP的角色可视化。

请为《{source}》中的角色 **{name}（{title}）** 生成完整的角色设定档案。

要求：
1. 性格特征：3-5个核心性格词 + 情感层次描述 + 说话风格
2. 口头禅：3句符合角色性格的日常用语
3. 习惯动作：3个独特的肢体语言或习惯
4. 外貌描述：身高体型、面部特征（需符合原著）
5. 服饰设计：符合宋代背景的服装描述 + 配色方案
6. 角色关系：与2-3个其他角色的关系简述
7. 故事背景：角色出身 + 3个关键人生事件

请严格以 JSON 格式输出，不要任何额外文字。格式：
{{
  "core_traits": ["性格1", "性格2", "性格3"],
  "emotional_range": "情感层次描述",
  "speech_style": "说话风格",
  "catchphrases": ["口头禅1", "口头禅2", "口头禅3"],
  "habits": ["习惯1", "习惯2", "习惯3"]
}}"""

        client = OpenAI(
            api_key=os.getenv("CODING_API_KEY", ""),
            base_url=os.getenv("CODING_BASE_URL", "https://api.coding.ai/v1"),
        )
        resp = client.chat.completions.create(
            model=MODEL.rstrip("/"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            timeout=30,
        )
        text = resp.choices[0].message.content.strip()
        # 清理可能的 markdown 包裹
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()
        return json.loads(text)
    except Exception as e:
        print(f"⚠️ AI 生成失败: {e}，使用预设 fallback")
        return None


def regenerate_render_on_profile_change(character_id: str, changed_fields: list) -> dict:
    """
    当角色属性变更时，判断是否需要重新渲染
    如果涉及 appearance/costume/color 变更，返回重新渲染指令

    Returns:
        {"need_rerender": True/False, "reason": "..."}
    """
    RENDER_FIELDS = {"appearance", "color_palette", "costume", "accessories", "basic_info"}
    need = bool(set(changed_fields) & RENDER_FIELDS)
    return {
        "need_rerender": need,
        "reason": f"修改了 {', '.join(changed_fields)}，涉及外观变更" if need else "仅修改非视觉属性，无需重新渲染",
    }


# ── CLI 入口 ──
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        name = sys.argv[1]
        title = sys.argv[2]
        profile = generate_character_profile(name, title)
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == "--all":
        # 为所有角色生成并合并到 visual_bible
        with open(BIBLE_PATH, encoding="utf-8") as f:
            bible = json.load(f)
        for char_id, ch in bible["characters"].items():
            name = ch.get("name", char_id)
            title = ch.get("title", "")
            profile = generate_character_profile(name, title)
            ch["personality"] = profile.get("personality", ch.get("personality", {}))
            ch["appearance"] = profile.get("appearance", ch.get("appearance", {}))
            ch["voice"] = profile.get("voice", ch.get("voice", {}))
        with open(BIBLE_PATH, "w", encoding="utf-8") as f:
            json.dump(bible, f, ensure_ascii=False, indent=2)
        print("✅ All characters regenerated")
    else:
        print("用法: python3 character_profile_generator.py <角色名> <称号>")
        print("   或: python3 character_profile_generator.py --all")
