#!/usr/bin/env python3
"""Replace Chinese character names in video_prompts with English pinyin references."""
import json, re, os

VB = os.path.expanduser("~/.agentic-os/character_designs/visual_bible.json")

# Map of Chinese name → English pinyin reference
CN_TO_EN = {
    "宋江": "Song Jiang", "卢俊义": "Lu Junyi", "吴用": "Wu Yong",
    "公孙胜": "Gongsun Sheng", "关胜": "Guan Sheng", "林冲": "Lin Chong",
    "秦明": "Qin Ming", "呼延灼": "Huyan Zhuo", "花荣": "Hua Rong",
    "柴进": "Chai Jin", "李应": "Li Ying", "朱仝": "Zhu Tong",
    "鲁智深": "Lu Zhishen", "武松": "Wu Song", "董平": "Dong Ping",
    "张清": "Zhang Qing", "杨志": "Yang Zhi", "徐宁": "Xu Ning",
    "索超": "Suo Chao", "戴宗": "Dai Zong", "刘唐": "Liu Tang",
    "史进": "Shi Jin", "穆弘": "Mu Hong", "雷横": "Lei Heng",
    "李逵": "Li Kui", "李俊": "Li Jun", "阮小二": "Ruan Xiaoer",
    "张横": "Zhang Heng", "阮小五": "Ruan Xiaowu", "张顺": "Zhang Shun",
    "阮小七": "Ruan Xiaoqi", "杨雄": "Yang Xiong", "石秀": "Shi Xiu",
    "解珍": "Xie Zhen", "解宝": "Xie Bao", "燕青": "Yan Qing",
    "朱武": "Zhu Wu", "黄信": "Huang Xin", "孙立": "Sun Li",
    "宣赞": "Xuan Zan", "郝思文": "Hao Siwen", "韩滔": "Han Tao",
    "彭玘": "Peng Qi", "单廷珪": "Shan Tinggui", "魏定国": "Wei Dingguo",
    "萧让": "Xiao Rang", "裴宣": "Pei Xuan", "欧鹏": "Ou Peng",
    "邓飞": "Deng Fei", "燕顺": "Yan Shun", "杨林": "Yang Lin",
    "凌振": "Ling Zhen", "蒋敬": "Jiang Jing", "吕方": "Lu Fang",
    "郭盛": "Guo Sheng", "安道全": "An Daoquan", "皇甫端": "Huangfu Duan",
    "王英": "Wang Ying", "扈三娘": "Hu Sanniang", "鲍旭": "Bao Xu",
    "樊瑞": "Fan Rui", "孔明": "Kong Ming", "孔亮": "Kong Liang",
    "项充": "Xiang Chong", "李衮": "Li Gun", "金大坚": "Jin Dajian",
    "马麟": "Ma Lin", "童威": "Tong Wei", "童猛": "Tong Meng",
    "孟康": "Meng Kang", "侯健": "Hou Jian", "陈达": "Chen Da",
    "杨春": "Yang Chun", "郑天寿": "Zheng Tianshou", "陶宗旺": "Tao Zongwang",
    "宋清": "Song Qing", "乐和": "Yue He", "龚旺": "Gong Wang",
    "丁得孙": "Ding Desun", "穆春": "Mu Chun", "曹正": "Cao Zheng",
    "宋万": "Song Wan", "杜迁": "Du Qian", "薛永": "Xue Yong",
    "施恩": "Shi En", "李忠": "Li Zhong", "周通": "Zhou Tong",
    "汤隆": "Tang Long", "杜兴": "Du Xing", "邹渊": "Zou Yuan",
    "邹润": "Zou Run", "朱贵": "Zhu Gui", "朱富": "Zhu Fu",
    "蔡福": "Cai Fu", "蔡庆": "Cai Qing", "李立": "Li Li",
    "李云": "Li Yun", "焦挺": "Jiao Ting", "石勇": "Shi Yong",
    "孙新": "Sun Xin", "顾大嫂": "Gu Dasao", "张青": "Zhang Qing",
    "孙二娘": "Sun Erniang", "王定六": "Wang Dingliu", "郁保四": "Yu Baosi",
    "白胜": "Bai Sheng", "时迁": "Shi Qian", "段景住": "Duan Jingzhu",
    "晁盖": "Chao Gai"
}

with open(VB) as f:
    d = json.load(f)

count = 0
for cid, char in d['characters'].items():
    name = char.get('name', '')
    en_name = CN_TO_EN.get(name, name)
    vp = char.get('video_prompts', {})
    
    for sk in ['方案一', '方案二', '方案三']:
        sv = vp.get(sk, {})
        if not isinstance(sv, dict):
            continue
        for field in ['prompt', '简练版']:
            txt = sv.get(field, '')
            if not txt:
                continue
            # Replace all occurrences of Chinese name in prompt
            new_txt = txt.replace(name, en_name)
            # Also clean any leftover "from the 1998" with redundant prefix
            new_txt = new_txt.replace(f"{en_name} from the 1998 from the 1998", f"{en_name} from the 1998")
            new_txt = new_txt.replace(f"{en_name} from the 1998, from the 1998", f"{en_name} from the 1998")
            if new_txt != txt:
                sv[field] = new_txt
                count += 1

with open(VB, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print(f"Fixed {count} prompt/video_prompt texts across all characters")

# Final validation
with open(VB) as f:
    d2 = json.load(f)

remaining = 0
for cid, char in d2['characters'].items():
    pe = char.get('prompt_en', '')
    # prompt_en still has Chinese in "played by 李雪健" — that's fine
    vp = char.get('video_prompts', {})
    for sk in ['方案一', '方案二', '方案三']:
        sv = vp.get(sk, {})
        if isinstance(sv, dict):
            txt = sv.get('prompt', '')
            cn = [ch for ch in txt if '\u4e00' <= ch <= '\u9fff']
            if cn:
                remaining += 1
                if remaining <= 3:
                    print(f"  REMAINING CHINESE in {cid} {sk}: {cn}")

print(f"Chars with Chinese remaining in video_prompts: {remaining}")
