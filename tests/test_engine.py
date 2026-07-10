import pytest
import sys
sys.path.insert(0, '..')
from core.engine import FlowEngine

def test_engine_initialization():
    engine = FlowEngine()
    assert not engine.is_running
    assert engine.current_step is None

def test_load_flow():
    engine = FlowEngine()
    flow = {
        "name": "Test",
        "version": "1.0",
        "steps": []
    }
    engine.load_flow(flow)
    assert engine.flow["name"] == "Test"

def test_stop_engine():
    engine = FlowEngine()
    engine.is_running = True
    engine.stop()
    assert not engine.is_running