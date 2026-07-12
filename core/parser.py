import json
import os
from typing import Dict, Any, List, Optional

class FlowParser:
    def __init__(self):
        self.required_fields = ["id", "type", "name", "config"]
        self.valid_step_types = [
            "mouse_click", "mouse_move", "mouse_drag", "mouse_scroll",
            "keyboard_type", "keyboard_press", "keyboard_hotkey",
            "wait", "image_find", "image_click", "image_exists",
            "ocr_find", "ocr_read",
            "if_else", "loop",
            "set_variable", "get_variable",
            "excel_read",
            "screenshot", "log",
            "window_find", "window_activate", "window_close"
        ]
    
    def parse(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        flow = flow_data.copy()
        
        # 如果有nodes和edges（节点图格式），转换为steps格式
        if "nodes" in flow and "edges" in flow:
            flow["steps"] = self._convert_nodes_to_steps(flow["nodes"], flow["edges"])
        else:
            flow["steps"] = self._parse_steps(flow.get("steps", []))
        
        flow["variables"] = flow.get("variables", {})
        flow["global_config"] = flow.get("global_config", {})
        return flow
    
    def _convert_nodes_to_steps(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        将节点图格式转换为步骤列表格式
        
        参数:
            nodes: 节点列表
            edges: 连线列表
        
        返回:
            steps: 步骤列表，按照执行顺序排列
        """
        # 创建节点映射（节点ID -> 节点数据）
        node_map = {node["id"]: node for node in nodes}
        
        # 找到开始节点
        start_node = None
        for node_id, node in node_map.items():
            if node.get("type") == "start":
                start_node = node_id
                break
        
        if not start_node:
            return []
        
        # 构建步骤列表（按照连线顺序）
        steps = []
        current_node_id = start_node
        
        while current_node_id:
            node = node_map.get(current_node_id)
            if not node:
                break
            
            node_type = node.get("type")
            
            # 跳过start和end节点，只添加实际操作节点
            if node_type not in ["start", "end"]:
                step = {
                    "id": node["id"],
                    "type": node_type,
                    "name": self._get_step_name(node_type),
                    "config": node.get("config", {}),
                    "next_step": None
                }
                steps.append(step)
            
            # 查找下一个节点
            next_node_id = None
            for edge in edges:
                if edge["source_node"] == current_node_id:
                    next_node_id = edge["target_node"]
                    break
            
            # 设置前一个步骤的next_step
            if len(steps) > 0:
                steps[-1]["next_step"] = next_node_id if next_node_id and node_map.get(next_node_id, {}).get("type") != "end" else None
            
            current_node_id = next_node_id
        
        return steps
    
    def _get_step_name(self, step_type: str) -> str:
        """获取步骤类型的中文名称"""
        name_map = {
            "mouse_click": "鼠标点击",
            "mouse_move": "鼠标移动",
            "mouse_drag": "鼠标拖拽",
            "mouse_scroll": "鼠标滚动",
            "keyboard_type": "键盘输入",
            "keyboard_press": "按键按下",
            "keyboard_hotkey": "快捷键",
            "wait": "等待",
            "image_find": "查找图片",
            "image_click": "点击图片",
            "image_exists": "图片存在判断",
            "ocr_find": "OCR查找",
            "ocr_read": "OCR读取",
            "if_else": "条件分支",
            "loop": "循环",
            "set_variable": "设置变量",
            "get_variable": "获取变量",
            "excel_read": "读取Excel",
            "screenshot": "截图",
            "log": "日志",
            "window_find": "查找窗口",
            "window_activate": "激活窗口",
            "window_close": "关闭窗口"
        }
        return name_map.get(step_type, step_type)
    
    def _parse_steps(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_steps = []
        for step in steps:
            if self.validate_step(step):
                parsed_steps.append(step)
        return parsed_steps
    
    def validate_step(self, step: Dict[str, Any]) -> bool:
        for field in self.required_fields:
            if field not in step:
                return False
        if step["type"] not in self.valid_step_types:
            return False
        if not isinstance(step["config"], dict):
            return False
        return True
    
    def load_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.parse(data)
        except Exception as e:
            return None
    
    def save_to_file(self, flow: Dict[str, Any], file_path: str) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(flow, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            return False
    
    def get_step_by_id(self, flow: Dict[str, Any], step_id: str) -> Optional[Dict[str, Any]]:
        for step in flow.get("steps", []):
            if step["id"] == step_id:
                return step
        return None