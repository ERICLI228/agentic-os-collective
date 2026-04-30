#!/usr/bin/env python3
"""
将 visual_bible.json 中 8 个角色升级为完整角色档案格式
保留原有 scenes/prompts 等渲染数据，新增 personality/appearance/background/voice 深度字段
"""
import json
from pathlib import Path

BIBLE_PATH = Path.home() / ".agentic-os" / "character_designs" / "visual_bible.json"

with open(BIBLE_PATH) as f:
    bible = json.load(f)

UPGRADES = {
    "wusong": {
        "id": "wusong",
        "name": "武松",
        "title": "行者·打虎英雄",
        "basic_info": {
            "height": "188cm",
            "build": "魁梧健壮，虎背熊腰",
            "face": "方颚浓眉，豹头环眼，燕颔虎须",
            "age": "二十八岁"
        },
        "personality": {
            "core_traits": ["勇猛刚直", "嫉恶如仇", "重情重义", "嗜酒豪爽"],
            "emotional_range": "外刚内柔，对兄弟情深义重，对仇人冷酷无情",
            "speech_style": "粗犷豪迈，声音洪亮，喜用江湖切口",
            "catchphrases": [
                "俺武松行不更名，坐不改姓！",
                "酒来！今日定要喝个痛快！",
                "你这厮，吃俺一拳！"
            ],
            "habits": [
                "每日必饮酒，无酒不欢",
                "走路虎虎生风，自带威压",
                "说话时习惯拍案而起"
            ]
        },
        "appearance": {
            "costume": "暗蓝战袍，红色腰带，皮质护臂，行者装扮",
            "accessories": ["哨棒", "酒葫芦", "戒刀"],
            "color_palette": {
                "primary": "#1a1a2e",
                "secondary": "#8b0000",
                "accent": "#d4a574"
            },
            "design_notes": "宋代行者装扮，服饰便于打斗，战袍下摆有磨损痕迹"
        },
        "background": {
            "origin": "清河县人士",
            "key_events": ["景阳冈打虎", "醉打蒋门神", "血溅鸳鸯楼"],
            "relationships": {
                "武大郎": "兄，被潘金莲毒杀",
                "宋江": "结义兄弟，敬重其为人",
                "鲁智深": "意气相投，并肩作战"
            }
        },
        "voice": {
            "nls_speaker": "zhiming",
            "description": "浑厚有力，中气十足",
            "sample_text": "俺乃打虎武松！谁敢与我一战！"
        }
    },
    "luzhishen": {
        "id": "luzhishen",
        "name": "鲁智深",
        "title": "花和尚·倒拔垂杨柳",
        "basic_info": {
            "height": "195cm",
            "build": "巨汉，熊腰虎背，肌肉虬结",
            "face": "圆面大耳，络腮胡，额上九个香疤",
            "age": "三十五岁"
        },
        "personality": {
            "core_traits": ["豪爽直率", "嫉恶如仇", "粗中有细", "扶弱抑强"],
            "emotional_range": "外表粗犷豪放，内心慈悲为怀，路见不平必拔刀相助",
            "speech_style": "声如洪钟，说话直来直去，不喜拐弯抹角",
            "catchphrases": [
                "洒家姓鲁，名智深，绰号花和尚！",
                "呔！你这鸟人，吃洒家一拳！",
                "酒肉穿肠过，佛祖心中留！"
            ],
            "habits": [
                "大口吃肉大碗喝酒，僧人戒律一概不理",
                "遇到不平事，先动手后动脑",
                "高兴时仰天大笑，声震屋瓦"
            ]
        },
        "appearance": {
            "costume": "灰褐色僧袍半敞，露出胸膛，脖挂一百单八颗念珠",
            "accessories": ["六十二斤水磨禅杖", "戒刀", "念珠"],
            "color_palette": {
                "primary": "#4a3728",
                "secondary": "#8b7355",
                "accent": "#c4a35a"
            },
            "design_notes": "武僧造型，僧袍半敞露出结实胸膛，念珠粗大，肌肉线条分明"
        },
        "background": {
            "origin": "关西人氏，原为经略府提辖",
            "key_events": ["拳打镇关西", "大闹五台山", "倒拔垂杨柳"],
            "relationships": {
                "林冲": "结义兄弟，野猪林救其性命",
                "武松": "意气相投的江湖好汉",
                "宋江": "梁山聚义后归附"
            }
        },
        "voice": {
            "nls_speaker": "zhiming",
            "description": "粗犷豪迈，声如洪钟",
            "sample_text": "洒家三拳打死镇关西，你待怎的！"
        }
    },
    "linchong": {
        "id": "linchong",
        "name": "林冲",
        "title": "豹子头·八十万禁军教头",
        "basic_info": {
            "height": "182cm",
            "build": "精干匀称，武者体型",
            "face": "儒雅面庞，薄髭，眼中含悲愤",
            "age": "三十二岁"
        },
        "personality": {
            "core_traits": ["隐忍克制", "武艺超群", "忠厚老实", "被逼至绝处方爆发"],
            "emotional_range": "长期忍辱负重，内心悲愤压抑，爆发时如雷霆万钧",
            "speech_style": "言辞克制有礼，但字字含恨，悲壮沉郁",
            "catchphrases": [
                "林冲一生清白，奈何奸臣当道！",
                "八十万禁军教头，竟落得如此下场！",
                "今日林冲便要讨个公道！"
            ],
            "habits": [
                "独处时习惯性抚摸丈八蛇矛",
                "眉头常锁，若有所思",
                "饮酒时沉默不语，一饮而尽"
            ]
        },
        "appearance": {
            "costume": "破旧红色披风配战甲，毛皮领口，手腕有枷锁印记",
            "accessories": ["丈八蛇矛", "斗笠"],
            "color_palette": {
                "primary": "#8b0000",
                "secondary": "#1c1c2a",
                "accent": "#ffffff"
            },
            "design_notes": "风雪中衣衫褴褛但身姿挺拔，披风破损，眼神中是不屈的意志"
        },
        "background": {
            "origin": "东京八十万禁军枪棒教头",
            "key_events": ["误入白虎堂", "风雪山神庙", "雪夜上梁山"],
            "relationships": {
                "高俅": "仇敌，设计陷害",
                "鲁智深": "结义兄弟，野猪林相救",
                "林娘子": "妻子，被高衙内逼死"
            }
        },
        "voice": {
            "nls_speaker": "zhilun",
            "description": "沉郁悲壮，隐忍中透出锋芒",
            "sample_text": "林冲一生忍辱，今日便要雪恨！"
        }
    },
    "songjiang": {
        "id": "songjiang",
        "name": "宋江",
        "title": "及时雨·呼保义",
        "basic_info": {
            "height": "175cm",
            "build": "矮小瘦弱，文官体型",
            "face": "面色黝黑，细眉沉目，神情温和中暗藏锋芒",
            "age": "四十岁"
        },
        "personality": {
            "core_traits": ["仗义疏财", "深谋远虑", "重视兄弟情义", "被逼时可下狠手"],
            "emotional_range": "表面温厚仁和，内心城府极深，被逼到绝境时会突然致命",
            "speech_style": "谦和有礼，措辞谨慎，说话时善于观察对方反应",
            "catchphrases": [
                "宋江不才，愿为各位哥哥效犬马之劳！",
                "替天行道，乃我梁山本分！",
                "兄弟们的情义，宋江铭记于心！"
            ],
            "habits": [
                "说话时习惯拱手作揖",
                "遇事先想后果，再定行动",
                "独处时常面露忧色"
            ]
        },
        "appearance": {
            "costume": "深绿色官服，黑色纱帽，腰系玉带",
            "accessories": ["短刀(暗藏)", "书信匣"],
            "color_palette": {
                "primary": "#1a3a1a",
                "secondary": "#2f1f0f",
                "accent": "#ffd700"
            },
            "design_notes": "文官打扮但气场不凡，面色黝黑是其标志，眼神从温和到凌厉的转变是关键"
        },
        "background": {
            "origin": "山东郓城县押司",
            "key_events": ["怒杀阎婆惜", "浔阳楼题反诗", "梁山聚义"],
            "relationships": {
                "晁盖": "恩人，劫生辰纲后上梁山",
                "李逵": "最忠心的兄弟",
                "阎婆惜": "妾，因发现梁山书信被杀"
            }
        },
        "voice": {
            "nls_speaker": "zhilun",
            "description": "沉稳内敛，温和中暗藏威严",
            "sample_text": "宋江一介小吏，蒙各位哥哥厚爱。"
        }
    },
    "likui": {
        "id": "likui",
        "name": "李逵",
        "title": "黑旋风·沂岭杀四虎",
        "basic_info": {
            "height": "190cm",
            "build": "黝黑粗壮，肌肉暴起",
            "face": "漆黑面皮，环眼暴突， wild messy hair",
            "age": "二十六岁"
        },
        "personality": {
            "core_traits": ["暴烈凶猛", "天真烂漫", "极度孝顺", "对宋江绝对忠诚"],
            "emotional_range": "情绪极端，高兴时手舞足蹈，愤怒时如疯虎，悲伤时嚎啕大哭",
            "speech_style": "嗓门极大，说话直白粗鲁，常大喊大叫",
            "catchphrases": [
                "铁牛在此！谁敢过来！",
                "哥哥说有，铁牛就去杀！",
                "娘啊！儿来迟了！"
            ],
            "habits": [
                "遇事第一反应是动手而不是动嘴",
                "见到哥哥宋江就咧嘴傻笑",
                "赤膊上阵，不爱穿铠甲"
            ]
        },
        "appearance": {
            "costume": "粗糙深褐色麻布衣，经常赤膊，手臂粗壮肌肉外露",
            "accessories": ["板斧(双)", "酒葫芦"],
            "color_palette": {
                "primary": "#0a0a0a",
                "secondary": "#8b0000",
                "accent": "#d4a574"
            },
            "design_notes": "黝黑皮肤是最大特征，衣服破烂不整，浑身充满野性力量"
        },
        "background": {
            "origin": "沂水县百丈村人",
            "key_events": ["沂岭杀四虎", "江州劫法场", "打死殷天锡"],
            "relationships": {
                "宋江": "最敬重的哥哥，绝对服从",
                "李母": "老母，被虎吃后怒杀四虎",
                "燕青": "常被其相扑摔翻，又敬又怕"
            }
        },
        "voice": {
            "nls_speaker": "zhiqiang",
            "description": "暴烈炽热，嗓门极大",
            "sample_text": "铁牛板斧在此！杀他娘的！"
        }
    },
    "wuyong": {
        "id": "wuyong",
        "name": "吴用",
        "title": "智多星·智取生辰纲",
        "basic_info": {
            "height": "176cm",
            "build": "清瘦文雅，书生体型",
            "face": "清瘦面庞，长须飘逸，目光睿智从容",
            "age": "三十八岁"
        },
        "personality": {
            "core_traits": ["足智多谋", "沉着冷静", "善用人心", "文雅中暗藏狡黠"],
            "emotional_range": "始终从容不迫，胜券在握时微微一笑，局势不利时反而更冷静",
            "speech_style": "语速平缓，措辞文雅，说话时习惯摇羽扇，每句话都暗藏机锋",
            "catchphrases": [
                "此事不难，吴某已有一计。",
                "兵不厌诈，且看我安排。",
                "天时地利人和，缺一不可。"
            ],
            "habits": [
                "思考时习惯轻摇羽扇",
                "下棋布局，以棋喻事",
                "笑时嘴角微扬，从不大笑"
            ]
        },
        "appearance": {
            "costume": "深青色丝绸学者袍，金色镶边，手持白色羽扇",
            "accessories": ["白色羽扇", "折扇", "地图卷轴"],
            "color_palette": {
                "primary": "#1a3a4a",
                "secondary": "#c0a060",
                "accent": "#f5f0e8"
            },
            "design_notes": "书生打扮但眼神锐利，羽扇是标志道具，伪装成枣商时穿粗麻衣戴斗笠"
        },
        "background": {
            "origin": "郓城县乡村教师",
            "key_events": ["智取生辰纲", "三打祝家庄", "梁山军师"],
            "relationships": {
                "晁盖": "挚友，共同策划生辰纲",
                "宋江": "辅佐其成为梁山之主",
                "公孙胜": "同门道友，联手施法"
            }
        },
        "voice": {
            "nls_speaker": "zhilun",
            "description": "睿智从容，语速平缓",
            "sample_text": "且看吴某如何智取这十万贯生辰纲。"
        }
    }
}

