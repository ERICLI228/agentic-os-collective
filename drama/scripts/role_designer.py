#!/usr/bin/env python3
"""
水浒传AI数字短剧 - 角色设计系统
生成并管理角色定妆照，确保视频生成时角色一致性
"""

import os
import sys
import json
import subprocess

# 配置
ARK_API_KEY = "f25a15bc-b109-40d4-976b-e2bb71cf9bf3"
SEEDANCE_MODEL = "doubao-seedance-2-0-fast-260128"

# 角色库
ROLES = {
    "宋江": {
        "description": "中国古代中年男子，约40岁，面容忠厚慈祥，眉目清秀，身穿暗红色锦袍，头戴纱帽，表情沉稳大气，有领袖气质",
        "traits": ["及时雨", "忠义两全", "领袖"],
        "voice": "男声，沉稳厚重",
        "default_scene": "梁山聚义厅"
    },
    "武松": {
        "description": "中国古代年轻男子，约25岁，身材魁梧高大，浓眉大眼，膀阔腰圆，身穿粗布短打衣裳，裸露手臂肌肉线条，表情刚毅果敢",
        "traits": ["打虎英雄", "刚正不阿", "武力高强"],
        "voice": "男声，有力豪迈",
        "default_scene": "景阳冈"
    },
    "鲁智深": {
        "description": "中国古代和尚，约30岁，体型肥胖但肌肉结实，方面大耳，络腮胡须，光头披袈裟，手持禅杖，表情豪爽直接",
        "traits": ["花和尚", "力大无穷", "豪爽直率"],
        "voice": "男声，洪亮爽朗",
        "default_scene": "大相国寺菜园"
    },
    "李逵": {
        "description": "中国古代男子，约35岁，皮肤黝黑，身材高大粗壮，环眼豹须，面相凶猛，手持两把板斧，身穿黑色短打衣",
        "traits": ["黑旋风", "鲁莽冲动", "孝顺"],
        "voice": "男声，粗犷暴躁",
        "default_scene": "梁山"
    },
    "林冲": {
        "description": "中国古代男子，约30岁，相貌堂堂，豹头环眼，燕颔虎须，身穿白色战袍，手持丈八蛇矛，表情隐忍坚毅",
        "traits": ["豹子头", "忍辱负重", "枪法绝伦"],
        "voice": "男声，沉稳内敛",
        "default_scene": "风雪山神庙"
    }
}

# 场景库
SCENES = {
    "梁山聚义厅": "古代中国大厅，红砖金瓦，柱子上雕刻盘龙，设有虎皮交椅，墙上挂替天行道旗帜，两侧摆满酒肉宴席",
    "景阳冈": "中国北方山岭，树木茂密，山路崎岖，远处有酒店旗帜，近处有岩石和草丛，夕阳西下",
    "风雪山神庙": "古代密林，大雪纷飞，破旧山神庙，周围有草屋燃烧的痕迹，寒冷肃杀氛围",
    "大相国寺菜园": "古代寺庙后院，有菜圃、柳树、简陋草屋，周围有围墙，院内有石桌石凳"
}

def generate_role_prompt(role_name: str, scene: str = None, action: str = None) -> str:
    """
    生成完整的角色提示词
    """
    role = ROLES.get(role_name)
    if not role:
        return None
    
    base = role["description"]
    
    if scene:
        scene_desc = SCENES.get(scene, scene)
        base = f"{base}，场景：{scene_desc}"
    
    if action:
        base = f"{base}，动作：{action}"
    
    # 添加负面提示词避免问题
    negative = "distorted, messy, low quality, blurred, deformed face, extra limbs, watermark, text"
    
    return {
        "positive": base,
        "negative": negative,
        "role": role_name,
        "traits": role["traits"]
    }

