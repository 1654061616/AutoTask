"""
变量管理器 — 负责运行时变量的存储和表达式解析
"""
import ast
import operator
import re
from typing import Dict, Any, Tuple, Optional

class VariableManager:
    """变量管理器，支持变量存取、${var} 表达式解析和 Excel 引用解析"""

    def __init__(self):
        self.variables: Dict[str, Any] = {}   # 变量字典
        self.excel_data: Dict[str, Any] = {}  # Excel 数据缓存

    def set_variable(self, name: str, value: Any):
        """设置变量值，支持算术表达式（如 ${a} + ${b} * 2）"""
        if isinstance(value, str):
            resolved = self.resolve_expression(value)
            self.variables[name] = self._try_eval_arithmetic(resolved)
        else:
            self.variables[name] = value

    def _try_eval_arithmetic(self, expr: str):
        """安全计算算术表达式，非表达式则返回原字符串

        支持的运算：+ - * / // % ** 括号 负数
        示例：${a} + ${b} → 13,  ${a} * 2 → 20,  (${a} + ${b}) * 2 → 26   // 整除   % 取余   ** 幂
        """
        if not re.search(r'[\d)]\s*[+\-*/%]', expr):
            return expr
        try:
            tree = ast.parse(expr.strip(), mode='eval')
            return _ASTEvaluator().visit(tree.body)
        except Exception:
            return expr

    def get_variable(self, name: str) -> Any:
        """获取变量值"""
        return self.variables.get(name)

    def resolve_expression(self, text: str) -> str:
        """解析字符串中的 ${变量名} 表达式，替换为实际值"""
        if not text:
            return text

        def replace_match(match):
            var_name = match.group(1)
            value = self.get_variable(var_name)
            if value is not None:
                return str(value)
            return match.group(0)

        pattern = r'\$\{(\w+)\}'
        return re.sub(pattern, replace_match, text)

    def parse_excel_reference(self, ref: str) -> Optional[Tuple[str, str]]:
        """解析 ${EXCEL:sheet!cell} 格式的引用"""
        pattern = r'\$\{EXCEL:([^!]+)!([A-Za-z]+\d+)\}'
        match = re.match(pattern, ref)
        if match:
            return match.group(1), match.group(2)
        return None

    def load_excel(self, file_path: str):
        """加载 Excel 数据（由子类或外部实现）"""
        pass

    def get_excel_value(self, sheet_name: str, cell_ref: str) -> Any:
        """获取 Excel 单元格值"""
        key = f"{sheet_name}!{cell_ref}"
        return self.excel_data.get(key)


class _ASTEvaluator:
    """安全的算术表达式求值器，基于 AST 遍历"""

    _BINARY_OPS = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    _UNARY_OPS = {
        ast.USub: operator.neg, ast.UAdd: operator.pos,
    }

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def visit_Constant(self, node):
        return node.value

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return self._BINARY_OPS[type(node.op)](left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        return self._UNARY_OPS[type(node.op)](operand)

    def visit_Expression(self, node):
        return self.visit(node.body)

    def _generic_visit(self, node):
        raise ValueError(f"不支持的操作: {ast.dump(node)}")