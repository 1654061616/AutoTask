import pytest
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)

from gui.node_graph.edge_widget import EdgeWidget
from gui.node_graph.node_widget import NodeWidget

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