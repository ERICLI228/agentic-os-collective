#!/usr/bin/env python3
"""
水浒传AI数字短剧 - 确认机制系统
基于 auto-coding-agent-demo 的三阶段确认机制

确认阶段:
- script_confirmed: 剧本确认
- roles_confirmed: 角色设计确认  
- video_confirmed: 视频确认
"""

import os
import json
import datetime
from pathlib import Path

# 默认配置
CONFIG_FILE = os.path.expanduser("~/.openclaw/skills/water-margin-drama/confirmation_state.json")

# 确认状态
class ConfirmationState:
    def __init__(self):
        self.state = {
            "project_name": None,
            "created_at": None,
            "updated_at": None,
            "stages": {
                "script": {
                    "confirmed": False,
                    "confirmed_at": None,
                    "confirmed_by": None,
                    "notes": None
                },
                "roles": {
                    "confirmed": False,
                    "confirmed_at": None,
                    "confirmed_by": None,
                    "notes": None
                },
                "video": {
                    "confirmed": False,
                    "confirmed_at": None,
                    "confirmed_by": None,
                    "notes": None
                }
            },
            "current_stage": "script",  # script → roles → video → completed
            "progress": []
        }
    
    def load(self):
        """从文件加载状态"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
        return self
    
    def save(self):
        """保存状态到文件"""
        self.state["updated_at"] = datetime.datetime.now().isoformat()
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def start_project(self, project_name: str):
        """开始新项目"""
        self.state["project_name"] = project_name
        self.state["created_at"] = datetime.datetime.now().isoformat()
        self.state["current_stage"] = "script"
        
        # 重置所有确认状态
        for stage in self.state["stages"].values():
            stage["confirmed"] = False
            stage["confirmed_at"] = None
            stage["confirmed_by"] = None
            stage["notes"] = None
        
        self.add_progress(f"项目 '{project_name}' 已创建")
        self.save()
    
    def confirm_stage(self, stage: str, confirmed_by: str = "human", notes: str = None):
        """确认某个阶段"""
        if stage not in self.state["stages"]:
            raise ValueError(f"未知阶段: {stage}")
        
        self.state["stages"][stage]["confirmed"] = True
        self.state["stages"][stage]["confirmed_at"] = datetime.datetime.now().isoformat()
        self.state["stages"][stage]["confirmed_by"] = confirmed_by
        self.state["stages"][stage]["notes"] = notes
        
        # 更新当前阶段
        stage_order = ["script", "roles", "video"]
        current_idx = stage_order.index(stage)
        if current_idx < len(stage_order) - 1:
            self.state["current_stage"] = stage_order[current_idx + 1]
        
        self.add_progress(f"阶段 '{stage}' 已确认 by {confirmed_by}")
        self.save()
    
    def unconfirm_stage(self, stage: str):
        """取消确认某个阶段"""
        if stage not in self.state["stages"]:
            raise ValueError(f"未知阶段: {stage}")
        
        self.state["stages"][stage]["confirmed"] = False
        self.state["stages"][stage]["confirmed_at"] = None
        self.state["stages"][stage]["confirmed_by"] = None
        
        # 重置后续阶段
        stage_order = ["script", "roles", "video"]
        current_idx = stage_order.index(stage)
        for later_stage in stage_order[current_idx + 1:]:
            self.state["stages"][later_stage]["confirmed"] = False
        
        self.add_progress(f"阶段 '{stage}' 已取消确认")
        self.save()
    
    def get_current_stage(self) -> str:
        """获取当前阶段"""
        return self.state["current_stage"]
    
    def is_stage_confirmed(self, stage: str) -> bool:
        """检查阶段是否已确认"""
        return self.state["stages"].get(stage, {}).get("confirmed", False)
    
    def can_proceed_to(self, target_stage: str) -> tuple:
        """
        检查是否可以进入目标阶段
        返回: (can_proceed: bool, reason: str)
        """
        stage_order = ["script", "roles", "video"]
        
        if target_stage not in stage_order:
            return False, f"未知阶段: {target_stage}"
        
        target_idx = stage_order.index(target_stage)
        
        # 检查所有前置阶段是否已确认
        for i in range(target_idx):
            prev_stage = stage_order[i]
            if not self.is_stage_confirmed(prev_stage):
                return False, f"前置阶段 '{prev_stage}' 尚未确认"
        
        return True, "可以进入"
    
    def add_progress(self, message: str):
        """添加进度记录"""
        self.state["progress"].append({
            "time": datetime.datetime.now().isoformat(),
            "message": message
        })
    
    def get_status(self) -> dict:
        """获取状态摘要"""
        return {
            "project": self.state.get("project_name"),
            "current_stage": self.state["current_stage"],
            "script_confirmed": self.is_stage_confirmed("script"),
            "roles_confirmed": self.is_stage_confirmed("roles"),
            "video_confirmed": self.is_stage_confirmed("video"),
            "progress_count": len(self.state["progress"])
        }
    
    def print_status(self):
        """打印状态"""
        status = self.get_status()
        
        print("\n" + "=" * 50)
        print(f"📊 项目状态: {status['project'] or '未开始'}")
        print("=" * 50)
        
        stage_order = ["script", "roles", "video"]
        stage_names = {"script": "剧本", "roles": "角色", "video": "视频"}
        stage_emojis = {"script": "📝", "roles": "🎭", "video": "🎬"}
        
        current_idx = stage_order.index(status["current_stage"]) if status["current_stage"] in stage_order else 0
        
        for i, stage in enumerate(stage_order):
            emoji = stage_emojis[stage]
            name = stage_names[stage]
            confirmed = self.is_stage_confirmed(stage)
            
            if i < current_idx:
                status_str = "✅ 已完成" if confirmed else "⏳ 待确认"
            elif i == current_idx:
                status_str = "🔄 当前阶段"
            else:
                status_str = "🔒 锁定"
            
            print(f"  {emoji} {name}: {status_str}")
        
        print("=" * 50)
        print(f"📈 进度记录: {status['progress_count']} 条")
        
        # 打印最近3条进度
        if self.state["progress"]:
            print("\n最近进度:")
            for p in self.state["progress"][-3:]:
                print(f"  - {p['message']}")


def confirm_command(args):
    """确认命令处理"""
    state = ConfirmationState().load()
    
    if len(args) < 1:
        state.print_status()
        return
    
    action = args[0]
    
    if action == "start":
        if len(args) < 2:
            print("用法: confirm start <项目名>")
            return
        state.start_project(args[1])
        print(f"✅ 项目 '{args[1]}' 已创建")
        state.print_status()
    
    elif action == "script":
        state.confirm_stage("script", notes=" ".join(args[1:]) if len(args) > 1 else None)
        print("✅ 剧本已确认")
        state.print_status()
    
    elif action == "roles":
        state.confirm_stage("roles", notes=" ".join(args[1:]) if len(args) > 1 else None)
        print("✅ 角色设计已确认")
        state.print_status()
    
    elif action == "video":
        state.confirm_stage("video", notes=" ".join(args[1:]) if len(args) > 1 else None)
        print("✅ 视频已确认")
        state.print_status()
    
    elif action == "unconfirm":
        if len(args) < 2:
            print("用法: confirm unconfirm <script|roles|video>")
            return
        stage = args[1]
        if stage in ["script", "roles", "video"]:
            state.unconfirm_stage(stage)
            print(f"⚠️ {stage} 已取消确认")
            state.print_status()
        else:
            print(f"未知阶段: {stage}")
    
    elif action == "check":
        if len(args) < 2:
            print("用法: confirm check <stage>")
            return
        stage = args[1]
        can_proceed, reason = state.can_proceed_to(stage)
        if can_proceed:
            print(f"✅ 可以进入 {stage} 阶段")
        else:
            print(f"❌ 无法进入 {stage} 阶段: {reason}")
    
    else:
        print(f"未知命令: {action}")
        print("用法: confirm <start|script|roles|video|unconfirm|check>")


def main():
    import sys
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    confirm_command(args)


if __name__ == "__main__":
    main()