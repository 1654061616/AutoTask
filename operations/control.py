"""
流程控制模块 — 实现 goto 跳转逻辑
"""
from typing import Dict, Any, List, Optional


class FlowControl:
    """流程控制器，管理 goto 跳转目标"""

    def __init__(self):
        self._goto_target: Optional[str] = None

    def find_label_node(self, nodes: List[Dict[str, Any]], target_label: str) -> Optional[str]:
        """查找匹配标签的节点 ID"""
        for node in nodes:
            if node.get("type") == "label" and node.get("config", {}).get("label_name") == target_label:
                return node["id"]
        return None

    def goto(self, config: Dict[str, Any], nodes: List[Dict[str, Any]]):
        """设置跳转目标"""
        target_label = config.get("target_label", "")
        if not target_label:
            return
        self._goto_target = self.find_label_node(nodes, target_label)

    @property
    def goto_target(self) -> Optional[str]:
        """获取跳转目标节点 ID"""
        return self._goto_target

    def clear_goto(self):
        """清除跳转目标"""
        self._goto_target = None