from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QComboBox, QPushButton, QStackedWidget,
                               QScrollArea)
from PySide6.QtCore import Qt, Signal
from .step_panels import PANEL_MAP, get_panel_class


STEP_TYPE_MAP = {
    "mouse_click": "鼠标点击",
    "mouse_move": "鼠标移动",
    "mouse_drag": "鼠标拖拽",
    "mouse_scroll": "鼠标滚动",
    "keyboard_type": "键盘输入",
    "keyboard_press": "按键操作",
    "keyboard_hotkey": "快捷键",
    "image_find": "查找图片",
    "image_click": "点击图片",
    "image_exists": "图片存在判断",
    "window_find": "查找窗口",
    "window_activate": "激活窗口",
    "window_close": "关闭窗口",
    "window_position": "窗口位置",
    "excel_read": "读取Excel",
    "wait": "等待",
    "if_else": "条件判断",
    "loop": "循环",
    "log": "日志",
    "label": "标记",
    "goto": "跳转",
    "set_variable": "设置变量",
    "get_variable": "获取变量",
}


class StepEditorDialog(QDialog):
    step_saved = Signal(dict)

    def __init__(self, step_type=None, step_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑步骤")
        self.setModal(True)
        self.resize(700, 600)
        
        self._step_type = step_type
        self._step_data = step_data or {}
        self._panels = {}
        
        self.init_ui()
        self.apply_stylesheet()
        
        if step_type:
            self.set_step_type(step_type)
            if step_data:
                self.load_step_data(step_data)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)
        
        type_label = QLabel("步骤类型:")
        type_label.setFixedWidth(80)
        type_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_layout.addWidget(type_label)
        
        self.type_combo = QComboBox()
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 150px;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
        """)
        
        for key, name in STEP_TYPE_MAP.items():
            self.type_combo.addItem(name, key)
        
        top_layout.addWidget(self.type_combo)
        top_layout.addStretch()
        
        main_layout.addLayout(top_layout)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.stacked_widget)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        
        main_layout.addWidget(self.scroll_area, 1)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()
        
        self.ok_btn = QPushButton("确定")
        self.ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 6px 20px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 6px 20px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(btn_layout)

        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        self.ok_btn.clicked.connect(self.on_ok)
        self.cancel_btn.clicked.connect(self.on_cancel)

        self._create_all_panels()

    def _create_all_panels(self):
        for step_type in STEP_TYPE_MAP.keys():
            panel_class = get_panel_class(step_type)
            if panel_class:
                panel = panel_class()
                self._panels[step_type] = panel
                self.stacked_widget.addWidget(panel)

    def on_type_changed(self, index):
        step_type = self.type_combo.itemData(index)
        self.set_step_type(step_type)

    def set_step_type(self, step_type):
        if step_type in self._panels:
            panel_index = list(self._panels.keys()).index(step_type)
            self.stacked_widget.setCurrentIndex(panel_index)
            self._step_type = step_type

    def load_step_data(self, step_data):
        if self._step_type in self._panels:
            panel = self._panels[self._step_type]
            config = step_data.get("params", {})
            panel.set_config(config)

    def get_current_panel(self):
        if self._step_type in self._panels:
            return self._panels[self._step_type]
        return None

    def get_step_config(self):
        panel = self.get_current_panel()
        if panel:
            return panel.get_config()
        return {}

    def on_ok(self):
        step_type = self.type_combo.itemData(self.type_combo.currentIndex())
        config = self.get_step_config()
        
        step_data = {
            "type": step_type,
            "name": STEP_TYPE_MAP.get(step_type, step_type),
            "params": config,
            "description": self.format_params_display(config),
        }
        
        self.step_saved.emit(step_data)
        self.accept()

    def on_cancel(self):
        self.reject()

    def format_params_display(self, params):
        if not params:
            return ""
        
        display_parts = []
        
        if self._step_type == "mouse_click":
            click_type_map = {"left_single": "左键单击", "left_double": "左键双击",
                             "right_single": "右键单击", "middle_single": "中键单击"}
            pos_type_map = {"current": "当前位置", "screen": f"屏幕坐标({params.get('x')},{params.get('y')})",
                           "image": f"图片:{params.get('image_path', '')}", "relative": "相对坐标"}
            
            display_parts.append(click_type_map.get(params.get("click_type"), ""))
            display_parts.append(pos_type_map.get(params.get("position_type"), ""))
            
        elif self._step_type == "mouse_move":
            move_type_map = {"linear": "直线", "ease": "缓动", "random": "随机"}
            display_parts.append(f"{move_type_map.get(params.get('move_type'), '')}移动")
            if params.get("position_type") == "screen":
                display_parts.append(f"到({params.get('x')},{params.get('y')})")
            
        elif self._step_type == "mouse_drag":
            display_parts.append(f"{['左键', '右键', '中键'][params.get('button', 0)]}拖拽")
            
        elif self._step_type == "mouse_scroll":
            dir_map = {"up": "向上", "down": "向下", "left": "向左", "right": "向右"}
            display_parts.append(f"{dir_map.get(params.get('direction'), '')}滚动{params.get('count', 1)}次")
            
        elif self._step_type == "keyboard_type":
            text = params.get("input_text", "")
            display_parts.append(f"输入: {text[:30]}..." if len(text) > 30 else f"输入: {text}")
            
        elif self._step_type == "keyboard_press":
            display_parts.append(f"按键: {params.get('key', '')}")
            
        elif self._step_type == "keyboard_hotkey":
            modifiers = params.get("modifiers", [])
            main_key = params.get("main_key", "")
            if modifiers:
                display_parts.append(f"{'+' .join(modifiers)}+{main_key}")
            else:
                display_parts.append(main_key)
                
        elif self._step_type.startswith("image_"):
            display_parts.append(f"图片: {params.get('image_path', '')}")
            
        elif self._step_type.startswith("window_"):
            display_parts.append(f"窗口: {params.get('window_title', '')}")
            
        elif self._step_type == "excel_read":
            display_parts.append(f"Excel: {params.get('file_path', '')}")
            
        elif self._step_type == "wait":
            wait_type_map = {"fixed": f"等待{params.get('time', 0)}秒",
                            "random": f"随机等待{params.get('min_time', 0)}-{params.get('max_time', 0)}秒",
                            "condition": "条件等待"}
            display_parts.append(wait_type_map.get(params.get("wait_type"), ""))
            
        elif self._step_type == "if_else":
            condition_map = {"value_compare": "值比较", "image_exists": "图片存在",
                           "text_exists": "文字存在", "window_exists": "窗口存在"}
            display_parts.append(f"条件: {condition_map.get(params.get('condition_type'), '')}")
            
        elif self._step_type == "loop":
            loop_map = {"count": f"循环{params.get('count', 0)}次",
                       "condition": "条件循环", "iterate": "遍历列表"}
            display_parts.append(loop_map.get(params.get("loop_type"), ""))
            
        elif self._step_type == "log":
            content = params.get("content", "")
            display_parts.append(f"日志: {content[:30]}..." if len(content) > 30 else f"日志: {content}")
            
        elif self._step_type == "label":
            display_parts.append(f"标记: {params.get('label_name', '')}")
            
        elif self._step_type == "goto":
            display_parts.append(f"跳转到: {params.get('target_label', '')}")
            
        elif self._step_type == "set_variable":
            display_parts.append(f"设置变量 {params.get('var_name', '')}")
            
        elif self._step_type == "get_variable":
            display_parts.append(f"获取变量 {params.get('var_name', '')}")
        
        delay = params.get("delay", 0)
        if delay > 0:
            display_parts.append(f"延时{delay}秒")
        
        return " ".join(filter(None, display_parts))

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #333;
                font-size: 13px;
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
        """)