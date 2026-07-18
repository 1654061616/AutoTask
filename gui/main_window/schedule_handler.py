"""定时任务 Mixin：定时启停、配置加载"""

from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Slot
from gui.styles import Styles


class ScheduleHandlerMixin:
    """定时任务 Mixin：启动/停止定时任务、加载定时配置"""

    def load_schedule_settings(self, task):
        schedule_config = task.get("schedule", {})
        self.schedule_panel.load_config(schedule_config)

    @Slot()
    def _on_start_scheduled(self):
        from core.scheduler import TaskScheduler

        if self.current_flow is None:
            QMessageBox.warning(self, "启动失败", "请先选择一个任务")
            return

        config = self.schedule_panel.get_config()
        if config is None:
            return

        trigger_type = config["trigger_type"]
        params = config["params"]

        if trigger_type == "immediate":
            QMessageBox.information(self, "定时任务", "立即执行任务已启动")
            self.on_run_flow()
            return

        self.scheduler = TaskScheduler()
        self.scheduler.add_task(
            task_id=self.current_flow.get("id", "scheduled"),
            name=self.current_flow.get("name", "定时任务"),
            trigger_type=trigger_type,
            func=lambda: self.on_run_flow(),
            **params
        )
        self.scheduler.start()
        self.log_panel.append(f"定时任务已启动: {trigger_type}")
        self.task_status_label.setText("定时中")

        self.start_scheduled_btn = self.schedule_panel.start_scheduled_btn
        self.start_scheduled_btn.setText("■ 停止定时")
        self.start_scheduled_btn.setStyleSheet(Styles.schedule_btn_stop())
        self.start_scheduled_btn.clicked.disconnect()
        self.start_scheduled_btn.clicked.connect(self._on_stop_scheduled)

    def _on_stop_scheduled(self):
        if hasattr(self, 'scheduler') and self.scheduler:
            self.scheduler.stop()
            self.scheduler = None
        self.log_panel.append("定时任务已停止")
        self.task_status_label.setText("已停止")

        self.start_scheduled_btn = self.schedule_panel.start_scheduled_btn
        self.start_scheduled_btn.setText("▶ 开始定时")
        self.start_scheduled_btn.setStyleSheet(Styles.schedule_btn_start())
        self.start_scheduled_btn.clicked.disconnect()
        self.start_scheduled_btn.clicked.connect(lambda: self.schedule_panel.start_scheduled.emit())