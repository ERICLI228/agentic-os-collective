"""会话归档器 - 提取关键决策到知识库"""
import json, os, re
from datetime import datetime

WIKI_DIR = os.path.expanduser("~/agentic-os-collective/shared/knowledge/wiki")
OUTPUTS_DIR = os.path.join(WIKI_DIR, "outputs")
LOG_FILE = os.path.join(WIKI_DIR, "log.md")
SESSION_DIR = os.path.expanduser("~/.openclaw/agents/main/sessions")

def ensure_dirs():
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

def get_latest_session():
    sessions = [f for f in os.listdir(SESSION_DIR)
                if f.endswith('.jsonl') and not f.startswith('.')
                and 'trajectory' not in f and 'checkpoint' not in f
                and f != 'sessions.json']
    if not sessions:
        return None
    sessions.sort(key=lambda f: os.path.getmtime(os.path.join(SESSION_DIR, f)), reverse=True)
    latest = os.path.join(SESSION_DIR, sessions[0])
    try:
        decisions, topics = [], set()
        with open(latest, 'r') as f:
            for line in f:
                try:
                    msg = json.loads(line)
                    if msg.get('type') == 'message':
                        m = msg.get('message', {})
                        if m.get('role') == 'user':
                            texts = [c.get('text', '') for c in m.get('content', []) if c.get('type') == 'text']
                            for t in texts:
                                clean = re.sub(r'<[^>]+>', '', t).strip()[:200]
                                if clean and len(clean) > 10:
                                    topics.add(clean)
                        if m.get('role') == 'assistant' and m.get('stopReason'):
                            texts = [c.get('text', '') for c in m.get('content', []) if c.get('type') == 'text']
                            for t in texts:
                                for line in t.split('\n'):
                                    line = line.strip()
                                    if any(kw in line for kw in ['决定：', '决策：', '选择：', '切换', '改为', '设置', '创建', '部署', '使用']):
                                        if len(line) > 10:
                                            decisions.append(line[:200])
                except (json.JSONDecodeError, KeyError):
                    continue
        return {
            'file': sessions[0],
            'mtime': os.path.getmtime(latest),
            'topics': list(topics)[-8:],
            'decisions': decisions[-15:],
            'msg_count': sum(1 for _ in open(latest) if line_has_message(_))
        }
    except Exception as e:
        return {'error': str(e)}

def line_has_message(line):
    try:
        m = json.loads(line)
        return m.get('type') == 'message'
    except:
        return False

def archive(session):
    date = datetime.fromtimestamp(session.get('mtime'))
    slug = f"session-{date.strftime('%Y%m%d-%H%M%S')}.md"
    path = os.path.join(OUTPUTS_DIR, slug)
    topics = '\n'.join(f'- {t}' for t in session.get('topics', []))
    decisions = '\n'.join(f'- {d}' for d in session.get('decisions', []))
    content = f"""---
title: "会话归档 {date.strftime('%Y-%m-%d %H:%M')}"
date_created: {date.strftime('%Y-%m-%d')}
session_file: "{session['file']}"
message_count: {session['msg_count']}
type: output
status: final
tags: [session-archive]
---
# 会话: {date.strftime('%Y-%m-%d %H:%M')}
## 主题
{topics}
## 决策
{decisions}
"""
    with open(path, 'w') as f:
        f.write(content)
    return slug

def update_log(session, slug):
    date = datetime.fromtimestamp(session['mtime'])
    topics = '\n'.join(f'  - {t}' for t in session.get('topics', []))
    decisions = '\n'.join(f'  - {d}' for d in session.get('decisions', []))
    entry = f"""
## [{date.strftime('%Y-%m-%d %H:%M')}] session | {session['file']}
- 消息数: {session['msg_count']}
- 主题:
{topics}
- 决策:
{decisions}
- 归档: wiki/outputs/{slug}
"""
    with open(LOG_FILE, 'a') as f:
        f.write(entry)

def main():
    ensure_dirs()
    session = get_latest_session()
    if not session:
        return print("❌ No session files")
    if session.get('error'):
        return print(f"❌ {session['error']}")
    slug = archive(session)
    update_log(session, slug)
    print(f"✅ {session['file']} → wiki/outputs/{slug}")
    print(f"   {session['msg_count']} msgs, {len(session['decisions'])} decisions")

if __name__ == "__main__":
    main()
