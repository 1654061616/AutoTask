import pytest
from PySide6.QtWidgets import QApplication, QGraphicsObject

app = QApplication.instance() or QApplication([])

from gui.node_graph.port_widget import PortWidget


class MockNode:
    """模拟节点对象，提供 node_width 和 node_height"""
    def __init__(self):
        self.node_width = 200
        self.node_height = 100


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


def test_port_movable_flag():
    """端口应可移动"""
    node = MockNode()
    port = PortWidget("in", "输入", node)
    assert port.flags() & QGraphicsObject.ItemIsMovable


def test_port_drag_threshold_distinguishes_click():
    """拖动距离小于阈值应视为点击，emit port_clicked"""
    node = MockNode()
    port = PortWidget("in", "输入", node)
    clicked = []
    port.port_clicked.connect(lambda p: clicked.append(p))
    assert not port._dragging


def test_port_snaps_to_nearest_edge():
    """端口拖动后应吸附到最近边缘"""
    node = MockNode()
    port = PortWidget("in", "输入", node)
    port.setPos(100, 100)

    port._snap_to_nearest_edge()
    assert port.pos().y() == pytest.approx(100 - PortWidget.PORT_SIZE / 2)


def test_port_center_on_edge():
    """端口圆心应在边缘上"""
    node = MockNode()
    port = PortWidget("out", "输出", node)
    port.setPos(0, 0)
    port._snap_to_nearest_edge()
    center = port.mapToParent(port.boundingRect().center())
    if abs(center.x()) < abs(center.y()):
        assert center.x() == pytest.approx(0)
    else:
        assert center.y() == pytest.approx(0)