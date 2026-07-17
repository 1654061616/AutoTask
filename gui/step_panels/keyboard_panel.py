from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
                               QCheckBox, QGroupBox, QTextEdit, QListView,
                               QLineEdit, QRadioButton, QPushButton, QFileDialog)
from PySide6.QtCore import Qt, Signal
from . import StepConfigPanel


class KeyboardTypePanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 数据来源选择
        self.data_source_combo = self.add_combobox("数据来源", ["手动输入", "从Excel读取", "从变量读取"])

        # --- Excel 读取配置区域 ---
        self.excel_group = QGroupBox("Excel 读取配置")
        excel_layout = QVBoxLayout(self.excel_group)
        excel_layout.setContentsMargins(8, 8, 8, 8)
        excel_layout.setSpacing(6)

        # 文件路径
        file_layout = QHBoxLayout()
        file_layout.setSpacing(4)
        file_label = QLabel("文件路径:")
        file_label.setStyleSheet("color: #555; font-size: 13px; min-width: 70px; max-width: 90px;")
        file_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        file_layout.addWidget(file_label)
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setStyleSheet("""
            QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 12px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        file_layout.addWidget(self.file_path_edit, 1)
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border: 1px solid #3498db; border-radius: 3px;
                color: #3498db; font-size: 12px; background: #fff; }
            QPushButton:hover { background: #3498db; color: #fff; }
        """)
        browse_btn.clicked.connect(lambda: self._browse_excel_file())
        file_layout.addWidget(browse_btn)
        excel_layout.addLayout(file_layout)

        # 工作表
        sheet_row = QHBoxLayout()
        sheet_row.setSpacing(4)
        sheet_label = QLabel("工作表:")
        sheet_label.setStyleSheet("color: #555; font-size: 13px; min-width: 70px; max-width: 90px;")
        sheet_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        sheet_row.addWidget(sheet_label)
        self.sheet_edit = QLineEdit()
        self.sheet_edit.setText("Sheet1")
        self.sheet_edit.setPlaceholderText("默认 Sheet1")
        self.sheet_edit.setStyleSheet("""
            QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 13px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        sheet_row.addWidget(self.sheet_edit, 1)
        excel_layout.addLayout(sheet_row)

        # 读取模式
        mode_row = QHBoxLayout()
        mode_row.setSpacing(4)
        mode_label = QLabel("读取模式:")
        mode_label.setStyleSheet("color: #555; font-size: 13px; min-width: 70px; max-width: 90px;")
        mode_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        mode_row.addWidget(mode_label)
        self.read_mode_combo = QComboBox()
        self.read_mode_combo.addItems(["顺序读取", "随机读取"])
        self.read_mode_combo.setStyleSheet("""
            QComboBox { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 13px; }
            QComboBox:focus { border-color: #3498db; }
        """)
        mode_row.addWidget(self.read_mode_combo, 1)
        excel_layout.addLayout(mode_row)

        # 读取范围单选
        self.read_range_group = QGroupBox("读取范围")
        range_layout = QVBoxLayout(self.read_range_group)
        self.read_range_radios = []
        range_options = ["单元格", "行", "列", "区域"]
        for i, option in enumerate(range_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.read_range_radios.append(radio)
            range_layout.addWidget(radio)
        excel_layout.addWidget(self.read_range_group)

        # 单元格地址
        self.cell_group = QGroupBox("单元格地址")
        cell_layout = QFormLayout(self.cell_group)
        self.cell_address_edit = QLineEdit()
        self.cell_address_edit.setPlaceholderText("例如: A1")
        self.cell_address_edit.setStyleSheet("""
            QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        cell_layout.addRow("单元格:", self.cell_address_edit)
        excel_layout.addWidget(self.cell_group)

        # 行号
        self.row_group = QGroupBox("行号")
        row_layout = QFormLayout(self.row_group)
        self.row_number_spin = QSpinBox()
        self.row_number_spin.setRange(1, 1048576)
        self.row_number_spin.setValue(1)
        self.row_number_spin.setStyleSheet("""
            QSpinBox { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        row_layout.addRow("起始行:", self.row_number_spin)
        excel_layout.addWidget(self.row_group)

        # 列号
        self.column_group = QGroupBox("列号")
        column_layout = QFormLayout(self.column_group)
        self.column_number_spin = QSpinBox()
        self.column_number_spin.setRange(1, 16384)
        self.column_number_spin.setValue(1)
        self.column_number_spin.setStyleSheet("""
            QSpinBox { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        column_layout.addRow("列号:", self.column_number_spin)
        excel_layout.addWidget(self.column_group)

        # 区域范围
        self.range_group = QGroupBox("区域范围")
        range_form = QFormLayout(self.range_group)
        self.start_cell_edit = QLineEdit()
        self.start_cell_edit.setPlaceholderText("起始: A1")
        self.start_cell_edit.setStyleSheet("""
            QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        self.end_cell_edit = QLineEdit()
        self.end_cell_edit.setPlaceholderText("结束: B5")
        self.end_cell_edit.setStyleSheet("""
            QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        range_form.addRow("起始:", self.start_cell_edit)
        range_form.addRow("结束:", self.end_cell_edit)
        excel_layout.addWidget(self.range_group)

        # 输出格式
        fmt_row = QHBoxLayout()
        fmt_row.setSpacing(4)
        fmt_label = QLabel("输出格式:")
        fmt_label.setStyleSheet("color: #555; font-size: 13px; min-width: 70px; max-width: 90px;")
        fmt_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        fmt_row.addWidget(fmt_label)
        self.var_format_combo = QComboBox()
        self.var_format_combo.addItems(["字符串", "数字", "列表"])
        self.var_format_combo.setStyleSheet("""
            QComboBox { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 13px; }
            QComboBox:focus { border-color: #3498db; }
        """)
        fmt_row.addWidget(self.var_format_combo, 1)
        excel_layout.addLayout(fmt_row)

        self.main_layout.addWidget(self.excel_group)

        # --- 变量读取区域 ---
        self.variable_group = QGroupBox("变量读取")
        var_layout = QVBoxLayout(self.variable_group)
        var_layout.setContentsMargins(8, 8, 8, 8)
        self.variable_name_edit = QLineEdit()
        self.variable_name_edit.setPlaceholderText("输入变量名")
        self.variable_name_edit.setStyleSheet("""
            QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 13px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        var_layout.addWidget(self.variable_name_edit)
        self.main_layout.addWidget(self.variable_group)

        # --- 手动输入区域（现有）---
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
        self.input_widget = QWidget()
        input_layout = QVBoxLayout(self.input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(2)
        input_label = QLabel("输入内容:")
        input_label.setStyleSheet("color: #555; font-size: 13px;")
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text_edit)
        self.main_layout.addWidget(self.input_widget)

        self.input_method_combo = self.add_combobox("输入方式", ["逐字输入", "剪贴板粘贴"])

        self.interval_spin = QDoubleSpinBox()
        self.interval_spin.setRange(0, 1)
        self.interval_spin.setValue(0.05)
        self.interval_spin.setDecimals(2)
        self.interval_spin.setStyleSheet("""
            QDoubleSpinBox {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 13px;
                min-width: 80px;
            }
            QDoubleSpinBox:focus {
                border-color: #3498db;
                outline: none;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                width: 20px;
            }
        """)
        self.interval_widget = QWidget()
        interval_row = QHBoxLayout(self.interval_widget)
        interval_row.setContentsMargins(0, 0, 0, 0)
        interval_row.setSpacing(6)
        interval_label = QLabel("输入间隔:")
        interval_label.setStyleSheet("color: #555; font-size: 13px; min-width: 70px; max-width: 90px;")
        interval_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        interval_row.addWidget(interval_label)
        interval_row.addWidget(self.interval_spin, 1)
        self.main_layout.addWidget(self.interval_widget)

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
        self._update_data_source_visibility()
        self._update_read_range_visibility()

    def _browse_excel_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.file_path_edit.setText(file_path)

    def _connect_signals(self):
        self.random_interval_check.toggled.connect(self._update_random_interval_visibility)
        self.data_source_combo.currentIndexChanged.connect(self._update_data_source_visibility)
        for radio in self.read_range_radios:
            radio.toggled.connect(self._update_read_range_visibility)

    def _update_random_interval_visibility(self):
        visible = self.random_interval_check.isChecked()
        self.interval_widget.setVisible(not visible)

    def _update_data_source_visibility(self):
        source = self.data_source_combo.currentIndex()
        self.input_widget.setVisible(source == 0)
        self.excel_group.setVisible(source == 1)
        self.variable_group.setVisible(source == 2)

    def _update_read_range_visibility(self):
        selected = -1
        for i, radio in enumerate(self.read_range_radios):
            if radio.isChecked():
                selected = i
                break
        self.cell_group.setVisible(selected == 0)
        self.row_group.setVisible(selected == 1)
        self.column_group.setVisible(selected == 2)
        self.range_group.setVisible(selected == 3)

    def get_config(self):
        source_map = {0: "manual", 1: "excel", 2: "variable"}
        read_range_types = ["cell", "row", "column", "range"]
        checked_index = next((i for i, r in enumerate(self.read_range_radios) if r.isChecked()), 0)

        config = {
            "data_source": source_map[self.data_source_combo.currentIndex()],
            "input_method": "typing" if self.input_method_combo.currentIndex() == 0 else "clipboard",
            "interval": self.interval_spin.value(),
            "random_interval": self.random_interval_check.isChecked(),
            "random_min_interval": self.random_min_spin.value(),
            "random_max_interval": self.random_max_spin.value(),
            "human_input": self.human_input_check.isChecked(),
            "delay": self.delay_spin.value(),
        }

        if config["data_source"] == "manual":
            config["input_text"] = self.input_text_edit.toPlainText()

        if config["data_source"] == "excel":
            config["excel"] = {
                "file_path": self.file_path_edit.text(),
                "sheet": self.sheet_edit.text(),
                "read_mode": "sequential" if self.read_mode_combo.currentIndex() == 0 else "random",
                "read_range": read_range_types[checked_index],
                "cell_address": self.cell_address_edit.text(),
                "row_number": self.row_number_spin.value(),
                "column_number": self.column_number_spin.value(),
                "start_cell": self.start_cell_edit.text(),
                "end_cell": self.end_cell_edit.text(),
                "var_format": ["string", "number", "list"][self.var_format_combo.currentIndex()],
            }

        if config["data_source"] == "variable":
            config["variable_name"] = self.variable_name_edit.text()

        return config

    def set_config(self, config):
        source_map = {"manual": 0, "excel": 1, "variable": 2}
        self.data_source_combo.setCurrentIndex(source_map.get(config.get("data_source", "manual"), 0))

        self.input_text_edit.setPlainText(config.get("input_text", ""))

        excel = config.get("excel", {})
        self.file_path_edit.setText(excel.get("file_path", ""))
        self.sheet_edit.setText(excel.get("sheet", "Sheet1"))
        self.read_mode_combo.setCurrentIndex(0 if excel.get("read_mode", "sequential") == "sequential" else 1)
        read_range_map = {"cell": 0, "row": 1, "column": 2, "range": 3}
        self.read_range_radios[read_range_map.get(excel.get("read_range", "cell"), 0)].setChecked(True)
        self.cell_address_edit.setText(excel.get("cell_address", ""))
        self.row_number_spin.setValue(excel.get("row_number", 1))
        self.column_number_spin.setValue(excel.get("column_number", 1))
        self.start_cell_edit.setText(excel.get("start_cell", ""))
        self.end_cell_edit.setText(excel.get("end_cell", ""))
        var_format_map = {"string": 0, "number": 1, "list": 2}
        self.var_format_combo.setCurrentIndex(var_format_map.get(excel.get("var_format", "string"), 0))

        self.variable_name_edit.setText(config.get("variable_name", ""))

        input_method_map = {"typing": 0, "clipboard": 1}
        self.input_method_combo.setCurrentIndex(input_method_map.get(config.get("input_method", "typing"), 0))
        self.interval_spin.setValue(config.get("interval", 0.05))
        self.random_interval_check.setChecked(config.get("random_interval", False))
        self.random_min_spin.setValue(config.get("random_min_interval", 0.02))
        self.random_max_spin.setValue(config.get("random_max_interval", 0.15))
        self.human_input_check.setChecked(config.get("human_input", False))
        self.delay_spin.setValue(config.get("delay", 0))

        self._update_random_interval_visibility()
        self._update_data_source_visibility()
        self._update_read_range_visibility()


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