import pytest
import sys
sys.path.insert(0, '..')
from operations.condition import ConditionEvaluator

def test_condition_initialization():
    ce = ConditionEvaluator()
    assert ce is not None

def test_evaluate_value_equal():
    ce = ConditionEvaluator()
    result = ce.evaluate("value", 10, 10, "==")
    assert result is True

def test_evaluate_value_not_equal():
    ce = ConditionEvaluator()
    result = ce.evaluate("value", 10, 20, "!=")
    assert result is True

def test_evaluate_value_greater_than():
    ce = ConditionEvaluator()
    result = ce.evaluate("value", 20, 10, ">")
    assert result is True

def test_evaluate_value_contains():
    ce = ConditionEvaluator()
    result = ce.evaluate("value", "hello world", "world", "contains")
    assert result is True

def test_if_else():
    ce = ConditionEvaluator()
    result = ce.if_else(True, "yes", "no")
    assert result == "yes"
    result = ce.if_else(False, "yes", "no")
    assert result == "no"