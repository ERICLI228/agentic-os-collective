#!/usr/bin/env python3
"""
达人 CRM 基础版 — v3.5 Sprint 4.4 (FR-TK-010)

管理 TikTok 联盟达人关系:
  1. 达人库 (基础信息/粉丝量/佣金率/合作状态)
  2. 佣金追踪 (待结算/已结算)
  3. 跟进记录 (沟通历史)
  4. 达人分层 (S/A/B/C)

数据: 本地 JSON (TK Affiliate API 暂不可用)

用法:
  python3 shared/core/affiliate_crm.py --test
  python3 shared/core/affiliate_crm.py --add "达人名称" --follower 100000 --country PH
"""

import json, sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional

DATA_DIR = Path.home() / ".agentic-os" / "affiliate_crm"
AFFILIATE_DB = DATA_DIR / "affiliates.json"
FOLLOWUP_LOG = DATA_DIR / "followups.json"


# ── 达人分层标准 ──
TIERS = {
    "S": {"min_followers": 500000, "min_gmv": 10000, "commission_range": (10, 15)},
    "A": {"min_followers": 100000, "min_gmv": 5000, "commission_range": (12, 18)},
    "B": {"min_followers": 20000, "min_gmv": 1000, "commission_range": (15, 20)},
    "C": {"min_followers": 0, "min_gmv": 0, "commission_range": (18, 25)},
}

COUNTRIES = ["SG", "MY", "TH", "PH", "VN"]


@dataclass
class Affiliate:
    """达人档案"""
    id: str
    name: str
    tiktok_handle: str          # @用户名
    country: str
    followers: int
    tier: str                   # S/A/B/C
    commission_rate: float      # 佣金百分比
    status: str                 # "active"/"pending"/"inactive"/"blocked"
    total_gmv: float            # 累计 GMV
    total_orders: int
    last_collab_date: str
    tags: List[str]
    notes: str
    created_at: str
    updated_at: str


@dataclass
class FollowUp:
    """跟进记录"""
    id: str
    affiliate_id: str
    date: str
    type: str                   # "invite"/"negotiate"/"review"/"settle"
    content: str
    result: str                 # "accepted"/"rejected"/"pending"/"completed"
    next_action: str
    next_action_date: str


def calculate_tier(followers: int, gmv: float) -> str:
    """根据粉丝量和 GMV 计算达人层级（新达人看粉丝量）"""
    # 新达人无 GMV 时按粉丝量分层
    if gmv == 0:
        for tier in ["S", "A", "B", "C"]:
            if followers >= TIERS[tier]["min_followers"]:
                return tier
        return "C"
    for tier in ["S", "A", "B", "C"]:
        std = TIERS[tier]
        if followers >= std["min_followers"] and gmv >= std["min_gmv"]:
            return tier
    return "C"


def load_affiliates() -> List[Affiliate]:
    """加载达人库"""
    if not AFFILIATE_DB.exists():
        return []
    with open(AFFILIATE_DB) as f:
        data = json.load(f)
    return [Affiliate(**a) for a in data.get("affiliates", [])]


