from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
                               QCheckBox, QGroupBox, QTextEdit, QListView)
from PySide6.QtCore import Qt, Signal
from . import StepConfigPanel


class KeyboardTypePanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("键盘输入配置")

        self.input_text_edit = QTextEdit()
        self.input_text_edit.setPlaceholderText("请输入要输入的文本内容")
        self.input_text_edit.setStyleSheet("""
            QTextEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-height: 100px;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        """)
        self.add_line("输入内容", self.input_text_edit)

        self.input_method_combo = self.add_combobox("输入方式", ["逐字输入", "剪贴板粘贴"])

        self.interval_spin = self.add_double_spinbox("输入间隔", 0, 1, 0.05, 2)

        self.random_interval_check = self.add_checkbox("随机间隔", checked=False)

        random_layout = QHBoxLayout()
        random_layout.setSpacing(8)
        min_label = QLabel("最小间隔:")
        min_label.setFixedWidth(80)
        min_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        random_layout.addWidget(min_label)
        self.random_min_spin = QDoubleSpinBox()
        self.random_min_spin.setRange(0, 1)
        self.random_min_spin.setValue(0.02)
        self.random_min_spin.setDecimals(2)
        self.random_min_spin.setStyleSheet("""
            QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 80px;
            }
            QDoubleSpinBox:focus {
                border-color: #3498db;
            }
        """)
        random_layout.addWidget(self.random_min_spin)
        max_label = QLabel("最大间隔:")
        max_label.setFixedWidth(60)
        max_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        random_layout.addWidget(max_label)
        self.random_max_spin = QDoubleSpinBox()
        self.random_max_spin.setRange(0, 1)
        self.random_max_spin.setValue(0.15)
        self.random_max_spin.setDecimals(2)
        self.random_max_spin.setStyleSheet("""
            QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 80px;
            }
            QDoubleSpinBox:focus {
                border-color: #3498db;
            }
        """)
        random_layout.addWidget(self.random_max_spin)
        random_layout.addStretch()
        self.main_layout.addLayout(random_layout)

        self.human_input_check = self.add_checkbox("模拟人类输入", checked=False)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_random_interval_visibility()

    def _connect_signals(self):
        self.random_interval_check.toggled.connect(self._update_random_interval_visibility)

    def _update_random_interval_visibility(self):
        visible = self.random_interval_check.isChecked()
        self.interval_spin.parentWidget().setVisible(not visible)

    def get_config(self):
        return {
            "input_text": self.input_text_edit.toPlainText(),
            "input_method": "typing" if self.input_method_combo.currentIndex() == 0 else "clipboard",
            "interval": self.interval_spin.value(),
            "random_interval": self.random_interval_check.isChecked(),
            "random_min_interval": self.random_min_spin.value(),
            "random_max_interval": self.random_max_spin.value(),
            "human_input": self.human_input_check.isChecked(),
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        self.input_text_edit.setPlainText(config.get("input_text", ""))
        input_method_map = {"typing": 0, "clipboard": 1}
        self.input_method_combo.setCurrentIndex(input_method_map.get(config.get("input_method", "typing"), 0))
        self.interval_spin.setValue(config.get("interval", 0.05))
        self.random_interval_check.setChecked(config.get("random_interval", False))
        self.random_min_spin.setValue(config.get("random_min_interval", 0.02))
        self.random_max_spin.setValue(config.get("random_max_interval", 0.15))
        self.human_input_check.setChecked(config.get("human_input", False))
        self.delay_spin.setValue(config.get("delay", 0))
        self._update_random_interval_visibility()


class KeyboardPressPanel(StepConfigPanel):
    KEYS = [
        "ENTER", "TAB", "SPACE", "BACKSPACE", "DELETE", "INSERT",
        "HOME", "END", "PAGE_UP", "PAGE_DOWN",
        "UP", "DOWN", "LEFT", "RIGHT",
        "F1", "F2", "F3", "F4", "F5", "F6",
        "F7", "F8", "F9", "F10", "F11", "F12",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "ESC", "CAPS_LOCK", "NUM_LOCK", "SCROLL_LOCK",
        "PRINT_SCREEN", "PAUSE",
        ";", ":", ",", ".", "/", "\\", "`", "~",
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
        "-", "_", "+", "=", "[", "]", "{", "}", "'", "\"", "?"
    ]

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("按键操作配置")

        self.key_combo = QComboBox()
        self.key_combo.addItems(self.KEYS)
        self.key_combo.setStyleSheet("""
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
        key_view = QListView()
        key_view.setStyleSheet("""
            QListView { color: #333333; background-color: #ffffff; font-size: 13px; }
            QListView::item { padding: 6px 10px; height: 28px; }
            QListView::item:selected { color: #ffffff; background-color: #3498db; }
            QListView::item:hover { color: #ffffff; background-color: #3498db; }
        """)
        self.key_combo.setView(key_view)
        self.add_line("按键", self.key_combo)

        self.hold_duration_spin = self.add_double_spinbox("按住时长", 0, 10, 0.1, 2)

        self.repeat_count_spin = self.add_spinbox("重复次数", 1, 100, 1)

        self.repeat_interval_spin = self.add_double_spinbox("重复间隔", 0, 10, 0.5, 2)

        self.add_separator()
        self.add_delay_section()

    def get_config(self):
        return {
            "key": self.key_combo.currentText(),
            "hold_duration": self.hold_duration_spin.value(),
            "repeat_count": self.repeat_count_spin.value(),
            "repeat_interval": self.repeat_interval_spin.value(),
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        key = config.get("key", "ENTER")
        self.key_combo.setCurrentText(key)
        self.hold_duration_spin.setValue(config.get("hold_duration", 0.1))
        self.repeat_count_spin.setValue(config.get("repeat_count", 1))
        self.repeat_interval_spin.setValue(config.get("repeat_interval", 0.5))
        self.delay_spin.setValue(config.get("delay", 0))


class KeyboardHotkeyPanel(StepConfigPanel):
    MODIFIER_KEYS = ["Ctrl", "Alt", "Shift", "Win"]
    MAIN_KEYS = [
        "ENTER", "TAB", "SPACE", "BACKSPACE", "DELETE", "INSERT",
        "HOME", "END", "PAGE_UP", "PAGE_DOWN",
        "UP", "DOWN", "LEFT", "RIGHT",
        "F1", "F2", "F3", "F4", "F5", "F6",
        "F7", "F8", "F9", "F10", "F11", "F12",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "ESC", "CAPS_LOCK", "NUM_LOCK", "SCROLL_LOCK",
        "PRINT_SCREEN", "PAUSE",
        ";", ":", ",", ".", "/", "\\", "`", "~",
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
        "-", "_", "+", "=", "[", "]", "{", "}", "'", "\"", "?"
    ]

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("快捷键配置")

        modifier_group = QGroupBox("修饰键")
        modifier_layout = QHBoxLayout(modifier_group)
        modifier_layout.setSpacing(12)

        self.modifier_checks = {}
        for key in self.MODIFIER_KEYS:
            checkbox = QCheckBox(key)
            self.modifier_checks[key] = checkbox
            modifier_layout.addWidget(checkbox)
        modifier_layout.addStretch()
        self.main_layout.addWidget(modifier_group)

        self.main_key_combo = QComboBox()
        self.main_key_combo.addItems(self.MAIN_KEYS)
        self.main_key_combo.setStyleSheet("""
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
        main_key_view = QListView()
        main_key_view.setStyleSheet("""
            QListView { color: #333333; background-color: #ffffff; font-size: 13px; }
            QListView::item { padding: 6px 10px; height: 28px; }
            QListView::item:selected { color: #ffffff; background-color: #3498db; }
            QListView::item:hover { color: #ffffff; background-color: #3498db; }
        """)
        self.main_key_combo.setView(main_key_view)
        self.add_line("主按键", self.main_key_combo)

        self.hold_duration_spin = self.add_double_spinbox("按住时长", 0, 10, 0.1, 2)

        preview_group = QGroupBox("实时预览")
        preview_layout = QHBoxLayout(preview_group)
        preview_layout.setSpacing(8)
        preview_label = QLabel("组合键:")
        preview_label.setFixedWidth(80)
        preview_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        preview_layout.addWidget(preview_label)

        self.preview_text = QLabel("")
        self.preview_text.setStyleSheet("""
            QLabel {
                padding: 5px 10px;
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-family: monospace;
                font-size: 14px;
                color: #27ae60;
                font-weight: bold;
                min-width: 200px;
            }
        """)
        self.preview_text.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.preview_text)
        preview_layout.addStretch()
        self.main_layout.addWidget(preview_group)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_preview()

    def _connect_signals(self):
        for checkbox in self.modifier_checks.values():
            checkbox.toggled.connect(self._update_preview)
        self.main_key_combo.currentTextChanged.connect(self._update_preview)

    def _update_preview(self):
        modifiers = [key for key, checkbox in self.modifier_checks.items() if checkbox.isChecked()]
        main_key = self.main_key_combo.currentText()

        if modifiers:
            preview = "+".join(modifiers) + "+" + main_key
        else:
            preview = main_key

        self.preview_text.setText(preview)

    def get_config(self):
        modifiers = [key for key, checkbox in self.modifier_checks.items() if checkbox.isChecked()]
        return {
            "modifiers": modifiers,
            "main_key": self.main_key_combo.currentText(),
            "hold_duration": self.hold_duration_spin.value(),
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        for key, checkbox in self.modifier_checks.items():
            checkbox.setChecked(key in config.get("modifiers", []))

        main_key = config.get("main_key", "ENTER")
        self.main_key_combo.setCurrentText(main_key)

        self.hold_duration_spin.setValue(config.get("hold_duration", 0.1))
        self.delay_spin.setValue(config.get("delay", 0))

        self._update_preview()