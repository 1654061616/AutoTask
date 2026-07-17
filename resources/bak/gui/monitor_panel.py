from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QTextEdit, QProgressBar,
                               QLabel, QHBoxLayout)
from PySide6.QtCore import Qt

class MonitorPanel(QGroupBox):
    def __init__(self):
        super().__init__("运行监控")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlaceholderText("运行日志将显示在这里...")
        layout.addWidget(self.log_text)
        
        progress_layout = QHBoxLayout()
        self.progress_label = QLabel("进度:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        layout.addLayout(progress_layout)
        
        status_layout = QHBoxLayout()
        self.status_label = QLabel("状态: 就绪")
        self.current_step_label = QLabel("当前步骤: 无")
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.current_step_label)
        layout.addLayout(status_layout)
        
        self.setLayout(layout)
    
    def add_log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def set_progress(self, value):
        self.progress_bar.setValue(value)
    
    def set_status(self, status):
        self.status_label.setText(f"状态: {status}")
    
    def set_current_step(self, step_name):
        self.current_step_label.setText(f"当前步骤: {step_name}")
    
    def clear_log(self):
        self.log_text.clear()
    
    def reset(self):
        self.clear_log()
        self.set_progress(0)
        self.set_status("就绪")
        self.set_current_step("无")