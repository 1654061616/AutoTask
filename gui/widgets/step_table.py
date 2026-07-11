from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView,
                               QMenu, QMessageBox, QAbstractItemView)
from PySide6.QtGui import QIcon, QColor, QBrush, QPixmap
from PySide6.QtCore import Qt, Signal, Slot, QPoint
import sys
import os

from ..step_editor import STEP_TYPE_MAP

STEP_TYPE_COLORS = {
    "mouse_click": "#b3e5fc",
    "mouse_move": "#b3e5fc",
    "mouse_drag": "#b3e5fc",
    "mouse_scroll": "#b3e5fc",
    "keyboard_type": "#c8e6c9",
    "keyboard_press": "#f8bbd9",
    "keyboard_hotkey": "#f8bbd9",
    "image_find": "#e1bee7",
    "image_click": "#e1bee7",
    "image_exists": "#e1bee7",
    "window_find": "#b2dfdb",
    "window_activate": "#b2dfdb",
    "window_close": "#b2dfdb",
    "window_position": "#b2dfdb",
    "excel_read": "#ffcc80",
    "wait": "#fff9c4",
    "if_else": "#ffcdd2",
    "loop": "#e0e0e0",
    "log": "#f5f5f5",
    "label": "#e0e0e0",
    "goto": "#e0e0e0",
    "set_variable": "#bbdefb",
    "get_variable": "#bbdefb"
}

STEP_TYPE_ICONS = {
    "mouse_click": "🖱️",
    "mouse_move": "↔️",
    "mouse_drag": "✋",
    "mouse_scroll": "🖲️",
    "keyboard_type": "⌨️",
    "keyboard_press": "🔑",
    "keyboard_hotkey": "⚡",
    "image_find": "🔍",
    "image_click": "🎯",
    "image_exists": "❓",
    "window_find": "🔍",
    "window_activate": "📱",
    "window_close": "❌",
    "window_position": "📐",
    "excel_read": "📊",
    "wait": "⏳",
    "if_else": "🔀",
    "loop": "🔄",
    "log": "📝",
    "label": "🏷️",
    "goto": "➡️",
    "set_variable": "🔧",
    "get_variable": "📥"
}


