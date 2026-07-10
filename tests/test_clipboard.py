import pytest
import sys
sys.path.insert(0, '..')
from operations.clipboard import ClipboardOperations

def test_clipboard_copy_paste():
    cb = ClipboardOperations()
    test_text = "hello clipboard"
    cb.copy_text(test_text)
    result = cb.paste_text()
    assert result == test_text

def test_clipboard_clear():
    cb = ClipboardOperations()
    cb.copy_text("test")
    cb.clear()
    result = cb.paste_text()
    assert result == ""

def test_clipboard_has_text():
    cb = ClipboardOperations()
    cb.copy_text("test")
    assert cb.has_text()
    cb.clear()
    assert not cb.has_text()