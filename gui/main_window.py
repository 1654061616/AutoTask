from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QToolBar, QStatusBar, QSplitter,
                               QTreeWidget, QTreeWidgetItem, QTableWidget,
                               QTableWidgetItem, QTextEdit, QLabel, QComboBox, 
                               QLineEdit, QGroupBox, QGridLayout, QFormLayout, 
                               QSpinBox, QDoubleSpinBox, QCheckBox, 
                               QFileDialog, QMessageBox, QProgressBar,
                               QInputDialog, QHeaderView)
from PySide6.QtGui import QIcon, QAction, QFont, QColor, QBrush, QPainter
from PySide6.QtCore import Qt, QSize, Signal, Slot
import sys
import os
import uuid
import json

from .step_editor import StepEditorDialog, STEP_TYPE_MAP
from .node_graph import GraphScene, GraphView, NodeToolbar

class MainWindow(QMainWindow):
    flow_loaded = Signal(dict)
    step_selected = Signal(dict)
    flow_started = Signal()
    flow_stopped = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoFlow - 自动化操作软件")
        self.setGeometry(100, 100, 1400, 900)
        self.flows = []
        self.current_flow = None
        self.init_ui()
    
    def init_ui(self):
        self.create_menu_bar()
        # self.create_tool_bar()
        self.create_status_bar()
        self.create_central_widget()
        self.apply_stylesheet()
    
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("文件(&F)")
        new_action = QAction("新建任务", self)
        open_action = QAction("打开任务", self)
        save_action = QAction("保存任务", self)
        save_as_action = QAction("另存为", self)
        exit_action = QAction("退出", self)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        new_action.triggered.connect(self.on_new_flow)
        open_action.triggered.connect(self.on_open_flow)
        save_action.triggered.connect(self.on_save_flow)
        exit_action.triggered.connect(self.close)
    
    def create_tool_bar(self):
        tool_bar = QToolBar("主工具栏")
        tool_bar.setIconSize(QSize(24, 24))
        self.addToolBar(tool_bar)
        
        new_icon = QIcon.fromTheme("document-new")
        open_icon = QIcon.fromTheme("document-open")
        save_icon = QIcon.fromTheme("document-save")
        run_icon = QIcon.fromTheme("media-play")
        stop_icon = QIcon.fromTheme("media-stop")
        
        tool_bar.addAction(new_icon, "新建", self.on_new_flow)
        tool_bar.addAction(open_icon, "打开", self.on_open_flow)
        tool_bar.addAction(save_icon, "保存", self.on_save_flow)
        tool_bar.addSeparator()
        tool_bar.addAction(run_icon, "运行", self.on_run_flow)
        tool_bar.addAction(stop_icon, "停止", self.on_stop_flow)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.hide()
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)
        
        self.splitter = QSplitter(Qt.Horizontal)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        btn_style = "background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;"
        self.new_task_btn = QPushButton("新建")
        self.new_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 12px; border-radius: 4px;")

        self.open_task_btn = QPushButton("导入")
        self.open_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 12px; border-radius: 4px;")
        
        self.save_task_btn = QPushButton("保存")
        self.save_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
        
        self.copy_task_btn = QPushButton("复制")
        self.copy_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")

        self.delete_task_btn = QPushButton("删除")
        self.delete_task_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
        
        self.task_list_group = QGroupBox("任务列表")
        task_list_layout = QVBoxLayout(self.task_list_group)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.new_task_btn)
        btn_layout.addWidget(self.open_task_btn)
        btn_layout.addWidget(self.save_task_btn)
        btn_layout.addWidget(self.copy_task_btn)
        btn_layout.addWidget(self.delete_task_btn)
     
        task_list_layout.addLayout(btn_layout)
        
        self.task_tree = QTreeWidget()
        self.task_tree.setHeaderLabels(["任务名称", "当前状态"])
        self.task_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.task_tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        task_list_layout.addWidget(self.task_tree)
        
        left_layout.addWidget(self.task_list_group)
        
        self.log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(self.log_group)
        
        log_header_layout = QHBoxLayout()
        log_header_layout.addWidget(QLabel("执行日志"))
        self.clear_log_btn = QPushButton("清空日志")
        log_header_layout.addStretch()
        log_header_layout.addWidget(self.clear_log_btn)
        log_layout.addLayout(log_header_layout)
        
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setPlaceholderText("运行日志将显示在这里...")
        log_layout.addWidget(self.log_panel)
        
        left_layout.addWidget(self.log_group)
        
        self.node_toolbar = NodeToolbar()
        left_layout.addWidget(self.node_toolbar)
        
        self.splitter.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        self.graph_scene = GraphScene()
        self.graph_view = GraphView(self.graph_scene)
        right_layout.addWidget(self.graph_view)
        
        action_btn_layout = QHBoxLayout()
        action_btn_layout.addStretch()
        
        self.start_task_btn = QPushButton("开始当前任务")
        self.start_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 8px 20px;")
        
        self.stop_task_btn = QPushButton("停止当前任务")
        self.stop_task_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 8px 20px;")
        
        self.save_config_btn = QPushButton("保存配置")
        self.save_config_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 8px 20px;")
        
        action_btn_layout.addWidget(self.start_task_btn)
        action_btn_layout.addWidget(self.stop_task_btn)
        action_btn_layout.addStretch()
        action_btn_layout.addWidget(self.save_config_btn)
        
        right_layout.addLayout(action_btn_layout)
        
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([350, 1050])
        
        main_layout.addWidget(self.splitter)
        
        self.new_task_btn.clicked.connect(self.on_new_flow)
        self.open_task_btn.clicked.connect(self.on_open_flow)
        self.save_task_btn.clicked.connect(self.on_save_flow)
        self.copy_task_btn.clicked.connect(self.on_copy_task)
        self.delete_task_btn.clicked.connect(self.on_delete_task)
        self.clear_log_btn.clicked.connect(self.on_clear_log)
        self.task_tree.itemClicked.connect(self.on_task_selected)
        self.task_tree.itemChanged.connect(self.on_task_name_changed)
        
        self.node_toolbar.node_drag_started.connect(self.on_node_drag_started)
        
        self.start_task_btn.clicked.connect(self.on_run_flow)
        self.stop_task_btn.clicked.connect(self.on_stop_flow)
        self.save_config_btn.clicked.connect(self.on_save_flow)
        
        self.load_default_tasks()
    
    def load_default_tasks(self):
        default_tasks = [
            {"id": "1", "name": "AI自动回复", "status": "已停止", "steps": []},
            {"id": "2", "name": "AI自动回复2", "status": "已停止", "steps": []},
            {"id": "3", "name": "导入的任务", "status": "已停止", "steps": []},
            {"id": "4", "name": "微信定时任务1314", "status": "定时执行中", "steps": [
                {"type": "键盘热键", "description": "CTRL+ALT+W", "params": "键盘热键: CTRL+ALT+W...", "delay": 0},
                {"type": "鼠标点击", "description": "左键双击", "params": "图片: CTRL+ALT+W...", "delay": 0},
                {"type": "文本输入", "description": "今天是2025年8月...", "params": "文本: 今天是2025年8月...", "delay": 0},
                {"type": "键盘热键", "description": "ENTER", "params": "键盘热键: ENTER", "delay": 0},
                {"type": "键盘热键", "description": "WIN+D", "params": "键盘热键: WIN+D", "delay": 0},
            ]}
        ]
        
        for task in default_tasks:
            self.add_task_to_tree(task)
    
    def add_task_to_tree(self, task):
        item = QTreeWidgetItem(self.task_tree)
        item.setText(0, task["name"])
        item.setText(1, task["status"])
        item.setData(0, Qt.UserRole, task)
        
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        
        status = task["status"]
        if "执行中" in status:
            item.setBackground(0, QBrush(QColor("#e8f5e9")))
            item.setBackground(1, QBrush(QColor("#c8e6c9")))
        else:
            item.setBackground(0, QBrush(QColor("#ffffff")))
            item.setBackground(1, QBrush(QColor("#ffebee")))
    
    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 2px;
                padding: 0 2px 0 2px;
            }
            QPushButton {
                padding: 5px 15px;
                border-radius: 4px;
                border: 1px solid #ccc;
                background-color: #ffffff;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QTreeWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                alternate-background-color: #f9f9f9;
                show-decoration-selected: 1;
            }
            QTreeWidget::item {
                padding: 6px 4px;
                height: 28px;
            }
            QTreeWidget::item:edit {
                background-color: #ffffff;
                color: #000000;
            }
            QTreeWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTreeWidget::item:selected:edit {
                background-color: #ffffff;
                color: #000000;
            }
            QTreeWidget QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #3498db;
                padding: 2px;
                margin: 1px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                gridline-color: #eee;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #ddd;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #3498db;
            }
        """)
    
    @Slot()
    def on_new_flow(self):
        flow_name, ok = QInputDialog.getText(self, "新建任务", "输入任务名称:")
        if ok and flow_name.strip():
            name = flow_name.strip()
        else:
            name = f"任务_{len(self.task_tree.findItems('', Qt.MatchContains)) + 1}"
        
        task = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "status": "已停止",
            "steps": [],
            "file_path": None
        }
        
        self.add_task_to_tree(task)
        self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
        self.status_label.setText(f"已新建任务: {name}")
        self.log_panel.append(f"新建任务: {name}")
    
    @Slot()
    def on_copy_task(self):
        current_item = self.task_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "复制失败", "请先选择一个任务")
            return
        
        task = current_item.data(0, Qt.UserRole)
        new_task = {
            "id": str(uuid.uuid4())[:8],
            "name": task["name"] + " (复制)",
            "status": "已停止",
            "steps": [dict(s) for s in task.get("steps", [])],
            "file_path": None
        }
        
        self.add_task_to_tree(new_task)
        self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
        self.status_label.setText(f"已复制任务: {new_task['name']}")
        self.log_panel.append(f"复制任务: {new_task['name']}")
    
    @Slot()
    def on_delete_task(self):
        current_item = self.task_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "删除失败", "请先选择一个任务")
            return
        
        task = current_item.data(0, Qt.UserRole)
        reply = QMessageBox.question(
            self, "确认删除", f"确定要删除任务 '{task['name']}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            index = self.task_tree.indexOfTopLevelItem(current_item)
            if index != -1:
                self.task_tree.takeTopLevelItem(index)
                self.status_label.setText(f"已删除任务: {task['name']}")
                self.log_panel.append(f"删除任务: {task['name']}")
                self.graph_scene.clear_all()
    
    @Slot(QTreeWidgetItem, int)
    def on_task_name_changed(self, item, column):
        if column == 0:
            task = item.data(0, Qt.UserRole)
            if task:
                old_name = task["name"]
                new_name = item.text(0)
                task["name"] = new_name
                item.setData(0, Qt.UserRole, task)
                
                self.log_panel.append(f"任务重命名: {old_name} -> {new_name}")
    
    @Slot()
    def on_open_flow(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开任务文件", "", "JSON文件 (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    flow_data = json.load(f)
                
                flow_name = flow_data.get("name", os.path.basename(file_path))
                task = {
                    "id": flow_data.get("id", str(uuid.uuid4())[:8]),
                    "name": flow_name,
                    "status": "已停止",
                    "nodes": flow_data.get("nodes", []),
                    "edges": flow_data.get("edges", []),
                    "file_path": file_path
                }
                
                self.add_task_to_tree(task)
                self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
                
                self.load_nodes_from_flow(flow_data)
                
                self.status_label.setText(f"打开任务: {flow_name}")
                self.log_panel.append(f"打开任务: {flow_name}")
            except Exception as e:
                QMessageBox.warning(self, "打开失败", f"无法打开任务文件: {str(e)}")
    
    @Slot()
    def on_save_flow(self):
        current_item = self.task_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "保存失败", "请先选择一个任务")
            return
        
        task = current_item.data(0, Qt.UserRole)
        file_path = task.get("file_path")
        
        if not file_path:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存任务文件", "", "JSON文件 (*.json)"
            )
        
        if file_path:
            try:
                graph_data = self.graph_scene.to_json()
                
                save_data = {
                    "id": task.get("id", ""),
                    "name": task.get("name", ""),
                    "version": "1.0",
                    "status": task.get("status", "已停止"),
                    "nodes": graph_data.get("nodes", []),
                    "edges": graph_data.get("edges", []),
                    "file_path": file_path
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, indent=2, ensure_ascii=False)
                
                task["file_path"] = file_path
                task["nodes"] = save_data["nodes"]
                task["edges"] = save_data["edges"]
                current_item.setData(0, Qt.UserRole, task)
                
                self.status_label.setText(f"已保存: {os.path.basename(file_path)}")
                self.log_panel.append(f"保存任务: {save_data['name']}")
            except Exception as e:
                QMessageBox.warning(self, "保存失败", f"无法保存任务文件: {str(e)}")
    
    @Slot()
    def on_run_flow(self):
        current_item = self.task_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "运行失败", "请先选择一个任务")
            return
        
        task = current_item.data(0, Qt.UserRole)
        task["status"] = "执行中"
        current_item.setText(1, "执行中")
        current_item.setBackground(0, QBrush(QColor("#e8f5e9")))
        current_item.setBackground(1, QBrush(QColor("#c8e6c9")))
        current_item.setData(0, Qt.UserRole, task)
        
        self.task_status_label.setText("执行中")
        self.task_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.status_label.setText("运行中...")
        self.log_panel.append(f"开始执行任务: {task['name']}")
        self.flow_started.emit()
    
    @Slot()
    def on_stop_flow(self):
        current_item = self.task_tree.currentItem()
        if current_item:
            task = current_item.data(0, Qt.UserRole)
            task["status"] = "已停止"
            current_item.setText(1, "已停止")
            current_item.setBackground(0, QBrush(QColor("#ffffff")))
            current_item.setBackground(1, QBrush(QColor("#ffebee")))
            current_item.setData(0, Qt.UserRole, task)
            
            self.task_status_label.setText("已停止")
            self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.status_label.setText("已停止")
            self.log_panel.append(f"停止任务: {task['name']}")
        
        self.flow_stopped.emit()
    
    @Slot(QTreeWidgetItem, int)
    def on_task_selected(self, item, column):
        task = item.data(0, Qt.UserRole)
        if task:
            self.current_flow = task
            
            status = task.get("status", "")
            if "执行中" in status:
                pass
            else:
                pass
            
            self.load_nodes_from_flow(task)
            self.log_panel.append(f"选择任务: {task['name']}")
    
    def load_steps_to_table(self, steps):
        self.step_table.setRowCount(0)
        for step in steps:
            row = self.step_table.rowCount()
            self.step_table.insertRow(row)
            
            step_type = step.get("type", "")
            step_name = STEP_TYPE_MAP.get(step_type, step_type)
            
            description = step.get("description", "")
            
            params = step.get("params", {})
            if isinstance(params, dict):
                params_str = str(params)
                delay = params.get("delay", 0)
            else:
                params_str = str(params)
                delay = step.get("delay", 0)
            
            type_item = QTableWidgetItem(step_name)
            desc_item = QTableWidgetItem(description)
            params_item = QTableWidgetItem(params_str)
            delay_item = QTableWidgetItem(str(delay))
            
            type_item.setTextAlignment(Qt.AlignCenter)
            delay_item.setTextAlignment(Qt.AlignCenter)
            
            type_item.setData(Qt.UserRole, step_type)
            
            self.step_table.setItem(row, 0, type_item)
            self.step_table.setItem(row, 1, desc_item)
            self.step_table.setItem(row, 2, params_item)
            self.step_table.setItem(row, 3, delay_item)
            
            self.apply_step_row_style(row)
    
    def apply_step_row_style(self, row):
        type_item = self.step_table.item(row, 0)
        step_type = type_item.data(Qt.UserRole) if type_item else ""
        
        type_colors = {
            "mouse_click": "#b3e5fc",
            "mouse_move": "#b3e5fc",
            "mouse_drag": "#b3e5fc",
            "mouse_scroll": "#b3e5fc",
            "keyboard_type": "#c8e6c9",
            "keyboard_press": "#f8bbd9",
            "keyboard_hotkey": "#f8bbd9",
            "image_find": "#e1bee7",
            "image_click": "#e1bee7",
            "image_exists": "#e1bee7",
            "window_find": "#b2dfdb",
            "window_activate": "#b2dfdb",
            "window_close": "#b2dfdb",
            "window_position": "#b2dfdb",
            "excel_read": "#ffcc80",
            "wait": "#fff9c4",
            "if_else": "#ffcdd2",
            "loop": "#e0e0e0",
            "log": "#f5f5f5",
            "label": "#e0e0e0",
            "goto": "#e0e0e0",
            "set_variable": "#bbdefb",
            "get_variable": "#bbdefb",
        }
        
        color = type_colors.get(step_type, "#ffffff")
        for col in range(4):
            item = self.step_table.item(row, col)
            if item:
                item.setBackground(QBrush(QColor(color)))
    
    @Slot()
    def on_add_step(self):
        dialog = StepEditorDialog(parent=self)
        dialog.setWindowTitle("添加步骤")
        
        def on_step_saved(step_data):
            row = self.step_table.rowCount()
            self.step_table.insertRow(row)
            
            step_type = step_data.get("type", "")
            step_name = STEP_TYPE_MAP.get(step_type, step_type)
            description = step_data.get("description", "")
            params = step_data.get("params", {})
            delay = params.get("delay", 0)
            
            type_item = QTableWidgetItem(step_name)
            desc_item = QTableWidgetItem(description)
            params_item = QTableWidgetItem(str(params))
            delay_item = QTableWidgetItem(str(delay))
            
            type_item.setTextAlignment(Qt.AlignCenter)
            delay_item.setTextAlignment(Qt.AlignCenter)
            
            type_item.setData(Qt.UserRole, step_type)
            
            self.step_table.setItem(row, 0, type_item)
            self.step_table.setItem(row, 1, desc_item)
            self.step_table.setItem(row, 2, params_item)
            self.step_table.setItem(row, 3, delay_item)
            
            self.apply_step_row_style(row)
            self.log_panel.append(f"添加步骤: {step_name}")
        
        dialog.step_saved.connect(on_step_saved)
        dialog.exec()
    
    @Slot()
    def on_edit_step(self):
        current_row = self.step_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "编辑失败", "请先选择一个步骤")
            return
        
        type_item = self.step_table.item(current_row, 0)
        step_type = type_item.data(Qt.UserRole) if type_item else ""
        description = self.step_table.item(current_row, 1).text() if self.step_table.item(current_row, 1) else ""
        params_text = self.step_table.item(current_row, 2).text() if self.step_table.item(current_row, 2) else ""
        delay = self.step_table.item(current_row, 3).text() if self.step_table.item(current_row, 3) else "0"
        
        try:
            params = eval(params_text) if params_text else {}
        except:
            params = {}
        
        step_data = {
            "type": step_type,
            "description": description,
            "params": params
        }
        
        dialog = StepEditorDialog(step_type=step_type, step_data=step_data, parent=self)
        dialog.setWindowTitle("编辑步骤")
        
        def on_step_saved(updated_data):
            updated_type = updated_data.get("type", "")
            updated_name = STEP_TYPE_MAP.get(updated_type, updated_type)
            updated_desc = updated_data.get("description", "")
            updated_params_dict = updated_data.get("params", {})
            updated_params = str(updated_params_dict)
            updated_delay = updated_params_dict.get("delay", 0)
            
            type_item = QTableWidgetItem(updated_name)
            type_item.setTextAlignment(Qt.AlignCenter)
            type_item.setData(Qt.UserRole, updated_type)
            
            desc_item = QTableWidgetItem(updated_desc)
            params_item = QTableWidgetItem(updated_params)
            delay_item = QTableWidgetItem(str(updated_delay))
            delay_item.setTextAlignment(Qt.AlignCenter)
            
            self.step_table.setItem(current_row, 0, type_item)
            self.step_table.setItem(current_row, 1, desc_item)
            self.step_table.setItem(current_row, 2, params_item)
            self.step_table.setItem(current_row, 3, delay_item)
            
            self.apply_step_row_style(current_row)
            self.log_panel.append(f"编辑步骤: {updated_name}")
        
        dialog.step_saved.connect(on_step_saved)
        dialog.exec()
    
    @Slot()
    def on_copy_step(self):
        current_row = self.step_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "复制失败", "请先选择一个步骤")
            return
        
        step_type = self.step_table.item(current_row, 0).text()
        description = self.step_table.item(current_row, 1).text()
        params = self.step_table.item(current_row, 2).text()
        delay = self.step_table.item(current_row, 3).text()
        
        new_row = current_row + 1
        self.step_table.insertRow(new_row)
        
        type_item = QTableWidgetItem(step_type + " (复制)")
        desc_item = QTableWidgetItem(description)
        params_item = QTableWidgetItem(params)
        delay_item = QTableWidgetItem(delay)
        
        type_item.setTextAlignment(Qt.AlignCenter)
        delay_item.setTextAlignment(Qt.AlignCenter)
        
        self.step_table.setItem(new_row, 0, type_item)
        self.step_table.setItem(new_row, 1, desc_item)
        self.step_table.setItem(new_row, 2, params_item)
        self.step_table.setItem(new_row, 3, delay_item)
        
        self.apply_step_row_style(new_row)
        self.log_panel.append(f"复制步骤: {step_type}")
    
    @Slot()
    def on_delete_step(self):
        current_row = self.step_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "删除失败", "请先选择一个步骤")
            return
        
        step_type = self.step_table.item(current_row, 0).text()
        reply = QMessageBox.question(
            self, "确认删除", f"确定要删除步骤 '{step_type}' 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.step_table.removeRow(current_row)
            self.log_panel.append(f"删除步骤: {step_type}")
    
    @Slot()
    def on_move_up(self):
        current_row = self.step_table.currentRow()
        if current_row > 0:
            self.step_table.insertRow(current_row - 1)
            for col in range(4):
                item = self.step_table.takeItem(current_row + 1, col)
                if item:
                    self.step_table.setItem(current_row - 1, col, item)
            self.step_table.removeRow(current_row + 1)
            self.step_table.setCurrentRow(current_row - 1)
    
    @Slot()
    def on_move_down(self):
        current_row = self.step_table.currentRow()
        if current_row < self.step_table.rowCount() - 1:
            self.step_table.insertRow(current_row + 2)
            for col in range(4):
                item = self.step_table.takeItem(current_row, col)
                if item:
                    self.step_table.setItem(current_row + 2, col, item)
            self.step_table.removeRow(current_row)
            self.step_table.setCurrentRow(current_row + 1)
    
    @Slot()
    def on_clear_log(self):
        self.log_panel.clear()
        self.log_panel.append("日志已清空")
    
    @Slot(str)
    def on_node_drag_started(self, node_type):
        self.graph_scene.add_node(node_type, 100, 100)
        self.log_panel.append(f"添加节点: {node_type}")
    
    def load_nodes_from_flow(self, flow_data):
        self.graph_scene.clear_all()
        
        nodes = flow_data.get("nodes", [])
        edges = flow_data.get("edges", [])
        
        node_map = {}
        for node_data in nodes:
            node = self.graph_scene.add_node(
                node_data.get("type", "wait"),
                node_data.get("x", 0),
                node_data.get("y", 0),
                node_data.get("config", {})
            )
            node.set_node_id(node_data.get("id", str(uuid.uuid4())))
            node_map[node_data.get("id", "")] = node
        
        for edge_data in edges:
            source_node = node_map.get(edge_data["source_node"])
            target_node = node_map.get(edge_data["target_node"])
            if source_node and target_node:
                source_port = source_node.get_output_port(edge_data["source_port"])
                target_port = target_node.get_input_port(edge_data["target_port"])
                if source_port and target_port:
                    self.graph_scene.add_edge(source_port, target_port)
    
    def add_log(self, message):
        self.log_panel.append(message)
        self.log_panel.verticalScrollBar().setValue(
            self.log_panel.verticalScrollBar().maximum()
        )
    
    def update_progress(self, value):
        self.progress_bar.show()
        self.progress_bar.setValue(value)

from PySide6.QtWidgets import QDialog

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()