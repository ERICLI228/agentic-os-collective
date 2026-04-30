#!/usr/bin/env python3
"""
飞书决策通知器 — DEC-01 (FR-BS-014)
在 pipeline 决策节点到达时，推送到飞书卡片并等待人工决策。
"""
import json, sys, requests
from pathlib import Path
from datetime import datetime

DECISIONS_DIR = Path.home() / ".agentic-os" / "decisions"
DECISIONS_DIR.mkdir(parents=True, exist_ok=True)

from shared.config import config

WEBHOOK_URL = config.get_feishu_webhook("选品作战室")
RESOLVE_CMD = "python3 shared/feishu_cards/resolve.py"


def build_decision_card(task_id: str, node_name: str, summary: str,
                        score: float, threshold: float,
                        options: list) -> dict:
    """构建飞书决策卡片"""
    score_color = "red" if score < threshold else "green"
    resolve_calls = []
    for opt in options:
        action = opt.get("action", "")
        label = opt.get("label", "")
        resolve_calls.append(f"{RESOLVE_CMD} {task_id} --action {action}")

    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**{node_name}**"}},
        {"tag": "hr"},
        {"tag": "div", "text": {"tag": "lark_md", "content": summary}},
        {"tag": "div", "text": {"tag": "lark_md",
         "content": f"评分: <font color={score_color}>{score}/10</font> (阈值 {threshold})"}},
        {"tag": "hr"},
        {"tag": "div", "text": {"tag": "lark_md",
         "content": "**决策方式**: 终端运行\n" + "\n".join(f"• `{c}`" for c in resolve_calls)}},
    ]

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"🔔 待决策: {node_name}"},
            "template": "red" if score < threshold else "green",
        },
        "elements": elements,
    }


def push_decision(task_id: str, node_name: str, summary: str,
                  score: float = 0, threshold: float = 8.0,
                  options: list = None, webhook_url: str = None) -> bool:
    """推送决策到飞书"""
    if options is None:
        options = [
            {"action": "approved", "label": "✅ 通过"},
            {"action": "modify", "label": "✏️ 修改"},
            {"action": "rejected", "label": "❌ 驳回"},
        ]

    card = build_decision_card(task_id, node_name, summary, score, threshold, options)
    url = webhook_url or WEBHOOK_URL

    try:
        resp = requests.post(url, json={"msg_type": "interactive", "card": card}, timeout=10)
        if resp.status_code == 200 and resp.json().get("code") == 0:
            print(f"✅ 飞书决策卡片已推送: {task_id} → {node_name}")
            _save_decision_log(task_id, node_name, score, card)
            return True
        else:
            print(f"⚠️ 飞书推送异常: {resp.status_code} {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 飞书推送失败: {e}")
        return False


def _save_decision_log(task_id: str, node_name: str, score: float, card: dict):
    """保存决策记录"""
    log_file = DECISIONS_DIR / f"notified_{task_id}.json"
    log_file.write_text(json.dumps({
        "task_id": task_id,
        "node": node_name,
        "score": score,
        "notified_at": datetime.now().isoformat(),
        "card_preview": str(card)[:500],
    }, ensure_ascii=False, indent=2))


def check_pending_decisions() -> list:
    """检查所有未决策的任务"""
    pending = []
    for f in DECISIONS_DIR.glob("*.json"):
        if f.name.startswith("ms"):
            data = json.loads(f.read_text())
            if data.get("status") in ("pending", "waiting_approval"):
                pending.append(data)
    return pending


if __name__ == "__main__":
    if "--test" in sys.argv:
        print("=" * 60)
        print("  飞书决策通知器 — 测试")
        print("=" * 60)
        push_decision(
            task_id="TK-TEST-20260429-001",
            node_name="MS-2 选品审核",
            summary="TOP3 商品已分析完成:\n1. HDMI转接头 8.42分\n2. 火把灯 7.64分\n3. 拓展坞 7.42分",
            score=7.8,
            threshold=8.0,
        )
        print("\n✅ 测试完毕，请检查飞书选品作战室群")
    elif "--node" in sys.argv:
        idx = sys.argv.index("--node")
        node_name = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "MS-2"
        tidx = sys.argv.index("--task") if "--task" in sys.argv else -1
        task_id = sys.argv[tidx + 1] if tidx > 0 else f"TK-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        sidx = sys.argv.index("--score") if "--score" in sys.argv else -1
        score = float(sys.argv[sidx + 1]) if sidx > 0 else 7.5
        summary = " ".join(sys.argv[-1:]) if len(sys.argv) > 2 else "Decision required"
        push_decision(task_id, node_name, summary, score=score)
    else:
        print(__doc__)
