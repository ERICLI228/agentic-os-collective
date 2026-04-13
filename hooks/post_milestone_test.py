#!/usr/bin/env python3
"""
里程碑完成后自动触发测试
"""
import subprocess
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEST_SUITES = {
    "drama": {
        "MS-1": "tests/drama/test_artifacts_unique.py",
        "MS-4": "tests/drama/test_glm_script.py",
        "MS-7": "tests/drama/test_artifacts_unique.py"
    },
    "tk": {
        "MS-1": "tests/tk/test_data_collector.py",
        "MS-10": "tests/tk/test_milestone_artifacts.py",
        "MS-12": "tests/tk/test_data_collector.py"
    }
}

TEST_TIMEOUT = 300

def run_tests_for_milestone(project: str, milestone_id: str) -> dict:
    """执行里程碑测试"""
    start_time = datetime.utcnow()
    
    test_path = TEST_SUITES.get(project, {}).get(milestone_id)
    if not test_path:
        return {"status": "skipped", "reason": "No tests defined"}
    
    work_dir = Path.home() / ".agentic-os-collective/test_runs" / f"{project}_{milestone_id}"
    work_dir.mkdir(parents=True, exist_ok=True)
    
    # 使用python3 -m pytest确保pytest可用
    test_cmd = [
        "python3", "-m", "pytest",
        test_path,
        "--junitxml=test_report.xml",
        "-q",
        "-v"
    ]
    
    logger.info(f"执行测试: {' '.join(test_cmd)}")
    
    try:
        result = subprocess.run(
            test_cmd,
            cwd=str(Path.home() / "agentic-os-collective"),
            capture_output=True,
            text=True,
            timeout=TEST_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "reason": f"超时{TEST_TIMEOUT}s"}
    
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    try:
        report_file = work_dir / "test_report.xml"
        if not report_file.exists():
            report_file = Path.home() / "agentic-os-collective/test_report.xml"
        
        tree = ElementTree.parse(report_file)
        root = tree.getroot()
        tests = int(root.attrib.get("tests", 0))
        failures = int(root.attrib.get("failures", 0))
        errors = int(root.attrib.get("errors", 0))
        
        return {
            "status": "passed" if failures == 0 and errors == 0 else "failed",
            "tests": tests,
            "failures": failures,
            "errors": errors,
            "duration_seconds": round(duration, 2),
            "stdout": result.stdout[:500],
            "stderr": result.stderr[:500],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"解析报告失败: {e}")
        return {
            "status": "error",
            "reason": str(e),
            "stdout": result.stdout[:500],
            "timestamp": datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python post_milestone_test.py <project> <milestone_id>")
        sys.exit(1)
    
    project = sys.argv[1]
    milestone_id = sys.argv[2]
    
    result = run_tests_for_milestone(project, milestone_id)
    print(json.dumps(result, indent=2))
    
    # 返回状态码：0=passed, 1=failed
    sys.exit(0 if result.get("status") == "passed" else 1)