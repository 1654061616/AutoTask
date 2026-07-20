"""
循环控制模块 — 支持计数/条件/遍历三种循环方式
"""
from typing import Dict, Any


class LoopController:
    """循环控制器，管理循环状态并判断是否继续迭代"""

    def __init__(self):
        self._loop_states: Dict[str, Dict[str, Any]] = {}

    def evaluate(self, config: Dict[str, Any], step_id: str, variable_manager) -> bool:
        """根据循环类型判断是否继续执行下一轮"""
        loop_type = config.get("loop_type", "count")

        if step_id not in self._loop_states:
            self._loop_states[step_id] = {"iteration": 0}
        state = self._loop_states[step_id]

        if loop_type == "count":
            return self._evaluate_count(config, state, variable_manager, step_id)
        elif loop_type == "condition":
            return self._evaluate_condition(config, state, variable_manager, step_id)
        elif loop_type == "iterate":
            return self._evaluate_iterate(config, state, variable_manager, step_id)
        return False

    def _evaluate_count(self, config, state, variable_manager, step_id):
        """计数循环：按次数迭代，可选设置循环变量"""
        max_count = config.get("count", 10)
        loop_var = config.get("loop_var", "")
        start_value = config.get("start_value", 0)
        step = config.get("step", 1)

        current = state["iteration"]
        if current < max_count:
            current_value = start_value + current * step
            if loop_var:
                variable_manager.set_variable(loop_var, current_value)
            state["iteration"] = current + 1
            return True
        del self._loop_states[step_id]
        return False

    def _evaluate_condition(self, config, state, variable_manager, step_id):
        """条件循环：当条件满足时继续迭代"""
        condition_var = config.get("condition_var", "")
        condition_op = config.get("condition_op", "==")
        condition_value = config.get("condition_value", "")
        var_value = variable_manager.get_variable(condition_var)
        result = self._compare_values(var_value, condition_op, condition_value)
        if not result:
            del self._loop_states[step_id]
        return result

    def _evaluate_iterate(self, config, state, variable_manager, step_id):
        """遍历循环：遍历列表中的每个元素"""
        list_var = config.get("list_var", "")
        element_var = config.get("element_var", "")
        items = variable_manager.get_variable(list_var)
        if not isinstance(items, list):
            items = [items]
        current = state["iteration"]
        if current < len(items):
            if element_var:
                variable_manager.set_variable(element_var, items[current])
            state["iteration"] = current + 1
            return True
        del self._loop_states[step_id]
        return False

    def reset(self, step_id):
        """重置指定步骤的循环状态"""
        if step_id in self._loop_states:
            del self._loop_states[step_id]

    def reset_all(self):
        """重置所有循环状态"""
        self._loop_states.clear()

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