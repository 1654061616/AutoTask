"""
节点图视图 — 支持缩放和平移的图形视图
"""
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QTransform, QPainter, QMouseEvent

class GraphView(QGraphicsView):
    """节点图视图，支持鼠标滚轮缩放和右键平移"""
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self._init_style()
        self._init_interaction()

    def _init_style(self):
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def _init_interaction(self):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        zoom_factor = 1.15 if event.angleDelta().y() > 0 else 0.87
        current_scale = self.transform().m11()
        new_scale = current_scale * zoom_factor
        
        if 0.2 <= new_scale <= 5.0:
            self.scale(zoom_factor, zoom_factor)
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            event = QMouseEvent(event.type(), event.localPos(), 
                               Qt.LeftButton, Qt.LeftButton, event.modifiers())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.scene().delete_selected()
        elif event.key() == Qt.Key_Escape:
            self.scene().clearSelection()
        else:
            super().keyPressEvent(event)

    def zoom_in(self):
        self.scale(1.15, 1.15)

    def zoom_out(self):
        self.scale(0.87, 0.87)

    def reset_view(self):
        self.resetTransform()

    def fit_to_view(self):
        scene_rect = self.scene().sceneRect()
        if not scene_rect.isNull():
            self.fitInView(scene_rect, Qt.KeepAspectRatio)

    def center_on(self, x, y):
        self.centerOn(x, y)