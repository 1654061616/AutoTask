from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsWidget
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QColor, QPen, QBrush, QFont
import uuid
from .node_types import get_node_type, get_node_color, get_node_icon, get_node_name

class PortWidget(QGraphicsItem):
    def __init__(self, node, port_type, index=0):
        super().__init__(node)
        self.node = node
        self.port_type = port_type
        self.index = index
        self.radius = 6
        self.connected = False
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QRectF(-self.radius, -self.radius, self.radius * 2, self.radius * 2)

    def paint(self, painter, option, widget=None):
        color = QColor("#4caf50") if self.port_type == "input" else QColor("#f44336")
        brush = QBrush(color)
        painter.setBrush(brush)
        painter.setPen(QPen(Qt.NoPen))
        painter.drawEllipse(self.boundingRect())
        
        if self.connected:
            painter.setBrush(QBrush(QColor("#fff")))
            painter.drawEllipse(-3, -3, 6, 6)

    def get_global_pos(self):
        return self.mapToScene(QPointF(0, 0))

class NodeWidget(QGraphicsWidget):
    node_moved = Signal(object)
    
    def __init__(self, node_type, config=None, parent=None):
        super().__init__(parent)
        self.node_type = node_type
        self.config = config or {}
        self.node_id = str(uuid.uuid4())
        
        node_info = get_node_type(node_type)
        self.color = QColor(get_node_color(node_type))
        self.icon = get_node_icon(node_type)
        self.name = get_node_name(node_type)
        
        self.width = 180
        self.height = 60
        
        self.input_ports = []
        self.output_ports = []
        
        self._init_ports()
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    def _init_ports(self):
        node_info = get_node_type(self.node_type)
        category = node_info["category"]
        
        if category in ["flow", "control"]:
            self.input_ports.append(PortWidget(self, "input", 0))
            self.output_ports.append(PortWidget(self, "output", 0))
            
            if self.node_type == "if_else":
                self.output_ports.append(PortWidget(self, "output", 1))
        else:
            self.input_ports.append(PortWidget(self, "input", 0))
            self.output_ports.append(PortWidget(self, "output", 0))

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget=None):
        rect = self.boundingRect()
        
        gradient = painter.linearGradient(rect.topLeft(), rect.bottomLeft())
        gradient.setColorAt(0, self.color.lighter(120))
        gradient.setColorAt(1, self.color.darker(120))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor("#fff"), 2))
        painter.drawRoundedRect(rect, 8, 8)
        
        font = QFont("Microsoft YaHei", 10, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))
        
        icon_rect = QRectF(10, 15, 30, 30)
        icon_font = QFont("Arial", 16)
        painter.setFont(icon_font)
        painter.drawText(icon_rect, Qt.AlignCenter, self.icon)
        
        text_font = QFont("Microsoft YaHei", 9)
        painter.setFont(text_font)
        text_rect = QRectF(45, 0, self.width - 45, self.height)
        painter.drawText(text_rect, Qt.AlignCenter, self.name)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.node_moved.emit(self)
        return super().itemChange(change, value)

    def get_input_port(self, index=0):
        if index < len(self.input_ports):
            return self.input_ports[index]
        return None

    def get_output_port(self, index=0):
        if index < len(self.output_ports):
            return self.output_ports[index]
        return None

    def set_node_id(self, node_id):
        self.node_id = node_id

    def to_json(self):
        pos = self.pos()
        return {
            "id": self.node_id,
            "type": self.node_type,
            "x": pos.x(),
            "y": pos.y(),
            "config": self.config
        }