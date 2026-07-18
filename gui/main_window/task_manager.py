import os
import uuid
import json

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTreeWidgetItem,
                               QFileDialog, QMessageBox, QInputDialog)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Slot

from utils.resource_path import ensure_resources_dir
from gui.styles import Styles, Colors


class TaskManagerMixin:
    """任务管理 Mixin：新建、复制、删除、打开、保存、重命名、选择、切换"""

    def load_default_tasks(self):
        resources_dir = ensure_resources_dir()
        for filename in os.listdir(resources_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(resources_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        flow_data = json.load(f)
                    task = {
                        "id": flow_data.get("id", str(uuid.uuid4())[:8]),
                        "name": flow_data.get("name", os.path.splitext(filename)[0]),
                        "status": "已停止",
                        "nodes": flow_data.get("nodes", []),
                        "edges": flow_data.get("edges", []),
                        "schedule": flow_data.get("schedule", {}),
                        "file_path": file_path
                    }
                    self.add_task_to_tree(task)
                except Exception as e:
                    print(f"加载任务文件失败: {filename} - {str(e)}")

    def add_task_to_tree(self, task):
        item = QTreeWidgetItem(self.task_tree)
        item.setText(0, task["name"])
        item.setData(0, Qt.UserRole, task)
        item.setFlags(item.flags() | Qt.ItemIsEditable)

        status = task["status"]

        widget = QWidget()
        widget_layout = QHBoxLayout(widget)
        widget_layout.setContentsMargins(2, 2, 2, 2)
        widget_layout.setSpacing(2)

        # 状态按钮
        status_btn = QPushButton()
        status_btn.setFixedSize(20, 20)
        if "执行中" in status:
            status_btn.setStyleSheet(Styles.task_tree_status_btn("#4caf50"))
            status_btn.setToolTip("点击停止任务")
        else:
            status_btn.setStyleSheet(Styles.task_tree_status_btn("#e74c3c"))
            status_btn.setToolTip("点击执行任务")
        status_btn.clicked.connect(lambda checked, t=task: self.on_toggle_task(t))

        # 保存按钮
        save_btn = QPushButton()
        save_btn.setIcon(QIcon.fromTheme("document-save", QIcon()))
        save_btn.setStyleSheet(Styles.task_tree_icon_btn("#3498db", "#e8f4fd"))
        save_btn.setToolTip("保存任务")
        save_btn.clicked.connect(lambda checked, t=task: self.on_save_flow(t))

        # 删除按钮
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon.fromTheme("edit-delete", QIcon()))
        delete_btn.setStyleSheet(Styles.task_tree_icon_btn("#e74c3c", "#fce4ec"))
        delete_btn.setToolTip("删除任务")
        delete_btn.clicked.connect(lambda checked, t=task: self.on_delete_task(t))

        widget_layout.addWidget(status_btn)
        widget_layout.addWidget(save_btn)
        widget_layout.addWidget(delete_btn)
        self.task_tree.setItemWidget(item, 1, widget)

    @Slot()
    def on_new_flow(self):
        flow_name, ok = QInputDialog.getText(self, "新建任务", "输入任务名称:")
        if ok and flow_name.strip():
            name = flow_name.strip()
        else:
            name = f"任务_{len(self.task_tree.findItems('', Qt.MatchContains)) + 1}"

        task = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "status": "已停止",
            "steps": [],
            "file_path": None
        }
        self.add_task_to_tree(task)
        self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
        self.status_label.setText(f"已新建任务: {name}")
        self.log_panel.append(f"新建任务: {name}")

    @Slot()
    def on_copy_task(self):
        current_item = self.task_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "复制失败", "请先选择一个任务")
            return

        task = current_item.data(0, Qt.UserRole)
        new_task = {
            "id": str(uuid.uuid4())[:8],
            "name": task["name"] + " (复制)",
            "status": "已停止",
            "steps": [dict(s) for s in task.get("steps", [])],
            "file_path": None
        }
        self.add_task_to_tree(new_task)
        self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
        self.status_label.setText(f"已复制任务: {new_task['name']}")
        self.log_panel.append(f"复制任务: {new_task['name']}")

    @Slot()
    def on_delete_task(self, task=None):
        if task is None:
            current_item = self.task_tree.currentItem()
            if not current_item:
                QMessageBox.warning(self, "删除失败", "请先选择一个任务")
                return
            task = current_item.data(0, Qt.UserRole)
        else:
            current_item = None
            for i in range(self.task_tree.topLevelItemCount()):
                item = self.task_tree.topLevelItem(i)
                if item.data(0, Qt.UserRole) == task:
                    current_item = item
                    break
            if not current_item:
                QMessageBox.warning(self, "删除失败", "未找到任务")
                return

        reply = QMessageBox.question(
            self, "确认删除", f"确定要删除任务 '{task['name']}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            index = self.task_tree.indexOfTopLevelItem(current_item)
            if index != -1:
                self.task_tree.takeTopLevelItem(index)
                self.status_label.setText(f"已删除任务: {task['name']}")
                self.log_panel.append(f"删除任务: {task['name']}")
                self.graph_scene.clear_all()
                self.task_name_edit.clear()
                self.task_status_label.setText("已停止")
                self.task_status_label.setStyleSheet(Styles.status_label("#e74c3c"))

    @Slot()
    def on_open_flow(self):
        resources_dir = ensure_resources_dir()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开任务文件", resources_dir, "JSON文件 (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    flow_data = json.load(f)
                flow_name = flow_data.get("name", os.path.basename(file_path))
                task = {
                    "id": flow_data.get("id", str(uuid.uuid4())[:8]),
                    "name": flow_name,
                    "status": "已停止",
                    "nodes": flow_data.get("nodes", []),
                    "edges": flow_data.get("edges", []),
                    "schedule": flow_data.get("schedule", {}),
                    "file_path": file_path
                }
                self.add_task_to_tree(task)
                self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
                self.task_name_edit.setText(flow_name)
                self.load_nodes_from_flow(flow_data)
                self.load_schedule_settings(task)
                self.status_label.setText(f"打开任务: {flow_name}")
                self.log_panel.append(f"打开任务: {flow_name}")
            except Exception as e:
                QMessageBox.warning(self, "打开失败", f"无法打开任务文件: {str(e)}")

    @Slot()
    def on_save_flow(self, task=None):
        if task is None:
            current_item = self.task_tree.currentItem()
            if not current_item:
                if self.current_flow:
                    task = self.current_flow
                    for i in range(self.task_tree.topLevelItemCount()):
                        item = self.task_tree.topLevelItem(i)
                        if item.data(0, Qt.UserRole) == task:
                            current_item = item
                            break
                else:
                    QMessageBox.warning(self, "保存失败", "请先选择一个任务")
                    return
            task = current_item.data(0, Qt.UserRole) if current_item else self.current_flow
        else:
            current_item = None
            for i in range(self.task_tree.topLevelItemCount()):
                item = self.task_tree.topLevelItem(i)
                if item.data(0, Qt.UserRole) == task:
                    current_item = item
                    break

        if not task:
            QMessageBox.warning(self, "保存失败", "未找到任务数据")
            return

        file_path = task.get("file_path")
        if not file_path:
            resources_dir = ensure_resources_dir()
            default_name = self.task_name_edit.text() or task.get("name", "未命名任务")
            default_path = os.path.join(resources_dir, f"{default_name}.json")
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存任务文件", default_path, "JSON文件 (*.json)"
            )

        if file_path:
            try:
                nodes = []
                edges = []
                if hasattr(self, 'graph_scene') and self.graph_scene:
                    graph_data = self.graph_scene.to_json()
                    if isinstance(graph_data, dict):
                        nodes = graph_data.get("nodes", [])
                        edges = graph_data.get("edges", [])
                if not nodes:
                    nodes = task.get("nodes", [])
                if not edges:
                    edges = task.get("edges", [])

                save_data = {
                    "id": task.get("id", ""),
                    "name": self.task_name_edit.text() or task.get("name", ""),
                    "version": "1.0",
                    "status": task.get("status", "已停止"),
                    "nodes": nodes,
                    "edges": edges,
                    "schedule": self.schedule_panel.get_config()
                }

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, indent=2, ensure_ascii=False)

                task["file_path"] = file_path
                task["name"] = save_data["name"]
                task["nodes"] = save_data["nodes"]
                task["edges"] = save_data["edges"]

                if current_item:
                    current_item.setText(0, save_data["name"])
                    current_item.setData(0, Qt.UserRole, task)

                self.status_label.setText(f"已保存: {os.path.basename(file_path)}")
                self.log_panel.append(f"保存任务: {save_data['name']}")
            except Exception as e:
                QMessageBox.warning(self, "保存失败", f"无法保存任务文件: {str(e)}")

    @Slot()
    def on_task_name_changed(self, item, column):
        if column == 0:
            task = item.data(0, Qt.UserRole)
            if task:
                old_name = task["name"]
                new_name = item.text(0)
                task["name"] = new_name
                item.setData(0, Qt.UserRole, task)
                self.log_panel.append(f"任务重命名: {old_name} -> {new_name}")
                if self.task_name_edit.text() == old_name:
                    self.task_name_edit.setText(new_name)

    @Slot()
    def on_task_selected(self, item, column):
        task = item.data(0, Qt.UserRole)
        if task:
            self.current_flow = task
            self.task_name_edit.setText(task.get("name", ""))
            self.task_status_label.setText(task.get("status", "已停止"))

            status = task.get("status", "")
            if "执行中" in status:
                self.task_status_label.setStyleSheet(Styles.status_label(Colors.SUCCESS))
            else:
                self.task_status_label.setStyleSheet(Styles.status_label("#e74c3c"))

            self.load_nodes_from_flow(task)
            self.load_schedule_settings(task)
            self.log_panel.append(f"选择任务: {task['name']}")

    def _update_status_widget(self, item, status):
        widget = self.task_tree.itemWidget(item, 1)
        if widget:
            btn = widget.findChild(QPushButton)
            if btn:
                if "执行中" in status:
                    btn.setStyleSheet(Styles.task_tree_status_btn("#4caf50"))
                    btn.setToolTip("点击停止任务")
                else:
                    btn.setStyleSheet(Styles.task_tree_status_btn("#e74c3c"))
                    btn.setToolTip("点击执行任务")

    @Slot()
    def on_toggle_task(self, task):
        item = None
        for i in range(self.task_tree.topLevelItemCount()):
            tree_item = self.task_tree.topLevelItem(i)
            if tree_item.data(0, Qt.UserRole) == task:
                item = tree_item
                break
        if not item:
            return

        if "执行中" in task.get("status", ""):
            self._stop_task(task, item)
            self.task_status_label.setText("已停止")
            self.task_status_label.setStyleSheet(Styles.status_label("#e74c3c"))
            self.status_label.setText("已停止")
            self.log_panel.append(f"停止执行任务: {task['name']}")
        else:
            self._start_task(task, item)