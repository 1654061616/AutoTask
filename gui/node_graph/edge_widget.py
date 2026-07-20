from PySide6.QtWidgets import QGraphicsObject, QGraphicsPathItem, QStyle
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath, QPainterPathStroker


class ControlPointHandle(QGraphicsObject):
    SIZE = 10
    COLOR = QColor("#ffaa00")

    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self._edge = edge
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsObject.ItemIsMovable, True)
        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges, True)
        self.setCursor(Qt.CursorShape.SizeAllCursor)
        self.setZValue(10)
        self.setVisible(False)

    def boundingRect(self):
        return QRectF(-self.SIZE, -self.SIZE, self.SIZE * 2, self.SIZE * 2)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#cc8800"), 1.5))
        painter.setBrush(QBrush(self.COLOR))
        painter.drawEllipse(QPointF(0, 0), self.SIZE, self.SIZE)

    def hoverEnterEvent(self, event):
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.update()
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsObject.ItemPositionHasChanged:
            self._edge._on_handle_moved()
        return super().itemChange(change, value)


class EdgeWidget(QGraphicsPathItem):
    def __init__(self, source_port, target_port, parent=None):
        super().__init__(parent)
        self.source_port = source_port
        self.target_port = target_port
        self.source_node = source_port.parent_node
        self.target_node = target_port.parent_node

        self._init_style()

        self.setFlag(QGraphicsPathItem.ItemIsSelectable, True)

        source_port.add_edge(self)
        target_port.add_edge(self)

        self._cp1_offset = (0.25, 0.0)
        self._cp2_offset = (0.75, 0.0)

        self._cp1_handle = ControlPointHandle(self, self)
        self._cp2_handle = ControlPointHandle(self, self)

        self.update_path()

    def _init_style(self):
        self.setPen(QPen(QColor("#5a5aff"), 2))
        self.setBrush(Qt.NoBrush)
        self.setZValue(-1)

    def update_path(self):
        try:
            if not hasattr(self, 'source_port') or not hasattr(self, 'target_port'):
                return
            start_point = self.source_port.get_global_pos()
            end_point = self.target_port.get_global_pos()

            dx = end_point.x() - start_point.x()
            dy = end_point.y() - start_point.y()

            cp1 = QPointF(
                start_point.x() + dx * self._cp1_offset[0] + dy * self._cp1_offset[1],
                start_point.y() + dy * self._cp1_offset[0] - dx * self._cp1_offset[1]
            )
            cp2 = QPointF(
                start_point.x() + dx * self._cp2_offset[0] + dy * self._cp2_offset[1],
                start_point.y() + dy * self._cp2_offset[0] - dx * self._cp2_offset[1]
            )

            path = QPainterPath()
            path.moveTo(start_point)
            path.cubicTo(cp1, cp2, end_point)
            self.setPath(path)

            self._update_handles()
        except Exception:
            pass

    def set_selected(self, selected):
        self.setSelected(selected)

    def _update_handles(self):
        try:
            start_point = self.source_port.get_global_pos()
            end_point = self.target_port.get_global_pos()
            dx = end_point.x() - start_point.x()
            dy = end_point.y() - start_point.y()

            cp1_pos = QPointF(
                start_point.x() + dx * self._cp1_offset[0] + dy * self._cp1_offset[1],
                start_point.y() + dy * self._cp1_offset[0] - dx * self._cp1_offset[1]
            )
            cp2_pos = QPointF(
                start_point.x() + dx * self._cp2_offset[0] + dy * self._cp2_offset[1],
                start_point.y() + dy * self._cp2_offset[0] - dx * self._cp2_offset[1]
            )
            self._cp1_handle.setPos(cp1_pos)
            self._cp2_handle.setPos(cp2_pos)
        except Exception:
            pass

    def _on_handle_moved(self):
        try:
            start_point = self.source_port.get_global_pos()
            end_point = self.target_port.get_global_pos()
            dx = end_point.x() - start_point.x()
            dy = end_point.y() - start_point.y()

            denom = dx * dx + dy * dy
            if denom < 0.001:
                return

            cp1_pos = self._cp1_handle.pos()
            delta1_x = cp1_pos.x() - start_point.x()
            delta1_y = cp1_pos.y() - start_point.y()
            self._cp1_offset = (
                (dx * delta1_x + dy * delta1_y) / denom,
                (dy * delta1_x - dx * delta1_y) / denom
            )

            cp2_pos = self._cp2_handle.pos()
            delta2_x = cp2_pos.x() - start_point.x()
            delta2_y = cp2_pos.y() - start_point.y()
            self._cp2_offset = (
                (dx * delta2_x + dy * delta2_y) / denom,
                (dy * delta2_x - dx * delta2_y) / denom
            )

            self.update_path()
        except Exception:
            pass

    def itemChange(self, change, value):
        if change == QGraphicsPathItem.ItemSelectedChange:
            if value:
                self.setPen(QPen(QColor("#00d4ff"), 3))
                self.setZValue(5)
                self._cp1_handle.setVisible(True)
                self._cp2_handle.setVisible(True)
            else:
                self.setPen(QPen(QColor("#5a5aff"), 2))
                self.setZValue(-1)
                self._cp1_handle.setVisible(False)
                self._cp2_handle.setVisible(False)
        return super().itemChange(change, value)

    def shape(self):
        stroker = QPainterPathStroker()
        stroker.setWidth(10)
        return stroker.createStroke(self.path())

    def paint(self, painter, option, widget=None):
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)

    def to_json(self):
        return {
            "source_node": self.source_node.node_id,
            "source_port": self.source_port.label,
            "target_node": self.target_node.node_id,
            "target_port": self.target_port.label,
            "cp1": {"x": self._cp1_offset[0], "y": self._cp1_offset[1]},
            "cp2": {"x": self._cp2_offset[0], "y": self._cp2_offset[1]}
        }

    def from_json(self, data):
        cp1 = data.get("cp1", {"x": 0.25, "y": 0.0})
        cp2 = data.get("cp2", {"x": 0.75, "y": 0.0})
        self._cp1_offset = (cp1.get("x", 0.25), cp1.get("y", 0.0))
        self._cp2_offset = (cp2.get("x", 0.75), cp2.get("y", 0.0))
        self.update_path()

    def disconnect(self):
        self.source_port.remove_edge(self)
        self.target_port.remove_edge(self)