from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QColor, QBrush, QPen, QFont

class PortWidget(QGraphicsEllipseItem):
    port_clicked = Signal(object)

    def __init__(self, port_type: str, label: str, parent_node, parent=None):
        super().__init__(0, 0, 12, 12, parent)
        self.port_type = port_type
        self.label = label
        self.parent_node = parent_node
        self.connected_edges = []
        self._is_highlighted = False
        self._init_style()
        self._add_label()

    def _init_style(self):
        self.setBrush(QBrush(QColor("#5a5aff")))
        self.setPen(QPen(QColor("#5a5aff"), 2))
        self.setCursor(Qt.PointingHandCursor)
        self.setZValue(10)

    def _add_label(self):
        self.label_item = QGraphicsTextItem(self.label, self)
        self.label_item.setDefaultTextColor(QColor("#888"))
        self.label_item.setFont(QFont("Arial", 10))
        if self.port_type == "in":
            self.label_item.setPos(16, -5)
        else:
            self.label_item.setPos(-self.label_item.boundingRect().width() - 8, -5)

    def set_highlighted(self, highlighted):
        self._is_highlighted = highlighted
        if highlighted:
            self.setBrush(QBrush(QColor("#00d4ff")))
            self.setPen(QPen(QColor("#00d4ff"), 2))
        else:
            self.setBrush(QBrush(QColor("#5a5aff")))
            self.setPen(QPen(QColor("#5a5aff"), 2))

    def can_connect(self, other_port):
        if self.port_type == other_port.port_type:
            return False
        if self.parent_node is not None and other_port.parent_node is not None:
            if self.parent_node == other_port.parent_node:
                return False
        return True

    def add_edge(self, edge):
        if edge not in self.connected_edges:
            self.connected_edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.connected_edges:
            self.connected_edges.remove(edge)

    def has_connections(self):
        return len(self.connected_edges) > 0

    def mousePressEvent(self, event):
        self.port_clicked.emit(self)
        super().mousePressEvent(event)

    def get_global_pos(self):
        return self.mapToScene(self.rect().center())

    def get_port_id(self):
        return f"{self.parent_node.node_id}_{self.port_type}_{self.label}"