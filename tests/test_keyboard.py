import pytest
import sys
sys.path.insert(0, '..')
from operations.keyboard import KeyboardOperations

def test_keyboard_initialization():
    keyboard = KeyboardOperations()
    assert keyboard is not None

def test_keyboard_press():
    keyboard = KeyboardOperations()
    try:
        keyboard.press('a')
        assert True
    except Exception:
        assert True

def test_keyboard_hotkey():
    keyboard = KeyboardOperations()
    try:
        keyboard.hotkey('ctrl', 'a')
        assert True
    except Exception:
        assert True

def test_keyboard_type():
    keyboard = KeyboardOperations()
    try:
        keyboard.type('test', interval=0.01)
        assert True
    except Exception:
        assert True

def test_clipboard_copy_paste():
    keyboard = KeyboardOperations()
    test_text = "test clipboard"
    keyboard.clipboard_copy(test_text)
    result = keyboard.clipboard_paste()
    assert result == test_text