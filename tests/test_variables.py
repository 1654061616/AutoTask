import pytest
import sys
sys.path.insert(0, '..')
from core.variables import VariableManager

def test_set_and_get_variable():
    vm = VariableManager()
    vm.set_variable("name", "test")
    assert vm.get_variable("name") == "test"

def test_resolve_expression():
    vm = VariableManager()
    vm.set_variable("name", "World")
    result = vm.resolve_expression("Hello ${name}")
    assert result == "Hello World"

def test_unresolved_variable():
    vm = VariableManager()
    result = vm.resolve_expression("Hello ${unknown}")
    assert result == "Hello ${unknown}"

def test_parse_excel_reference():
    vm = VariableManager()
    result = vm.parse_excel_reference("${EXCEL:Sheet1!A1}")
    assert result == ("Sheet1", "A1")