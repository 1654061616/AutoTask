"""
节点工具栏 — 按分类展示可拖拽的节点类型
"""
from PySide6.QtWidgets import (QToolBar, QPushButton, QLabel, QWidget,
                               QVBoxLayout, QScrollArea, QGroupBox, QSizePolicy)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Signal

from .node_types import NODE_CATEGORIES, get_node_type
from gui.styles import Styles


class NodeToolbar(QWidget):
    """节点工具栏，按分类分组展示可拖拽到画布的节点按钮"""

    node_drag_started = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        content_widget = QWidget()
        content_widget.setStyleSheet(Styles.toolbar_bg())
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(8)
        content_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("      节点工具箱")
        title_label.setStyleSheet(Styles.toolbar_title())
        content_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(Styles.toolbar_scroll_area())
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        groups_widget = QWidget()
        groups_widget.setStyleSheet(Styles.toolbar_bg())
        groups_layout = QVBoxLayout(groups_widget)
        groups_layout.setSpacing(6)
        groups_layout.setContentsMargins(0, 0, 0, 0)

        for category_key, category_info in NODE_CATEGORIES.items():
            group = QGroupBox(category_info["name"])
            group.setStyleSheet(Styles.toolbar_group())

            group_layout = QVBoxLayout(group)
            group_layout.setSpacing(4)
            group_layout.setContentsMargins(8, 8, 8, 8)

            for node_type in category_info["nodes"]:
                node_info = get_node_type(node_type)
                btn = QPushButton(f"{node_info['icon']} {node_info['name']}")
                btn.setStyleSheet(Styles.toolbar_node_btn(node_info['color']))
                btn.clicked.connect(lambda checked, nt=node_type: self._on_node_clicked(nt))
                group_layout.addWidget(btn)

            groups_layout.addWidget(group)

        groups_layout.addStretch()
        scroll_area.setWidget(groups_widget)
        content_layout.addWidget(scroll_area)

        layout.addWidget(content_widget)

    def _on_node_clicked(self, node_type):
        self.node_drag_started.emit(node_type)