# 杨志（EP05 被李逵替代，但保留在档案中）和晁盖（EP06 被吴用替代）
UPGRADES["yangzhi"] = {
    "id": "yangzhi",
    "name": "杨志",
    "title": "青面兽·杨家将后裔",
    "basic_info": {
        "height": "185cm",
        "build": "高挑挺拔，军人体型",
        "face": "棱角分明，面颊青记，薄唇紧抿",
        "age": "三十岁"
    },
    "personality": {
        "core_traits": ["骄傲自尊", "刚毅不屈", "重视荣誉", "落魄但不失尊严"],
        "emotional_range": "表面冷峻，内心极度骄傲，落魄后压抑着不甘与愤懑",
        "speech_style": "言辞简洁有力，不爱多说，但每句话都掷地有声",
        "catchphrases": [
            "俺乃杨家将后人，岂能受你这泼皮辱没！",
            "祖传宝刀在此，不识货的滚开！",
            "杨志宁可饿死，不折尊严！"
        ],
        "habits": [
            "习惯性摩挲祖传宝刀刀柄",
            "站姿笔挺，军人习惯不改",
            "被激怒时咬牙忍住的微表情"
        ]
    },
    "appearance": {
        "costume": "补丁军装但整洁干净，蓝色军服",
        "accessories": ["祖传宝刀", "发间插草标(卖身标志)"],
        "color_palette": {
            "primary": "#2d5016",
            "secondary": "#1c3a6e",
            "accent": "#d4a574"
        },
        "design_notes": "落魄将官造型，军装有补丁但整洁，面颊青记和金色流配金印是标志"
    },
    "background": {
        "origin": "杨家将后裔，世代将门",
        "key_events": ["失陷花石纲", "汴京卖刀", "怒杀牛二"],
        "relationships": {
            "杨业": "先祖，杨家将创始人",
            "牛二": "街头泼皮，被杨志所杀",
            "梁中书": "赏识杨志，命其押送生辰纲"
        }
    },
    "voice": {
        "nls_speaker": "zhiqiang",
        "description": "深沉自尊，言辞铿锵",
        "sample_text": "杨家将后人杨志，岂是尔等能欺的！"
    }
}

