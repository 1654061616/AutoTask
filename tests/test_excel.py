import pytest
import sys
sys.path.insert(0, '..')
from operations.excel import ExcelOperations

def test_excel_initialization():
    excel = ExcelOperations()
    assert excel is not None

def test_get_sheet_names():
    excel = ExcelOperations()
    assert excel.get_sheet_names() == []