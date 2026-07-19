from PySide6.QtWidgets import QGraphicsObject, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF, QSizeF, Signal
from PySide6.QtGui import QColor, QBrush, QPen, QFont
import uuid

from .node_types import get_node_type
from .port_widget import PortWidget


class NodeWidget(QGraphicsObject):
    node_selected = Signal(object)
    node_double_clicked = Signal(object)
    node_moved = Signal(object)

    def __init__(self, node_type: str, config: dict = None, parent=None):
        super().__init__(parent)
        self.node_type = node_type
        self.node_id = str(uuid.uuid4())
        self.config = config or {}
        self._is_selected = False
        self._is_deleted = False

        self.input_ports = []
        self.output_ports = []

        self._init_structure()
        self._create_ports()

        self.setFlag(QGraphicsObject.ItemIsMovable, True)
        self.setFlag(QGraphicsObject.ItemIsSelectable, True)
        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges, True)

    def _init_structure(self):
        node_info = get_node_type(self.node_type)

        self.node_width = 200
        self._calc_height()

        self.body = QGraphicsRectItem(0, 0, self.node_width, self.node_height, self)
        self.body.setBrush(QBrush(QColor("#2a2a4a")))
        self.body.setPen(QPen(QColor("#4a4a6e"), 1))
        self.body.setZValue(0)

        self.header = QGraphicsRectItem(0, 0, self.node_width, 30, self)
        self.header.setBrush(QBrush(QColor(node_info["color"])))
        self.header.setPen(QPen(QColor(node_info["color"]), 1))
        self.header.setZValue(1)

        self.title = QGraphicsTextItem(f"{node_info['icon']} {node_info['name']}", self)
        self.title.setDefaultTextColor(QColor("#ffffff"))
        self.title.setFont(QFont("Arial", 12, QFont.Bold))
        self.title.setPos(10, 5)
        self.title.setZValue(2)

        self.param_text = QGraphicsTextItem(self._format_params(), self)
        self.param_text.setDefaultTextColor(QColor("#aaa"))
        self.param_text.setFont(QFont("Arial", 9))
        self.param_text.setPos(10, 48)
        self.param_text.setZValue(2)

    def _calc_height(self):
        params = self._format_params()
        lines = 1
        if len(params) > 25:
            lines = (len(params) // 25) + 1
        base_height = 75
        if self.node_type in ("image_find", "image_click", "image_exists", "if_else", "loop"):
            base_height = 105
        self.node_height = base_height + (lines - 1) * 18

    def _create_ports(self):
        port_offset = -PortWidget.PORT_SIZE / 2

        if self.node_type != "start":
            in_port = PortWidget("in", "输入", self, self)
            in_port.setPos(port_offset, 40)
            self.input_ports.append(in_port)

        if self.node_type in ("if_else", "loop"):
            true_port = PortWidget("out", "True", self, self)
            true_port.setPos(self.node_width + port_offset, 32)
            self.output_ports.append(true_port)

            false_port = PortWidget("out", "False", self, self)
            false_port.setPos(self.node_width + port_offset, 88)
            self.output_ports.append(false_port)

        elif self.node_type in ("image_find", "image_click", "image_exists"):
            true_port = PortWidget("out", "True", self, self)
            true_port.setPos(self.node_width + port_offset, 32)
            self.output_ports.append(true_port)

            false_port = PortWidget("out", "False", self, self)
            false_port.setPos(self.node_width + port_offset, 88)
            self.output_ports.append(false_port)

        elif self.node_type != "end":
            out_port = PortWidget("out", "输出", self, self)
            out_port.setPos(self.node_width + port_offset, 40)
            self.output_ports.append(out_port)

    def _format_params(self):
        display_parts = []
        if "image_path" in self.config:
            import os
            filename = os.path.basename(self.config['image_path'])
            if len(filename) > 25:
                filename = filename[:12] + "..." + filename[-10:]
            display_parts.append(f"{filename}")
        if "text" in self.config:
            display_parts.append(f"文本: {self.config['text'][:15]}")
        if "key" in self.config:
            display_parts.append(f"按键: {self.config['key']}")
        if "wait_time" in self.config:
            display_parts.append(f"等待: {self.config['wait_time']}s")
        if "variable_name" in self.config:
            display_parts.append(f"变量: {self.config['variable_name']}")
        result = ", ".join(display_parts) if display_parts else ""
        if len(result) > 20:
            result = result[:18] + "..."
        return result

    def update_params(self, config):
        self.config = config
        new_params = self._format_params()
        self.param_text.setPlainText(new_params)
        
        old_height = self.node_height
        self._calc_height()
        
        if self.node_height != old_height:
            self.body.setRect(0, 0, self.node_width, self.node_height)
            self._create_ports()
            self.prepareGeometryChange()

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
        else:
            self.body.setPen(QPen(QColor("#4a4a6e"), 1))

    def boundingRect(self):
        return QRectF(-PortWidget.PORT_SIZE, 0, 
                      self.node_width + PortWidget.PORT_SIZE * 2, 
                      self.node_height)

    def paint(self, painter, option, widget=None):
        pass

    def mousePressEvent(self, event):
        self.node_selected.emit(self)
        self.set_selected(True)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.node_double_clicked.emit(self)
        super().mouseDoubleClickEvent(event)

    def itemChange(self, change, value):
        if getattr(self, '_is_deleted', False):
            return super().itemChange(change, value)
        if change == QGraphicsObject.ItemPositionChange:
            try:
                self.node_moved.emit(self)
                for port in self.input_ports + self.output_ports:
                    for edge in port.connected_edges[:]:
                        try:
                            edge.update_path()
                        except Exception:
                            pass
            except Exception:
                pass
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