class StepTable(QTableWidget):
    step_added = Signal()
    step_edited = Signal(int)
    step_deleted = Signal(int)
    step_moved_up = Signal(int)
    step_moved_down = Signal(int)
    step_copied = Signal(int)
    step_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._init_context_menu()
        self._steps = []

    def _init_ui(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["序号", "类型", "描述", "参数", "延时(秒)"])
        
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                gridline-color: #eee;
                background-color: #ffffff;
            }
            QTableWidget::item {
                padding: 6px;
                height: 32px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)

    def _init_context_menu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _show_context_menu(self, pos: QPoint):
        row = self.rowAt(pos.y())
        if row < 0:
            return

        menu = QMenu(self)

        edit_action = menu.addAction("编辑步骤")
        copy_action = menu.addAction("复制步骤")
        delete_action = menu.addAction("删除步骤")
        menu.addSeparator()
        move_up_action = menu.addAction("上移")
        move_down_action = menu.addAction("下移")

        edit_action.triggered.connect(lambda: self.step_edited.emit(row))
        copy_action.triggered.connect(lambda: self.step_copied.emit(row))
        delete_action.triggered.connect(lambda: self.step_deleted.emit(row))
        move_up_action.triggered.connect(lambda: self.step_moved_up.emit(row))
        move_down_action.triggered.connect(lambda: self.step_moved_down.emit(row))

        menu.exec(self.mapToGlobal(pos))

    def set_steps(self, steps: list):
        self._steps = steps.copy()
        self._refresh_table()

    def get_steps(self) -> list:
        return self._steps.copy()

    def _refresh_table(self):
        self.setRowCount(0)
        for index, step in enumerate(self._steps):
            self._add_row(index, step)

    def _add_row(self, index: int, step: dict):
        row = self.rowCount()
        self.insertRow(row)

        step_type = step.get("type", "")
        display_name = STEP_TYPE_MAP.get(step_type, step_type)
        icon = STEP_TYPE_ICONS.get(step_type, "📋")
        color = STEP_TYPE_COLORS.get(step_type, "#ffffff")

        num_item = QTableWidgetItem(str(index + 1))
        num_item.setTextAlignment(Qt.AlignCenter)
        num_item.setBackground(QBrush(QColor(color)))

        type_item = QTableWidgetItem(f"{icon} {display_name}")
        type_item.setTextAlignment(Qt.AlignCenter)
        type_item.setBackground(QBrush(QColor(color)))
        type_item.setData(Qt.UserRole, step_type)

        desc_item = QTableWidgetItem(step.get("description", ""))
        desc_item.setBackground(QBrush(QColor(color)))

        params_str = step.get("params", "")
        if isinstance(params_str, dict):
            params_display = self._format_params(params_str)
        else:
            params_display = str(params_str)
        params_item = QTableWidgetItem(params_display[:100] + "..." if len(str(params_display)) > 100 else params_display)
        params_item.setBackground(QBrush(QColor(color)))

        delay = step.get("delay", 0)
        if isinstance(delay, dict):
            delay = delay.get("delay", 0)
        delay_item = QTableWidgetItem(str(delay))
        delay_item.setTextAlignment(Qt.AlignCenter)
        delay_item.setBackground(QBrush(QColor(color)))

        self.setItem(row, 0, num_item)
        self.setItem(row, 1, type_item)
        self.setItem(row, 2, desc_item)
        self.setItem(row, 3, params_item)
        self.setItem(row, 4, delay_item)

    def _format_params(self, params: dict) -> str:
        display_parts = []
        if "image_path" in params:
            display_parts.append(f"图片: {os.path.basename(params['image_path'])}")
        if "text" in params:
            display_parts.append(f"文本: {params['text'][:30]}")
        if "key" in params:
            display_parts.append(f"按键: {params['key']}")
        if "hotkey" in params:
            display_parts.append(f"热键: {params['hotkey']}")
        if "x" in params and "y" in params:
            display_parts.append(f"位置: ({params['x']}, {params['y']})")
        if "click_type" in params:
            display_parts.append(f"点击: {params['click_type']}")
        if "wait_time" in params:
            display_parts.append(f"等待: {params['wait_time']}s")
        if "variable_name" in params:
            display_parts.append(f"变量: {params['variable_name']}")
        if "value" in params:
            display_parts.append(f"值: {params['value'][:30]}")
        return ", ".join(display_parts) if display_parts else "无参数"

    def add_step(self, step: dict):
        self._steps.append(step)
        self._refresh_table()
        self.step_added.emit()

    def insert_step_at(self, index: int, step: dict):
        self._steps.insert(index, step)
        self._refresh_table()

    def update_step_at(self, index: int, step: dict):
        if 0 <= index < len(self._steps):
            self._steps[index] = step
            self._refresh_table()

    def remove_step_at(self, index: int):
        if 0 <= index < len(self._steps):
            del self._steps[index]
            self._refresh_table()

    def move_step_up(self, index: int):
        if index > 0 and index < len(self._steps):
            self._steps[index], self._steps[index - 1] = self._steps[index - 1], self._steps[index]
            self._refresh_table()
            self.setCurrentRow(index - 1)

    def move_step_down(self, index: int):
        if index >= 0 and index < len(self._steps) - 1:
            self._steps[index], self._steps[index + 1] = self._steps[index + 1], self._steps[index]
            self._refresh_table()
            self.setCurrentRow(index + 1)

    def copy_step_at(self, index: int):
        if 0 <= index < len(self._steps):
            step_copy = self._steps[index].copy()
            step_copy["id"] = step_copy.get("id", "") + "_copy"
            self._steps.insert(index + 1, step_copy)
            self._refresh_table()
            self.setCurrentRow(index + 1)

    def get_current_step_index(self) -> int:
        return self.currentRow()

    def get_step_at(self, index: int) -> dict:
        if 0 <= index < len(self._steps):
            return self._steps[index]
        return {}

    def clear_all(self):
        self._steps = []
        self.setRowCount(0)

    def get_step_count(self) -> int:
        return len(self._steps)
