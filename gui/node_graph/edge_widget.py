from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPen, QPainterPath

class EdgeWidget(QGraphicsPathItem):
    def __init__(self, source_port, target_port):
        super().__init__()
        self.source_port = source_port
        self.target_port = target_port
        self.source_node = source_port.node
        self.target_node = target_port.node
        
        self._init_style()
        self.update_path()
        
        source_port.connected = True
        if target_port:
            target_port.connected = True

    def _init_style(self):
        pen = QPen(QColor("#4caf50"), 2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        self.setPen(pen)
        self.setZValue(-1)

    def update_path(self):
        if self.source_port and self.target_port:
            source_pos = self.source_port.get_global_pos()
            target_pos = self.target_port.get_global_pos()
            
            dx = abs(target_pos.x() - source_pos.x())
            control_offset = min(dx * 0.5, 100)
            
            path = QPainterPath()
            path.moveTo(source_pos)
            
            mid_x = (source_pos.x() + target_pos.x()) / 2
            path.cubicTo(
                QPointF(mid_x, source_pos.y()),
                QPointF(mid_x, target_pos.y()),
                target_pos
            )
            
            self.setPath(path)

    def to_json(self):
        return {
            "source_node": self.source_node.node_id,
            "source_port": self.source_port.index,
            "target_node": self.target_node.node_id,
            "target_port": self.target_port.index
        }