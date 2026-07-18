from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QTextEdit, QTabWidget,
                               QWidget, QRadioButton, QButtonGroup, QCheckBox,
                               QSpinBox, QGridLayout, QGroupBox)
from PySide6.QtCore import Qt, Signal
from croniter import croniter
from datetime import datetime
from gui.styles import Styles


TAB_CONFIGS = [
    {"name": "秒", "key": "second", "count": 60, "start": 0},
    {"name": "分钟", "key": "minute", "count": 60, "start": 0},
    {"name": "小时", "key": "hour", "count": 24, "start": 0},
    {"name": "日", "key": "day", "count": 31, "start": 1},
    {"name": "月", "key": "month", "count": 12, "start": 1},
    {"name": "周", "key": "week", "count": 7, "start": 0},
    {"name": "年", "key": "year", "count": 10, "start": 2026},
]

WEEKDAY_NAMES = ["日", "一", "二", "三", "四", "五", "六"]


class CronTabWidget(QWidget):
    value_changed = Signal()

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self._value = "*"
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.mode_group = QButtonGroup(self)

        # 模式1: 每X
        mode1_layout = QHBoxLayout()
        self.radio_every = QRadioButton()
        self.mode_group.addButton(self.radio_every, 0)
        mode1_layout.addWidget(self.radio_every)
        mode1_layout.addWidget(QLabel(f"每{self.config['name']}  允许的通配符[, - * /]"))
        mode1_layout.addStretch()
        layout.addLayout(mode1_layout)

        # 模式2: 周期范围
        mode2_layout = QHBoxLayout()
        self.radio_range = QRadioButton()
        self.mode_group.addButton(self.radio_range, 1)
        mode2_layout.addWidget(self.radio_range)
        mode2_layout.addWidget(QLabel("周期从"))
        self.range_start = QSpinBox()
        self.range_start.setRange(self.config["start"], self.config["start"] + self.config["count"] - 1)
        self.range_start.setValue(self.config["start"])
        self.range_start.valueChanged.connect(lambda: self.value_changed.emit())
        mode2_layout.addWidget(self.range_start)
        mode2_layout.addWidget(QLabel("到"))
        self.range_end = QSpinBox()
        self.range_end.setRange(self.config["start"], self.config["start"] + self.config["count"] - 1)
        self.range_end.setValue(self.config["start"] + 2)
        self.range_end.valueChanged.connect(lambda: self.value_changed.emit())
        mode2_layout.addWidget(self.range_end)
        mode2_layout.addWidget(QLabel(self.config["name"]))
        mode2_layout.addStretch()
        layout.addLayout(mode2_layout)

        # 模式3: 间隔执行
        mode3_layout = QHBoxLayout()
        self.radio_interval = QRadioButton()
        self.mode_group.addButton(self.radio_interval, 2)
        mode3_layout.addWidget(self.radio_interval)
        mode3_layout.addWidget(QLabel(f"周期从"))
        self.interval_start = QSpinBox()
        self.interval_start.setRange(self.config["start"], self.config["start"] + self.config["count"] - 1)
        self.interval_start.setValue(self.config["start"])
        self.interval_start.valueChanged.connect(lambda: self.value_changed.emit())
        mode3_layout.addWidget(self.interval_start)
        mode3_layout.addWidget(QLabel(f"{self.config['name']}开始，每"))
        self.interval_step = QSpinBox()
        self.interval_step.setRange(1, self.config["count"])
        self.interval_step.setValue(1)
        self.interval_step.valueChanged.connect(lambda: self.value_changed.emit())
        mode3_layout.addWidget(self.interval_step)
        mode3_layout.addWidget(QLabel(f"{self.config['name']}执行一次"))
        mode3_layout.addStretch()
        layout.addLayout(mode3_layout)

        # 模式4: 指定
        mode4_layout = QHBoxLayout()
        self.radio_specify = QRadioButton()
        self.mode_group.addButton(self.radio_specify, 3)
        mode4_layout.addWidget(self.radio_specify)
        mode4_layout.addWidget(QLabel("指定"))
        mode4_layout.addStretch()
        layout.addLayout(mode4_layout)

        self.checkbox_grid = QGridLayout()
        cols = 8
        for i in range(self.config["count"]):
            cb = QCheckBox(str(self.config["start"] + i))
            cb.stateChanged.connect(lambda: self.value_changed.emit())
            self.checkbox_grid.addWidget(cb, i // cols, i % cols)
        layout.addLayout(self.checkbox_grid)

        self.mode_group.buttonClicked.connect(self._on_mode_changed)
        self.radio_every.setChecked(True)
        self._on_mode_changed()

        layout.addStretch()

    def _on_mode_changed(self):
        mode = self.mode_group.checkedId()
        self.range_start.setEnabled(mode == 1)
        self.range_end.setEnabled(mode == 1)
        self.interval_start.setEnabled(mode == 2)
        self.interval_step.setEnabled(mode == 2)
        for i in range(self.checkbox_grid.count()):
            item = self.checkbox_grid.itemAt(i)
            if item and item.widget():
                item.widget().setEnabled(mode == 3)
        self.value_changed.emit()

    def get_value(self) -> str:
        mode = self.mode_group.checkedId()
        if mode == 0:
            return "*"
        elif mode == 1:
            return f"{self.range_start.value()}-{self.range_end.value()}"
        elif mode == 2:
            return f"{self.interval_start.value()}/{self.interval_step.value()}"
        elif mode == 3:
            selected = []
            for i in range(self.checkbox_grid.count()):
                item = self.checkbox_grid.itemAt(i)
                if item and item.widget() and item.widget().isChecked():
                    selected.append(str(self.config["start"] + i))
            return ",".join(selected) if selected else "*"
        return "*"

    def set_value(self, value: str):
        if value == "*":
            self.radio_every.setChecked(True)
        elif "-" in value:
            parts = value.split("-")
            if len(parts) == 2:
                self.radio_range.setChecked(True)
                self.range_start.setValue(int(parts[0]))
                self.range_end.setValue(int(parts[1]))
        elif "/" in value:
            parts = value.split("/")
            if len(parts) == 2:
                self.radio_interval.setChecked(True)
                self.interval_start.setValue(int(parts[0]))
                self.interval_step.setValue(int(parts[1]))
        elif "," in value:
            self.radio_specify.setChecked(True)
            selected = set(value.split(","))
            for i in range(self.checkbox_grid.count()):
                item = self.checkbox_grid.itemAt(i)
                if item and item.widget():
                    val = str(self.config["start"] + i)
                    item.widget().setChecked(val in selected)
        else:
            self.radio_specify.setChecked(True)
            for i in range(self.checkbox_grid.count()):
                item = self.checkbox_grid.itemAt(i)
                if item and item.widget():
                    val = str(self.config["start"] + i)
                    item.widget().setChecked(val == value)
        self._on_mode_changed()


class CronGeneratorDialog(QDialog):
    cron_generated = Signal(str)

    def __init__(self, current_expression="0 0 9 * * * *", parent=None):
        super().__init__(parent)
        self.setWindowTitle("CRON 表达式生成器")
        self.setModal(True)
        self.resize(650, 550)
        self._init_ui()
        self._load_expression(current_expression)

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        self.tab_panels = []
        for cfg in TAB_CONFIGS:
            panel = CronTabWidget(cfg)
            panel.value_changed.connect(self._on_value_changed)
            self.tab_widget.addTab(panel, cfg["name"])
            self.tab_panels.append(panel)
        layout.addWidget(self.tab_widget)

        expr_layout = QHBoxLayout()
        expr_layout.addWidget(QLabel("CRON 表达式:"))
        self.expression_label = QLabel("0 0 9 * * * *")
        self.expression_label.setStyleSheet(Styles.cron_expression_label())
        expr_layout.addWidget(self.expression_label)
        expr_layout.addStretch()
        layout.addLayout(expr_layout)

        layout.addWidget(QLabel("最近执行时间:"))
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(120)
        layout.addWidget(self.preview_text)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self._on_accept)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def _on_value_changed(self):
        self._build_and_show()

    def _build_expression(self) -> str:
        values = [p.get_value() for p in self.tab_panels]
        return " ".join(values)

    def _build_and_show(self):
        expr = self._build_expression()
        self.expression_label.setText(expr)
        self._update_preview()

    def _load_expression(self, expr):
        parts = expr.split()
        field_count = len(parts)
        for i in range(len(self.tab_panels)):
            if i < field_count:
                self.tab_panels[i].set_value(parts[i])
            else:
                self.tab_panels[i].set_value("*")
        self._build_and_show()

    def _update_preview(self):
        expr = self._build_expression()
        try:
            cron = croniter(expr, datetime.now())
            lines = []
            for _ in range(5):
                lines.append(cron.get_next(datetime).strftime("%Y-%m-%d %H:%M:%S"))
            self.preview_text.setText("\n".join(lines))
        except Exception:
            self.preview_text.setText("表达式无效")

    def _on_accept(self):
        self.cron_generated.emit(self._build_expression())
        self.accept()