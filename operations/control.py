from typing import Dict, Any, List, Optional


class FlowControl:
    def __init__(self):
        self._goto_target: Optional[str] = None

    def find_label_node(self, nodes: List[Dict[str, Any]], target_label: str) -> Optional[str]:
        for node in nodes:
            if node.get("type") == "label" and node.get("config", {}).get("label_name") == target_label:
                return node["id"]
        return None

    def goto(self, config: Dict[str, Any], nodes: List[Dict[str, Any]]):
        target_label = config.get("target_label", "")
        if not target_label:
            return
        self._goto_target = self.find_label_node(nodes, target_label)

    @property
    def goto_target(self) -> Optional[str]:
        return self._goto_target

    def clear_goto(self):
        self._goto_target = None