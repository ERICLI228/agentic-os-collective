#!/usr/bin/env python3
"""Structured feedback collector (S4-4). 
Usage:
  python3 feedback_collector.py --save --type 剧本质量 --desc "剧情节奏太慢" --severity major
  python3 feedback_collector.py --list
"""
import json, os, sys, time
from pathlib import Path
from datetime import datetime

FEEDBACK_DIR = Path.home() / ".agentic-os" / "quality_feedback"
FEEDBACK_FILE = FEEDBACK_DIR / "feedback.jsonl"

def save_feedback(fb_type, desc, severity="minor", task_id="", source=""):
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": fb_type,
        "description": desc,
        "severity": severity,
        "task_id": task_id,
        "source": source
    }
    with open(FEEDBACK_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def list_feedback(limit=50):
    if not FEEDBACK_FILE.exists():
        return []
    entries = []
    with open(FEEDBACK_FILE) as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except:
                continue
    entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    return entries[:limit]

def stats():
    entries = list_feedback(1000)
    by_type = {}
    for e in entries:
        t = e.get("type", "其他")
        by_type[t] = by_type.get(t, 0) + 1
    return {"total": len(entries), "by_type": by_type}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--type", default="其他")
    parser.add_argument("--desc", default="")
    parser.add_argument("--severity", default="minor")
    parser.add_argument("--task", default="")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    if args.save:
        e = save_feedback(args.type, args.desc, args.severity, args.task)
        print(json.dumps(e, ensure_ascii=False))
    if args.list:
        for e in list_feedback():
            print(json.dumps(e, ensure_ascii=False))
