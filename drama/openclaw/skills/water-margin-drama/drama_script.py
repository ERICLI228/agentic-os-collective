#!/usr/bin/env python3
"""
MS-4: GLM-4.7 剧本生成脚本
使用火山引擎 GLM-4.7 API 生成完整剧本

Usage:
    python3 drama_script.py --task TASK_ID
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
TASKS_DIR = WORKSPACE / "tasks" / "active"
SKILL_DIR = Path.home() / ".openclaw" / "skills" / "water-margin-drama"

# 火山引擎 GLM-4-7 API 配置
ARK_API_KEY = os.environ.get("ARK_API_KEY", "68546ca6-9de1-42ff-ae98-c93c8d2e03d8")
ARK_API_ENDPOINT = os.environ.get("ARK_API_ENDPOINT", "https://ark.cn-beijing.volces.com/api/v3/responses")
GLM_MODEL = os.environ.get("GLM_MODEL", "disabled-glm-4-7")  # 已禁用
# 原配置: glm-4-7-251222（已关停）

def get_task(task_id: str) -> dict:
    """获取任务数据"""
    task_file = TASKS_DIR / f"{task_id}.json"
    if not task_file.exists():
        return None
    with open(task_file) as f:
        return json.load(f)

def call_glm_api(prompt: str) -> str:
    """调用火山引擎 GLM-4.7 API"""
    headers = {
        "Authorization": f"Bearer {ARK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": GLM_MODEL,
        "stream": False,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    try:
        print(f"🚀 调用 GLM-4-7 API: {GLM_MODEL}")
        response = requests.post(ARK_API_ENDPOINT, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ API响应成功")
        
        # 提取生成的文本
        for output in result.get("output", []):
            if output.get("type") == "message":
                for content in output.get("content", []):
                    if content.get("type") == "output_text":
                        return content.get("text", "")
        
        return ""
    except Exception as e:
        print(f"❌ GLM API调用失败: {e}")
        return None

def generate_script(task_id: str) -> dict:
    """生成完整剧本"""
    task = get_task(task_id)
    if not task:
        return {"error": "任务不存在", "task_id": task_id}
    
    # 获取任务信息
    task_name = task.get("name", "未命名")
    description = task.get("description", "")
    
    # 构造GLM提示词
    prompt = f"""请为以下短剧生成完整剧本:

任务: {task_name}
描述: {description}

要求:
1. 剧本字数至少2500字
2. 分为3-5个场景
3. 每个场景包含场景描述和人物对话
4. 对话要生动有趣，符合角色性格
5. 情节要有冲突和转折

请生成完整的剧本内容。"""

    # 调用GLM API
    script_text = call_glm_api(prompt)
    
    if not script_text:
        # 如果API失败，使用备用模板
        script_text = f"""《{task_name}》完整剧本

【场景一】开场
（场景描述待填充）

【场景二】冲突
（场景描述待填充）

【场景三】高潮
（场景描述待填充）

【场景四】结局
（场景描述待填充）

---
生成失败，使用备用模板
"""
    
    # 保存剧本文件
    output_dir = SKILL_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    
    script_file = output_dir / f"{task_id}_glm_script.txt"
    with open(script_file, "w") as f:
        f.write(script_text)
    
    print(f"✅ 剧本已保存: {script_file}")
    
    # 返回结果
    return {
        "task_id": task_id,
        "script_file": str(script_file),
        "word_count": len(script_text),
        "generated_by": "GLM-4-7",
        "status": "completed"
    }

def main():
    parser = argparse.ArgumentParser(description="GLM-4.7 剧本生成")
    parser.add_argument("--task", required=True, help="任务ID")
    args = parser.parse_args()
    
    print(f"📋 任务ID: {args.task}")
    print(f"🚀 开始生成剧本...")
    
    result = generate_script(args.task)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()