import pytest
import sys
sys.path.insert(0, '..')
from operations.window import WindowOperations

def test_window_initialization():
    window = WindowOperations()
    assert window is not None

def test_get_all_windows():
    window = WindowOperations()
    windows = window.get_all_windows()
    assert isinstance(windows, list)

def test_find_window():
    window = WindowOperations()
    windows = window.get_all_windows()
    if windows:
        hwnd, title = windows[0]
        found = window.find_window(title)
        assert found == hwnd
    else:
        assert True

def test_get_window_title():
    window = WindowOperations()
    active = window.get_active_window()
    if active:
        title = window.get_window_title(active)
        assert isinstance(title, str)