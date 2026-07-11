import pytest
from gui.node_graph.node_types import NODE_TYPES, get_node_type, get_node_color

def test_get_node_type():
    node_info = get_node_type("mouse_click")
    assert node_info["name"] == "鼠标点击"
    assert node_info["icon"] == "🖱️"

def test_get_node_color():
    color = get_node_color("image_find")
    assert color == "#ff9800"

def test_unknown_node_type():
    node_info = get_node_type("unknown")
    assert node_info is not None