UPGRADES["chaogai"] = {
    "id": "chaogai",
    "name": "晁盖",
    "title": "托塔天王·梁山之主",
    "basic_info": {
        "height": "180cm",
        "build": "宽厚壮实，领袖体型",
        "face": "宽额浓眉，三绺黑白胡须，目光精算",
        "age": "四十岁"
    },
    "personality": {
        "core_traits": ["仗义疏财", "善于谋略", "天生的领袖魅力", "从容不迫"],
        "emotional_range": "沉稳大气，对兄弟慷慨大方，面对危险时愈发冷静",
        "speech_style": "声音洪亮，措辞大气，说话时不怒自威",
        "catchphrases": [
            "晁某一生仗义，各位兄弟的事就是我的事！",
            "十万贯生辰纲，取之何妨！",
            "梁山聚义，替天行道！"
        ],
        "habits": [
            "说话时习惯性捋胡须",
            "做决定前目光扫视众人",
            "大笑时声如洪钟"
        ]
    },
    "appearance": {
        "costume": "深紫色丝绸锦袍配刺绣，玉饰发带；伪装时为粗布衣斗笠",
        "accessories": ["玉饰发带", "推车(伪装时)"],
        "color_palette": {
            "primary": "#4a0080",
            "secondary": "#8b7355",
            "accent": "#d4a574"
        },
        "design_notes": "富家财主打扮，贵气逼人；伪装枣商时判若两人，眼神仍是关键"
    },
    "background": {
        "origin": "山东郓城县东溪村保正（村长）",
        "key_events": ["智取生辰纲", "火并王伦", "梁山称王"],
        "relationships": {
            "吴用": "挚友，智囊搭档",
            "宋江": "后继者，晁盖死后宋江继位",
            "刘唐": "通风报信之恩人"
        }
    },
    "voice": {
        "nls_speaker": "zhiming",
        "description": "稳重威严，领袖气场",
        "sample_text": "晁盖在此！各位兄弟，干了这碗！"
    }
}

