#!/usr/bin/env python3
"""
决策解析器 — v3.5 Sprint 1.3

文件轮询方案的核心 CLI。用户在终端输入决策指令，系统写入决策文件，
/callback 或 API 轮询读到文件变化后更新任务状态。

用法:
  python3 shared/feishu_cards/resolve.py DEC-xxx --action approved
  python3 shared/feishu_cards/resolve.py DEC-xxx --action modify --reason "价格太高，换供应商"
  python3 shared/feishu_cards/resolve.py DEC-xxx --action rejected
  python3 shared/feishu_cards/resolve.py --pending       # 列出所有待决策
"""

import json
import sys
import os
import urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
DECISIONS_DIR = Path.home() / ".agentic-os" / "decisions"
DECISION_API = "http://localhost:5001/api/decision"

def list_pending():
    if not DECISIONS_DIR.exists():
        print("(无待决策项)")
        return
    found = False
    for f in sorted(DECISIONS_DIR.glob("*.json")):
        with open(f) as fh:
            d = json.load(fh)
        if d.get("status") == "waiting_decision":
            print(f"  {d['task_id']} | {d['type']} | {d.get('created_at','?')[:16]}")
            print(f"    选项: {', '.join(d.get('options', []))}")
            found = True
    if not found:
        print("(无待决策项)")

def resolve(task_id, action, reason=""):
    decision_file = DECISIONS_DIR / f"{task_id}.json"
    if not decision_file.exists():
        print(f"❌ 决策文件不存在: {decision_file}")
        print("  (可用 --pending 列出所有待决策项)")
        sys.exit(1)

    with open(decision_file) as f:
        data = json.load(f)

    if data.get("status") != "waiting_decision":
        print(f"⚠️ 该决策已是: {data.get('status')}")
        return

    data["status"] = action if action == "approved" else ("rejected" if action == "rejected" else "modify_requested")
    data["decision"] = action
    data["reason"] = reason
    data["resolved_at"] = datetime.now(tz).isoformat()

    with open(decision_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 决策已写入: {task_id} → {action}")

    # 同时调用 API（如果 Flask 在运行）
    try:
        payload = json.dumps({"task_id": task_id, "action": action, "reason": reason}).encode("utf-8")
        req = urllib.request.Request(DECISION_API, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            print(f"📡 API 同步完成: {json.loads(resp.read())}")
    except Exception:
        print("⚠️ API 同步跳过（Flask 可能未运行）")

def main():
    if "--pending" in sys.argv:
        print("📋 待决策项:")
        list_pending()
        return

    task_id = None
    action = None
    reason = ""

    i = 0
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--action" and i + 1 < len(sys.argv):
            action = sys.argv[i + 1]; i += 2
        elif arg == "--reason" and i + 1 < len(sys.argv):
            reason = sys.argv[i + 1]; i += 2
        elif not arg.startswith("--") and task_id is None:
            task_id = arg; i += 1
        else:
            i += 1

    if not task_id or not action:
        print("用法: resolve.py <task_id> --action <approved|modify|rejected> [--reason '...']")
        print("      resolve.py --pending")
        sys.exit(1)

    if action not in ("approved", "modify", "rejected"):
        print(f"❌ 无效动作: {action} (应为 approved/modify/rejected)")
        sys.exit(1)

    resolve(task_id, action, reason)

if __name__ == "__main__":
    main()
