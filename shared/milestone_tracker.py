#!/usr/bin/env python3
"""
里程碑状态追踪器 — v3.5 Sprint 2.4

中心化状态机，记录每个里程碑的状态变更。

状态转换:
  pending → running → waiting_decision → approved/rejected → completed/failed

存储: ~/.agentic-os/milestones.json (JSON 文件，不依赖数据库)

用法:
  from shared.milestone_tracker import get_all, update, record_decision
  milestones = get_all()
  update("MS-1.5", {"status": "waiting_decision"})
  record_decision("MS-1.5", "approved", "市场判断通过")
"""

import json
import yaml
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
STATE_FILE = Path.home() / ".agentic-os" / "milestones.json"
PIPELINE_YAML = Path(__file__).resolve().parent.parent / "shared/templates/tk_pipeline.yaml"

VALID_STATUSES = [
    "pending",
    "running",
    "waiting_decision",
    "approved",
    "rejected",
    "completed",
    "failed",
]


def _load_pipeline_stages():
    """从 tk_pipeline.yaml 动态加载里程碑定义"""
    if PIPELINE_YAML.exists():
        with open(PIPELINE_YAML) as f:
            pipeline = yaml.safe_load(f)
        stages = []
        for s in pipeline.get("stages", []):
            stages.append({
                "id": s["id"],
                "name": s["name"],
                "decision_point": s.get("decision_point", False),
                "decision_type": s.get("decision_type", ""),
                "decision_options": s.get("decision_options", []),
                "decision_timeout_hours": s.get("decision_timeout_hours", 24),
            })
        return stages
    # Pipeline 文件不存在时的最小回退
    return [
        {"id": "MS-1", "name": "数据采集", "decision_point": False},
        {"id": "MS-2", "name": "选品分析", "decision_point": True},
        {"id": "MS-3", "name": "发布准备", "decision_point": False},
        {"id": "MS-4", "name": "发布审批", "decision_point": True},
        {"id": "MS-5", "name": "日报生成", "decision_point": False},
    ]


def _ensure_file():
    """确保状态文件存在，不存在则用默认值初始化"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        data = {
            "project": "TK运营",
            "updated_at": datetime.now(tz).isoformat(),
            "milestones": {}
        }
        for m in _load_pipeline_stages():
            data["milestones"][m["id"]] = {
                "id": m["id"],
                "name": m["name"],
                "status": "pending",
                "decision_point": m["decision_point"],
                "decision": None,
                "decision_at": None,
                "decision_by": None,
                "updated_at": datetime.now(tz).isoformat(),
                "log": [f"{datetime.now(tz).isoformat()} 初始化: pending"]
            }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def get_all():
    """获取所有里程碑状态"""
    _ensure_file()
    with open(STATE_FILE) as f:
        data = json.load(f)
    return data


def get(milestone_id):
    """获取单个里程碑状态"""
    data = get_all()
    return data["milestones"].get(milestone_id)


def update(milestone_id, updates):
    """更新里程碑状态"""
    _ensure_file()
    with open(STATE_FILE) as f:
        data = json.load(f)

    if milestone_id not in data["milestones"]:
        data["milestones"][milestone_id] = {
            "id": milestone_id,
            "name": milestone_id,
            "status": "pending",
            "decision_point": False,
            "decision": None,
            "decision_at": None,
            "decision_by": None,
            "updated_at": datetime.now(tz).isoformat(),
            "log": []
        }

    ms = data["milestones"][milestone_id]

    if "status" in updates:
        new_status = updates["status"]
        if new_status not in VALID_STATUSES:
            raise ValueError(f"无效状态: {new_status}, 有效值: {VALID_STATUSES}")
        ms["log"].append(f"{datetime.now(tz).isoformat()} {ms['status']} → {new_status}")
        ms["status"] = new_status

    for k, v in updates.items():
        if k != "status":
            ms[k] = v

    ms["updated_at"] = datetime.now(tz).isoformat()
    data["updated_at"] = datetime.now(tz).isoformat()

    with open(STATE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return ms


def record_decision(milestone_id, decision, reason=""):
    """记录决策结果"""
    update(milestone_id, {
        "status": "completed" if decision == "approved" else "rejected",
        "decision": decision,
        "decision_at": datetime.now(tz).isoformat(),
        "decision_by": "human",
        "decision_reason": reason
    })


def pending_decisions():
    """返回所有待决策的里程碑"""
    data = get_all()
    return {
        mid: ms for mid, ms in data["milestones"].items()
        if ms.get("status") == "waiting_decision"
    }


def print_status():
    """打印所有里程碑状态"""
    data = get_all()
    print(f"\n{'='*60}")
    print(f"  里程碑状态 | {data.get('project','?')} | {data.get('updated_at','?')[:16]}")
    print(f"{'='*60}")

    status_icons = {
        "pending": "⏳",
        "running": "🏃",
        "waiting_decision": "🔴",
        "approved": "✅",
        "rejected": "❌",
        "completed": "✅",
        "failed": "💀",
    }

    for mid, ms in data["milestones"].items():
        icon = status_icons.get(ms.get("status", "pending"), "?")
        dp = " [决策点]" if ms.get("decision_point") else ""
        decision_info = ""
        if ms.get("decision"):
            decision_info = f" → {ms['decision']} ({ms.get('decision_at','?')[:10]})"
        print(f"  {icon} {mid}: {ms['name']:12s} {ms['status']:16s}{dp}{decision_info}")

    pending = pending_decisions()
    if pending:
        print(f"\n  ⚠️ {len(pending)} 项待决策: {', '.join(pending.keys())}")

    print(f"{'='*60}\n")


# ── CLI ──

if __name__ == "__main__":
    print_status()