# 合并到 bible
for char_id, profile in UPGRADES.items():
    if char_id in bible["characters"]:
        ch = bible["characters"][char_id]
        # 保留原有的 scenes, seedance_base_prompt
        old_scenes = ch.get("scenes", [])
        old_seedance = ch.get("seedance_base_prompt", "")
        old_episode = ch.get("episode", "")
        # 合并
        ch.update(profile)
        ch["renders"] = profile.get("renders", [])
        # 保留原有渲染数据
        if old_scenes:
            ch["scenes"] = old_scenes
        if old_seedance:
            ch["seedance_base_prompt"] = old_seedance
        if old_episode:
            ch["episode"] = old_episode
        # 标记升级
        ch["_upgraded"] = "2026-04-30"

# 保存
with open(BIBLE_PATH, "w", encoding="utf-8") as f:
    json.dump(bible, f, ensure_ascii=False, indent=2)

print(f"✅ visual_bible.json upgraded: {len(UPGRADES)} characters")
# Verify
with open(BIBLE_PATH) as f:
    v = json.load(f)
for cid in UPGRADES:
    ch = v["characters"].get(cid, {})
    has = []
    for k in ["basic_info","personality","appearance","background","voice"]:
        if k in ch and ch[k]: has.append(k)
    print(f"  {cid}: {len(has)}/5 new fields ✅" if len(has)==5 else f"  {cid}: {has} ⚠️")
