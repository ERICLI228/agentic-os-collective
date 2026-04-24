import sys
from pathlib import Path
#!/usr/bin/env python3
"""
水浒传AI数字短剧 - 剧本筛选与精华提取系统
基于行业最佳实践：观众熟悉度、戏剧冲突、人物高光、视觉表现力
# ⚠️ 完成度: 25% - MOCK 未实测（有框架但依赖 mock 数据，未跑通真实流程）
"""

import os
import sys
import json
import urllib.request
import urllib.parse

# 配置
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.config import config
ARK_API_KEY = config.ARK_API_KEY
GLM_MODEL = "glm-4-7-251222"
API_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

# 水浒传精华章节标准
SELECTION_CRITERIA = {
    "观众熟悉度": "民间流传度最高的桥段",
    "戏剧冲突强度": "情节起伏大、情感张力强",
    "人物高光时刻": "核心角色的成名战或转折点",
    "视觉表现力": "适合AI视频生成的场景（打斗、山水、市井）"
}

# 120回袁无涯本精华章节候选
CHAPTERS = [
    {"chapter": 3, "title": "鲁提辖拳打镇关西", "character": "鲁智深", "tags": ["高光", "动作", "正义"]},
    {"chapter": 4, "title": "鲁智深倒拔垂杨柳", "character": "鲁智深", "tags": ["高光", "力量", "视觉强"]},
    {"chapter": 7, "title": "花和尚倒拔垂杨柳", "character": "鲁智深", "tags": ["经典", "力量"]},
    {"chapter": 23, "title": "武松打虎", "character": "武松", "tags": ["高光", "动作", "经典", "视觉强"]},
    {"chapter": 27, "title": "武松斗杀西门庆", "character": "武松", "tags": ["复仇", "动作"]},
    {"chapter": 29, "title": "武松醉打蒋门神", "character": "武松", "tags": ["动作", "侠义"]},
    {"chapter": 31, "title": "血溅鸳鸯楼", "character": "武松", "tags": ["复仇", "冲突强", "需改编"]},
    {"chapter": 10, "title": "林冲风雪山神庙", "character": "林冲", "tags": ["转折", "悲情", "视觉强"]},
    {"chapter": 11, "title": "林冲雪夜上梁山", "character": "林冲", "tags": ["转折", "经典"]},
    {"chapter": 16, "title": "智取生辰纲", "character": "吴用", "tags": ["智慧", "谋略", "经典"]},
    {"chapter": 43, "title": "李逵沂岭杀四虎", "character": "李逵", "tags": ["高光", "动作", "需改编"]},
    {"chapter": 22, "title": "宋江杀阎婆惜", "character": "宋江", "tags": ["转折", "争议", "需改编"]},
]

def call_glm(prompt: str) -> str:
    """调用 GLM-4.7 API (直连，无代理)"""
    data = {
        "model": GLM_MODEL,
        "messages": [
            {"role": "system", "content": "你是一位资深编剧，熟悉水浒传原著和现代观众审美。请基于以下标准进行剧本筛选和改编。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        req = urllib.request.Request(
            API_ENDPOINT,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {ARK_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        resp = urllib.request.urlopen(req, timeout=60)
        body = json.loads(resp.read().decode('utf-8'))
        return body.get('choices', [{}])[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f"GLM API 调用失败: {e}")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None

def select_best_chapters(top_n: int = 10) -> list:
    """
    剧本筛选：基于四大标准选出最适合AI短剧的章节
    """
    print("📊 剧本筛选：分析水浒传精华章节...")
    print("=" * 50)
    
    # 计算每个章节的得分
    scored_chapters = []
    for ch in CHAPTERS:
        score = 0
        # 观众熟悉度 (tags中含"经典"加分)
        if "经典" in ch["tags"]:
            score += 25
        # 戏剧冲突强度
        if "冲突强" in ch["tags"] or "复仇" in ch["tags"]:
            score += 25
        # 人物高光时刻
        if "高光" in ch["tags"]:
            score += 25
        # 视觉表现力
        if "视觉强" in ch["tags"] or "动作" in ch["tags"]:
            score += 25
        
        # 需改编标记
        if "需改编" in ch["tags"]:
            ch["needs_rewrite"] = True
        else:
            ch["needs_rewrite"] = False
        
        ch["score"] = score
        scored_chapters.append(ch)
    
    # 排序
    scored_chapters.sort(key=lambda x: x["score"], reverse=True)
    
    # 输出TOP N
    print(f"\n🏆 TOP {top_n} 精华章节：")
    print("-" * 50)
    for i, ch in enumerate(scored_chapters[:top_n], 1):
        status = "⚠️需改编" if ch["needs_rewrite"] else "✅可用"
        print(f"{i}. 第{ch['chapter']}回 {ch['title']} [{ch['character']}] 评分:{ch['score']} {status}")
    
    return scored_chapters[:top_n]

def generate_episode_list() -> dict:
    """
    生成完整的剧集列表：包含剧本建议和改编提示
    """
    best_chapters = select_best_chapters(10)
    
    episode_list = {
        "version": "v1.0",
        "source": "120回袁无涯本",
        "selection_criteria": SELECTION_CRITERIA,
        "episodes": []
    }
    
    for i, ch in enumerate(best_chapters, 1):
        episode = {
            "episode_number": i,
            "source_chapter": ch["chapter"],
            "title": ch["title"],
            "main_character": ch["character"],
            "score": ch["score"],
            "needs_rewrite": ch["needs_rewrite"],
            "status": "pending" if ch["needs_rewrite"] else "ready"
        }
        episode_list["episodes"].append(episode)
    
    return episode_list

def save_episode_list(output_path: str = None):
    """保存剧集列表到JSON文件"""
    if output_path is None:
        output_path = os.path.expanduser("~/.openclaw/skills/water-margin-drama/episode_list.json")
    
    episode_list = generate_episode_list()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(episode_list, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 剧集列表已保存: {output_path}")
    return output_path

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n📖 用法:")
        print("  python script_selector.py --select      # 精华章节筛选")
        print("  python script_selector.py --list        # 生成剧集列表JSON")
        print("  python script_selector.py --analyze     # 深度分析(调用GLM)")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "--select":
        select_best_chapters()
    elif action == "--list":
        save_episode_list()
    elif action == "--analyze":
        # 调用GLM进行深度分析
        prompt = """请分析水浒传原著，基于以下标准提取最适合制作AI短剧的20个章节：
1. 观众熟悉度：民间流传度最高的桥段
2. 戏剧冲突强度：情节起伏大、情感张力强
3. 人物高光时刻：核心角色的成名战或转折点
4. 视觉表现力：适合AI视频生成的场景（打斗、山水、市井）

请按优先级排序，并标注每个章节是否需要改编（涉及争议剧情）。
输出格式：JSON列表，包含章节号、标题、主角、评分、是否需改编。"""
        
        print("🤖 调用GLM-4.7进行深度分析...")
        result = call_glm(prompt)
        if result:
            print(result)

if __name__ == "__main__":
    main()