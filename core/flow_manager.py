"""
流程管理器 — 负责流程的创建、加载、保存、删除和步骤管理
"""
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from .parser import FlowParser

class FlowManager:
    """流程管理器，维护流程的 CRUD 操作与步骤增删改查"""

    def __init__(self):
        self.parser = FlowParser()                  # JSON 流程解析器
        self.flows: Dict[str, Any] = {}             # 流程字典 {flow_id: flow_data}
        self.current_flow_id = None                 # 当前选中流程 ID

    def create_flow(self, name: str) -> Dict[str, Any]:
        """创建新流程并返回流程数据"""
        flow_id = f"flow_{int(datetime.now().timestamp())}"
        flow = {
            "id": flow_id,
            "name": name,
            "version": "1.0",
            "description": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "steps": [],
            "variables": {},
            "global_config": {
                "loop_limit": 100,
                "timeout": 300,
                "screenshot_on_error": True,
                "log_level": "info"
            }
        }
        self.flows[flow_id] = flow
        self.current_flow_id = flow_id
        return flow
    
    def load_flow(self, file_path: str) -> Optional[Dict[str, Any]]:
        """从文件加载流程"""
        flow = self.parser.load_from_file(file_path)
        if flow:
            flow_id = flow.get("id", f"flow_{int(datetime.now().timestamp())}")
            flow["id"] = flow_id
            self.flows[flow_id] = flow
            self.current_flow_id = flow_id
        return flow
    
    def save_flow(self, flow_id: str, file_path: str) -> bool:
        """保存流程到文件"""
        if flow_id not in self.flows:
            return False
        flow = self.flows[flow_id]
        flow["updated_at"] = datetime.now().isoformat()
        return self.parser.save_to_file(flow, file_path)

    def get_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取流程"""
        return self.flows.get(flow_id)

    def get_current_flow(self) -> Optional[Dict[str, Any]]:
        """获取当前选中流程"""
        if self.current_flow_id:
            return self.flows.get(self.current_flow_id)
        return None

    def set_current_flow(self, flow_id: str):
        """设置当前选中流程"""
        if flow_id in self.flows:
            self.current_flow_id = flow_id

    def add_step(self, flow_id: str, step: Dict[str, Any]):
        """向流程添加步骤"""
        if flow_id in self.flows:
            self.flows[flow_id]["steps"].append(step)
            self.flows[flow_id]["updated_at"] = datetime.now().isoformat()

    def remove_step(self, flow_id: str, step_id: str):
        """从流程中移除指定步骤"""
        if flow_id in self.flows:
            self.flows[flow_id]["steps"] = [
                s for s in self.flows[flow_id]["steps"] if s["id"] != step_id
            ]
            self.flows[flow_id]["updated_at"] = datetime.now().isoformat()

    def update_step(self, flow_id: str, step_id: str, updates: Dict[str, Any]):
        """更新流程中的指定步骤"""
        if flow_id in self.flows:
            for step in self.flows[flow_id]["steps"]:
                if step["id"] == step_id:
                    step.update(updates)
                    break
            self.flows[flow_id]["updated_at"] = datetime.now().isoformat()

    def reorder_steps(self, flow_id: str, steps: List[Dict[str, Any]]):
        """重新排序流程中的步骤列表"""
        if flow_id in self.flows:
            self.flows[flow_id]["steps"] = steps
            self.flows[flow_id]["updated_at"] = datetime.now().isoformat()

    def set_variable(self, flow_id: str, name: str, value: Any):
        """设置流程变量"""
        if flow_id in self.flows:
            self.flows[flow_id]["variables"][name] = value

    def get_variable(self, flow_id: str, name: str) -> Any:
        """获取流程变量"""
        if flow_id in self.flows:
            return self.flows[flow_id]["variables"].get(name)
        return None

    def get_all_flows(self) -> List[Dict[str, Any]]:
        """获取所有流程列表"""
        return list(self.flows.values())

    def delete_flow(self, flow_id: str):
        """删除指定流程"""
        if flow_id in self.flows:
            del self.flows[flow_id]
            if self.current_flow_id == flow_id:
                self.current_flow_id = None