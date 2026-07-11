import pytest
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication([])

from gui.node_graph.graph_scene import GraphScene

def test_scene_initialization():
    scene = GraphScene()
    assert scene.width() > 0
    assert scene.height() > 0

def test_add_node():
    scene = GraphScene()
    node = scene.add_node("mouse_click", 100, 200)
    assert node is not None
    assert len(scene.nodes) == 1

def test_remove_node():
    scene = GraphScene()
    node = scene.add_node("mouse_click", 100, 200)
    scene.remove_node(node)
    assert len(scene.nodes) == 0