import pytest
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication([])

from gui.node_graph.graph_view import GraphView
from gui.node_graph.graph_scene import GraphScene

def test_view_initialization():
    scene = GraphScene()
    view = GraphView(scene)
    assert view.scene() == scene

def test_zoom_in():
    scene = GraphScene()
    view = GraphView(scene)
    initial_scale = view.transform().m11()
    view.zoom_in()
    assert view.transform().m11() > initial_scale

def test_zoom_out():
    scene = GraphScene()
    view = GraphView(scene)
    initial_scale = view.transform().m11()
    view.zoom_out()
    assert view.transform().m11() < initial_scale