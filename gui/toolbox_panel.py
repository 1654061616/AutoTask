from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QListWidget, QListWidgetItem,
                               QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt, Signal

class ToolboxPanel(QGroupBox):
    tool_selected = Signal(dict)
    
    def __init__(self):
        super().__init__("工具箱")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tool_list = QListWidget()
        self._load_tools()
        layout.addWidget(self.tool_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加到流程")
        button_layout.addWidget(self.add_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.tool_list.itemDoubleClicked.connect(self.on_tool_double_clicked)
        self.add_button.clicked.connect(self.on_add_button_clicked)
    
    def _load_tools(self):
        tools = [
            {"id": "mouse_click", "name": "鼠标点击", "category": "mouse"},
            {"id": "mouse_move", "name": "鼠标移动", "category": "mouse"},
            {"id": "mouse_drag", "name": "鼠标拖拽", "category": "mouse"},
            {"id": "mouse_scroll", "name": "鼠标滚动", "category": "mouse"},
            {"id": "keyboard_type", "name": "键盘输入", "category": "keyboard"},
            {"id": "keyboard_press", "name": "按键", "category": "keyboard"},
            {"id": "keyboard_hotkey", "name": "快捷键", "category": "keyboard"},
            {"id": "wait", "name": "等待", "category": "control"},
            {"id": "image_find", "name": "查找图片", "category": "image"},
            {"id": "image_click", "name": "点击图片", "category": "image"},
            {"id": "image_exists", "name": "图片存在判断", "category": "image"},
            {"id": "ocr_find", "name": "查找文字", "category": "ocr"},
            {"id": "ocr_read", "name": "读取文字", "category": "ocr"},
            {"id": "if_else", "name": "条件判断", "category": "control"},
            {"id": "loop", "name": "循环", "category": "control"},
            {"id": "set_variable", "name": "设置变量", "category": "variable"},
            {"id": "get_variable", "name": "获取变量", "category": "variable"},
            {"id": "excel_read", "name": "读取Excel", "category": "excel"},
            {"id": "screenshot", "name": "截图", "category": "image"},
            {"id": "log", "name": "日志输出", "category": "control"},
            {"id": "window_find", "name": "查找窗口", "category": "window"},
            {"id": "window_activate", "name": "激活窗口", "category": "window"},
            {"id": "window_close", "name": "关闭窗口", "category": "window"},
            {"id": "file_read", "name": "读取文件", "category": "file"},
            {"id": "file_write", "name": "写入文件", "category": "file"},
            {"id": "clipboard_copy", "name": "复制到剪贴板", "category": "clipboard"},
            {"id": "clipboard_paste", "name": "粘贴剪贴板", "category": "clipboard"},
        ]
        
        for tool in tools:
            item = QListWidgetItem(f"{tool['name']}")
            item.setData(Qt.UserRole, tool)
            self.tool_list.addItem(item)
    
    def on_tool_double_clicked(self, item):
        tool = item.data(Qt.UserRole)
        if tool:
            self.tool_selected.emit(tool)
    
    def on_add_button_clicked(self):
        current_item = self.tool_list.currentItem()
        if current_item:
            tool = current_item.data(Qt.UserRole)
            self.tool_selected.emit(tool)