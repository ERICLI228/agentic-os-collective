#!/usr/bin/env python3
"""
执行详情记录器 v3.0 - 生产环境版本
支持日志轮转、命令安全验证、错误处理
"""
import json
import fcntl
import subprocess
import logging
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORKSPACE = Path.home() / "agentic-os-collective"
EXEC_LOGS_DIR = WORKSPACE / "shared/logs/executions"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_ROTATION_DAYS = 30
ALLOWED_COMMAND_PREFIXES = [
    'python3 ~/.openclaw/skills/',
    'python3 ~/.agents/skills/',
    'bash ~/.agents/skills/',
    'python3 ~/agentic-os-collective/',
    # 注: 'echo ' 已从白名单移除，防止 shell 注入
]

# 危险命令黑名单
BLOCKED_COMMANDS = [
    'rm -rf /', 'mkfs', 'dd if=', '> /dev/sd', 
    'curl | sh', 'wget | sh', 'chmod 777', 
    'chown -R', ':(){:|:&};:'
]

def init_dirs():
    """初始化目录结构"""
    EXEC_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    (EXEC_LOGS_DIR / "rotated").mkdir(exist_ok=True)

def rotate_log_if_needed(log_path: Path):
    """日志文件过大时轮转"""
    if not log_path.exists() or log_path.stat().st_size < LOG_MAX_SIZE:
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rotated = EXEC_LOGS_DIR / "rotated" / f"{log_path.stem}_{timestamp}.log"
    log_path.rename(rotated)
    logger.info(f"Log rotated: {rotated}")
    
    # 清理旧日志
    cleanup_old_logs()

def cleanup_old_logs():
    """清理旧日志文件"""
    cutoff = datetime.now() - timedelta(days=LOG_ROTATION_DAYS)
    rotated_dir = EXEC_LOGS_DIR / "rotated"
    
    if not rotated_dir.exists():
        return
    
    for old in rotated_dir.glob("*.log"):
        try:
            mtime = datetime.fromtimestamp(old.stat().st_mtime)
            if mtime < cutoff:
                old.unlink()
                logger.info(f"Deleted old log: {old}")
        except Exception as e:
            logger.warning(f"Failed to delete {old}: {e}")

def validate_command(command: str) -> tuple[bool, str]:
    """命令安全验证 — 已委托 base_executor (shell=False + shlex + 危险字符)"""
    from shared.core.base_executor import validate_command as safe_validate
    return safe_validate(command)

