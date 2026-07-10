import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from .parser import FlowParser

class FlowManager:
    def __init__(self):
        self.parser = FlowParser()
        self.flows: Dict[str, Any] = {}
        self.current_flow_id = None
    
    def create_flow(self, name: str) -> Dict[str, Any]:
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
        flow = self.parser.load_from_file(file_path)
        if flow:
            flow_id = flow.get("id", f"flow_{int(datetime.now().timestamp())}")
            flow["id"] = flow_id
            self.flows[flow_id] = flow
            self.current_flow_id = flow_id
        return flow
    
    def save_flow(self, flow_id: str, file_path: str) -> bool:
        if flow_id not in self.flows:
            return False
        flow = self.flows[flow_id]
        flow["updated_at"] = datetime.now().isoformat()
        return self.parser.save_to_file(flow, file_path)
    
    def get_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        return self.flows.get(flow_id)
    
    def get_current_flow(self) -> Optional[Dict[str, Any]]:
        if self.current_flow_id:
            return self.flows.get(self.current_flow_id)
        return None
    
    def set_current_flow(self, flow_id: str):
        if flow_id in self.flows:
            self.current_flow_id = flow_id
    
    def add_step(self, flow_id: str, step: Dict[str, Any]):
        if flow_id in self.flows:
            self.flows[flow_id]["steps"].append(step)
            self.flows[flow_id]["updated_at"] = datetime.now().isoformat()
    
    def remove_step(self, flow_id: str, step_id: str):
        if flow_id in self.flows:
            self.flows[flow_id]["steps"] = [
                s for s in self.flows[flow_id]["steps"] if s["id"] != step_id
            ]
            self.flows[flow_id]["updated_at"] = datetime.now().isoformat()
    
    def update_step(self, flow_id: str, step_id: str, updates: Dict[str, Any]):
        if flow_id in self.flows:
            for step in self.flows[flow_id]["steps"]:
                if step["id"] == step_id:
                    step.update(updates)
                    break
            self.flows[flow_id]["updated_at"] = datetime.now().isoformat()
    
    def reorder_steps(self, flow_id: str, steps: List[Dict[str, Any]]):
        if flow_id in self.flows:
            self.flows[flow_id]["steps"] = steps
            self.flows[flow_id]["updated_at"] = datetime.now().isoformat()
    
    def set_variable(self, flow_id: str, name: str, value: Any):
        if flow_id in self.flows:
            self.flows[flow_id]["variables"][name] = value
    
    def get_variable(self, flow_id: str, name: str) -> Any:
        if flow_id in self.flows:
            return self.flows[flow_id]["variables"].get(name)
        return None
    
    def get_all_flows(self) -> List[Dict[str, Any]]:
        return list(self.flows.values())
    
    def delete_flow(self, flow_id: str):
        if flow_id in self.flows:
            del self.flows[flow_id]
            if self.current_flow_id == flow_id:
                self.current_flow_id = None