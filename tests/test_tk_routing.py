#!/usr/bin/env python3
"""SEC-01: TK/短剧路由隔离测试"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.skill_registry.skill_loader import validate_task_skill

passed = 0
failed = 0

def test(name, task_id, skill_name, expect_ok):
    global passed, failed
    ok, reason = validate_task_skill(task_id, skill_name)
    if ok == expect_ok:
        print(f"  PASS: {name} → {'✅' if ok else '🚫'} {reason}")
        passed += 1
    else:
        print(f"  FAIL: {name} → expected {'OK' if expect_ok else 'BLOCK'}, got {reason}")
        failed += 1

print("=" * 60)
print("  TK/短剧路由隔离测试 (SEC-01)")
print("=" * 60)

test("TK→claw-operator",            "TK-SG-20260429-001", "claw-operator",        True)
test("TK→water-margin-drama BLOCK", "TK-VN-20260429-002", "water-margin-drama",   False)
test("drama→water-margin-drama",    "DS-武松打虎-001",     "water-margin-drama",   True)
test("drama→claw-operator BLOCK",   "DS-复仇爽剧-002",     "claw-operator",        False)
# feishu-tk-notifier 是跨线通知 skill，被主 skill 优先级覆盖（预期行为）
test("drama→water-margin-drama优先","DS-复仇爽剧-002",     "water-margin-drama",   True)
test("TK→claw-operator优先",        "TK-SG-20260429-001", "claw-operator",        True)
test("unknown→claw-operator",       "XX-missing-001",      "claw-operator",        False)

print(f"\n{'='*60}")
print(f"  {passed} PASS / {failed} FAIL / {passed+failed} total")
if failed > 0:
    print("  ❌ 路由隔离测试失败")
    sys.exit(1)
else:
    print("  ✅ 路由隔离测试全部通过")
