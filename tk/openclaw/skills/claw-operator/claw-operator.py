#!/usr/bin/env python3
"""
Claw Operator - 状态机 + 失败分类 + 自动恢复
基于 Claude Code 核心逻辑实现
"""
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict
from enum import Enum

# ========== 状态机定义 ==========
class WorkerStatus(Enum):
    SPAWNING = "spawning"
    TRUST_REQUIRED = "trust_required"
    READY_FOR_PROMPT = "ready_for_prompt"
    PROMPT_ACCEPTED = "prompt_accepted"
    RUNNING = "running"
    BLOCKED = "blocked"
    FINISHED = "finished"
    FAILED = "failed"

# ========== 失败分类定义 ==========
class FailureKind(Enum):
    AUTH_RATE_LIMIT = "rate_limit"
    AUTH_API_KEY = "api_key_missing"
    AUTH_TOKEN_EXPIRED = "token_expired"
    NETWORK_TIMEOUT = "timeout"
    NETWORK_REFUSED = "connection_refused"
    NETWORK_DNS = "dns_fail"
    CONFIG_MISSING = "missing_config"
    CONFIG_INVALID = "invalid_config"
    CONFIG_PERMISSION = "permission_denied"
    TOOL_NOT_FOUND = "tool_not_found"
    TOOL_FAILED = "tool_failed"
    TOOL_TIMEOUT = "tool_timeout"
    CODE_SYNTAX = "syntax_error"
    CODE_COMPILE = "compile_error"
    CODE_TEST = "test_failed"
    INFRA_DISK = "disk_full"
    INFRA_MEMORY = "memory_limit"
    INFRA_KILLED = "process_killed"
    DELIVERY_WEBHOOK = "webhook_failed"
    DELIVERY_FEISHU = "feishu_error"
    UNKNOWN = "unknown"

# ========== 恢复配方 ==========
RECOVERY_RECIPES = {
    FailureKind.AUTH_RATE_LIMIT: {"action": "wait_and_retry", "wait": 60, "max_retries": 3},
    FailureKind.AUTH_API_KEY: {"action": "notify_user", "message": "请检查 API Key 配置"},
    FailureKind.NETWORK_TIMEOUT: {"action": "retry_with_backoff", "wait": 10, "max_retries": 2},
    FailureKind.DELIVERY_WEBHOOK: {"action": "check_webhook_config", "fallback": "use_announce"},
    FailureKind.DELIVERY_FEISHU: {"action": "check_feishu_config"},
    FailureKind.CODE_TEST: {"action": "run_diagnostics"},
}

# ========== 失败分类器 ==========
class FailureClassifier:
    @staticmethod
    def classify(error_message: str) -> FailureKind:
        error_lower = error_message.lower()
        
        if "rate_limit" in error_lower or "限流" in error_message:
            return FailureKind.AUTH_RATE_LIMIT
        if "api key" in error_lower or "no api key" in error_lower or "auth" in error_lower:
            return FailureKind.AUTH_API_KEY
        if "token" in error_lower and "expired" in error_lower:
            return FailureKind.AUTH_TOKEN_EXPIRED
        if "timeout" in error_lower or "超时" in error_message:
            return FailureKind.NETWORK_TIMEOUT
        if "connection refused" in error_lower:
            return FailureKind.NETWORK_REFUSED
        if "dns" in error_lower:
            return FailureKind.NETWORK_DNS
        if "permission denied" in error_lower:
            return FailureKind.CONFIG_PERMISSION
        if "webhook" in error_lower:
            return FailureKind.DELIVERY_WEBHOOK
        if "feishu" in error_lower:
            return FailureKind.DELIVERY_FEISHU
        if "syntax" in error_lower:
            return FailureKind.CODE_SYNTAX
        if "compile" in error_lower:
            return FailureKind.CODE_COMPILE
        if "test" in error_lower and "fail" in error_lower:
            return FailureKind.CODE_TEST
        if "disk" in error_lower:
            return FailureKind.INFRA_DISK
        if "memory" in error_lower:
            return FailureKind.INFRA_MEMORY
        if "killed" in error_lower:
            return FailureKind.INFRA_KILLED
            
        return FailureKind.UNKNOWN

    @staticmethod
    def get_recipe(failure_kind: FailureKind) -> Optional[dict]:
        return RECOVERY_RECIPES.get(failure_kind)

