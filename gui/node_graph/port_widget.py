"""
端口控件 — 节点上的输入/输出端口，支持拖拽连线
"""
from PySide6.QtWidgets import QGraphicsObject, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF, Signal, QPointF
from PySide6.QtGui import QColor, QBrush, QPen, QFont, QPainterPath


class PortWidget(QGraphicsObject):
    """端口控件，支持点击连线和高亮显示"""

    port_clicked = Signal(object)

    PORT_SIZE = 16
    PORT_MARGIN = 4
    DRAG_THRESHOLD = 3

    def __init__(self, port_type: str, label: str, parent_node, parent=None):
        super().__init__(parent)
        self.port_type = port_type
        self.label = label
        self.parent_node = parent_node
        self.connected_edges = []
        self._is_highlighted = False
        self._dragging = False
        self._press_pos = None
        self._init_style()

        self.setFlag(QGraphicsObject.ItemIsMovable, True)
        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges, True)

    def _init_style(self):
        self.ellipse = QGraphicsEllipseItem(0, 0, self.PORT_SIZE, self.PORT_SIZE, self)
        self.setZValue(20)

        if self.port_type == "in":
            fill_color = QColor("#ff9800")
        else:
            if self.label == "False":
                fill_color = QColor("#f44336")
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
                if self.label == "False":
                    self.ellipse.setBrush(QBrush(QColor("#f44336")))
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
        self._press_pos = event.pos()
        self._dragging = False
        event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._press_pos is not None and not self._dragging:
            delta = event.pos() - self._press_pos
            if (abs(delta.x()) > self.DRAG_THRESHOLD or
                    abs(delta.y()) > self.DRAG_THRESHOLD):
                self._dragging = True
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not self._dragging and self._press_pos is not None:
            self.port_clicked.emit(self)
        self._press_pos = None
        self._dragging = False
        super().mouseReleaseEvent(event)

    def _update_connected_edges(self):
        for edge in self.connected_edges[:]:
            try:
                edge.update_path()
            except Exception:
                pass

    def _snap_to_nearest_edge(self):
        if self.parent_node is None:
            return
        node_w = self.parent_node.node_width
        node_h = self.parent_node.node_height
        half = self.PORT_SIZE / 2

        cx = self.pos().x() + half
        cy = self.pos().y() + half

        dist_left = abs(cx)
        dist_right = abs(cx - node_w)
        dist_top = abs(cy)
        dist_bottom = abs(cy - node_h)

        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)

        if min_dist == dist_left:
            cx = 0
            cy = max(0, min(cy, node_h))
        elif min_dist == dist_right:
            cx = node_w
            cy = max(0, min(cy, node_h))
        elif min_dist == dist_top:
            cy = 0
            cx = max(0, min(cx, node_w))
        else:
            cy = node_h
            cx = max(0, min(cx, node_w))

        self.setPos(cx - half, cy - half)

    def _constrain_to_edge(self, pos):
        if self.parent_node is None:
            return pos
        node_w = self.parent_node.node_width
        node_h = self.parent_node.node_height
        half = self.PORT_SIZE / 2

        cx = pos.x() + half
        cy = pos.y() + half

        dist_left = abs(cx)
        dist_right = abs(cx - node_w)
        dist_top = abs(cy)
        dist_bottom = abs(cy - node_h)

        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)

        if min_dist == dist_left:
            cx = 0
            cy = max(0, min(cy, node_h))
        elif min_dist == dist_right:
            cx = node_w
            cy = max(0, min(cy, node_h))
        elif min_dist == dist_top:
            cy = 0
            cx = max(0, min(cx, node_w))
        else:
            cy = node_h
            cx = max(0, min(cx, node_w))

        return QPointF(cx - half, cy - half)

    def itemChange(self, change, value):
        if change == QGraphicsObject.ItemPositionChange:
            value = self._constrain_to_edge(value)
        elif change == QGraphicsObject.ItemPositionHasChanged:
            self._update_connected_edges()
        return super().itemChange(change, value)

    def get_global_pos(self):
        return self.mapToScene(self.boundingRect().center())

    def get_port_id(self):
        return f"{self.parent_node.node_id}_{self.port_type}_{self.label}"

    def boundingRect(self):
        m = self.PORT_MARGIN
        total = self.PORT_SIZE + 2 * m
        return QRectF(-m, -m, total, total)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget=None):
        pass