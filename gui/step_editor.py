from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                               QPushButton, QHBoxLayout, QMenu, QMessageBox)
from PySide6.QtCore import Qt, Signal
import uuid

class StepEditor(QGroupBox):
    step_added = Signal(dict)
    step_removed = Signal(str)
    step_selected = Signal(dict)
    step_reordered = Signal(list)
    
    def __init__(self):
        super().__init__("步骤编辑")
        self.steps = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.step_tree = QTreeWidget()
        self.step_tree.setHeaderLabel("步骤列表")
        self.step_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        layout.addWidget(self.step_tree)
        
        button_layout = QHBoxLayout()
        
        self.up_button = QPushButton("上移")
        self.down_button = QPushButton("下移")
        self.delete_button = QPushButton("删除")
        
        button_layout.addWidget(self.up_button)
        button_layout.addWidget(self.down_button)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.step_tree.itemClicked.connect(self.on_step_clicked)
        self.step_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.up_button.clicked.connect(self.on_move_up)
        self.down_button.clicked.connect(self.on_move_down)
        self.delete_button.clicked.connect(self.on_delete_step)
    
    def add_step(self, tool: dict):
        step_id = str(uuid.uuid4())[:8]
        step = {
            "id": step_id,
            "type": tool["id"],
            "name": tool["name"],
            "config": {},
            "wait_before": 0,
            "wait_after": 0,
            "next_step": None
        }
        
        self.steps.append(step)
        self._update_tree()
        self.step_added.emit(step)
    
    def remove_step(self, step_id: str):
        self.steps = [s for s in self.steps if s["id"] != step_id]
        self._update_tree()
        self.step_removed.emit(step_id)
    
    def _update_tree(self):
        self.step_tree.clear()
        for i, step in enumerate(self.steps):
            item = QTreeWidgetItem(self.step_tree)
            item.setText(0, f"{i+1}. {step['name']}")
            item.setData(0, Qt.UserRole, step)
    
    def on_step_clicked(self, item, column):
        step = item.data(0, Qt.UserRole)
        if step:
            self.step_selected.emit(step)
    
    def show_context_menu(self, pos):
        item = self.step_tree.itemAt(pos)
        if item:
            menu = QMenu()
            delete_action = menu.addAction("删除步骤")
            action = menu.exec_(self.step_tree.mapToGlobal(pos))
            if action == delete_action:
                step = item.data(0, Qt.UserRole)
                if step:
                    self.remove_step(step["id"])
    
    def on_move_up(self):
        current_item = self.step_tree.currentItem()
        if current_item:
            index = self.step_tree.indexOfTopLevelItem(current_item)
            if index > 0:
                step = self.steps.pop(index)
                self.steps.insert(index - 1, step)
                self._update_tree()
                self.step_tree.setCurrentItem(self.step_tree.topLevelItem(index - 1))
                self.step_reordered.emit(self.steps)
    
    def on_move_down(self):
        current_item = self.step_tree.currentItem()
        if current_item:
            index = self.step_tree.indexOfTopLevelItem(current_item)
            if index < len(self.steps) - 1:
                step = self.steps.pop(index)
                self.steps.insert(index + 1, step)
                self._update_tree()
                self.step_tree.setCurrentItem(self.step_tree.topLevelItem(index + 1))
                self.step_reordered.emit(self.steps)
    
    def on_delete_step(self):
        current_item = self.step_tree.currentItem()
        if current_item:
            step = current_item.data(0, Qt.UserRole)
            if step:
                reply = QMessageBox.question(
                    self, "确认删除", f"确定要删除步骤 '{step['name']}' 吗？",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.remove_step(step["id"])
    
    def get_steps(self):
        return self.steps
    
    def load_steps(self, steps):
        self.steps = steps
        self._update_tree()