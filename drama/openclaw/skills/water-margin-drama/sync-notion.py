#!/usr/bin/python3
"""
水浒传AI数字短剧 - Notion同步脚本
将完整能力文档和索引同步到Notion
"""

import json
import urllib.request
import urllib.parse
import base64
import os
from datetime import datetime

NOTION_TOKEN = "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"
PAGE_ID = "3343318a3fa48056b6cfe8fff343d974"

def create_page(title: str, content: str):
    """创建Notion页面"""
    url = "https://api.notion.com/v1/pages"
    
    # 构建blocks - 支持更丰富的格式
    blocks = []
    for line in content.split('\n'):
        line = line.rstrip()
        if not line.strip():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            })
        elif line.startswith('# '):
            # Heading 1
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        elif line.startswith('## '):
            # Heading 2
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
        elif line.startswith('### '):
            # Heading 3
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })
        elif line.startswith('- '):
            # Bulleted list
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        elif '|' in line and line.startswith('|'):
            # 表格行 - 跳过，在代码块中显示
            continue
        else:
            # Paragraph
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                }
            })
    
    # 限制blocks数量
    if len(blocks) > 90:
        # 简化处理
        blocks = blocks[:90]
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "... (更多内容见本地备份)"}}]
            }
        })
    
    data = {
        "parent": {"page_id": PAGE_ID},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title}}]
            }
        },
        "children": blocks
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        },
        method="POST"
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        print(f"✅ 创建页面: {title}")
        return result
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def read_file(filepath: str) -> str:
    """读取文件内容"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def generate_index_content(base_dir: str) -> str:
    """生成完整的文件索引"""
    
    files_info = [
        ("SKILL.md", "主文档 - 完整能力说明"),
        ("STATUS_REPORT.md", "状态报告 - 基础设施总览"),
        ("drama_audio.py", "音视频合成 - TTS+BGM+FFmpeg"),
        ("script_selector.py", "剧本筛选 - 精华章节自动筛选"),
        ("controversy_rewriter.py", "争议改写 - 广电合规改写"),
        ("role_designer.py", "角色设计 - 角色库管理"),
        ("auto_publisher.py", "发布运营 - 自动发布+数据回流"),
        ("seedance.py", "视频生成 - Seedance 2.0集成"),
        ("role_library.json", "角色库数据 - 5个核心角色"),
        ("episode_list.json", "剧集列表 - TOP10精华章节"),
        ("role-prompts.md", "角色提示词"),
        ("compliance-check.md", "合规检查清单"),
    ]
    
    content = f"""# 水浒传AI数字短剧 - 完整索引

## 备份时间
{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 文件清单

### 核心脚本
"""
    for filename, desc in files_info:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            content += f"- ✅ {filename} ({size} bytes) - {desc}\n"
        else:
            content += f"- ❌ {filename} - {desc}\n"
    
    content += """
## 快速使用

```bash
# 生成剧集
帮我制作一集"武松打虎"AI短剧

# 查看角色库
python3 role_designer.py --list

# 剧本筛选
python3 script_selector.py --list

# 音视频合成
python3 drama_audio.py --full video_url "配音文字"
```
"""
    return content

def main():
    # 读取备份文档
    base_dir = os.path.expanduser("~/.openclaw/skills/water-margin-drama")
    
    print("📤 开始同步到Notion...")
    print(f"目标页面: https://notion.so/MagicPockets-{PAGE_ID}")
    print("=" * 50)
    
    # 1. 同步完整索引
    print("\n1️⃣ 创建完整索引...")
    index_content = generate_index_content(base_dir)
    create_page("[索引] 水浒传AI短剧完整能力", index_content)
    
    # 2. 同步主文档
    print("\n2️⃣ 同步主文档...")
    skill_content = read_file(os.path.join(base_dir, "SKILL.md"))
    if skill_content:
        create_page("[能力] 水浒传AI短剧制作系统", skill_content)
    
    # 3. 同步状态报告
    print("\n3️⃣ 同步状态报告...")
    status_content = read_file(os.path.join(base_dir, "STATUS_REPORT.md"))
    if status_content:
        create_page("[报告] 基础设施状态报告", status_content)
    
    # 4. 同步剧集列表
    print("\n4️⃣ 同步剧集列表...")
    episode_content = read_file(os.path.join(base_dir, "episode_list.json"))
    if episode_content:
        # 转换为可读格式
        try:
            ep_data = json.loads(episode_content)
            formatted = json.dumps(ep_data, ensure_ascii=False, indent=2)
            create_page("[数据] 精华剧集列表", formatted)
        except:
            pass
    
    print("=" * 50)
    print("🎉 同步完成!")
    print(f"\n📍 查看Notion: https://notion.so/MagicPockets-{PAGE_ID}")

if __name__ == "__main__":
    main()