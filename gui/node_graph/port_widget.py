from PySide6.QtWidgets import QGraphicsObject, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QColor, QBrush, QPen, QFont


class PortWidget(QGraphicsObject):
    port_clicked = Signal(object)

    PORT_SIZE = 16

    def __init__(self, port_type: str, label: str, parent_node, parent=None):
        super().__init__(parent)
        self.port_type = port_type
        self.label = label
        self.parent_node = parent_node
        self.connected_edges = []
        self._is_highlighted = False
        self._init_style()

    def _init_style(self):
        self.ellipse = QGraphicsEllipseItem(0, 0, self.PORT_SIZE, self.PORT_SIZE, self)

        if self.port_type == "in":
            fill_color = QColor("#ff9800")
        else:
            fill_color = QColor("#4caf50")

        self.ellipse.setBrush(QBrush(fill_color))
        self.ellipse.setPen(QPen(QColor("#ffffff"), 2))
        self.setCursor(Qt.PointingHandCursor)

        self.label_item = QGraphicsTextItem(self.label, self)
        self.label_item.setDefaultTextColor(QColor("#cccccc"))
        self.label_item.setFont(QFont("Arial", 9))

        if self.port_type == "in":
            self.label_item.setPos(self.PORT_SIZE + 4, -2)
        else:
            self.label_item.setPos(-self.label_item.boundingRect().width() - self.PORT_SIZE - 4, -2)

    def set_highlighted(self, highlighted):
        self._is_highlighted = highlighted
        if highlighted:
            self.ellipse.setBrush(QBrush(QColor("#00d4ff")))
            self.ellipse.setPen(QPen(QColor("#ffffff"), 3))
        else:
            if self.port_type == "in":
                self.ellipse.setBrush(QBrush(QColor("#ff9800")))
            else:
                self.ellipse.setBrush(QBrush(QColor("#4caf50")))
            self.ellipse.setPen(QPen(QColor("#ffffff"), 2))

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
        return self.mapToScene(self.boundingRect().center())

    def get_port_id(self):
        return f"{self.parent_node.node_id}_{self.port_type}_{self.label}"

    def boundingRect(self):
        return QRectF(0, 0, self.PORT_SIZE, self.PORT_SIZE)

    def paint(self, painter, option, widget=None):
        pass
