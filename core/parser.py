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
        flow["variables"] = flow.get("variables", {})
        flow["global_config"] = flow.get("global_config", {})
        return flow

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