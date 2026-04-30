#!/usr/bin/env python3
"""
Token 预算门禁 — pipeline 每步前 check_budget()
超预算 → 暂停 + 飞书提醒
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

BUDGET_FILE = Path.home() / ".openclaw" / "data" / "token_budget.json"
DEFAULT_DAILY_LIMIT = 500000


def load_budget():
    if not BUDGET_FILE.exists():
        return {"daily_limit": DEFAULT_DAILY_LIMIT, "daily_used": 0, "status": "ok"}
    try:
        with open(BUDGET_FILE) as f:
            return json.load(f)
    except Exception:
        return {"daily_limit": DEFAULT_DAILY_LIMIT, "daily_used": 0, "status": "ok"}


def check_budget(step_name="", estimated_tokens=0):
    """
    检查Token预算。返回 (ok, remaining, total, msg)

    Args:
        step_name: 步骤名 (用于告警)
        estimated_tokens: 预估消耗 (0=跳过检查)

    Returns:
        (True, remaining, total, "") if ok
        (False, remaining, total, "警告信息") if over budget
    """
    budget = load_budget()
    daily_limit = budget.get("daily_limit", DEFAULT_DAILY_LIMIT)
    daily_used = budget.get("daily_used", 0)
    remaining = daily_limit - daily_used

    if estimated_tokens == 0:
        return True, remaining, daily_limit, ""

    if daily_used + estimated_tokens > daily_limit:
        msg = f"Token预算不足: 已用{daily_used}/{daily_limit}, 预估{estimated_tokens}"
        try:
            from feishu_decision_notifier import push_decision
            push_decision(
                task_id=f"budget_{datetime.now().strftime('%Y%m%d')}",
                node_name="Token预算门禁",
                summary=msg,
                score=remaining / daily_limit * 10 if daily_limit else 0,
                threshold=5.0,
            )
        except Exception:
            pass
        return False, remaining, daily_limit, msg

    return True, remaining, daily_limit, ""


def consume_tokens(tokens: int, desc: str = ""):
    """消耗 Token"""
    budget = load_budget()
    budget["daily_used"] = budget.get("daily_used", 0) + tokens
    budget["last_consumed"] = datetime.now().isoformat()
    budget["last_description"] = desc
    BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BUDGET_FILE, "w") as f:
        json.dump(budget, f, indent=2)


def main():
    budget = load_budget()
    remaining = budget.get("daily_limit", DEFAULT_DAILY_LIMIT) - budget.get("daily_used", 0)
    pct = 100 - (budget.get("daily_used", 0) / budget.get("daily_limit", DEFAULT_DAILY_LIMIT) * 100)

    print(json.dumps({
        "daily_limit": budget.get("daily_limit", DEFAULT_DAILY_LIMIT),
        "daily_used": budget.get("daily_used", 0),
        "remaining": remaining,
        "remaining_pct": round(pct, 1),
        "status": budget.get("status", "ok"),
    }, ensure_ascii=False, indent=2))

    ok = budget.get("daily_used", 0) < budget.get("daily_limit", DEFAULT_DAILY_LIMIT)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
