import pytest
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication([])

from gui.node_graph.node_widget import NodeWidget
from gui.node_graph.port_widget import PortWidget


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


def test_node_to_json_includes_port_positions():
    """to_json 应包含端口位置信息"""
    node = NodeWidget("mouse_click", {})
    data = node.to_json()
    assert "ports" in data
    assert len(data["ports"]) == 2


def test_node_from_json_restores_port_positions():
    """from_json 应恢复端口位置（位置会被吸附到边缘）"""
    node = NodeWidget("mouse_click", {})
    data = {
        "id": node.node_id,
        "type": "mouse_click",
        "x": 100,
        "y": 200,
        "config": {},
        "ports": {
            "输入": [200, 50],
            "输出": [-8, 40]
        }
    }
    node.from_json(data)
    in_port = node.get_input_port("输入")
    out_port = node.get_output_port("输出")
    assert in_port.pos().x() == pytest.approx(192)
    assert in_port.pos().y() == pytest.approx(50)
    assert out_port.pos().x() == pytest.approx(-8)
    assert out_port.pos().y() == pytest.approx(40)


def test_node_bounding_rect_includes_top_bottom_ports():
    """boundingRect 应包含上下边缘的端口"""
    node = NodeWidget("mouse_click", {})
    rect = node.boundingRect()
    assert rect.top() <= -PortWidget.PORT_SIZE
    assert rect.bottom() >= node.node_height + PortWidget.PORT_SIZE


def test_restore_ports_from_data():
    """restore_ports_from_data 应恢复端口位置（不触发 update_params）"""
    node = NodeWidget("mouse_click", {})
    node_data = {
        "ports": {
            "输入": [50, -8],
            "输出": [192, 40]
        }
    }
    node.restore_ports_from_data(node_data)
    in_port = node.get_input_port("输入")
    out_port = node.get_output_port("输出")
    assert in_port.pos().x() == pytest.approx(50)
    assert in_port.pos().y() == pytest.approx(-8)
    assert out_port.pos().x() == pytest.approx(192)
    assert out_port.pos().y() == pytest.approx(40)


def test_restore_ports_from_data_empty():
    """restore_ports_from_data 无 ports 数据时不应报错"""
    node = NodeWidget("mouse_click", {})
    node_data = {}
    node.restore_ports_from_data(node_data)