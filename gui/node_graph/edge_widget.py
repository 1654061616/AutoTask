from PySide6.QtWidgets import QGraphicsPathItem, QStyle
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPen, QBrush, QPainterPath, QPainterPathStroker

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
        
        self.update_path()

    def _init_style(self):
        self.setPen(QPen(QColor("#5a5aff"), 2))
        self.setBrush(Qt.NoBrush)
        self.setZValue(0)

    def update_path(self):
        try:
            if not hasattr(self, 'source_port') or not hasattr(self, 'target_port'):
                return
            start_point = self.source_port.get_global_pos()
            end_point = self.target_port.get_global_pos()
            
            path = QPainterPath()
            path.moveTo(start_point)
            
            dx = abs(end_point.x() - start_point.x())
            control_offset = min(dx * 0.5, 100)
            
            control_point1 = QPointF(start_point.x() + control_offset, start_point.y())
            control_point2 = QPointF(end_point.x() - control_offset, end_point.y())
            
            path.cubicTo(control_point1, control_point2, end_point)
            self.setPath(path)
        except Exception:
            pass

    def set_selected(self, selected):
        self.setSelected(selected)

    def itemChange(self, change, value):
        if change == QGraphicsPathItem.ItemSelectedChange:
            if value:
                self.setPen(QPen(QColor("#00d4ff"), 3))
                self.setZValue(10)
            else:
                self.setPen(QPen(QColor("#5a5aff"), 2))
                self.setZValue(0)
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
            "target_port": self.target_port.label
        }

    def disconnect(self):
        self.source_port.remove_edge(self)
        self.target_port.remove_edge(self)