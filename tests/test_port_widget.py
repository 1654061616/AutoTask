import pytest
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication([])

from gui.node_graph.port_widget import PortWidget

def test_port_initialization():
    port = PortWidget("in", "input", None)
    assert port.port_type == "in"
    assert port.label == "input"

def test_port_connection():
    port1 = PortWidget("out", "output1", None)
    port2 = PortWidget("in", "input", None)
    assert port1.can_connect(port2) == True

def test_port_cannot_connect_same_type():
    port1 = PortWidget("in", "input1", None)
    port2 = PortWidget("in", "input2", None)
    assert port1.can_connect(port2) == False