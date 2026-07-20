import pytest
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication([])

from gui.node_graph.edge_widget import EdgeWidget, ControlPointHandle
from gui.node_graph.node_widget import NodeWidget
from gui.node_graph.graph_scene import GraphScene

def test_edge_initialization():
    source_node = NodeWidget("mouse_click", {})
    target_node = NodeWidget("wait", {})
    source_port = source_node.output_ports[0]
    target_port = target_node.input_ports[0]
    
    edge = EdgeWidget(source_port, target_port)
    assert edge.source_port == source_port
    assert edge.target_port == target_port

def test_edge_to_json():
    source_node = NodeWidget("mouse_click", {})
    target_node = NodeWidget("wait", {})
    source_port = source_node.output_ports[0]
    target_port = target_node.input_ports[0]
    
    edge = EdgeWidget(source_port, target_port)
    data = edge.to_json()
    assert data["source_node"] == source_node.node_id
    assert data["target_node"] == target_node.node_id


def test_control_point_handles_created():
    """EdgeWidget 创建时包含两个 ControlPointHandle，初始隐藏"""
    scene = GraphScene()
    node1 = scene.add_node("mouse_click", 100, 100)
    node2 = scene.add_node("mouse_click", 400, 100)
    source_port = node1.get_output_port("输出")
    target_port = node2.get_input_port("输入")
    edge = scene.add_edge(source_port, target_port)

    assert hasattr(edge, '_cp1_handle')
    assert hasattr(edge, '_cp2_handle')
    assert not edge._cp1_handle.isVisible()
    assert not edge._cp2_handle.isVisible()


def test_handles_visible_on_selected():
    """选中边时控制点手柄可见"""
    scene = GraphScene()
    node1 = scene.add_node("mouse_click", 100, 100)
    node2 = scene.add_node("mouse_click", 400, 100)
    edge = scene.add_edge(node1.get_output_port("输出"), node2.get_input_port("输入"))

    edge.setSelected(True)
    assert edge._cp1_handle.isVisible()
    assert edge._cp2_handle.isVisible()

    edge.setSelected(False)
    assert not edge._cp1_handle.isVisible()
    assert not edge._cp2_handle.isVisible()


def test_control_points_persisted():
    """to_json/from_json 包含控制点偏移量"""
    scene = GraphScene()
    node1 = scene.add_node("mouse_click", 100, 100)
    node2 = scene.add_node("mouse_click", 400, 100)
    edge = scene.add_edge(node1.get_output_port("输出"), node2.get_input_port("输入"))

    edge._cp1_offset = (0.3, 0.1)
    edge._cp2_offset = (0.7, -0.1)

    data = edge.to_json()
    assert data["cp1"]["x"] == 0.3
    assert data["cp1"]["y"] == 0.1
    assert data["cp2"]["x"] == 0.7
    assert data["cp2"]["y"] == -0.1

    edge._cp1_offset = (0.25, 0.0)
    edge._cp2_offset = (0.75, 0.0)
    edge.from_json(data)
    assert edge._cp1_offset == (0.3, 0.1)
    assert edge._cp2_offset == (0.7, -0.1)


def test_control_points_default_offsets():
    """EdgeWidget 创建时控制点偏移量为默认值"""
    scene = GraphScene()
    node1 = scene.add_node("mouse_click", 100, 100)
    node2 = scene.add_node("mouse_click", 400, 100)
    edge = scene.add_edge(node1.get_output_port("输出"), node2.get_input_port("输入"))

    assert edge._cp1_offset == (0.25, 0.0)
    assert edge._cp2_offset == (0.75, 0.0)