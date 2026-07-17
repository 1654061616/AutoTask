from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QComboBox, QSpinBox, QLineEdit, QPushButton,
                               QDateTimeEdit, QStackedWidget)
from PySide6.QtCore import Qt, QDateTime, Signal
from croniter import croniter
from datetime import datetime

from .cron_generator import CronGeneratorDialog


class SchedulePanel(QWidget):
    schedule_changed = Signal()
    start_scheduled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._on_trigger_changed(0)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        trigger_layout = QHBoxLayout()
        trigger_layout.addWidget(QLabel("触发类型:"))
        self.trigger_combo = QComboBox()
        self.trigger_combo.addItems(["立即执行1次", "间隔执行", "CRON定时", "指定时间"])
        self.trigger_combo.currentIndexChanged.connect(self._on_trigger_changed)
        trigger_layout.addWidget(self.trigger_combo)
        self.start_scheduled_btn = QPushButton("▶ 开始定时")
        self.start_scheduled_btn.setStyleSheet(
            "QPushButton {"
            "  background-color: #1890ff; color: white; border: none;"
            "  border-radius: 4px; padding: 4px 14px; font-size: 13px;"
            "  font-weight: bold;"
            "}"
            "QPushButton:hover { background-color: #40a9ff; }"
            "QPushButton:pressed { background-color: #096dd9; }"
        )
        self.start_scheduled_btn.clicked.connect(lambda: self.start_scheduled.emit())
        trigger_layout.addWidget(self.start_scheduled_btn)
        trigger_layout.addStretch()
        layout.addLayout(trigger_layout)

        self.stack = QStackedWidget()

        # 0: immediate
        immediate_widget = QWidget()
        immediate_layout = QVBoxLayout(immediate_widget)
        immediate_layout.setContentsMargins(0, 5, 0, 0)
        immediate_layout.addWidget(QLabel("任务启动后立即执行一次"))
        immediate_layout.addStretch()
        self.stack.addWidget(immediate_widget)

        # 1: interval
        interval_widget = QWidget()
        interval_layout = QHBoxLayout(interval_widget)
        interval_layout.setContentsMargins(0, 5, 0, 0)
        interval_layout.addWidget(QLabel("间隔:"))
        self.interval_hour_spin = QSpinBox()
        self.interval_hour_spin.setRange(0, 23)
        self.interval_hour_spin.setValue(0)
        self.interval_hour_spin.valueChanged.connect(lambda: self.schedule_changed.emit())
        interval_layout.addWidget(self.interval_hour_spin)
        interval_layout.addWidget(QLabel("时"))
        self.interval_minute_spin = QSpinBox()
        self.interval_minute_spin.setRange(0, 59)
        self.interval_minute_spin.setValue(1)
        self.interval_minute_spin.valueChanged.connect(lambda: self.schedule_changed.emit())
        interval_layout.addWidget(self.interval_minute_spin)
        interval_layout.addWidget(QLabel("分"))
        self.interval_second_spin = QSpinBox()
        self.interval_second_spin.setRange(0, 59)
        self.interval_second_spin.setValue(0)
        self.interval_second_spin.valueChanged.connect(lambda: self.schedule_changed.emit())
        interval_layout.addWidget(self.interval_second_spin)
        interval_layout.addWidget(QLabel("秒"))
        interval_layout.addStretch()
        self.stack.addWidget(interval_widget)

        # 2: cron
        cron_widget = QWidget()
        cron_layout = QVBoxLayout(cron_widget)
        cron_layout.setContentsMargins(0, 5, 0, 0)
        cron_line_layout = QHBoxLayout()
        cron_line_layout.addWidget(QLabel("CRON表达式:"))
        self.cron_edit = QLineEdit("0 0 9 * * * *")
        self.cron_edit.setPlaceholderText("秒 分 时 日 月 周 年")
        self.cron_edit.textChanged.connect(self._on_cron_changed)
        cron_line_layout.addWidget(self.cron_edit)
        self.cron_generator_btn = QPushButton("生成器")
        self.cron_generator_btn.clicked.connect(self._open_cron_generator)
        cron_line_layout.addWidget(self.cron_generator_btn)
        cron_layout.addLayout(cron_line_layout)
        cron_time_layout = QHBoxLayout()
        cron_time_layout.addWidget(QLabel("最近执行时间:"))
        self.cron_preview_label = QLabel()
        self.cron_preview_label.setStyleSheet("color: #555; font-family: monospace;")
        cron_time_layout.addWidget(self.cron_preview_label)
        cron_time_layout.addStretch()
        cron_layout.addLayout(cron_time_layout)
        cron_layout.addStretch()
        self.stack.addWidget(cron_widget)

        # 3: date
        date_widget = QWidget()
        date_layout = QHBoxLayout(date_widget)
        date_layout.setContentsMargins(0, 5, 0, 0)
        date_layout.addWidget(QLabel("执行时间:"))
        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_edit.dateTimeChanged.connect(lambda: self.schedule_changed.emit())
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()
        self.stack.addWidget(date_widget)

        layout.addWidget(self.stack)
        layout.addStretch()

    def _on_trigger_changed(self, index):
        self.stack.setCurrentIndex(index)
        self.schedule_changed.emit()

    def _on_cron_changed(self, text):
        self._update_cron_preview()
        self.schedule_changed.emit()

    def _update_cron_preview(self):
        expr = self.cron_edit.text().strip()
        try:
            cron = croniter(expr, datetime.now())
            next_time = cron.get_next(datetime).strftime("%Y-%m-%d %H:%M:%S")
            self.cron_preview_label.setText(next_time)
        except Exception:
            self.cron_preview_label.setText("表达式无效")

    def _open_cron_generator(self):
        dialog = CronGeneratorDialog(self.cron_edit.text(), self)
        dialog.cron_generated.connect(self._on_cron_generated)
        dialog.exec()

    def _on_cron_generated(self, expression):
        self.cron_edit.setText(expression)

    def get_config(self) -> dict:
        index = self.trigger_combo.currentIndex()
        trigger_types = ["immediate", "interval", "cron", "date"]
        trigger_type = trigger_types[index]

        params = {}
        if trigger_type == "interval":
            params["interval"] = (
                self.interval_hour_spin.value() * 3600 +
                self.interval_minute_spin.value() * 60 +
                self.interval_second_spin.value()
            )
        elif trigger_type == "cron":
            params["cron_expression"] = self.cron_edit.text().strip()
        elif trigger_type == "date":
            params["run_date"] = self.date_edit.dateTime().toPython().isoformat()

        return {"trigger_type": trigger_type, "params": params}

    def load_config(self, config: dict):
        if not config:
            self.trigger_combo.setCurrentIndex(0)
            return

        trigger_type = config.get("trigger_type", "immediate")
        params = config.get("params", {})

        type_index = {"immediate": 0, "interval": 1, "cron": 2, "date": 3}
        self.trigger_combo.setCurrentIndex(type_index.get(trigger_type, 0))

        if trigger_type == "interval":
            total_seconds = params.get("interval", 60)
            h = total_seconds // 3600
            m = (total_seconds % 3600) // 60
            s = total_seconds % 60
            self.interval_hour_spin.setValue(h)
            self.interval_minute_spin.setValue(m)
            self.interval_second_spin.setValue(s)
        elif trigger_type == "cron":
            self.cron_edit.setText(params.get("cron_expression", "0 0 9 * * * *"))
        elif trigger_type == "date":
            if params.get("run_date"):
                dt = QDateTime.fromString(params["run_date"], Qt.ISODate)
                if dt.isValid():
                    self.date_edit.setDateTime(dt)