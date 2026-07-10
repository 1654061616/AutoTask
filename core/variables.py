import re
from typing import Dict, Any, Tuple, Optional

class VariableManager:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.excel_data: Dict[str, Any] = {}
    
    def set_variable(self, name: str, value: Any):
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Any:
        return self.variables.get(name)
    
    def resolve_expression(self, text: str) -> str:
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
        pattern = r'\$\{EXCEL:([^!]+)!([A-Za-z]+\d+)\}'
        match = re.match(pattern, ref)
        if match:
            return match.group(1), match.group(2)
        return None
    
    def load_excel(self, file_path: str):
        pass
    
    def get_excel_value(self, sheet_name: str, cell_ref: str) -> Any:
        key = f"{sheet_name}!{cell_ref}"
        return self.excel_data.get(key)