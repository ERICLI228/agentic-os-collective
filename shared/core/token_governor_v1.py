#!/usr/bin/env python3
"""
Token Governor v1 - 静态预算追踪（无自适应）
功能：记录各项目 Token 消耗，超限时告警
"""
import json
import os
import fcntl
from pathlib import Path
from datetime import datetime

BUDGET_FILE = Path.home() / ".openclaw/data/token_budget.json"
AUDIT_LOG = Path.home() / ".openclaw/workspace/logs/token_audit.log"

class TokenGovernorV1:
    def __init__(self):
        self.budget_file = BUDGET_FILE
        self._ensure_file()
    
    def _ensure_file(self):
        if not self.budget_file.exists():
            self.budget_file.parent.mkdir(parents=True, exist_ok=True)
            default = {"drama": {"limit": 400000, "used": 0}, "tk": {"limit": 600000, "used": 0}}
            with open(self.budget_file, 'w') as f:
                json.dump(default, f, indent=2)
    
    def _load_budget(self):
        with open(self.budget_file, 'r') as f:
            data = json.load(f)
        return data
    
    def _save_budget(self, data):
        with open(self.budget_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def consume(self, project_id: str, tokens: int, description: str = "") -> bool:
        """消耗 Token，超限时返回 False 并告警"""
        data = self._load_budget()
        proj = data.get(project_id)
        if not proj:
            raise ValueError(f"Unknown project: {project_id}")
        
        limit = proj["limit"]
        used = proj["used"]
        if used + tokens > limit:
            # 超限告警
            self._log_alert(project_id, used, limit, tokens)
            self._save_budget(data)
            return False
        
        proj["used"] += tokens
        self._save_budget(data)
        self._log_consumption(project_id, tokens, description)
        return True
    
    def get_status(self, project_id: str = None):
        """获取预算状态"""
        with open(self.budget_file, 'r') as f:
            data = json.load(f)
        if project_id:
            return data.get(project_id, {})
        return data
    
    def _log_consumption(self, project_id, tokens, description):
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(AUDIT_LOG, 'a') as f:
            f.write(f"{datetime.now().isoformat()} | {project_id} | +{tokens} | {description}\n")
    
    def _log_alert(self, project_id, used, limit, requested):
        alert_msg = f"⚠️ 预算超限！项目 {project_id} 已用 {used}/{limit}，本次请求 {requested} tokens 被拒绝"
        print(alert_msg)
        with open(AUDIT_LOG, 'a') as f:
            f.write(f"{datetime.now().isoformat()} | ALERT | {alert_msg}\n")

# 单例
governor = TokenGovernorV1()

if __name__ == "__main__":
    # 测试消耗
    print("drama status:", governor.get_status("drama"))
    success = governor.consume("drama", 5000, "测试剧本生成")
    print("Consume success:", success)
    print("drama status:", governor.get_status("drama"))