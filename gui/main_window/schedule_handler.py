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

        self.scheduler = TaskScheduler()
        self.scheduler.add_task(
            task_id=self.current_flow.get("id", "scheduled"),
            name=self.current_flow.get("name", "定时任务"),
            trigger_type=trigger_type,
            func=lambda: self._execute_scheduled_task(),
            **params
        )
        self.scheduler.start()
        self.log_panel.append(f"定时任务已启动: {trigger_type}")
        self._update_task_status_label()

        self.schedule_panel.set_schedule_running()

    def _execute_scheduled_task(self):
        self._is_scheduled_executing = True
        self._update_task_status_label()

        self.start_task_btn.setEnabled(False)
        self.stop_task_btn.setEnabled(True)

        self.on_run_flow()

    def _on_scheduled_task_completed(self):
        self._is_scheduled_executing = False
        self._update_task_status_label()

        if not self._is_manual_executing:
            self.start_task_btn.setEnabled(True)

    def _on_stop_scheduled(self):
        if hasattr(self, 'scheduler') and self.scheduler:
            self.scheduler.stop()
            self.scheduler = None
        self.log_panel.append("定时任务已停止")
        self._update_task_status_label()

        self.schedule_panel.set_schedule_stopped()

    def _update_task_status_label(self):
        is_scheduled = hasattr(self, 'scheduler') and self.scheduler is not None
        is_scheduled_executing = getattr(self, '_is_scheduled_executing', False)
        is_manual_executing = getattr(self, '_is_manual_executing', False)

        if is_manual_executing and is_scheduled:
            text = "定时中；手动执行中"
        elif is_scheduled_executing:
            text = "定时任务执行中"
        elif is_manual_executing:
            text = "执行中"
        elif is_scheduled:
            text = "定时中"
        else:
            text = "已停止"

        self.task_status_label.setText(text)