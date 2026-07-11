from PySide6.QtWidgets import QGraphicsWidget, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem
from PySide6.QtCore import Qt, QRectF, QSizeF, Signal
from PySide6.QtGui import QColor, QBrush, QPen, QFont
import uuid

from .node_types import get_node_type
from .port_widget import PortWidget


class NodeWidget(QGraphicsWidget):
    node_selected = Signal(object)
    node_double_clicked = Signal(object)
    node_moved = Signal(object)

    def __init__(self, node_type: str, config: dict = None, parent=None):
        super().__init__(parent)
        self.node_type = node_type
        self.node_id = str(uuid.uuid4())
        self.config = config or {}
        self._is_selected = False

        self.input_ports = []
        self.output_ports = []

        self._init_structure()
        self._create_ports()

    def _init_structure(self):
        node_info = get_node_type(self.node_type)

        self.setMinimumSize(QSizeF(200, 80))
        self.setMaximumSize(QSizeF(350, 500))

        self.body = QGraphicsRectItem(0, 0, 200, 80, self)
        self.body.setBrush(QBrush(QColor("#2a2a4a")))
        self.body.setPen(QPen(QColor("#4a4a6e"), 1))

        self.header = QGraphicsRectItem(0, 0, 200, 30, self)
        self.header.setBrush(QBrush(QColor(node_info["color"])))
        self.header.setPen(QPen(QColor(node_info["color"]), 1))

        self.title = QGraphicsTextItem(f"{node_info['icon']} {node_info['name']}", self)
        self.title.setDefaultTextColor(QColor("#ffffff"))
        self.title.setFont(QFont("Arial", 12, QFont.Bold))
        self.title.setPos(10, 5)

        self.param_text = QGraphicsTextItem(self._format_params(), self)
        self.param_text.setDefaultTextColor(QColor("#aaa"))
        self.param_text.setFont(QFont("Arial", 10))
        self.param_text.setPos(10, 35)

    def _create_ports(self):
        if self.node_type != "start":
            in_port = PortWidget("in", "输入", self)
            in_port.setPos(0, 40)
            self.input_ports.append(in_port)

        if self.node_type == "if_else":
            true_port = PortWidget("out", "True", self)
            true_port.setPos(188, 25)
            self.output_ports.append(true_port)

            false_port = PortWidget("out", "False", self)
            false_port.setPos(188, 55)
            self.output_ports.append(false_port)
        elif self.node_type != "end":
            out_port = PortWidget("out", "输出", self)
            out_port.setPos(188, 40)
            self.output_ports.append(out_port)

    def _format_params(self):
        display_parts = []
        if "image_path" in self.config:
            import os
            display_parts.append(f"图片: {os.path.basename(self.config['image_path'])}")
        if "text" in self.config:
            display_parts.append(f"文本: {self.config['text'][:20]}")
        if "key" in self.config:
            display_parts.append(f"按键: {self.config['key']}")
        if "wait_time" in self.config:
            display_parts.append(f"等待: {self.config['wait_time']}s")
        if "variable_name" in self.config:
            display_parts.append(f"变量: {self.config['variable_name']}")
        return ", ".join(display_parts) if display_parts else "无参数"

    def update_params(self, config):
        self.config = config
        self.param_text.setPlainText(self._format_params())

    def set_node_id(self, node_id):
        self.node_id = node_id

    def get_input_port(self, port_label="输入"):
        for port in self.input_ports:
            if port.label == port_label:
                return port
        return None

    def get_output_port(self, port_label="输出"):
        for port in self.output_ports:
            if port.label == port_label:
                return port
        return None

    def set_selected(self, selected):
        self._is_selected = selected
        if selected:
            self.body.setPen(QPen(QColor("#00d4ff"), 2))
            self.body.setZValue(5)
        else:
            self.body.setPen(QPen(QColor("#4a4a6e"), 1))
            self.body.setZValue(1)

    def boundingRect(self):
        return QRectF(0, 0, 200, 80)

    def mousePressEvent(self, event):
        self.node_selected.emit(self)
        self.set_selected(True)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.node_double_clicked.emit(self)
        super().mouseDoubleClickEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.node_moved.emit(self)
            for port in self.input_ports + self.output_ports:
                for edge in port.connected_edges:
                    edge.update_path()
        return super().itemChange(change, value)

    def to_json(self):
        return {
            "id": self.node_id,
            "type": self.node_type,
            "x": self.x(),
            "y": self.y(),
            "config": self.config
        }

    def from_json(self, data):
        self.node_id = data.get("id", self.node_id)
        self.setPos(data.get("x", 0), data.get("y", 0))
        self.config = data.get("config", {})
        self.update_params(self.config)