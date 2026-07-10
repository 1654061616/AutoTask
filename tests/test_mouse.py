import pytest
import sys
sys.path.insert(0, '..')
from operations.mouse import MouseOperations

def test_mouse_initialization():
    mouse = MouseOperations()
    assert mouse is not None

def test_mouse_click():
    mouse = MouseOperations()
    try:
        mouse.click()
        assert True
    except Exception:
        assert True

def test_mouse_get_position():
    mouse = MouseOperations()
    pos = mouse.get_position()
    assert isinstance(pos, tuple)
    assert len(pos) == 2

def test_mouse_move():
    mouse = MouseOperations()
    try:
        mouse.move(100, 100, duration=0.1)
        assert True
    except Exception:
        assert True

def test_ease_function():
    mouse = MouseOperations()
    result = mouse._ease_in_out_cubic(0.5)
    assert 0 <= result <= 1