"""任务执行 Mixin：启动、停止、日志、进度回调"""

from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, Slot
from gui.styles import Styles, Colors


class TaskExecutorMixin:
    """任务执行 Mixin：运行/停止任务、日志处理、进度更新"""

    @Slot()
    def on_run_flow(self):
        current_item = self.task_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "运行失败", "请先选择一个任务")
            return

        task = current_item.data(0, Qt.UserRole)
        self._start_task(task, current_item)

    def _start_task(self, task, item=None):
        if item is None:
            item = self.task_tree.currentItem()
            if not item:
                return

        task["status"] = "执行中"
        self.current_flow = task
        item.setData(0, Qt.UserRole, task)
        self._update_status_widget(item, "执行中")

        self._is_manual_executing = True
        self._update_task_status_label()
        self.task_status_label.setStyleSheet(Styles.status_label(Colors.SUCCESS))
        self.status_label.setText("运行中...")
        self.log_panel.append(f"开始执行任务: {task['name']}")

        self.start_task_btn.setEnabled(False)
        self.stop_task_btn.setEnabled(True)

        flow_data = {
            "id": task["id"],
            "name": task["name"],
            "version": task.get("version", "1.0"),
            "nodes": task.get("nodes", []),
            "edges": task.get("edges", []),
            "schedule": task.get("schedule", {})
        }

        self.engine.load_flow(flow_data)
        self.engine.add_completed_callback(self._on_task_completed)
        self.engine.run()
        self.flow_started.emit()

    def _on_engine_log(self, log_entry: str):
        self.log_received.emit(log_entry)

    @Slot(str)
    def _on_log_received(self, log_entry: str):
        self.log_panel.append(log_entry)

    def _on_task_completed(self, success: bool, error_message: str):
        self.task_completed.emit(success, error_message)

    @Slot(bool, str)
    def _on_task_completed_slot(self, success: bool, error_message: str):
        self._is_manual_executing = False

        if self.current_flow:
            current_item = None
            for i in range(self.task_tree.topLevelItemCount()):
                item = self.task_tree.topLevelItem(i)
                if item.data(0, Qt.UserRole) == self.current_flow:
                    current_item = item
                    break

            if current_item:
                self.current_flow["status"] = "已停止"
                current_item.setData(0, Qt.UserRole, self.current_flow)
                self._update_status_widget(current_item, "已停止")
                self._update_task_status_label()
                self.task_status_label.setStyleSheet(Styles.status_label("#e74c3c"))

        if success:
            self.status_label.setText("任务执行完成")
            self.log_panel.append("任务执行完成")
        else:
            self.status_label.setText("任务执行异常")
            self.log_panel.append(f"任务执行异常: {error_message}")

        if not getattr(self, '_is_scheduled_executing', False):
            self.start_task_btn.setEnabled(True)
        self.stop_task_btn.setEnabled(False)
        self.flow_stopped.emit()

        if getattr(self, '_is_scheduled_executing', False):
            self._on_scheduled_task_completed()

    @Slot()
    def on_stop_flow(self):
        current_item = self.task_tree.currentItem()
        if current_item:
            task = current_item.data(0, Qt.UserRole)
            self._stop_task(task, current_item)

    def _stop_task(self, task, item=None):
        if item is None:
            item = self.task_tree.currentItem()
            if not item:
                return

        self._is_manual_executing = False
        self.engine.stop()
        task["status"] = "已停止"
        item.setData(0, Qt.UserRole, task)
        self._update_status_widget(item, "已停止")

        self._update_task_status_label()
        self.task_status_label.setStyleSheet(Styles.status_label("#e74c3c"))
        self.status_label.setText("已停止")
        self.log_panel.append(f"停止任务: {task['name']}")

        if not getattr(self, '_is_scheduled_executing', False):
            self.start_task_btn.setEnabled(True)
        self.stop_task_btn.setEnabled(False)
        self.flow_stopped.emit()

    @Slot()
    def on_clear_log(self):
        self.log_panel.clear()
        self.log_panel.append("日志已清空")

    def add_log(self, message):
        self.log_panel.append(message)
        self.log_panel.verticalScrollBar().setValue(
            self.log_panel.verticalScrollBar().maximum()
        )

    def update_progress(self, value):
        self.progress_bar.show()
        self.progress_bar.setValue(value)