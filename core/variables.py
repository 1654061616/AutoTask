"""
变量管理器 — 负责运行时变量的存储和表达式解析
"""
import re
from typing import Dict, Any, Tuple, Optional

class VariableManager:
    """变量管理器，支持变量存取、${var} 表达式解析和 Excel 引用解析"""

    def __init__(self):
        self.variables: Dict[str, Any] = {}   # 变量字典
        self.excel_data: Dict[str, Any] = {}  # Excel 数据缓存

    def set_variable(self, name: str, value: Any):
        """设置变量值"""
        self.variables[name] = value

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