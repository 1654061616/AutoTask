from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QToolBar, QStatusBar, QSplitter,
                               QTreeWidget, QTreeWidgetItem, QTabWidget,
                               QTextEdit, QLabel, QComboBox, QLineEdit,
                               QGroupBox, QGridLayout, QFormLayout, QSpinBox, QDoubleSpinBox,
                               QCheckBox, QListWidget, QListWidgetItem,
                               QFileDialog, QMessageBox, QProgressBar)
from PySide6.QtGui import QIcon, QAction, QFont
from PySide6.QtCore import Qt, QSize, Signal, Slot
import sys
import os

class MainWindow(QMainWindow):
    flow_loaded = Signal(dict)
    step_selected = Signal(dict)
    flow_started = Signal()
    flow_stopped = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoFlow - 自动化操作软件")
        self.setGeometry(100, 100, 1400, 900)
        self.init_ui()
    
    def init_ui(self):
        self.create_menu_bar()
        self.create_tool_bar()
        self.create_status_bar()
        self.create_central_widget()
    
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("文件(&F)")
        new_action = QAction("新建流程", self)
        open_action = QAction("打开流程", self)
        save_action = QAction("保存流程", self)
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
        main_layout.setSpacing(5)
        
        left_splitter = QSplitter(Qt.Vertical)
        
        self.step_tree = QTreeWidget()
        self.step_tree.setHeaderLabel("步骤列表")
        self.step_tree.setFixedWidth(280)
        
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setPlaceholderText("运行日志将显示在这里...")
        left_splitter.addWidget(self.step_tree)
        left_splitter.addWidget(self.log_panel)
        left_splitter.setSizes([400, 300])
        
        right_splitter = QSplitter(Qt.Vertical)
        
        self.tool_box_panel = QGroupBox("工具箱")
        tool_box_layout = QVBoxLayout(self.tool_box_panel)
        
        self.tool_list = QListWidget()
        tools = [
            ("mouse", "鼠标操作"),
            ("keyboard", "键盘操作"),
            ("image", "图片识别"),
            ("ocr", "文字识别"),
            ("window", "窗口操作"),
            ("excel", "Excel操作"),
            ("file", "文件操作"),
            ("condition", "条件判断"),
            ("loop", "循环"),
            ("wait", "等待"),
            ("log", "日志")
        ]
        for tool_id, tool_name in tools:
            item = QListWidgetItem(tool_name)
            item.setData(Qt.UserRole, tool_id)
            self.tool_list.addItem(item)
        
        tool_box_layout.addWidget(self.tool_list)
        
        self.properties_panel = QGroupBox("属性配置")
        properties_layout = QFormLayout(self.properties_panel)
        
        self.step_name_edit = QLineEdit()
        self.step_name_edit.setPlaceholderText("步骤名称")
        
        self.step_type_combo = QComboBox()
        step_types = [
            "mouse_click", "mouse_move", "mouse_drag", "mouse_scroll",
            "keyboard_type", "keyboard_press", "keyboard_hotkey",
            "wait", "image_find", "image_click", "image_exists",
            "ocr_find", "ocr_read",
            "if_else", "loop",
            "set_variable", "get_variable",
            "excel_read",
            "screenshot", "log",
            "window_find", "window_activate", "window_close"
        ]
        self.step_type_combo.addItems(step_types)
        
        properties_layout.addRow("步骤名称:", self.step_name_edit)
        properties_layout.addRow("步骤类型:", self.step_type_combo)
        
        right_splitter.addWidget(self.tool_box_panel)
        right_splitter.addWidget(self.properties_panel)
        right_splitter.setSizes([200, 400])
        
        main_layout.addWidget(left_splitter)
        main_layout.addWidget(right_splitter)
        
        self.tool_list.itemDoubleClicked.connect(self.on_tool_double_clicked)
    
    @Slot()
    def on_new_flow(self):
        self.log_panel.clear()
        self.step_tree.clear()
        self.status_label.setText("新建流程")
        QMessageBox.information(self, "新建流程", "已新建空白流程")
    
    @Slot()
    def on_open_flow(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开流程文件", "", "JSON文件 (*.json)"
        )
        if file_path:
            self.status_label.setText(f"打开流程: {os.path.basename(file_path)}")
            QMessageBox.information(self, "打开流程", f"已打开流程: {file_path}")
    
    @Slot()
    def on_save_flow(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存流程文件", "", "JSON文件 (*.json)"
        )
        if file_path:
            self.status_label.setText(f"已保存: {os.path.basename(file_path)}")
            QMessageBox.information(self, "保存成功", f"流程已保存到: {file_path}")
    
    @Slot()
    def on_run_flow(self):
        self.status_label.setText("运行中...")
        self.log_panel.append("开始执行流程...")
        self.flow_started.emit()
    
    @Slot()
    def on_stop_flow(self):
        self.status_label.setText("已停止")
        self.log_panel.append("流程已停止")
        self.flow_stopped.emit()
    
    @Slot(QListWidgetItem)
    def on_tool_double_clicked(self, item):
        tool_id = item.data(Qt.UserRole)
        tool_name = item.text()
        
        new_item = QTreeWidgetItem(self.step_tree)
        new_item.setText(0, tool_name)
        new_item.setData(0, Qt.UserRole, {"type": tool_id, "name": tool_name})
        
        self.status_label.setText(f"已添加步骤: {tool_name}")
        self.log_panel.append(f"添加步骤: {tool_name}")
    
    def add_log(self, message):
        self.log_panel.append(message)
    
    def update_progress(self, value):
        self.progress_bar.show()
        self.progress_bar.setValue(value)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()