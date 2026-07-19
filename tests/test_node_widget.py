import pytest
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)

from gui.node_graph.node_widget import NodeWidget


def test_node_initialization():
    node = NodeWidget("mouse_click", {})
    assert node.node_type == "mouse_click"
    assert node.node_id is not None


def test_node_has_ports():
    node = NodeWidget("mouse_click", {})
    assert len(node.input_ports) == 1
    assert len(node.output_ports) == 1


def test_node_to_json():
    node = NodeWidget("mouse_click", {"click_type": "left"})
    node.setPos(100, 200)
    data = node.to_json()
    assert data["type"] == "mouse_click"
    assert data["x"] == 100
    assert data["y"] == 200
    assert data["config"]["click_type"] == "left"


def test_if_else_has_two_outputs():
    node = NodeWidget("if_else", {})
    assert len(node.output_ports) == 2


def test_loop_has_two_outputs():
    node = NodeWidget("loop", {})
    assert len(node.output_ports) == 2
    labels = [p.label for p in node.output_ports]
    assert "True" in labels
    assert "False" in labels