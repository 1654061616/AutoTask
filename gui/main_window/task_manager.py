import os
import uuid
import json

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTreeWidgetItem,
                               QFileDialog, QMessageBox, QInputDialog)
from PySide6.QtCore import Qt, Slot

from utils.resource_path import ensure_resources_dir
from gui.styles import Styles, Colors
from gui.styles.theme_manager import ThemeManager


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
                        "version": flow_data.get("version", "1.0"),
                        "status": "已停止",
                        "nodes": flow_data.get("nodes", []),
                        "edges": flow_data.get("edges", []),
                        "variables": flow_data.get("variables", {}),
                        "global_config": flow_data.get("global_config", {}),
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
        widget_layout.setSpacing(4)
        widget_layout.addStretch()

        # 状态按钮
        status_btn = QPushButton()
        status_btn.setFixedSize(28, 28)
        if "执行中" in status:
            status_btn.setIcon(ThemeManager.load_icon("停止.svg", "media-stop"))
            status_btn.setToolTip("点击停止任务")
        else:
            status_btn.setIcon(ThemeManager.load_icon("运行.svg", "media-play"))
            status_btn.setToolTip("点击执行任务")
        status_btn.setStyleSheet(Styles.task_tree_icon_btn("#3498db", "#e8f4fd"))
        status_btn.clicked.connect(lambda checked, t=task: self.on_toggle_task(t))

        # 定时按钮
        schedule_btn = QPushButton()
        schedule_btn.setFixedSize(28, 28)
        schedule_active = task.get("schedule_active", False)
        if schedule_active:
            schedule_btn.setIcon(ThemeManager.load_icon("定时执行.svg", "media-play"))
            schedule_btn.setToolTip("点击暂停定时任务")
        else:
            schedule_btn.setIcon(ThemeManager.load_icon("定时暂停.svg", "media-pause"))
            schedule_btn.setToolTip("点击启动定时任务")
        schedule_btn.setStyleSheet(Styles.task_tree_icon_btn("#3498db", "#e8f4fd"))
        schedule_btn.clicked.connect(lambda checked, t=task: self.on_toggle_schedule(t))

        # 保存按钮
        save_btn = QPushButton()
        save_btn.setFixedSize(28, 28)
        save_btn.setIcon(ThemeManager.load_icon("保存.svg", "document-save"))
        save_btn.setStyleSheet(Styles.task_tree_icon_btn("#3498db", "#e8f4fd"))
        save_btn.setToolTip("保存任务")
        save_btn.clicked.connect(lambda checked, t=task: self.on_save_flow(t))

        # 另存为按钮
        save_as_btn = QPushButton()
        save_as_btn.setFixedSize(28, 28)
        save_as_btn.setIcon(ThemeManager.load_icon("另存为.svg", "document-save-as"))
        save_as_btn.setStyleSheet(Styles.task_tree_icon_btn("#3498db", "#e8f4fd"))
        save_as_btn.setToolTip("另存为")
        save_as_btn.clicked.connect(lambda checked, t=task: self.on_save_as_flow(t))

        # 删除按钮
        delete_btn = QPushButton()
        delete_btn.setFixedSize(28, 28)
        delete_btn.setIcon(ThemeManager.load_icon("删除.svg", "edit-delete"))
        delete_btn.setStyleSheet(Styles.task_tree_icon_btn("#e74c3c", "#fce4ec"))
        delete_btn.setToolTip("删除任务")
        delete_btn.clicked.connect(lambda checked, t=task: self.on_delete_task(t))

        widget_layout.addWidget(status_btn)
        widget_layout.addWidget(schedule_btn)
        widget_layout.addWidget(save_btn)
        widget_layout.addWidget(save_as_btn)
        widget_layout.addWidget(delete_btn)
        self.task_tree.setItemWidget(item, 1, widget)

    @Slot()
    def on_new_flow(self):
        # 点击菜单"新建"或工具栏新建图标都会触发 on_new_flow，创建新的空白流程
        flow_name, ok = QInputDialog.getText(self, "新建任务", "输入任务名称:")
        if ok and flow_name.strip():
            name = flow_name.strip()
        else:
            name = f"任务_{len(self.task_tree.findItems('', Qt.MatchContains)) + 1}"

        task = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "version": "1.0",
            "status": "已停止",
            "nodes": [],
            "edges": [],
            "variables": {},
            "global_config": {},
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
            "version": task.get("version", "1.0"),
            "status": "已停止",
            "nodes": [dict(n) for n in task.get("nodes", [])],
            "edges": [dict(e) for e in task.get("edges", [])],
            "variables": dict(task.get("variables", {})),
            "global_config": dict(task.get("global_config", {})),
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
                    "version": flow_data.get("version", "1.0"),
                    "status": "已停止",
                    "nodes": flow_data.get("nodes", []),
                    "edges": flow_data.get("edges", []),
                    "variables": flow_data.get("variables", {}),
                    "global_config": flow_data.get("global_config", {}),
                    "schedule": flow_data.get("schedule", {}),
                    "file_path": file_path
                }
                self.add_task_to_tree(task)
                self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
                self.task_name_edit.setText(flow_name)
                self.load_nodes_from_flow(flow_data)
                self.load_schedule_settings(task)
                self.load_wait_config(task.get("global_config", {}))
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

                global_config = dict(task.get("global_config", {}))
                global_config.update(self.get_wait_config())

                save_data = {
                    "id": task.get("id", ""),
                    "name": self.task_name_edit.text() or task.get("name", ""),
                    "version": "1.0",
                    "status": task.get("status", "已停止"),
                    "nodes": nodes,
                    "edges": edges,
                    "variables": task.get("variables", {}),
                    "global_config": global_config,
                    "schedule": self.schedule_panel.get_config()
                }

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, indent=2, ensure_ascii=False)

                task["file_path"] = file_path
                task["name"] = save_data["name"]
                task["version"] = save_data["version"]
                task["nodes"] = save_data["nodes"]
                task["edges"] = save_data["edges"]
                task["variables"] = save_data["variables"]
                task["global_config"] = save_data["global_config"]

                if current_item:
                    current_item.setText(0, save_data["name"])
                    current_item.setData(0, Qt.UserRole, task)

                self.status_label.setText(f"已保存: {os.path.basename(file_path)}")
                self.log_panel.append(f"保存任务: {save_data['name']}")
            except Exception as e:
                QMessageBox.warning(self, "保存失败", f"无法保存任务文件: {str(e)}")

    @Slot()
    def on_save_as_flow(self, task=None):
        if task is None:
            current_item = self.task_tree.currentItem()
            if not current_item:
                QMessageBox.warning(self, "另存失败", "请先选择一个任务")
                return
            task = current_item.data(0, Qt.UserRole)

        if not task:
            QMessageBox.warning(self, "另存失败", "未找到任务数据")
            return

        resources_dir = ensure_resources_dir()
        default_name = task.get("name", "未命名任务")
        default_path = os.path.join(resources_dir, f"{default_name}.json")
        file_path, _ = QFileDialog.getSaveFileName(
            self, "另存为", default_path, "JSON文件 (*.json)"
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

                save_name = os.path.splitext(os.path.basename(file_path))[0]
                global_config = dict(task.get("global_config", {}))
                global_config.update(self.get_wait_config())
                save_data = {
                    "id": str(uuid.uuid4())[:8],
                    "name": save_name,
                    "version": "1.0",
                    "status": "已停止",
                    "nodes": nodes,
                    "edges": edges,
                    "variables": task.get("variables", {}),
                    "global_config": global_config,
                    "schedule": self.schedule_panel.get_config() if hasattr(self, 'schedule_panel') else {}
                }

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, indent=2, ensure_ascii=False)

                new_task = {
                    "id": save_data["id"],
                    "name": save_name,
                    "version": save_data["version"],
                    "status": "已停止",
                    "nodes": save_data["nodes"],
                    "edges": save_data["edges"],
                    "variables": save_data["variables"],
                    "global_config": save_data["global_config"],
                    "schedule": save_data["schedule"],
                    "file_path": file_path
                }
                self.add_task_to_tree(new_task)
                self.task_tree.setCurrentItem(
                    self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1)
                )
                self.task_name_edit.setText(save_name)
                self.status_label.setText(f"已另存为: {os.path.basename(file_path)}")
                self.log_panel.append(f"另存为: {save_name}")
            except Exception as e:
                QMessageBox.warning(self, "另存失败", f"无法保存任务文件: {str(e)}")

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
            self.load_wait_config(task.get("global_config", {}))
            self.log_panel.append(f"选择任务: {task['name']}")

    def _update_status_widget(self, item, status):
        widget = self.task_tree.itemWidget(item, 1)
        if widget:
            btn = widget.findChild(QPushButton)
            if btn:
                if "执行中" in status:
                    btn.setIcon(ThemeManager.load_icon("停止.svg", "media-stop"))
                    btn.setToolTip("点击停止任务")
                else:
                    btn.setIcon(ThemeManager.load_icon("运行.svg", "media-play"))
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

    @Slot()
    def on_toggle_schedule(self, task):
        item = None
        for i in range(self.task_tree.topLevelItemCount()):
            tree_item = self.task_tree.topLevelItem(i)
            if tree_item.data(0, Qt.UserRole) == task:
                item = tree_item
                break
        if not item:
            return

        schedule_active = task.get("schedule_active", False)
        if schedule_active:
            task["schedule_active"] = False
            item.setData(0, Qt.UserRole, task)
            self._update_schedule_widget(item, False)
            self._on_stop_scheduled()
            self.log_panel.append(f"暂停定时任务: {task['name']}")
        else:
            self.task_tree.setCurrentItem(item)
            self.current_flow = task
            task["schedule_active"] = True
            item.setData(0, Qt.UserRole, task)
            self._update_schedule_widget(item, True)
            self.schedule_panel.start_scheduled.emit()
            self.log_panel.append(f"启动定时任务: {task['name']}")

    def _update_schedule_widget(self, item, active):
        widget = self.task_tree.itemWidget(item, 1)
        if widget:
            buttons = widget.findChildren(QPushButton)
            if len(buttons) >= 2:
                schedule_btn = buttons[1]
                if active:
                    schedule_btn.setIcon(ThemeManager.load_icon("定时执行.svg", "media-play"))
                    schedule_btn.setToolTip("点击暂停定时任务")
                else:
                    schedule_btn.setIcon(ThemeManager.load_icon("定时暂停.svg", "media-pause"))
                    schedule_btn.setToolTip("点击启动定时任务")