#!/usr/bin/env python3
"""
Token Governor v2 - 自适应预算 + 反死亡螺旋门禁
"""
import json
import fcntl
from pathlib import Path
from datetime import datetime, timedelta

BUDGET_FILE = Path.home() / ".openclaw/data/token_budget.json"
KPI_LOG = Path.home() / ".openclaw/workspace/logs/kpi_history.jsonl"

class AdaptiveTokenGovernor:
    def __init__(self):
        self.budget_file = BUDGET_FILE
        self.kpi_log = KPI_LOG
        self.confidence_min_samples = 100  # 最小样本量
        self.deviation_freeze_threshold = 0.5  # 偏差超过50%则冻结
    
    def _load_budget(self):
        with open(self.budget_file, 'r') as f:
            return json.load(f)
    
    def _save_budget(self, data):
        with open(self.budget_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def consume(self, project_id: str, tokens: int, desc: str = ""):
        """消耗Token，超限时返回False并告警"""
        data = self._load_budget()
        proj = data.get(project_id)
        if not proj:
            raise ValueError(f"Unknown project: {project_id}")
        
        limit = proj['limit']
        used = proj['used']
        
        if used + tokens > limit:
            self._log_alert(project_id, used, limit, tokens)
            return False
        
        proj['used'] += tokens
        self._save_budget(data)
        self._log_consumption(project_id, tokens, desc)
        return True
    
    def get_status(self, project_id=None):
        """获取预算状态"""
        data = self._load_budget()
        if project_id:
            return data.get(project_id, {})
        return data
    
    def adjust_budget_weights(self):
        """根据KPI动态调整预算权重（带门禁）"""
        # 读取KPI数据
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        kpis = self._load_kpis(yesterday)
        
        data = self._load_budget()
        
        for proj_id in ['drama', 'tk']:
            kpi = kpis.get(proj_id, {})
            samples = kpi.get('samples', 0)
            value = kpi.get('value', 0)
            
            # 门禁1：样本量不足跳过
            if samples < self.confidence_min_samples:
                print(f"[Governor] {proj_id}: 样本量不足 ({samples})，跳过调权")
                continue
            
            # 门禁2：偏差过大冻结（与前日对比）
            prev = self._get_previous_kpi(proj_id, yesterday)
            if prev and prev > 0:
                deviation = abs(value - prev) / prev
                if deviation > self.deviation_freeze_threshold:
                    print(f"[Governor] {proj_id}: KPI偏差过大 ({deviation:.1%})，冻结调权")
                    continue
            
            # 执行调权逻辑
            if proj_id == 'drama' and value < 0.6:
                old_limit = data[proj_id]['limit']
                data[proj_id]['limit'] = int(old_limit * 0.95)
                print(f"[Governor] {proj_id}: 预算调整 {old_limit} -> {data[proj_id]['limit']}")
        
        self._save_budget(data)
    
    def _load_kpis(self, date_str):
        """从KPI日志读取数据"""
        if not Path(self.kpi_log).exists():
            return {}
        kpis = {}
        with open(self.kpi_log, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('date') == date_str:
                        kpis[entry['project']] = entry
                except:
                    pass
        return kpis
    
    def _get_previous_kpi(self, proj_id, date_str):
        """获取前一天的KPI值"""
        prev_date = (datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        kpis = self._load_kpis(prev_date)
        return kpis.get(proj_id, {}).get('value')
    
    def _log_consumption(self, project_id, tokens, description):
        """记录消耗日志"""
        Path(self.kpi_log).parent.mkdir(parents=True, exist_ok=True)
        with open(self.kpi_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()} | {project_id} | +{tokens} | {description}\n")
    
    def _log_alert(self, project_id, used, limit, requested):
        """记录告警"""
        alert_msg = f"⚠️ 预算超限！项目 {project_id} 已用 {used}/{limit}，本次请求 {requested} tokens 被拒绝"
        print(alert_msg)

if __name__ == '__main__':
    gov = AdaptiveTokenGovernor()
    print("✅ TokenGovernor v2 已就绪（含反死亡螺旋门禁）")
    print("   - 最小样本量:", gov.confidence_min_samples)
    print("   - 偏差冻结阈值:", gov.deviation_freeze_threshold)
    print("   当前状态:", gov.get_status())