def log_execution(project: str, task_id: str, milestone_id: str, 
                  command: str, stdout: str, stderr: str, duration: float,
                  artifacts: list = None, executor: str = "OpenClaw"):
    """记录执行详情（生产环境安全版本）"""
    init_dirs()
    rotate_log_if_needed(EXEC_LOGS_DIR / f"{task_id}_{milestone_id}.log")
    
    timestamp = datetime.now().isoformat()
    log_file = EXEC_LOGS_DIR / f"{project}_{task_id}_{milestone_id}.log"
    
    log_content = f"""# 执行日志
# 项目: {project}
# 任务: {task_id}
# 里程碑: {milestone_id}
# 执行器: {executor}
# 开始时间: {timestamp}
# 命令: {command[:500]}
{'='*60}
STDOUT:
{stdout[:5000]}
{'='*60}
STDERR:
{stderr[:2000] if stderr else '(无)'}
# 执行耗时: {duration:.2f}s
"""
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    # 更新任务 JSON
    task_file = Path.home() / ".openclaw/workspace/tasks/active" / f"{task_id}.json"
    if task_file.exists():
        with open(task_file, 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                task = json.load(f)
                for m in task.get('milestones', []):
                    if m.get('id') == milestone_id:
                        m['execution_details'] = {
                            'command': command,
                            'duration': round(duration, 2),
                            'log_file': str(log_file.relative_to(WORKSPACE)),
                            'stdout_preview': stdout[:1000],
                            'stderr_preview': stderr[:500] if stderr else None,
                            'artifacts': artifacts or [],
                            'executed_at': timestamp,
                            'executor': executor
                        }
                        break
                f.seek(0)
                json.dump(task, f, ensure_ascii=False, indent=2)
                f.truncate()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    
    return str(log_file)

def run_and_log(project: str, task_id: str, milestone_id: str,
                command: str, timeout: int = 3600, executor: str = "OpenClaw"):
    """执行命令并自动记录 — 委托 base_executor (shell=False)"""
    init_dirs()

    from shared.core.base_executor import run_command as safe_run

    start = datetime.now()
    result = safe_run(command, timeout=timeout, cwd=WORKSPACE)

    if result["status"] == "error":
        duration = (datetime.now() - start).total_seconds()
        log_execution(project, task_id, milestone_id, command,
                      "", result.get("error", ""), duration, executor=executor)
        return {"status": "error", "error": result.get("error", ""), "duration": duration}

    duration = result.get("duration", (datetime.now() - start).total_seconds())
    log_execution(project, task_id, milestone_id, command,
                  result.get("stdout", ""), result.get("stderr", ""),
                  duration, executor=executor)

    return {
        "status": result["status"],
        "return_code": result.get("return_code", -1),
        "duration": duration,
        "stdout": result.get("stdout", "")[:5000],
        "stderr": result.get("stderr", "")[:2000],
    }

# ========== 第九阶段：全透明流水线功能 ==========

def update_milestone_content(task_id: str, milestone_id: str, 
                            output_type: str, output_title: str,
                            output_content: str, output_suggestions: list = None,
                            decision_required: bool = False,
                            decision_options: list = None,
                            decision_deadline: str = None,
                            artifacts: list = None) -> bool:
    """
    更新里程碑产出内容 - 第九阶段核心功能
    记录中间产出物、创建决策点
    """
    ACTIVE_DIR = Path.home() / ".openclaw/workspace/tasks/active"
    task_file = ACTIVE_DIR / f"{task_id}.json"
    
    if not task_file.exists():
        logger.error(f"任务文件不存在: {task_file}")
        return False
    
    with open(task_file, 'r+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            task = json.load(f)
            
            for m in task.get('milestones', []):
                if m.get('id') == milestone_id:
                    # 初始化 execution_details
                    m.setdefault('execution_details', {})
                    
                    # 更新 output_content - 统一数据结构
                    m['execution_details']['output_content'] = {
                        'type': output_type,
                        'title': output_title,
                        'data': output_content,  # 统一为 data 字段
                        'artifacts': artifacts or [],
                        'generated_at': datetime.now().isoformat()
                    }
                    
                    # 决策点配置
                    if decision_required:
                        m['decision_point'] = True
                        m['decision_required'] = True
                        if decision_options:
                            m['decision_options'] = decision_options
                        if decision_deadline:
                            m['decision_deadline'] = decision_deadline
                        # 初始化决策历史
                        m.setdefault('decision_history', [{
                            'decision_type': 'pending',
                            'decision_at': None,
                            'decision_value': None,
                            'decision_by': None,
                            'comment': None
                        }])
                    
                    break
            
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
            logger.info(f"已更新里程碑 {milestone_id} 产出内容")
            return True
        
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def handle_decision(task_id: str, milestone_id: str, 
                    decision_type: str, comment: str = "") -> bool:
    """
    处理决策 - 通过/修改/驳回
    """
    ACTIVE_DIR = Path.home() / ".openclaw/workspace/tasks/active"
    task_file = ACTIVE_DIR / f"{task_id}.json"
    
    if not task_file.exists():
        return False
    
    with open(task_file, 'r+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            task = json.load(f)
            
            for m in task.get('milestones', []):
                if m.get('id') == milestone_id:
                    # 记录决策
                    decision_entry = {
                        'decision_type': decision_type,
                        'decision_at': datetime.now().isoformat(),
                        'decision_value': decision_type,
                        'decision_by': 'human',
                        'comment': comment
                    }
                    
                    m.setdefault('decision_history', []).append(decision_entry)
                    
                    # 更新状态
                    if decision_type == 'approve':
                        m['status'] = 'completed'
                        m['decision_status'] = 'approved'
                    elif decision_type == 'modify':
                        m['status'] = 'pending'
                        m['decision_status'] = 'modifying'
                    elif decision_type == 'reject':
                        m['status'] = 'rejected'
                        m['decision_status'] = 'rejected'
                    
                    m['decision_completed_at'] = datetime.now().isoformat()
                    break
            
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
            logger.info(f"决策已记录: {task_id}/{milestone_id} -> {decision_type}")
            return True
        
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


if __name__ == "__main__":
    # CLI 测试
    import sys
    if len(sys.argv) > 3:
        result = run_and_log(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, ensure_ascii=False, indent=2))