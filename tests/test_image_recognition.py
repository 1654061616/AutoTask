import pytest
import sys
sys.path.insert(0, '..')
from operations.image_recognition import ImageRecognition

def test_image_recognition_initialization():
    ir = ImageRecognition()
    assert ir is not None

def test_get_screen_size():
    ir = ImageRecognition()
    width, height = ir.get_screen_size()
    assert width > 0
    assert height > 0

def test_capture_screen():
    ir = ImageRecognition()
    img = ir.capture_screen()
    assert img is not None
    assert len(img.shape) == 3

def test_image_exists_nonexistent():
    ir = ImageRecognition()
    result = ir.image_exists("nonexistent.png")
    assert result is False