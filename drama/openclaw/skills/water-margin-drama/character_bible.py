"""
水浒传 6 角色视觉圣经 — Visual Bible for AI Video Generation
每个角色提供: 外貌/服装/兵器/性格/中文描述 + English Stable Diffusion/Seedance prompt
"""
import json
import os
from pathlib import Path

CHARACTERS = {
    "wusong": {
        "name_cn": "武松",
        "name_en": "Wu Song",
        "episode": "EP01 · 武松打虎",
        "age": 28,
        "height": "188cm",
        "build": "muscular, broad shoulders, hero physique",
        "face": "square jaw, thick eyebrows, fierce eyes, high nose bridge, weathered skin",
        "hair": "long black hair tied in warrior bun, sideburns",
        "costume": "Song dynasty warrior: dark blue battle robe (战袍), leather belt with bronze buckle, "
                   "brown leather boots, red sash around waist, iron wrist guards",
        "weapon": "哨棒 (wooden staff, 1.8m, oak color)",
        "personality": "brave, righteous, hot-tempered, heavy drinker, loyal to brother",
        "key_scenes": [
            "drinking 18 bowls of wine at Jingyang Ridge inn",
            "bare-handed tiger fight in moonlight forest",
            "standing victorious on dead tiger, blood on fists",
        ],
        "cn_appearance": (
            "身材魁梧，身高八尺，虎背熊腰。方脸膛，浓眉大眼，目光如电。"
            "黑发束武士髻，留鬓角。身着玄青色战袍，腰系革带，足蹬快靴。"
            "手执哨棒，步履生风。面上常带三分酒意，七分豪气。"
        ),
        "en_prompt": (
            "a heroic Chinese warrior from Song dynasty, tall muscular build, "
            "square jaw, thick black eyebrows, fierce determined eyes, "
            "long black hair in warrior topknot, wearing dark blue battle robe "
            "with red sash, leather arm guards, standing in ancient Chinese forest "
            "at night with moonlight, cinematic lighting, photorealistic, 8K, "
            "Chinese water margin style, dramatic atmosphere"
        ),
        "color_palette": ["#1a1a2e", "#8b0000", "#d4a574", "#2d5016"],
        "voice": "nls_voice=zhiming (男声, 浑厚有力)",
    },

    "luzhishen": {
        "name_cn": "鲁智深",
        "name_en": "Lu Zhishen",
        "episode": "EP02 · 鲁智深倒拔垂杨柳",
        "age": 35,
        "height": "195cm",
        "build": "extremely muscular, giant frame, bear-like strength",
        "face": "round face, bushy beard, large eyes, red complexion from drinking, "
               "9 dot incense scars on forehead (monk ordination marks)",
        "hair": "shaved bald (Buddhist monk), full black beard",
        "costume": "Buddhist monk robe (袈裟) in grey-brown, prayer beads (108 beads) "
                   "around neck, straw sandals, iron staff leaning on shoulder",
        "weapon": "62斤水磨禅杖 (62-jin iron monk staff, crescent blade at top)",
        "personality": "fierce, straightforward, justice-driven, loves meat and wine despite being monk, "
                       "protective of the weak",
        "key_scenes": [
            "uprooting a full willow tree with bare hands",
            "wielding 62-jin iron staff with one arm",
            "laughing thunderously while drunk in temple courtyard",
        ],
        "cn_appearance": (
            "花和尚，身长八尺，腰阔十围，面圆耳大，鼻直口方。"
            "腮边一部络腮胡须，满布钢针般根根竖起。顶上九点戒疤，"
            "颈挂一百零八颗念珠。身着灰褐色僧袍，敞开胸膛，露出黑毛。"
            "手提水磨禅杖，杖头月牙铲寒光闪闪。"
        ),
        "en_prompt": (
            "a giant Chinese Buddhist warrior monk, bald head with 9 incense burn scars "
            "on forehead, full black beard, muscular bear-like physique, wearing grey-brown "
            "kasaya robe half open revealing chest, 108 prayer beads around neck, "
            "holding massive iron monk staff with crescent blade, standing in temple "
            "courtyard next to uprooted willow tree, dramatic lighting, photorealistic, "
            "Chinese water margin style, epic scale"
        ),
        "color_palette": ["#4a3728", "#8b7355", "#c4a35a", "#2f1f0f"],
        "voice": "nls_voice=zhiming (男声, 粗犷豪迈)",
    },

    "linchong": {
        "name_cn": "林冲",
        "name_en": "Lin Chong",
        "episode": "EP03 · 林冲风雪山神庙",
        "age": 34,
        "height": "182cm",
        "build": "lean and athletic, leopard-like agility, trained warrior",
        "face": "scholarly yet sharp features, thin mustache, piercing eyes, "
               "high cheekbones, weathered from exile",
        "hair": "long black hair, disheveled (exiled), tied loosely",
        "costume": "worn soldier uniform — faded red cape over battered armor, "
                   "fur-lined collar (winter scene), shackle marks on wrists, "
                   "straw cape (蓑衣) over shoulders in snow scene",
        "weapon": "丈八蛇矛 (18-foot serpent spear, polished steel tip)",
        "personality": "skilled, patient, endures humiliation until breaking point, "
                       "former 80,000 Imperial Guard instructor, tragic hero",
        "key_scenes": [
            "standing alone in snowstorm at Mountain Spirit Temple",
            "spear thrust through snow, killing revenge final blow",
            "fire-lit face reflecting agonized decision in blizzard",
        ],
        "cn_appearance": (
            "豹头环眼，燕颔虎须，身长八尺。原是八十万禁军教头，"
            "面如冠玉，唇若涂脂，但流放后面容憔悴，颧骨高耸。"
            "身披破旧红披风，内衬锁子甲，腕有镣铐痕。大雪中戴斗笠蓑衣，"
            "手持丈八蛇矛，枪尖寒芒刺骨。"
        ),
        "en_prompt": (
            "a Chinese warrior with scholarly face, lean athletic build, thin mustache, "
            "piercing eyes filled with sorrow and rage, disheveled long black hair, "
            "wearing worn red cape and battle armor with fur collar, shackle marks "
            "on wrists, holding 18-foot serpent spear, standing alone in heavy "
            "snowstorm in front of burning mountain temple, orange firelight on face, "
            "cinematic, dramatic contrast of fire and snow, photorealistic, 8K"
        ),
        "color_palette": ["#8b0000", "#1c1c2a", "#ffffff", "#ff4500"],
        "voice": "nls_voice=zhilun (男声, 沉郁悲壮)",
    },

    "songjiang": {
        "name_cn": "宋江",
        "name_en": "Song Jiang",
        "episode": "EP04 · 宋江怒杀阎婆惜",
        "age": 32,
        "height": "175cm",
        "build": "medium, unassuming official look, black complexion",
        "face": "dark complexion (黑面), short stature, scholarly eyes, "
               "calm expression hiding inner turmoil, thin eyebrows",
        "hair": "black hair in official's cap (乌纱帽), neat scholar appearance",
        "costume": "county clerk official robe (押司官服) in dark green, "
                   "official cap with wings, belt with jade buckle, "
                   "civil official boots. Later: simple commoner clothes",
        "weapon": "朴刀 (long-handled saber) — only when forced",
        "personality": "generous, calculating, values brotherhood above all, "
                       "Timely Rain (及时雨) nickname for helping others, "
                       "but capable of sudden lethal violence when pushed",
        "key_scenes": [
            "confronting Yan Poxi in dimly lit room, hand on hidden dagger",
            "briefcase of Liangshan letters discovered, face turns murderous",
            "blood on hands, standing over body, lamplight flickering",
        ],
        "cn_appearance": (
            "面黑身矮，人称黑宋江。坐定时浑如虎相，走动时有若狼形。"
            "眼如丹凤，眉似卧蚕，唇方口正，额阔顶平。身着押司绿袍，"
            "头戴乌纱，看似文弱书生，实则暗藏杀机。年及三旬，"
            "有养济万人之度量，怀扫除四海之心机。"
        ),
        "en_prompt": (
            "a Chinese Song dynasty county clerk, dark complexion, short stature, "
            "scholarly face with thin eyebrows and calm but intense eyes, "
            "wearing dark green official robe and black gauze cap, "
            "standing in dimly lit ancient Chinese room, one hand hidden "
            "behind back gripping something, lamplight casting dramatic shadows, "
            "expression shifting from calm to dangerous, moody atmosphere, "
            "cinematic, photorealistic, water margin drama style"
        ),
        "color_palette": ["#1a3a1a", "#2f1f0f", "#8b7355", "#ffd700"],
        "voice": "nls_voice=zhilun (男声, 沉稳内敛)",
    },

    "yangzhi": {
        "name_cn": "杨志",
        "name_en": "Yang Zhi",
        "episode": "EP05 · 杨志卖刀",
        "age": 30,
        "height": "185cm",
        "build": "tall, wiry, military bearing, face branded with exile mark",
        "face": "angular face, thin lips pressed tight with pride, "
               "golden brand/tattoo on cheek (criminal exile mark — 金印), "
               "proud eyes hiding desperation",
        "hair": "long black hair in military topknot, sweat-dampened",
        "costume": "worn military uniform (former Imperial Guard General), "
                   "patched but kept clean. Blue cloth wrap on head covering brand. "
                   "Simple cotton clothes, straw sandals. Proud despite poverty.",
        "weapon": "祖传宝刀 (ancestral treasure blade — legendary sharpness, "
                  "three special properties: cuts iron like mud, hair splits on edge, "
                  "kills without blood on blade)",
        "personality": "proud, stubborn, values honor above life, "
                       "descendant of famous general Yang Ye (杨家将), "
                       "fallen from grace, desperate but dignified",
        "key_scenes": [
            "standing in marketplace, sword planted in ground, straw in hair (selling sign)",
            "demonstrating blade cutting copper coin in one stroke",
            "confronting street thug Niu Er, hand tightening on sword hilt",
        ],
        "cn_appearance": (
            "面皮上老大一搭青记，腮边微露些少赤须。身躯凛凛，相貌堂堂。"
            "一双眼光射寒星，两弯眉浑如刷漆。原是殿司制使官，杨家将后人，"
            "因失陷花石纲被刺金印发配。身穿打补丁的青布旧军衣，却洗得一尘不染。"
            "脚踏草鞋，头缠青巾遮金印。手按祖传宝刀，虽落魄而气度不减。"
        ),
        "en_prompt": (
            "a tall Chinese warrior with angular proud face, thin tight lips, "
            "blue-green birthmark on cheek with golden criminal exile brand tattoo, "
            "piercing proud eyes hiding desperation, military topknot, "
            "wearing patched but clean blue military uniform, straw in hair "
            "indicating item for sale, hands resting on ancestral treasure sword, "
            "standing in bustling ancient Chinese marketplace, crowd blurred behind, "
            "dramatic contrast of fallen nobility, cinematic, photorealistic, 8K"
        ),
        "color_palette": ["#2d5016", "#1c3a6e", "#d4a574", "#8b0000"],
        "voice": "nls_voice=zhiqiang (男声, 深沉自尊)",
    },

    "chaogai": {
        "name_cn": "晁盖",
        "name_en": "Chao Gai",
        "episode": "EP06 · 晁盖智取生辰纲",
        "age": 40,
        "height": "180cm",
        "build": "sturdy, dignified, village chief bearing",
        "face": "broad forehead, thick eyebrows, long black beard (three-strand), "
               "dignified expression, calculating eyes, authoritative presence",
        "hair": "long black hair with grey streaks at temples, tied in "
                "village elder style with cloth headband",
        "costume": "rich village chief attire: dark purple silk robe with "
                   "embroidery, black headband with jade ornament, leather boots. "
                   "Later: disguised as date merchant in plain brown clothes "
                   "with straw hat for ambush.",
        "weapon": "朴刀 (long saber) — leader commands rather than fights",
        "personality": "generous to followers, strategic mind, natural leader, "
                       "wealthy village chief turned outlaw mastermind, "
                       "carries authority effortlessly",
        "key_scenes": [
            "gathering seven heroes under candlelight to plan heist",
            "disguised as date merchant, pushing cart on Yellow Mud Ridge road",
            "giving command signal, seven men ambush the convoy with drugged wine",
        ],
        "cn_appearance": (
            "年及四旬，身躯凛凛，胸脯横阔。面如银盘，眼似铜铃，"
            "两鬓微霜，三绺长髯飘洒胸前。本为东溪村保正，"
            "平日仗义疏财，专爱结识天下好汉。身着紫缎绣袍，"
            "头戴万字巾，腰系蛮狮带，一副员外气派。智取生辰纲时"
            "改扮贩枣客商，布衣草帽，推独轮车，却掩不住领袖气度。"
        ),
        "en_prompt": (
            "a dignified Chinese village chief turned outlaw mastermind, 40 years old, "
            "broad forehead, thick eyebrows, long three-strand black-grey beard, "
            "calculating intelligent eyes, wearing dark purple silk robe with "
            "embroidery and jade ornament headband, later disguised as date merchant "
            "in plain brown clothes and straw hat pushing wooden cart, "
            "standing on dusty Yellow Mud Ridge mountain road under summer sun, "
            "cinematic wide shot, photorealistic, Chinese water margin epic style"
        ),
        "color_palette": ["#4a0080", "#8b7355", "#d4a574", "#1a3a1a"],
        "voice": "nls_voice=zhiming (男声, 稳重威严)",
    },
}


