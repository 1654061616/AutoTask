from PySide6.QtWidgets import (QToolBar, QPushButton, QLabel, QWidget,
                               QVBoxLayout, QScrollArea, QGroupBox, QSizePolicy)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Signal

from .node_types import NODE_CATEGORIES, get_node_type


class NodeToolbar(QWidget):
    node_drag_started = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #1a1a2e;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(8)
        content_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("节点工具箱")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #fff;")
        content_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #2a2a4a;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a6e;
                border-radius: 4px;
            }
        """)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        groups_widget = QWidget()
        groups_widget.setStyleSheet("background-color: #1a1a2e;")
        groups_layout = QVBoxLayout(groups_widget)
        groups_layout.setSpacing(6)
        groups_layout.setContentsMargins(0, 0, 0, 0)

        for category_key, category_info in NODE_CATEGORIES.items():
            group = QGroupBox(category_info["name"])
            group.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    font-size: 12px;
                    color: #aaa;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    margin-top: 8px;
                    padding-top: 8px;
                    background-color: transparent;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 8px;
                    padding: 0 4px;
                }
            """)

            group_layout = QVBoxLayout(group)
            group_layout.setSpacing(4)
            group_layout.setContentsMargins(8, 8, 8, 8)

            for node_type in category_info["nodes"]:
                node_info = get_node_type(node_type)
                btn = QPushButton(f"{node_info['icon']} {node_info['name']}")
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #2a2a4a;
                        color: #fff;
                        border: 1px solid {node_info['color']};
                        border-radius: 4px;
                        padding: 6px 8px;
                        text-align: left;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {node_info['color']};
                        border-color: {node_info['color']};
                    }}
                """)
                btn.clicked.connect(lambda checked, nt=node_type: self._on_node_clicked(nt))
                group_layout.addWidget(btn)

            groups_layout.addWidget(group)

        groups_layout.addStretch()
        scroll_area.setWidget(groups_widget)
        content_layout.addWidget(scroll_area)

        layout.addWidget(content_widget)

    def _on_node_clicked(self, node_type):
        self.node_drag_started.emit(node_type)