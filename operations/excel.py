from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from typing import Dict, Any, List, Optional

class ExcelOperations:
    def __init__(self):
        self.workbook = None
        self.file_path = None
    
    def open_workbook(self, file_path: str):
        self.file_path = file_path
        self.workbook = load_workbook(file_path, data_only=True)
    
    def get_sheet_names(self) -> List[str]:
        if self.workbook:
            return self.workbook.sheetnames
        return []
    
    def get_cell_value(self, sheet_name: str, cell_ref: str) -> Any:
        if not self.workbook:
            return None
        if sheet_name not in self.workbook.sheetnames:
            return None
        sheet = self.workbook[sheet_name]
        return sheet[cell_ref].value
    
    def get_row_values(self, sheet_name: str, row: int) -> List[Any]:
        if not self.workbook or sheet_name not in self.workbook.sheetnames:
            return []
        sheet = self.workbook[sheet_name]
        return [cell.value for cell in sheet[row]]
    
    def get_column_values(self, sheet_name: str, column: int) -> List[Any]:
        if not self.workbook or sheet_name not in self.workbook.sheetnames:
            return []
        sheet = self.workbook[sheet_name]
        col_letter = get_column_letter(column)
        return [cell.value for cell in sheet[col_letter]]
    
    def get_range_values(self, sheet_name: str, start_cell: str, end_cell: str) -> List[List[Any]]:
        if not self.workbook or sheet_name not in self.workbook.sheetnames:
            return []
        sheet = self.workbook[sheet_name]
        return [[cell.value for cell in row] for row in sheet[start_cell:end_cell]]
    
    def get_sheet_data(self, sheet_name: str) -> Dict[str, Any]:
        if not self.workbook or sheet_name not in self.workbook.sheetnames:
            return {}
        sheet = self.workbook[sheet_name]
        data = {}
        for row in sheet.iter_rows(values_only=True):
            for i, cell in enumerate(row):
                col_letter = get_column_letter(i + 1)
                data[f"{col_letter}{row[0]}"] = cell
        return data
    
    def close_workbook(self):
        if self.workbook:
            self.workbook.close()
            self.workbook = None
    
    def get_row_count(self, sheet_name: str) -> int:
        if not self.workbook or sheet_name not in self.workbook.sheetnames:
            return 0
        sheet = self.workbook[sheet_name]
        return sheet.max_row
    
    def get_column_count(self, sheet_name: str) -> int:
        if not self.workbook or sheet_name not in self.workbook.sheetnames:
            return 0
        sheet = self.workbook[sheet_name]
        return sheet.max_column