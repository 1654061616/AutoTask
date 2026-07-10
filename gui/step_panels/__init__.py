from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QDoubleSpinBox, QLineEdit,
                               QTextEdit, QComboBox, QCheckBox, QRadioButton,
                               QSlider, QPushButton, QFileDialog, QGroupBox,
                               QFrame)
from PySide6.QtCore import Qt, Signal


class StepConfigPanel(QWidget):
    config_changed = Signal(dict)

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)
        self.setLayout(self.main_layout)
        self._config = {}

    def get_config(self):
        raise NotImplementedError("Subclasses must implement get_config()")

    def set_config(self, config):
        raise NotImplementedError("Subclasses must implement set_config(config)")

    def add_section_title(self, text):
        label = QLabel(f"<b>{text}</b>")
        label.setStyleSheet("color: #27ae60; font-size: 14px;")
        self.main_layout.addWidget(label)
        return label

    def add_line(self, label_text, widget, stretch=0):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(8)
        
        label = QLabel(f"{label_text}:")
        label.setFixedWidth(100)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row_layout.addWidget(label)
        
        row_layout.addWidget(widget)
        if stretch > 0:
            row_layout.addStretch(stretch)
        
        self.main_layout.addLayout(row_layout)
        return widget

    def add_spinbox(self, label_text, min_val, max_val, default, step=1):
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default)
        spinbox.setSingleStep(step)
        spinbox.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 100px;
            }
            QSpinBox:focus {
                border-color: #3498db;
            }
        """)
        return self.add_line(label_text, spinbox)

    def add_double_spinbox(self, label_text, min_val, max_val, default, decimals=2):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default)
        spinbox.setDecimals(decimals)
        spinbox.setStyleSheet("""
            QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 100px;
            }
            QDoubleSpinBox:focus {
                border-color: #3498db;
            }
        """)
        return self.add_line(label_text, spinbox)

    def add_lineedit(self, label_text, default="", placeholder=""):
        lineedit = QLineEdit()
        lineedit.setText(default)
        lineedit.setPlaceholderText(placeholder)
        lineedit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        return self.add_line(label_text, lineedit)

    def add_textedit(self, label_text, default="", placeholder=""):
        textedit = QTextEdit()
        textedit.setPlaceholderText(placeholder)
        if default:
            textedit.setText(default)
        textedit.setStyleSheet("""
            QTextEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-height: 80px;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        """)
        return self.add_line(label_text, textedit)

    def add_combobox(self, label_text, items, default_index=0):
        combobox = QComboBox()
        combobox.addItems(items)
        if 0 <= default_index < len(items):
            combobox.setCurrentIndex(default_index)
        combobox.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
        """)
        return self.add_line(label_text, combobox)

    def add_checkbox(self, text, checked=False):
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
            }
        """)
        self.main_layout.addWidget(checkbox)
        return checkbox

    def add_radio_group(self, label_text, options, default_index=0):
        group_box = QGroupBox(label_text)
        group_layout = QVBoxLayout(group_box)
        
        buttons = []
        for i, option in enumerate(options):
            radio_btn = QRadioButton(option)
            if i == default_index:
                radio_btn.setChecked(True)
            buttons.append(radio_btn)
            group_layout.addWidget(radio_btn)
        
        self.main_layout.addWidget(group_box)
        return buttons

    def add_slider(self, label_text, min_val, max_val, default, suffix=""):
        slider_layout = QVBoxLayout()
        slider_layout.setSpacing(4)
        
        label = QLabel(f"{label_text}:")
        label.setStyleSheet("color: #333;")
        slider_layout.addWidget(label)
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval((max_val - min_val) // 10)
        
        value_label = QLabel(f"{default}{suffix}")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        
        slider.valueChanged.connect(lambda val: value_label.setText(f"{val}{suffix}"))
        
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        
        self.main_layout.addLayout(slider_layout)
        return slider

    def add_file_browser(self, label_text, file_filter="All Files (*)", default_path=""):
        file_layout = QHBoxLayout()
        file_layout.setSpacing(8)
        
        label = QLabel(f"{label_text}:")
        label.setFixedWidth(100)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        file_layout.addWidget(label)
        
        line_edit = QLineEdit()
        line_edit.setText(default_path)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                flex: 1;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet("""
            QPushButton {
                padding: 4px 12px;
                border-radius: 4px;
                border: 1px solid #ccc;
                background-color: #ffffff;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        def browse_file():
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", file_filter)
            if file_path:
                line_edit.setText(file_path)
        
        browse_btn.clicked.connect(browse_file)
        
        file_layout.addWidget(line_edit)
        file_layout.addWidget(browse_btn)
        
        self.main_layout.addLayout(file_layout)
        return line_edit

    def add_delay_section(self, default_delay=0):
        delay_group = QGroupBox("延时设置")
        delay_layout = QFormLayout(delay_group)
        
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 3600)
        self.delay_spin.setValue(default_delay)
        self.delay_spin.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        
        delay_layout.addRow("执行后延时(秒):", self.delay_spin)
        
        self.main_layout.addWidget(delay_group)
        return self.delay_spin

    def add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #ddd;")
        self.main_layout.addWidget(separator)
        return separator

    def add_buttons(self, confirm_callback, cancel_callback):
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()
        
        confirm_btn = QPushButton("确定")
        confirm_btn.setStyleSheet("""
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
        """)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
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
        
        confirm_btn.clicked.connect(confirm_callback)
        cancel_btn.clicked.connect(cancel_callback)
        
        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)
        
        self.main_layout.addLayout(btn_layout)
        return confirm_btn, cancel_btn


from .mouse_panel import (MouseClickPanel, MouseMovePanel, 
                          MouseDragPanel, MouseScrollPanel)
from .keyboard_panel import (KeyboardTypePanel, KeyboardPressPanel, 
                            KeyboardHotkeyPanel)
from .image_panel import (ImageFindPanel, ImageClickPanel, ImageExistsPanel)
from .window_panel import (WindowFindPanel, WindowActivatePanel, 
                          WindowClosePanel, WindowPositionPanel)
from .excel_panel import ExcelReadPanel
from .control_panel import (WaitPanel, IfElsePanel, LoopPanel, 
                           LogPanel, LabelPanel, GotoPanel)
from .variable_panel import SetVariablePanel, GetVariablePanel


PANEL_MAP = {
    "mouse_click": MouseClickPanel,
    "mouse_move": MouseMovePanel,
    "mouse_drag": MouseDragPanel,
    "mouse_scroll": MouseScrollPanel,
    "keyboard_type": KeyboardTypePanel,
    "keyboard_press": KeyboardPressPanel,
    "keyboard_hotkey": KeyboardHotkeyPanel,
    "image_find": ImageFindPanel,
    "image_click": ImageClickPanel,
    "image_exists": ImageExistsPanel,
    "window_find": WindowFindPanel,
    "window_activate": WindowActivatePanel,
    "window_close": WindowClosePanel,
    "window_position": WindowPositionPanel,
    "excel_read": ExcelReadPanel,
    "wait": WaitPanel,
    "if_else": IfElsePanel,
    "loop": LoopPanel,
    "log": LogPanel,
    "label": LabelPanel,
    "goto": GotoPanel,
    "set_variable": SetVariablePanel,
    "get_variable": GetVariablePanel,
}


def get_panel_class(step_type):
    return PANEL_MAP.get(step_type)