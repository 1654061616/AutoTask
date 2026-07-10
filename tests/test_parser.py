import pytest
import sys
import json
sys.path.insert(0, '..')
from core.parser import FlowParser

def test_parse_flow():
    flow_data = {
        "name": "Test Flow",
        "version": "1.0",
        "steps": [
            {
                "id": "step_1",
                "type": "mouse_click",
                "name": "Test Click",
                "config": {},
                "next_step": None
            }
        ]
    }
    parser = FlowParser()
    flow = parser.parse(flow_data)
    assert flow["name"] == "Test Flow"
    assert len(flow["steps"]) == 1
    assert flow["steps"][0]["type"] == "mouse_click"

def test_validate_step():
    parser = FlowParser()
    step = {
        "id": "step_1",
        "type": "mouse_click",
        "name": "Test",
        "config": {},
        "next_step": None
    }
    assert parser.validate_step(step) is True

def test_invalid_step_missing_id():
    parser = FlowParser()
    step = {
        "type": "mouse_click",
        "name": "Test",
        "config": {},
        "next_step": None
    }
    assert parser.validate_step(step) is False