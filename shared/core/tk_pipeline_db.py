"""
Agentic OS SQLite 运行库 — 替代 JSON 文件
所有 pipeline 运行/决策/里程碑/健康度/竞品/订单 统一存储
"""
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path.home() / ".agentic-os" / "pipeline.db"


@contextmanager
def get_db(write=False):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        if write:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """初始化数据库 schema"""
    with get_db(write=True) as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT UNIQUE NOT NULL,
            episode TEXT,
            voice_mode TEXT DEFAULT 'say',
            silent_mode INTEGER DEFAULT 0,
            status TEXT DEFAULT 'running',
            milestones_total INTEGER DEFAULT 0,
            milestones_completed INTEGER DEFAULT 0,
            output_path TEXT,
            error_log TEXT,
            started_at TEXT NOT NULL DEFAULT (datetime('now')),
            ended_at TEXT
        );

        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            node_name TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            score REAL DEFAULT 0,
            threshold REAL DEFAULT 8.0,
            reason TEXT,
            summary TEXT,
            decided_at TEXT,
            decided_by TEXT DEFAULT '驾驶舱',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ms_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            decision_point INTEGER DEFAULT 0,
            decision TEXT,
            note TEXT,
            completed_at TEXT,
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS shop_health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id TEXT NOT NULL,
            shop_name TEXT,
            site TEXT,
            item_count INTEGER DEFAULT 0,
            score INTEGER DEFAULT 100,
            status TEXT DEFAULT 'healthy',
            issues TEXT,
            checked_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS competitor_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            product_name TEXT,
            price REAL,
            sales INTEGER DEFAULT 0,
            shop_id TEXT,
            source TEXT DEFAULT 'miaoshou',
            recorded_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_item_id TEXT UNIQUE NOT NULL,
            title TEXT,
            price REAL,
            categories TEXT,
            shop_id TEXT,
            synced_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE NOT NULL,
            product_id TEXT,
            shop_id TEXT,
            amount REAL DEFAULT 0,
            quantity INTEGER DEFAULT 1,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_pipeline_runs_status ON pipeline_runs(status);
        CREATE INDEX IF NOT EXISTS idx_decisions_status ON decisions(status);
        CREATE INDEX IF NOT EXISTS idx_milestones_status ON milestones(status);
        CREATE INDEX IF NOT EXISTS idx_shop_health_shop ON shop_health(shop_id);
        CREATE INDEX IF NOT EXISTS idx_competitor_product ON competitor_snapshots(product_id);
        CREATE INDEX IF NOT EXISTS idx_products_source ON products(source_item_id);
        """)
    return True


# ============================================================
# Pipeline Runs
# ============================================================

def start_run(run_id=None, episode=None, voice_mode="say", silent=False):
    if run_id is None:
        run_id = f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    with get_db(write=True) as db:
        db.execute(
            "INSERT INTO pipeline_runs (run_id, episode, voice_mode, silent_mode, status) VALUES (?,?,?,?,?)",
            (run_id, episode, voice_mode, 1 if silent else 0, "running")
        )
    return run_id


def complete_run(run_id, output_path="", milestones_completed=0, milestones_total=0):
    with get_db(write=True) as db:
        db.execute(
            "UPDATE pipeline_runs SET status='completed', ended_at=datetime('now'), output_path=?, milestones_completed=?, milestones_total=? WHERE run_id=?",
            (output_path, milestones_completed, milestones_total, run_id)
        )


def fail_run(run_id, error=""):
    with get_db(write=True) as db:
        db.execute(
            "UPDATE pipeline_runs SET status='failed', ended_at=datetime('now'), error_log=? WHERE run_id=?",
            (error, run_id)
        )


def get_recent_runs(limit=20):
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


# ============================================================
# Decisions
# ============================================================

def create_decision(task_id, node_name, summary="", score=0, threshold=8.0):
    with get_db(write=True) as db:
        db.execute(
            "INSERT INTO decisions (task_id, node_name, summary, score, threshold) VALUES (?,?,?,?,?)",
            (task_id, node_name, summary, score, threshold)
        )


def resolve_decision(task_id, action, reason=""):
    status_map = {"approved": "approved", "rejected": "rejected", "modify": "modify"}
    status = status_map.get(action, action)
    with get_db(write=True) as db:
        db.execute(
            "UPDATE decisions SET status=?, reason=?, decided_at=datetime('now') WHERE task_id=? AND status='pending'",
            (status, reason, task_id)
        )


def get_pending_decisions():
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM decisions WHERE status='pending' ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_decision_stats():
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]
        approved = db.execute("SELECT COUNT(*) FROM decisions WHERE status='approved'").fetchone()[0]
        pending = db.execute("SELECT COUNT(*) FROM decisions WHERE status='pending'").fetchone()[0]
        rejected = db.execute("SELECT COUNT(*) FROM decisions WHERE status='rejected'").fetchone()[0]
    return {"total": total, "approved": approved, "pending": pending, "rejected": rejected}


# ============================================================
# Milestones
# ============================================================

def init_milestones(milestones_list):
    with get_db(write=True) as db:
        for ms in milestones_list:
            db.execute(
                "INSERT OR IGNORE INTO milestones (ms_id, name, status, decision_point, note) VALUES (?,?,?,?,?)",
                (ms["id"], ms["name"], ms.get("status", "pending"),
                 ms.get("decision_point", 0), ms.get("note", ""))
            )


def update_milestone(ms_id, status=None, decision=None, note=None):
    fields = []
    values = []
    if status:
        fields.append("status=?")
        values.append(status)
        if status == "completed":
            fields.append("completed_at=datetime('now')")
    if decision:
        fields.append("decision=?")
        values.append(decision)
    if note is not None:
        fields.append("note=?")
        values.append(note)
    fields.append("updated_at=datetime('now')")
    values.append(ms_id)

    with get_db(write=True) as db:
        db.execute(f"UPDATE milestones SET {', '.join(fields)} WHERE ms_id=?", values)


def get_milestones():
    with get_db() as db:
        rows = db.execute("SELECT * FROM milestones ORDER BY ms_id").fetchall()
    return [dict(r) for r in rows]


def get_milestone_stats():
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM milestones").fetchone()[0]
        completed = db.execute("SELECT COUNT(*) FROM milestones WHERE status='completed'").fetchone()[0]
        pending = db.execute("SELECT COUNT(*) FROM milestones WHERE status='waiting_approval'").fetchone()[0]
    pct = round(completed / total * 100, 1) if total > 0 else 0
    return {"total_milestones": total, "completed": completed, "decision_pending": pending, "completion_pct": pct}


# ============================================================
# Shop Health
# ============================================================

def record_shop_health(shop_id, shop_name, site, item_count, score, status, issues=None):
    issues_json = json.dumps(issues, ensure_ascii=False) if issues else "[]"
    with get_db(write=True) as db:
        db.execute(
            "INSERT INTO shop_health (shop_id, shop_name, site, item_count, score, status, issues) VALUES (?,?,?,?,?,?,?)",
            (shop_id, shop_name, site, item_count, score, status, issues_json)
        )


def get_latest_shop_health():
    with get_db() as db:
        rows = db.execute("""
            SELECT * FROM shop_health WHERE (shop_id, checked_at) IN (
                SELECT shop_id, MAX(checked_at) FROM shop_health GROUP BY shop_id
            )
        """).fetchall()
    return [dict(r) for r in rows]


# ============================================================
# Competitor Snapshots
# ============================================================

def record_competitor(product_id, product_name, price, sales=0, shop_id=None, source="miaoshou"):
    with get_db(write=True) as db:
        db.execute(
            "INSERT INTO competitor_snapshots (product_id, product_name, price, sales, shop_id, source) VALUES (?,?,?,?,?,?)",
            (product_id, product_name, price, sales, shop_id, source)
        )


def get_competitor_trend(product_id, days=7):
    with get_db() as db:
        rows = db.execute("""
            SELECT * FROM competitor_snapshots
            WHERE product_id=? AND recorded_at >= datetime('now', ?)
            ORDER BY recorded_at DESC
        """, (product_id, f"-{days} days")).fetchall()
    return [dict(r) for r in rows]


# ============================================================
# Products
# ============================================================

def sync_product(source_item_id, title, price, categories=None, shop_id=None):
    cats_json = json.dumps(categories, ensure_ascii=False) if categories else "[]"
    with get_db(write=True) as db:
        db.execute("""
            INSERT INTO products (source_item_id, title, price, categories, shop_id, synced_at)
            VALUES (?,?,?,?,?,datetime('now'))
            ON CONFLICT(source_item_id) DO UPDATE SET
                title=excluded.title, price=excluded.price,
                categories=excluded.categories, synced_at=datetime('now')
        """, (source_item_id, title, price, cats_json, shop_id))


def get_products(limit=100):
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM products ORDER BY synced_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


# ============================================================
# Orders
# ============================================================

def record_order(order_id, product_id=None, shop_id=None, amount=0, quantity=1, status="pending"):
    with get_db(write=True) as db:
        db.execute("""
            INSERT INTO orders (order_id, product_id, shop_id, amount, quantity, status)
            VALUES (?,?,?,?,?,?)
            ON CONFLICT(order_id) DO UPDATE SET
                amount=excluded.amount, status=excluded.status
        """, (order_id, product_id, shop_id, amount, quantity, status))


def get_order_stats():
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        revenue = db.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM orders WHERE status='completed'"
        ).fetchone()[0]
    return {"total_orders": total, "total_revenue": round(revenue, 2)}


# ============================================================
# Dashboard Aggregation
# ============================================================

def get_dashboard():
    """聚合所有数据 → /api/dashboard 响应格式"""
    ms = get_milestone_stats()
    dec = get_decision_stats()
    runs = get_recent_runs(5)
    health = get_latest_shop_health()
    orders = get_order_stats()

    health_summary = {"total": len(health), "healthy": 0, "warning": 0, "critical": 0}
    for h in health:
        health_summary[h["status"]] = health_summary.get(h["status"], 0) + 1

    return {
        **ms,
        "decisions": dec,
        "recent_runs": len(runs),
        "last_run": runs[0]["started_at"] if runs else None,
        "shop_health": health_summary,
        "orders": orders,
        "milestones": [dict(m) for m in get_milestones()],
        "timestamp": datetime.now().isoformat(),
    }


# ============================================================
# Migration: JSON → SQLite
# ============================================================

def migrate_from_json():
    """将现有 JSON 数据迁移到 SQLite"""
    init_db()

    # 迁移 milestones
    milestones_path = Path.home() / ".agentic-os" / "milestones.json"
    if milestones_path.exists():
        with open(milestones_path) as f:
            raw = json.load(f)
        ms_list = raw if isinstance(raw, list) else raw.get("milestones", [])
        if isinstance(ms_list, dict):
            ms_list = [{"id": k, "name": v.get("name", k), "status": v.get("status", "pending"), 
                        "decision_point": v.get("decision_point", 0), "note": v.get("note", ""),
                        "decision": v.get("decision")}
                       for k, v in ms_list.items()]
        init_milestones(ms_list)
        print(f"✅ 迁移 {len(ms_list)} 个里程碑")

    # 迁移决策日志
    decisions_dir = Path.home() / ".agentic-os" / "decisions"
    if decisions_dir.exists():
        count = 0
        for f in sorted(decisions_dir.glob("*.json")):
            try:
                d = json.loads(f.read_text())
                create_decision(
                    task_id=d.get("task_id", f.stem),
                    node_name=d.get("node", d.get("node_name", "unknown")),
                    summary=d.get("summary", ""),
                    score=d.get("score", 0),
                    threshold=d.get("threshold", 8.0),
                )
                if d.get("decision_status"):
                    resolve_decision(d["task_id"], d["decision_status"], d.get("judge_reason", ""))
                count += 1
            except Exception:
                pass
        print(f"✅ 迁移 {count} 条决策")

    # 迁移 miaoshou 产品
    products_path = Path.home() / ".agentic-os" / "miaoshou_products.json"
    if products_path.exists():
        with open(products_path) as f:
            data = json.load(f)
        count = 0
        for p in data.get("products", data.get("items", [])):
            try:
                sync_product(
                    source_item_id=p.get("sourceItemId", p.get("id", "")),
                    title=p.get("title", ""),
                    price=p.get("price", 0),
                    shop_id=p.get("shopId", ""),
                )
                count += 1
            except Exception:
                pass
        print(f"✅ 迁移 {count} 个产品")

    print(f"📄 数据库: {DB_PATH}")
    return True


def main():
    import sys
    if "--migrate" in sys.argv:
        migrate_from_json()
    elif "--init" in sys.argv:
        init_db()
        print(f"✅ 数据库初始化: {DB_PATH}")
    elif "--test" in sys.argv:
        init_db()
        rid = start_run(episode="01", voice_mode="nls")
        complete_run(rid, output_path="/tmp/final.mp4", milestones_completed=5, milestones_total=5)
        create_decision("TK-TEST-001", "market_assessment", "防水手机壳 81%毛利", 8.5)
        resolve_decision("TK-TEST-001", "approved", "通过")
        record_shop_health("8371977", "PH店", "PH", 15, 100, "healthy")
        record_competitor("p001", "防水手机壳", 5.99, 500, "8371977")
        sync_product("src001", "防水手机壳 X Pro", 5.99)

        dash = get_dashboard()
        print(json.dumps(dash, ensure_ascii=False, indent=2))
        print("\n✅ --test PASS: tk_pipeline_db")
    else:
        dash = get_dashboard()
        print(json.dumps(dash, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
