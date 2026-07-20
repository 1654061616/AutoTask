"""
条件判断模块 — 支持值比较、图片/窗口存在性判断等条件运算
"""
from typing import Any, Callable, Dict


class ConditionEvaluator:
    """条件求值器，支持从配置驱动和程序化调用两种方式"""

    def __init__(self):
        self._image = None
        self._window = None

    def set_image_ops(self, image_ops):
        """注入图像识别模块"""
        self._image = image_ops

    def set_window_ops(self, window_ops):
        """注入窗口操作模块"""
        self._window = window_ops

    def evaluate_from_config(self, config: Dict[str, Any], variable_manager) -> bool:
        """从流程配置中解析条件并求值"""
        condition_type = config.get("condition_type", "value_compare")

        if condition_type == "value_compare":
            var_name = config.get("var_name", "")
            compare_op = config.get("compare_op", "==")
            compare_value = config.get("compare_value", "")
            var_value = variable_manager.get_variable(var_name)
            return self._compare_values(var_value, compare_op, compare_value)

        elif condition_type == "image_exists":
            image_path = variable_manager.resolve_expression(config.get("image_path", ""))
            similarity = config.get("similarity", 0.9)
            if self._image:
                return self._image.image_exists(image_path, threshold=similarity)
            return False

        elif condition_type == "text_exists":
            return False

        elif condition_type == "window_exists":
            window_title = variable_manager.resolve_expression(config.get("window_title", ""))
            if self._window:
                return self._window.find_window(window_title) is not None
            return False

        return False

    @staticmethod
    def _compare_values(var_value, compare_op, compare_value):
        """比较两个值，优先数值比较，失败则字符串比较"""
        try:
            num_var = float(var_value)
            num_cmp = float(compare_value)
            if compare_op == "==":
                return num_var == num_cmp
            elif compare_op == "!=":
                return num_var != num_cmp
            elif compare_op == ">":
                return num_var > num_cmp
            elif compare_op == "<":
                return num_var < num_cmp
            elif compare_op == ">=":
                return num_var >= num_cmp
            elif compare_op == "<=":
                return num_var <= num_cmp
        except (ValueError, TypeError):
            var_str = str(var_value) if var_value is not None else ""
            cmp_str = str(compare_value)
            if compare_op == "==":
                return var_str == cmp_str
            elif compare_op == "!=":
                return var_str != cmp_str
        return False

    def evaluate(self, condition_type: str, left: Any, right: Any, operator: str = "==") -> bool:
        """程序化条件求值入口"""
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
        """值比较：支持 ==, !=, >, <, >=, <=, contains, not_contains"""
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
        """判断图片是否存在"""
        from operations.image_recognition import ImageRecognition
        ir = ImageRecognition()
        return ir.image_exists(template_path, region)

    def _evaluate_text_exists(self, image_path: str, text: str) -> bool:
        """判断文本是否存在"""
        from operations.ocr import OCROperations
        ocr = OCROperations()
        return ocr.text_exists(image_path, text)

    def _evaluate_window_exists(self, window_title: str) -> bool:
        """判断窗口是否存在"""
        from operations.window import WindowOperations
        wo = WindowOperations()
        return wo.find_window(window_title) is not None

    def _evaluate_custom(self, func: Callable, args: Any) -> bool:
        """执行自定义条件函数"""
        try:
            return func(*args)
        except Exception:
            return False

    def if_else(self, condition: bool, true_step: Any, false_step: Any = None) -> Any:
        """三元条件选择"""
        return true_step if condition else false_step