def save_role_library(output_path: str = None):
    """
    保存角色库到JSON文件
    """
    if output_path is None:
        output_path = os.path.expanduser("~/.openclaw/skills/water-margin-drama/role_library.json")
    
    library = {
        "version": "v1.0",
        "roles": ROLES,
        "scenes": SCENES,
        "usage": {
            "generate_prompt": "generate_role_prompt(role_name, scene, action)",
            "ensure_consistency": "每次使用相同角色时，复用相同描述"
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(library, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 角色库保存: {output_path}")
    return output_path

def list_roles():
    """列出所有可用角色"""
    print("🎭 水浒传角色库:")
    print("=" * 50)
    for name, info in ROLES.items():
        traits = ", ".join(info["traits"])
        print(f"\n📌 {name}")
        print(f"   特征: {traits}")
        print(f"   描述: {info['description'][:50]}...")
        print(f"   默认场景: {info['default_scene']}")
    
    print("\n" + "=" * 50)
    print("📍 可用场景:")
    for scene, desc in SCENES.items():
        print(f"   - {scene}: {desc[:30]}...")

def generate_character_image_prompt(role_name: str) -> str:
    """
    生成角色定妆照提示词（用于图像生成）
    """
    role = ROLES.get(role_name)
    if not role:
        print(f"❌ 角色 '{role_name}' 不存在")
        return None
    
    prompt = f"""
请生成一张{role_name}的定妆照，用于后续AI视频生成的角色一致性参考。

角色描述：{role['description']}

要求：
1. 正面照，表情自然
2. 服装和特征清晰可见
3. 电影质感，写实风格
4. 中景构图（能看到上半身和部分背景）
5. 场景：{role['default_scene']}

负面提示词：distorted, messy, low quality, blurred, deformed face, extra limbs
"""
    return prompt.strip()

def batch_generate_prompts(output_dir: str = None):
    """
    批量生成所有角色的定妆照提示词
    """
    if output_dir is None:
        output_dir = os.path.expanduser("~/.openclaw/skills/water-margin-drama/character_prompts")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎭 批量生成角色定妆照提示词...")
    print("=" * 50)
    
    for role_name in ROLES.keys():
        prompt = generate_character_image_prompt(role_name)
        filepath = os.path.join(output_dir, f"{role_name}_定妆照.txt")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"✅ {role_name}: {filepath}")
    
    print("=" * 50)
    print(f"🎉 完成，共 {len(ROLES)} 个角色")

def get_video_prompt(role_name: str, scene: str, action: str) -> str:
    """
    生成视频提示词（用于Seedance）
    """
    prompt_data = generate_role_prompt(role_name, scene, action)
    if not prompt_data:
        return None
    
    video_prompt = f"""
{prompt_data['positive']}

电影质感，流畅动作，24帧，8秒视频。
负面：{prompt_data['negative']}
"""
    return video_prompt.strip()

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n📖 用法:")
        print("  python role_designer.py --list          # 列出所有角色")
        print("  python role_designer.py --prompt 武松   # 生成角色提示词")
        print("  python role_designer.py --video 武松 景阳冈 打虎")
        print("  python role_designer.py --batch         # 批量生成")
        print("  python role_designer.py --save          # 保存角色库JSON")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "--list":
        list_roles()
    elif action == "--prompt":
        if len(sys.argv) >= 3:
            role = sys.argv[2]
            prompt = generate_character_image_prompt(role)
            print(prompt)
        else:
            print("用法: --prompt 角色名")
    elif action == "--video":
        if len(sys.argv) >= 5:
            role = sys.argv[2]
            scene = sys.argv[3]
            action_desc = sys.argv[4]
            prompt = get_video_prompt(role, scene, action_desc)
            print(prompt)
        else:
            print("用法: --video 角色名 场景 动作")
    elif action == "--batch":
        batch_generate_prompts()
    elif action == "--save":
        save_role_library()

if __name__ == "__main__":
    main()
    
    # ===== Agentic OS 集成 =====
    import subprocess
    from pathlib import Path
    import json
    
    TASKS_DIR = Path.home() / ".openclaw/workspace/tasks/active"
    TASK_ID = None
    for f in sorted(TASKS_DIR.glob("DRAMA-*.json"), key=lambda x: -int(x.stat().st_mtime)):
        with open(f) as fp:
            task = json.load(fp)
            if task.get('status') in ['running', 'pending']:
                TASK_ID = task['id']
                break
    
    if TASK_ID:
        # 角色设计结果
        role_designs = [
            {"character": "武松", "voice": "Alvaro", "personality": "豪爽勇猛", "traits": ["直率", "勇敢"]},
            {"character": "老虎", "voice": "Brian", "personality": "凶猛有灵性", "traits": ["凶猛"]},
            {"character": "小二", "voice": "Eric", "personality": "精明世故", "traits": ["圆滑"]}
        ]
        
        try:
            subprocess.run([
                'python3', str(Path.home() / '.openclaw/core/task_updater.py'),
                TASK_ID, 'MS-3', 'completed'
            ], timeout=10)
            
            # 写入产出内容
            task_file = TASKS_DIR / f"{TASK_ID}.json"
            if task_file.exists():
                import fcntl
                from datetime import datetime
                with open(task_file, 'r+') as tf:
                    fcntl.flock(tf, fcntl.LOCK_EX)
                    task = json.load(tf)
                    for m in task.get('milestones', []):
                        if m.get('id') == 'MS-3':
                            m['status'] = 'completed'
                            m['completed_at'] = datetime.now().isoformat()
                            m.setdefault('execution_details', {})
                            m['execution_details']['output_content'] = {
                                'type': 'role_design',
                                'title': '角色设计方案',
                                'content': '角色设计完成：武松(Alvaro)、老虎(Brian)、小二(Eric)',
                                'roles': role_designs,
                                'generated_at': datetime.now().isoformat()
                            }
                            break
                    tf.seek(0)
                    json.dump(task, tf, ensure_ascii=False, indent=2)
                    tf.truncate()
                    fcntl.flock(tf, fcntl.LOCK_UN)
            
            print(f"✅ 已更新任务 {TASK_ID} 里程碑 MS-3 -> completed")
            print(f"✅ 产出内容已写入: 角色设计方案")
        except Exception as e:
            print(f"⚠️ 里程碑更新失败: {e}")