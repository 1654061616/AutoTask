from typing import Dict, Any, List, Optional


class FlowControl:
    def __init__(self):
        self._goto_target: Optional[int] = None

    def find_label_index(self, steps: List[Dict[str, Any]], target_label: str) -> int:
        for i, step in enumerate(steps):
            if step.get("type") == "label" and step.get("config", {}).get("label_name") == target_label:
                return i
        return -1

    def goto(self, config: Dict[str, Any], steps: List[Dict[str, Any]]):
        target_label = config.get("target_label", "")
        if not target_label:
            return
        index = self.find_label_index(steps, target_label)
        if index >= 0:
            self._goto_target = index
        else:
            self._goto_target = None

    @property
    def goto_target(self) -> Optional[int]:
        return self._goto_target

    def clear_goto(self):
        self._goto_target = None