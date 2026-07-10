from typing import Any, Callable

class ConditionEvaluator:
    def __init__(self):
        pass
    
    def evaluate(self, condition_type: str, left: Any, right: Any, operator: str = "==") -> bool:
        if condition_type == "value":
            return self._evaluate_value(left, right, operator)
        elif condition_type == "image_exists":
            return self._evaluate_image_exists(left, right)
        elif condition_type == "text_exists":
            return self._evaluate_text_exists(left, right)
        elif condition_type == "window_exists":
            return self._evaluate_window_exists(left)
        elif condition_type == "custom":
            return self._evaluate_custom(left, right)
        return False
    
    def _evaluate_value(self, left: Any, right: Any, operator: str) -> bool:
        try:
            if operator == "==":
                return left == right
            elif operator == "!=":
                return left != right
            elif operator == ">":
                return float(left) > float(right)
            elif operator == "<":
                return float(left) < float(right)
            elif operator == ">=":
                return float(left) >= float(right)
            elif operator == "<=":
                return float(left) <= float(right)
            elif operator == "contains":
                return str(right) in str(left)
            elif operator == "not_contains":
                return str(right) not in str(left)
        except Exception:
            return False
        return False
    
    def _evaluate_image_exists(self, template_path: str, region: Any) -> bool:
        from operations.image_recognition import ImageRecognition
        ir = ImageRecognition()
        return ir.image_exists(template_path, region)
    
    def _evaluate_text_exists(self, image_path: str, text: str) -> bool:
        from operations.ocr import OCROperations
        ocr = OCROperations()
        return ocr.text_exists(image_path, text)
    
    def _evaluate_window_exists(self, window_title: str) -> bool:
        from operations.window import WindowOperations
        wo = WindowOperations()
        return wo.find_window(window_title) is not None
    
    def _evaluate_custom(self, func: Callable, args: Any) -> bool:
        try:
            return func(*args)
        except Exception:
            return False
    
    def if_else(self, condition: bool, true_step: Any, false_step: Any = None) -> Any:
        return true_step if condition else false_step