# ========== 任务分析器 ==========
class CronJobAnalyzer:
    """分析 cron 任务状态"""
    
    def __init__(self, jobs_data: dict):
        self.jobs = jobs_data.get("jobs", [])
    
    def analyze(self) -> dict:
        analysis = {
            "total": len(self.jobs),
            "ok": 0,
            "error": 0,
            "idle": 0,
            "jobs": []
        }
        
        classifier = FailureClassifier()
        
        for job in self.jobs:
            state = job.get("state", {})
            last_status = state.get("lastStatus", "unknown")
            
            job_info = {
                "name": job.get("name", "unknown"),
                "enabled": job.get("enabled", True),
                "status": last_status,
                "last_error": state.get("lastError"),
                "consecutive_errors": state.get("consecutiveErrors", 0),
                "failure_kind": None,
                "recovery_recipe": None,
                "recommendation": None
            }
            
            # 分类失败
            if last_status == "error":
                error_msg = state.get("lastError", "")
                if error_msg:
                    failure_kind = classifier.classify(error_msg)
                    job_info["failure_kind"] = failure_kind.value
                    
                    recipe = classifier.get_recipe(failure_kind)
                    if recipe:
                        job_info["recovery_recipe"] = recipe.get("action")
                        job_info["recommendation"] = recipe.get("message", f"尝试: {recipe.get('action')}")
            
            # 统计
            if last_status == "ok":
                analysis["ok"] += 1
            elif last_status == "error":
                analysis["error"] += 1
            else:
                analysis["idle"] += 1
            
            analysis["jobs"].append(job_info)
        
        return analysis

# ========== 输出格式化 ==========
def format_analysis(analysis: dict) -> str:
    """格式化分析结果为 markdown"""
    lines = []
    
    lines.append("# 📊 Cron 任务状态分析")
    lines.append("")
    lines.append(f"**总计**: {analysis['total']} | ✅ 正常: {analysis['ok']} | ❌ 错误: {analysis['error']} | ⏸️ 空闲: {analysis['idle']}")
    lines.append("")
    lines.append("## 任务列表")
    lines.append("")
    
    for job in analysis.get("jobs", []):
        status = job["status"]
        
        if status == "ok":
            icon = "✅"
        elif status == "error":
            icon = "❌"
        else:
            icon = "⏸️"
        
        lines.append(f"### {icon} {job['name']}")
        lines.append(f"- 状态: **{status}**")
        
        if job["enabled"]:
            lines.append(f"- 启用: 是")
        else:
            lines.append(f"- 启用: ❌ 已禁用")
        
        if status == "error":
            if job.get("failure_kind"):
                lines.append(f"- 失败类型: `{job['failure_kind']}`")
            if job.get("consecutive_errors", 0) > 0:
                lines.append(f"- 连续错误: {job['consecutive_errors']}次")
            if job.get("recommendation"):
                lines.append(f"- 💡 建议: {job['recommendation']}")
        
        lines.append("")
    
    return "\n".join(lines)

# ========== 主函数（被工具调用） ==========
def run_analysis(jobs_json: dict) -> str:
    """分析 cron 任务并返回格式化报告"""
    analyzer = CronJobAnalyzer(jobs_json)
    analysis = analyzer.analyze()
    return format_analysis(analysis)

# 如果直接运行
if __name__ == "__main__":
    # 这个脚本通过工具调用，jobs 会作为参数传入
    import json
    import sys
    
    if len(sys.argv) > 1:
        # 从文件读取 JSON
        with open(sys.argv[1]) as f:
            jobs = json.load(f)
    else:
        print("Usage: python claw-operator.py <jobs.json>")
        sys.exit(1)
    
    result = run_analysis(jobs)
    print(result)