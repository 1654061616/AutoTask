from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                               QComboBox, QSpinBox, QDateTimeEdit, QPushButton,
                               QHBoxLayout, QGroupBox, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt, QDateTime, Signal
import datetime

class SchedulerDialog(QDialog):
    task_scheduled = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("定时调度")
        self.setModal(True)
        self.setGeometry(200, 200, 500, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)
        
        trigger_group = QGroupBox("触发类型")
        trigger_layout = QFormLayout(trigger_group)
        
        self.trigger_combo = QComboBox()
        self.trigger_combo.addItems(["interval", "cron", "date"])
        trigger_layout.addRow("类型:", self.trigger_combo)
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 3600)
        self.interval_spin.setValue(60)
        trigger_layout.addRow("间隔(秒):", self.interval_spin)
        
        self.cron_hour_spin = QSpinBox()
        self.cron_hour_spin.setRange(0, 23)
        trigger_layout.addRow("小时:", self.cron_hour_spin)
        
        self.cron_minute_spin = QSpinBox()
        self.cron_minute_spin.setRange(0, 59)
        trigger_layout.addRow("分钟:", self.cron_minute_spin)
        
        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        trigger_layout.addRow("执行时间:", self.date_edit)
        
        layout.addWidget(trigger_group)
        
        self.task_name_edit = QLineEdit()
        self.task_name_edit.setPlaceholderText("任务名称")
        layout.addWidget(self.task_name_edit)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加任务")
        self.remove_button = QPushButton("删除任务")
        self.start_button = QPushButton("启动调度")
        self.close_button = QPushButton("关闭")
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.trigger_combo.currentTextChanged.connect(self.on_trigger_changed)
        self.add_button.clicked.connect(self.on_add_task)
        self.remove_button.clicked.connect(self.on_remove_task)
        self.start_button.clicked.connect(self.on_start_scheduler)
        self.close_button.clicked.connect(self.close)
        
        self.on_trigger_changed(self.trigger_combo.currentText())
    
    def on_trigger_changed(self, trigger_type):
        self.interval_spin.setVisible(trigger_type == "interval")
        self.cron_hour_spin.setVisible(trigger_type == "cron")
        self.cron_minute_spin.setVisible(trigger_type == "cron")
        self.date_edit.setVisible(trigger_type == "date")
    
    def on_add_task(self):
        task_name = self.task_name_edit.text() or "未命名任务"
        trigger_type = self.trigger_combo.currentText()
        
        config = {"type": trigger_type}
        
        if trigger_type == "interval":
            config["interval"] = self.interval_spin.value()
        elif trigger_type == "cron":
            config["hour"] = self.cron_hour_spin.value()
            config["minute"] = self.cron_minute_spin.value()
        elif trigger_type == "date":
            config["run_date"] = self.date_edit.dateTime().toPython()
        
        item = QListWidgetItem(f"{task_name} - {trigger_type}")
        item.setData(Qt.UserRole, config)
        self.task_list.addItem(item)
        self.task_name_edit.clear()
    
    def on_remove_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            self.task_list.takeItem(self.task_list.row(current_item))
    
    def on_start_scheduler(self):
        tasks = []
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            config = item.data(Qt.UserRole)
            tasks.append(config)
        
        if tasks:
            self.task_scheduled.emit({"tasks": tasks})
            self.accept()