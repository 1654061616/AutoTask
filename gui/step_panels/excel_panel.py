from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QLineEdit, QComboBox,
                               QRadioButton, QGroupBox)
from PySide6.QtCore import Qt, Signal
from . import StepConfigPanel


class ExcelReadPanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("读取Excel配置")

        self.file_path_edit = self.add_file_browser("文件路径", "Excel Files (*.xlsx *.xls)")

        self.sheet_edit = self.add_lineedit("工作表", default="Sheet1", placeholder="默认 Sheet1")

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
        self.main_layout.addWidget(self.read_range_group)

        self.cell_group = QGroupBox("单元格地址")
        cell_layout = QFormLayout(self.cell_group)
        self.cell_address_edit = QLineEdit()
        self.cell_address_edit.setPlaceholderText("例如: A1")
        self.cell_address_edit.setStyleSheet("""
            QLineEdit { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        cell_layout.addRow("单元格:", self.cell_address_edit)
        self.main_layout.addWidget(self.cell_group)

        self.row_group = QGroupBox("行号")
        row_layout = QFormLayout(self.row_group)
        self.row_number_spin = QSpinBox()
        self.row_number_spin.setRange(1, 1048576)
        self.row_number_spin.setValue(1)
        self.row_number_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        row_layout.addRow("行号:", self.row_number_spin)
        self.main_layout.addWidget(self.row_group)

        self.column_group = QGroupBox("列号")
        column_layout = QFormLayout(self.column_group)
        self.column_number_spin = QSpinBox()
        self.column_number_spin.setRange(1, 16384)
        self.column_number_spin.setValue(1)
        self.column_number_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        column_layout.addRow("列号:", self.column_number_spin)
        self.main_layout.addWidget(self.column_group)

        self.range_group = QGroupBox("区域范围")
        range_layout = QFormLayout(self.range_group)
        self.start_cell_edit = QLineEdit()
        self.start_cell_edit.setPlaceholderText("起始单元格: A1")
        self.start_cell_edit.setStyleSheet("""
            QLineEdit { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        self.end_cell_edit = QLineEdit()
        self.end_cell_edit.setPlaceholderText("结束单元格: B5")
        self.end_cell_edit.setStyleSheet("""
            QLineEdit { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        range_layout.addRow("起始单元格:", self.start_cell_edit)
        range_layout.addRow("结束单元格:", self.end_cell_edit)
        self.main_layout.addWidget(self.range_group)

        self.output_var_edit = self.add_lineedit("输出变量", placeholder="存储结果的变量名")

        self.var_format_combo = self.add_combobox("变量格式", ["字符串", "数字", "列表"])

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_read_range_visibility()

    def _connect_signals(self):
        for radio in self.read_range_radios:
            radio.toggled.connect(self._update_read_range_visibility)

    def _update_read_range_visibility(self):
        selected_index = -1
        for i, radio in enumerate(self.read_range_radios):
            if radio.isChecked():
                selected_index = i
                break

        self.cell_group.setVisible(selected_index == 0)
        self.row_group.setVisible(selected_index == 1)
        self.column_group.setVisible(selected_index == 2)
        self.range_group.setVisible(selected_index == 3)

    def get_config(self):
        read_range_type = self.read_range_radios.index([r for r in self.read_range_radios if r.isChecked()][0])
        read_range_types = ["cell", "row", "column", "range"]

        config = {
            "file_path": self.file_path_edit.text(),
            "sheet": self.sheet_edit.text(),
            "read_range": read_range_types[read_range_type],
            "output_variable": self.output_var_edit.text(),
            "var_format": ["string", "number", "list"][self.var_format_combo.currentIndex()],
            "delay": self.delay_spin.value()
        }

        if read_range_type == 0:
            config["cell_address"] = self.cell_address_edit.text()
        elif read_range_type == 1:
            config["row_number"] = self.row_number_spin.value()
        elif read_range_type == 2:
            config["column_number"] = self.column_number_spin.value()
        elif read_range_type == 3:
            config["start_cell"] = self.start_cell_edit.text()
            config["end_cell"] = self.end_cell_edit.text()

        return config

    def set_config(self, config):
        self.file_path_edit.setText(config.get("file_path", ""))
        self.sheet_edit.setText(config.get("sheet", "Sheet1"))

        read_range_map = {"cell": 0, "row": 1, "column": 2, "range": 3}
        read_range_type = read_range_map.get(config.get("read_range", "cell"), 0)
        self.read_range_radios[read_range_type].setChecked(True)

        self.output_var_edit.setText(config.get("output_variable", ""))

        var_format_map = {"string": 0, "number": 1, "list": 2}
        self.var_format_combo.setCurrentIndex(var_format_map.get(config.get("var_format", "string"), 0))

        self.cell_address_edit.setText(config.get("cell_address", ""))
        self.row_number_spin.setValue(config.get("row_number", 1))
        self.column_number_spin.setValue(config.get("column_number", 1))
        self.start_cell_edit.setText(config.get("start_cell", ""))
        self.end_cell_edit.setText(config.get("end_cell", ""))

        self.delay_spin.setValue(config.get("delay", 0))

        self._update_read_range_visibility()