def save_affiliates(affiliates: List[Affiliate]):
    """保存达人库"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "updated_at": datetime.now().isoformat(),
        "total": len(affiliates),
        "affiliates": [asdict(a) for a in affiliates],
    }
    with open(AFFILIATE_DB, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_affiliate(name: str, follower: int = 0, country: str = "PH",
                  handle: str = "", commission: float = 15.0) -> Affiliate:
    """添加达人"""
    affiliates = load_affiliates()
    tier = calculate_tier(follower, 0)

    new_id = f"AF-{len(affiliates) + 1:04d}"
    new = Affiliate(
        id=new_id,
        name=name,
        tiktok_handle=handle or f"@{name.lower().replace(' ', '_')}",
        country=country,
        followers=follower,
        tier=tier,
        commission_rate=commission,
        status="pending",
        total_gmv=0,
        total_orders=0,
        last_collab_date="",
        tags=[],
        notes="",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
    )
    affiliates.append(new)
    save_affiliates(affiliates)
    return new


def log_followup(affiliate_id: str, type: str, content: str,
                 result: str = "pending", next_action: str = "", next_date: str = "") -> FollowUp:
    """记录跟进"""
    if not FOLLOWUP_LOG.exists():
        with open(FOLLOWUP_LOG, "w") as f:
            json.dump({"followups": []}, f)

    with open(FOLLOWUP_LOG) as f:
        data = json.load(f)

    new_id = f"FU-{len(data.get('followups', [])) + 1:04d}"
    followup = FollowUp(
        id=new_id,
        affiliate_id=affiliate_id,
        date=datetime.now().isoformat(),
        type=type,
        content=content,
        result=result,
        next_action=next_action,
        next_action_date=next_date,
    )
    data["followups"].append(asdict(followup))
    with open(FOLLOWUP_LOG, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return followup


def generate_dashboard() -> dict:
    """生成达人 CRM 仪表盘"""
    affiliates = load_affiliates()
    if not affiliates:
        return {"message": "No affiliates in database"}

    tier_counts = {}
    for a in affiliates:
        tier_counts[a.tier] = tier_counts.get(a.tier, 0) + 1

    country_counts = {}
    for a in affiliates:
        country_counts[a.country] = country_counts.get(a.country, 0) + 1

    status_counts = {}
    for a in affiliates:
        status_counts[a.status] = status_counts.get(a.status, 0) + 1

    total_gmv = sum(a.total_gmv for a in affiliates)
    total_orders = sum(a.total_orders for a in affiliates)

    # 待跟进
    if FOLLOWUP_LOG.exists():
        with open(FOLLOWUP_LOG) as f:
            followups = json.load(f).get("followups", [])
        pending = [fu for fu in followups if fu.get("result") == "pending"]
    else:
        pending = []

    return {
        "total_affiliates": len(affiliates),
        "tier_distribution": tier_counts,
        "country_distribution": country_counts,
        "status_distribution": status_counts,
        "total_gmv": round(total_gmv, 2),
        "total_orders": total_orders,
        "pending_followups": len(pending),
        "top_affiliates": sorted([asdict(a) for a in affiliates],
                                  key=lambda x: x["total_gmv"], reverse=True)[:5],
    }


def main():
    if "--test" in sys.argv:
        print("=" * 60)
        print("  达人 CRM — Mock 测试")
        print("=" * 60)

        # 清空测试数据
        for p in [AFFILIATE_DB, FOLLOWUP_LOG]:
            if p.exists():
                p.unlink()

        # 添加测试达人
        mock_affiliates = [
            {"name": "TechGuruSG", "follower": 850000, "country": "SG", "commission": 12},
            {"name": "GadgetReviewPH", "follower": 320000, "country": "PH", "commission": 15},
            {"name": "UnboxingMY", "follower": 150000, "country": "MY", "commission": 18},
            {"name": "TechDailyTH", "follower": 80000, "country": "TH", "commission": 20},
            {"name": "BudgetGadgetsVN", "follower": 25000, "country": "VN", "commission": 22},
            {"name": "SmartLifeSG", "follower": 5000, "country": "SG", "commission": 25},
            {"name": "PhoneHacksPH", "follower": 1200000, "country": "PH", "commission": 10},
            {"name": "CheapTechMY", "follower": 45000, "country": "MY", "commission": 18},
            {"name": "ElectroReviewTH", "follower": 600000, "country": "TH", "commission": 14},
            {"name": "VNUnboxer", "follower": 95000, "country": "VN", "commission": 16},
        ]

        print("\n📋 添加达人:")
        for ma in mock_affiliates:
            af = add_affiliate(**ma)
            print(f"  ✅ {af.id} | {af.tier} | {af.followers:,}粉 | {af.commission_rate}% | {af.country}")

        # 添加跟进记录
        print("\n📝 跟进记录:")
        followups = [
            ("AF-0001", "invite", "发送合作邀请 — 15% 佣金", "accepted", "寄送样品", "2026-05-05"),
            ("AF-0002", "invite", "邀请测评手机壳", "pending", "", ""),
            ("AF-0007", "negotiate", "协商 S 级佣金 10%", "pending", "确认合同", "2026-05-03"),
            ("AF-0003", "review", "审核视频数据: 5万播放, 2% 转化", "completed", "续约谈判", "2026-05-10"),
        ]
        for fu in followups:
            f = log_followup(*fu)
            print(f"  ✅ {f.id} | {f.affiliate_id} | {f.type} | {f.result}")

        # 生成仪表盘
        dash = generate_dashboard()
        print(f"\n📊 达人 CRM 仪表盘:\n")
        print(f"  总达人: {dash['total_affiliates']}")
        print(f"  分层: {dash['tier_distribution']}")
        print(f"  国家: {dash['country_distribution']}")
        print(f"  状态: {dash['status_distribution']}")
        print(f"  总 GMV: ${dash['total_gmv']:,.2f}")
        print(f"  总订单: {dash['total_orders']}")
        print(f"  待跟进: {dash['pending_followups']}")
        print()

        if dash.get("top_affiliates"):
            print("  🏆 TOP 达人:")
            for t in dash["top_affiliates"][:3]:
                print(f"    {t['name']} ({t['country']}) | {t['followers']:,}粉 | ${t['total_gmv']:,.0f} GMV")
            print()

        print(f"✅ 数据已保存:")
        print(f"  达人库: {AFFILIATE_DB}")
        print(f"  跟进记录: {FOLLOWUP_LOG}")
        return

    # CLI 操作模式
    if "--add" in sys.argv:
        idx = sys.argv.index("--add")
        name = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "Unknown"
        follower = int(sys.argv[sys.argv.index("--follower") + 1]) if "--follower" in sys.argv else 0
        country = sys.argv[sys.argv.index("--country") + 1] if "--country" in sys.argv else "PH"
        commission = float(sys.argv[sys.argv.index("--commission") + 1]) if "--commission" in sys.argv else 15.0
        handle = sys.argv[sys.argv.index("--handle") + 1] if "--handle" in sys.argv else ""

        af = add_affiliate(name, follower, country, handle, commission)
        print(f"✅ Added: {af.id} | {af.name} | {af.tier} | {af.country}")
        return

    if "--dashboard" in sys.argv:
        dash = generate_dashboard()
        print(json.dumps(dash, ensure_ascii=False, indent=2))
        return

    print(__doc__)


if __name__ == "__main__":
    main()
