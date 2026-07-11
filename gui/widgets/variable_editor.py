from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QLineEdit, QComboBox, QMessageBox, QAbstractItemView,
                               QDialog, QFormLayout)
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt, Signal, Slot
from typing import Dict, Any


class VariableEditor(QWidget):
    variable_added = Signal(str, Any)
    variable_removed = Signal(str)
    variable_updated = Signal(str, Any)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._variables: Dict[str, Any] = {}
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        header_layout = QHBoxLayout()
        self.title_label = QLabel("变量管理")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        self.add_btn = QPushButton("添加变量")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 4px 12px; border-radius: 4px;")
        self.add_btn.clicked.connect(self._add_variable)
        header_layout.addWidget(self.add_btn)
        layout.addLayout(header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["变量名", "值", "类型"])
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                gridline-color: #eee;
                background-color: #ffffff;
            }
            QTableWidget::item {
                padding: 6px;
                height: 30px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 6px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.edit_btn = QPushButton("编辑")
        self.edit_btn.clicked.connect(self._edit_variable)
        
        self.delete_btn = QPushButton("删除")
        self.delete_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 4px 12px; border-radius: 4px;")
        self.delete_btn.clicked.connect(self._delete_variable)
        
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

    def set_variables(self, variables: Dict[str, Any]):
        self._variables = dict(variables)
        self._refresh_table()

    def get_variables(self) -> Dict[str, Any]:
        return dict(self._variables)

    def _refresh_table(self):
        self.table.setRowCount(0)
        for name, value in self._variables.items():
            self._add_row(name, value)

    def _add_row(self, name: str, value: Any):
        row = self.table.rowCount()
        self.table.insertRow(row)

        name_item = QTableWidgetItem(name)
        name_item.setBackground(QBrush(QColor("#bbdefb")))

        value_str = str(value)
        if len(value_str) > 50:
            value_str = value_str[:50] + "..."
        value_item = QTableWidgetItem(value_str)
        value_item.setBackground(QBrush(QColor("#bbdefb")))

        type_name = type(value).__name__
        type_item = QTableWidgetItem(type_name)
        type_item.setTextAlignment(Qt.AlignCenter)
        type_item.setBackground(QBrush(QColor("#bbdefb")))

        self.table.setItem(row, 0, name_item)
        self.table.setItem(row, 1, value_item)
        self.table.setItem(row, 2, type_item)

    def _add_variable(self):
        dialog = VariableEditDialog(self)
        if dialog.exec() == QDialog.Accepted:
            name = dialog.get_name()
            value = dialog.get_value()
            if name and name not in self._variables:
                self._variables[name] = value
                self._refresh_table()
                self.variable_added.emit(name, value)
            elif name in self._variables:
                QMessageBox.warning(self, "变量已存在", f"变量 '{name}' 已存在")

    def _edit_variable(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "选择变量", "请先选择一个变量")
            return

        name = self.table.item(current_row, 0).text()
        value = self._variables.get(name)
        
        dialog = VariableEditDialog(self, name, value)
        if dialog.exec() == QDialog.Accepted:
            new_name = dialog.get_name()
            new_value = dialog.get_value()
            
            if new_name != name and new_name in self._variables:
                QMessageBox.warning(self, "变量已存在", f"变量 '{new_name}' 已存在")
                return
            
            del self._variables[name]
            self._variables[new_name] = new_value
            self._refresh_table()
            self.variable_updated.emit(new_name, new_value)

    def _delete_variable(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "选择变量", "请先选择一个变量")
            return

        name = self.table.item(current_row, 0).text()
        
        reply = QMessageBox.question(
            self, "确认删除", f"确定要删除变量 '{name}' 吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            del self._variables[name]
            self._refresh_table()
            self.variable_removed.emit(name)

    def add_variable(self, name: str, value: Any):
        if name not in self._variables:
            self._variables[name] = value
            self._refresh_table()
            self.variable_added.emit(name, value)

    def remove_variable(self, name: str):
        if name in self._variables:
            del self._variables[name]
            self._refresh_table()
            self.variable_removed.emit(name)

    def update_variable(self, name: str, value: Any):
        if name in self._variables:
            self._variables[name] = value
            self._refresh_table()
            self.variable_updated.emit(name, value)

    def get_variable(self, name: str) -> Any:
        return self._variables.get(name)

    def clear_all(self):
        self._variables = {}
        self.table.setRowCount(0)


class VariableEditDialog(QDialog):
    def __init__(self, parent=None, name: str = "", value: Any = ""):
        super().__init__(parent)
        self.setWindowTitle("编辑变量")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self._name = name
        self._value = value
        
        self._init_ui()

    def _init_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        self.name_edit = QLineEdit(self._name)
        self.name_edit.setPlaceholderText("输入变量名")
        layout.addRow("变量名:", self.name_edit)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["字符串", "数字", "布尔值", "列表", "字典"])
        layout.addRow("类型:", self.type_combo)

        self.value_edit = QLineEdit(str(self._value))
        self.value_edit.setPlaceholderText("输入变量值")
        layout.addRow("值:", self.value_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addRow(btn_layout)

    def get_name(self) -> str:
        return self.name_edit.text().strip()

    def get_value(self) -> Any:
        type_name = self.type_combo.currentText()
        value_str = self.value_edit.text().strip()
        
        if type_name == "字符串":
            return value_str
        elif type_name == "数字":
            try:
                if "." in value_str:
                    return float(value_str)
                return int(value_str)
            except ValueError:
                return 0
        elif type_name == "布尔值":
            return value_str.lower() in ["true", "是", "1"]
        elif type_name == "列表":
            try:
                return eval(value_str) if value_str else []
            except:
                return value_str.split(",") if value_str else []
        elif type_name == "字典":
            try:
                return eval(value_str) if value_str else {}
            except:
                return {}
        return value_str
