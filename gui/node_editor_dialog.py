from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QSplitter, QWidget)
from PySide6.QtCore import Qt, Signal
import uuid

from .node_graph import GraphScene, GraphView, NodeToolbar


class NodeEditorDialog(QDialog):
    """节点编辑器对话框 - 独立弹窗用于编辑节点图"""

    def __init__(self, flow_data=None, parent=None):
        super().__init__(parent)
        self.flow_data = flow_data or {}
        self._init_ui()
        self._load_data()

    def _init_ui(self):
        task_name = self.flow_data.get("name", "未命名任务")
        self.setWindowTitle(f"节点编辑器 - {task_name}")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(1200, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        splitter = QSplitter(Qt.Horizontal)

        self.node_toolbar = NodeToolbar()
        self.node_toolbar.setFixedWidth(200)
        splitter.addWidget(self.node_toolbar)

        self.graph_scene = GraphScene()
        self.graph_view = GraphView(self.graph_scene)
        splitter.addWidget(self.graph_view)

        splitter.setSizes([200, 1000])

        main_layout.addWidget(splitter)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.ok_btn = QPushButton("确定")
        self.ok_btn.setStyleSheet(
            "background-color: #27ae60; color: white; "
            "font-weight: bold; padding: 8px 30px; border-radius: 4px;"
        )

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet(
            "background-color: #e74c3c; color: white; "
            "font-weight: bold; padding: 8px 30px; border-radius: 4px;"
        )

        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(btn_layout)

        self.node_toolbar.node_drag_started.connect(self._on_node_drag_started)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
            }
        """)

    def _load_data(self):
        self.graph_scene.clear_all()

        nodes = self.flow_data.get("nodes", [])
        edges = self.flow_data.get("edges", [])

        node_map = {}
        for node_data in nodes:
            node = self.graph_scene.add_node(
                node_data.get("type", "wait"),
                node_data.get("x", 100),
                node_data.get("y", 100),
                node_data.get("config", {})
            )
            node.set_node_id(node_data.get("id", str(uuid.uuid4())))
            node_map[node_data.get("id", "")] = node

        for edge_data in edges:
            source_node = node_map.get(edge_data.get("source_node"))
            target_node = node_map.get(edge_data.get("target_node"))
            if source_node and target_node:
                source_port = source_node.get_output_port(edge_data.get("source_port", "输出"))
                target_port = target_node.get_input_port(edge_data.get("target_port", "输入"))
                if source_port and target_port:
                    self.graph_scene.add_edge(source_port, target_port)

    def _on_node_drag_started(self, node_type):
        self.graph_scene.add_node(node_type, 100, 100)

    def get_graph_data(self):
        return self.graph_scene.to_json()
