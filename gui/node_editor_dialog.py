from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QSplitter, QWidget, QStackedWidget,
                               QScrollArea, QSizePolicy)
from PySide6.QtCore import Qt, Signal
import uuid

from .node_graph import GraphScene, GraphView, NodeToolbar
from .step_panels import PANEL_MAP, get_panel_class


class NodeEditorDialog(QDialog):
    """节点编辑器对话框 - 独立弹窗用于编辑节点图"""

    def __init__(self, flow_data=None, parent=None):
        super().__init__(parent)
        self.flow_data = flow_data or {}
        self._selected_node = None
        self._current_panel = None
        self._init_ui()
        self._load_data()

    def _init_ui(self):
        task_name = self.flow_data.get("name", "未命名任务")
        self.setWindowTitle(f"节点编辑器 - {task_name}")
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowContextHelpButtonHint |
            Qt.WindowMaximizeButtonHint |
            Qt.WindowMinimizeButtonHint
        )
        self.resize(1400, 800)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.setChildrenCollapsible(False)

        self.node_toolbar = NodeToolbar()
        self.node_toolbar.setFixedWidth(180)
        self.node_toolbar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        splitter.addWidget(self.node_toolbar)

        self.graph_scene = GraphScene()
        self.graph_view = GraphView(self.graph_scene)
        self.graph_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.addWidget(self.graph_view)

        self.config_panel = QWidget()
        self.config_panel.setFixedWidth(320)
        self.config_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.config_panel.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
            }
        """)
        self._init_config_panel()
        splitter.addWidget(self.config_panel)

        splitter.setSizes([180, 900, 320])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

        self.layout().addWidget(splitter)

        self.node_toolbar.node_drag_started.connect(self._on_node_drag_started)

    def _init_config_panel(self):
        layout = QVBoxLayout(self.config_panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        self.title_label = QLabel("节点配置")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding-bottom: 8px;
                border-bottom: 2px solid #27ae60;
            }
        """)
        layout.addWidget(self.title_label)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.empty_label = QLabel("请点击节点查看配置")
        self.empty_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #999;
                text-align: center;
                padding: 40px 20px;
            }
        """)
        self.empty_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.empty_label)

        self.panel_container = QStackedWidget()
        self.panel_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.panel_container)

        layout.addWidget(self.content_widget, 1)

        self.save_btn = QPushButton("保存配置")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 6px 20px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.save_btn.clicked.connect(self._on_save_config)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)

        self.ok_btn = QPushButton("确定")
        self.ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 8px 30px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        layout.addWidget(self.ok_btn)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 8px 30px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(self.cancel_btn)

        self._setup_node_selection()

        self.ok_btn.clicked.connect(self._on_ok_clicked)
        self.cancel_btn.clicked.connect(self.reject)

    def _on_ok_clicked(self):
        self._save_current_node_config()
        self.accept()

    def closeEvent(self, event):
        try:
            if hasattr(self, 'graph_scene') and self.graph_scene:
                try:
                    self.graph_scene.selectionChanged.disconnect(self._on_selection_changed)
                except Exception:
                    pass
            if hasattr(self, '_current_panel') and self._current_panel:
                try:
                    self._clear_current_panel()
                except Exception:
                    pass
        except Exception as e:
            print(f"关闭对话框时清理失败: {e}")
        event.accept()

    def cleanup(self):
        try:
            if hasattr(self, 'graph_scene') and self.graph_scene:
                try:
                    self.graph_scene.selectionChanged.disconnect(self._on_selection_changed)
                except Exception:
                    pass
                try:
                    self.graph_scene.clear_all()
                except Exception:
                    pass
        except Exception as e:
            print(f"清理场景失败: {e}")

    def _setup_node_selection(self):
        self.graph_scene.selectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        try:
            self._save_current_node_config()
            
            selected_nodes = self.graph_scene.get_selected_nodes()
            if selected_nodes:
                self._selected_node = selected_nodes[0]
                self._show_node_config(self._selected_node)
            else:
                self._selected_node = None
                self._clear_config()
        except Exception as e:
            print(f"选择变化处理失败: {e}")

    def _save_current_node_config(self):
        if self._selected_node and self._current_panel:
            try:
                if hasattr(self._current_panel, 'get_config'):
                    config = self._current_panel.get_config()
                    self._selected_node.update_params(config)
            except Exception as e:
                print(f"保存节点配置失败: {e}")

    def _show_node_config(self, node):
        self.empty_label.hide()

        panel_class = get_panel_class(node.node_type)
        if panel_class:
            self._clear_current_panel()

            panel = panel_class()
            panel.set_config(node.config)

            scroll_area = QScrollArea()
            scroll_area.setWidget(panel)
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    border: none;
                }
            """)
            scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.panel_container.addWidget(scroll_area)
            self.panel_container.setCurrentWidget(scroll_area)

            self._current_panel = panel
            self._current_scroll_area = scroll_area

            self.title_label.setText(f"节点配置 - {node.node_type}")
            self.save_btn.setEnabled(True)
        else:
            self._show_unsupported_message(node)

    def _show_unsupported_message(self, node):
        self._clear_current_panel()

        msg_label = QLabel(f"节点类型 '{node.node_type}' 暂无配置面板")
        msg_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #e74c3c;
                text-align: center;
                padding: 40px 20px;
            }
        """)
        msg_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._current_panel = msg_label
        self.panel_container.addWidget(msg_label)
        self.panel_container.setCurrentWidget(msg_label)

        self.title_label.setText(f"节点配置 - {node.node_type}")
        self.save_btn.setEnabled(False)

    def _clear_current_panel(self):
        if hasattr(self, '_current_scroll_area') and self._current_scroll_area:
            self.panel_container.removeWidget(self._current_scroll_area)
            self._current_scroll_area.deleteLater()
            self._current_scroll_area = None
        elif self._current_panel:
            self.panel_container.removeWidget(self._current_panel)
            self._current_panel.deleteLater()
        self._current_panel = None

    def _clear_config(self):
        self.empty_label.show()

        if self._current_panel:
            self.panel_container.removeWidget(self._current_panel)
            self._current_panel.deleteLater()
            self._current_panel = None

        self.title_label.setText("节点配置")
        self.save_btn.setEnabled(False)

    def _on_save_config(self):
        if self._selected_node and self._current_panel:
            try:
                config = self._current_panel.get_config()
                self._selected_node.update_params(config)
            except Exception as e:
                print(f"保存配置失败: {e}")

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
        node_count = len(self.graph_scene.nodes)
        x = 100 + (node_count % 5) * 230
        y = 100 + (node_count // 5) * 120
        node = self.graph_scene.add_node(node_type, x, y)
        self.graph_scene.clearSelection()
        node.setSelected(True)

    def get_graph_data(self):
        return self.graph_scene.to_json()