def generate_fal_prompts(character_key):
    """为指定角色生成 fal.ai Seedance 视频 prompt"""
    char = CHARACTERS.get(character_key)
    if not char:
        return None

    scene_prompts = []
    for i, scene in enumerate(char["key_scenes"]):
        scene_prompts.append({
            "shot": f"shot_{i+1:02d}",
            "description": scene,
            "prompt": (
                f"{char['en_prompt']}, specific scene: {scene}, "
                f"Chinese ancient style, Song dynasty aesthetic, "
                f"dynamic camera movement, 5 seconds, 24fps, "
                f"consistent character design, same person throughout"
            ),
            "negative_prompt": (
                "modern elements, cars, phones, western clothing, "
                "cartoon, anime, 3D render, blurry, low quality, "
                "different face, inconsistent appearance, extra limbs, "
                "deformed hands, text, watermark"
            ),
        })

    return {
        "character": char["name_cn"],
        "episode": char["episode"],
        "voice": char["voice"],
        "height": char["height"],
        "personality": char["personality"],
        "color_palette": char["color_palette"],
        "scenes": scene_prompts,
        "seedance_base_prompt": char["en_prompt"],
    }


def generate_visual_bible(output_path=None):
    """生成完整视觉圣经 JSON"""
    bible = {"version": "1.0", "project": "水浒传 AI 数字短剧", "total_characters": 6,
             "generated_for": "fal.ai Seedance / Stable Diffusion / Wan 2.5",
             "style_guidelines": {
                 "era": "北宋徽宗年间 (1100-1126 AD)",
                 "visual_style": "cinematic realism, muted earth tones, dramatic lighting, "
                                 "Zhang Yimou film aesthetic mixed with classical Chinese painting",
                 "aspect_ratio": "16:9 horizontal",
                 "resolution": "1920x1080 or higher",
                 "consistency_rules": [
                     "每个角色在全部镜头中外观一致",
                     "同一角色的服装/发型/面部特征不得改变",
                     "背景符合宋风 — 无现代化元素",
                     "光线自然，避免过度HDR",
                 ],
             },
             "characters": {}}

    for key, char in CHARACTERS.items():
        prompts = generate_fal_prompts(key)
        bible["characters"][key] = prompts

    if output_path:
        with open(output_path, "w") as f:
            json.dump(bible, f, ensure_ascii=False, indent=2)

    return bible


def main():
    import sys
    bible = generate_visual_bible()
    output_path = Path.home() / ".agentic-os" / "character_designs" / "visual_bible.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_visual_bible(str(output_path))

    if "--test" in sys.argv:
        print(f"✅ 视觉圣经: {len(bible['characters'])} 角色")
        for key, char in bible["characters"].items():
            nc = char["character"]
            ep = char["episode"]
            scenes = len(char["scenes"])
            print(f"  {nc:6s} {ep:30s} {scenes}个分镜 | {char['voice']}")
        print(f"\n📄 已保存: {output_path}")
        return

    print(f"📄 视觉圣经: {output_path}")
    print(f"   {len(bible['characters'])} 角色 × 各3分镜 = {sum(len(c['scenes']) for c in bible['characters'].values())} 个 fal.ai prompt")


if __name__ == "__main__":
    main()
