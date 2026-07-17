from PySide6.QtWidgets import (QGroupBox, QFormLayout, QLineEdit, QComboBox,
                               QSpinBox, QDoubleSpinBox, QCheckBox, QTextEdit,
                               QPushButton, QHBoxLayout, QLabel, QFileDialog)
from PySide6.QtCore import Qt, Signal
import json

class PropertiesPanel(QGroupBox):
    properties_changed = Signal(dict)
    
    def __init__(self):
        super().__init__("属性配置")
        self.current_step = None
        self.init_ui()
    
    def init_ui(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
        self.step_name_edit = QLineEdit()
        self.step_name_edit.setPlaceholderText("输入步骤名称")
        self.layout.addRow("步骤名称:", self.step_name_edit)
        
        self.step_type_label = QLabel("")
        self.layout.addRow("步骤类型:", self.step_type_label)
        
        self.config_group = QGroupBox("配置参数")
        self.config_layout = QFormLayout(self.config_group)
        self.layout.addRow(self.config_group)
        
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存配置")
        self.reset_button = QPushButton("重置")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)
        self.layout.addRow(button_layout)
        
        self.step_name_edit.textChanged.connect(self.on_name_changed)
        self.save_button.clicked.connect(self.on_save_config)
        self.reset_button.clicked.connect(self.on_reset)
    
    def load_step(self, step):
        self.current_step = step
        self.step_name_edit.setText(step.get("name", ""))
        self.step_type_label.setText(step.get("type", ""))
        self._build_config_ui(step["type"], step.get("config", {}))
    
    def _build_config_ui(self, step_type, config):
        while self.config_layout.rowCount() > 0:
            item = self.config_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        config_fields = {
            "mouse_click": [
                ("x", "X坐标", "spinbox", {"min": 0, "max": 4000}),
                ("y", "Y坐标", "spinbox", {"min": 0, "max": 4000}),
                ("button", "按钮", "combo", {"options": ["left", "right", "middle"]}),
                ("clicks", "点击次数", "spinbox", {"min": 1, "max": 10})
            ],
            "mouse_move": [
                ("x", "目标X坐标", "spinbox", {"min": 0, "max": 4000}),
                ("y", "目标Y坐标", "spinbox", {"min": 0, "max": 4000}),
                ("duration", "移动时间(秒)", "doublespin", {"min": 0, "max": 10})
            ],
            "keyboard_type": [
                ("text", "输入文本", "textedit", {}),
                ("interval", "输入间隔(秒)", "doublespin", {"min": 0, "max": 1}),
                ("human_like", "模拟人类输入", "checkbox", {})
            ],
            "wait": [
                ("type", "等待类型", "combo", {"options": ["fixed", "random"]}),
                ("value", "等待时间(秒)", "doublespin", {"min": 0, "max": 60}),
                ("min", "最小等待(秒)", "doublespin", {"min": 0, "max": 60}),
                ("max", "最大等待(秒)", "doublespin", {"min": 0, "max": 60})
            ],
            "image_find": [
                ("template_path", "模板图片路径", "file", {}),
                ("threshold", "匹配阈值", "doublespin", {"min": 0, "max": 1, "decimals": 2}),
                ("method", "匹配方法", "combo", {"options": ["template", "akaze"]})
            ],
            "if_else": [
                ("condition_type", "条件类型", "combo", {"options": ["value", "image_exists", "text_exists", "window_exists"]}),
                ("left", "左值", "lineedit", {}),
                ("right", "右值", "lineedit", {}),
                ("operator", "操作符", "combo", {"options": ["==", "!=", ">", "<", ">=", "<=", "contains"]})
            ],
            "loop": [
                ("count", "循环次数", "spinbox", {"min": 1, "max": 100}),
                ("step_id", "循环步骤ID", "lineedit", {})
            ],
            "set_variable": [
                ("name", "变量名", "lineedit", {}),
                ("value", "变量值", "textedit", {})
            ],
            "excel_read": [
                ("file_path", "Excel文件路径", "file", {}),
                ("sheet_name", "工作表名称", "lineedit", {}),
                ("cell_ref", "单元格引用", "lineedit", {})
            ],
            "log": [
                ("message", "日志消息", "textedit", {}),
                ("level", "日志级别", "combo", {"options": ["info", "error", "warning", "debug"]})
            ]
        }
        
        fields = config_fields.get(step_type, [])
        
        for field_id, label, widget_type, params in fields:
            self._add_field(field_id, label, widget_type, params, config.get(field_id))
    
    def _add_field(self, field_id, label, widget_type, params, value):
        if widget_type == "lineedit":
            widget = QLineEdit()
            widget.setText(str(value) if value else "")
        elif widget_type == "textedit":
            widget = QTextEdit()
            widget.setText(str(value) if value else "")
        elif widget_type == "spinbox":
            widget = QSpinBox()
            widget.setRange(params.get("min", 0), params.get("max", 100))
            widget.setValue(value if value else 0)
        elif widget_type == "doublespin":
            widget = QDoubleSpinBox()
            widget.setRange(params.get("min", 0), params.get("max", 100))
            widget.setDecimals(params.get("decimals", 2))
            widget.setValue(value if value else 0)
        elif widget_type == "combo":
            widget = QComboBox()
            widget.addItems(params.get("options", []))
            if value:
                index = widget.findText(str(value))
                if index >= 0:
                    widget.setCurrentIndex(index)
        elif widget_type == "checkbox":
            widget = QCheckBox()
            widget.setChecked(value if value else False)
        elif widget_type == "file":
            layout = QHBoxLayout()
            file_edit = QLineEdit()
            file_edit.setText(str(value) if value else "")
            browse_btn = QPushButton("浏览")
            browse_btn.clicked.connect(lambda checked, e=file_edit: self._browse_file(e))
            layout.addWidget(file_edit)
            layout.addWidget(browse_btn)
            self.config_layout.addRow(label, layout)
            return
        
        widget.setProperty("field_id", field_id)
        self.config_layout.addRow(label, widget)
    
    def _browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            line_edit.setText(file_path)
    
    def on_name_changed(self, text):
        if self.current_step:
            self.current_step["name"] = text
    
    def on_save_config(self):
        if not self.current_step:
            return
        
        config = {}
        for i in range(self.config_layout.rowCount()):
            label_item = self.config_layout.itemAt(i, QFormLayout.LabelRole)
            field_item = self.config_layout.itemAt(i, QFormLayout.FieldRole)
            
            if label_item and field_item:
                widget = field_item.widget()
                if widget:
                    field_id = widget.property("field_id")
                    if field_id:
                        if isinstance(widget, QLineEdit):
                            config[field_id] = widget.text()
                        elif isinstance(widget, QTextEdit):
                            config[field_id] = widget.toPlainText()
                        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                            config[field_id] = widget.value()
                        elif isinstance(widget, QComboBox):
                            config[field_id] = widget.currentText()
                        elif isinstance(widget, QCheckBox):
                            config[field_id] = widget.isChecked()
        
        self.current_step["config"] = config
        self.properties_changed.emit(self.current_step)
    
    def on_reset(self):
        if self.current_step:
            self.load_step(self.current_step)