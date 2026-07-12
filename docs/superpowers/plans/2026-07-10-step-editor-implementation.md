# 步骤编辑器界面实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 实现步骤编辑器对话框，根据不同步骤类型动态显示定制化配置界面

**架构：** 使用 QStackedWidget + 动态表单构建，每种步骤类型对应独立的配置面板类，通过信号槽实现控件交互和动态显示

**技术栈：** PySide6 (Qt), Python 3.11+, Miniconda3 环境

---

## 文件结构

### 新建文件

| 文件路径 | 职责 |
|----------|------|
| `gui/step_editor.py` | 步骤编辑器对话框主类，管理步骤类型切换和数据保存 |
| `gui/step_panels/__init__.py` | 步骤面板模块初始化，导出所有面板类 |
| `gui/step_panels/mouse_panel.py` | 鼠标操作配置面板（点击、移动、拖拽、滚动） |
| `gui/step_panels/keyboard_panel.py` | 键盘操作配置面板（输入、按键、快捷键） |
| `gui/step_panels/image_panel.py` | 图像操作配置面板（查找图片、点击图片、图片存在） |
| `gui/step_panels/window_panel.py` | 窗口操作配置面板（查找、激活、关闭、位置） |
| `gui/step_panels/excel_panel.py` | Excel操作配置面板（读取Excel） |
| `gui/step_panels/control_panel.py` | 控制操作配置面板（等待、条件判断、循环、日志、标记、跳转） |
| `gui/step_panels/variable_panel.py` | 变量操作配置面板（设置变量、获取变量） |

### 修改文件

| 文件路径 | 修改内容 |
|----------|----------|
| `gui/main_window.py` | 集成步骤编辑器对话框，替换现有简单编辑逻辑 |

---

## 任务列表

### 任务 1：创建步骤面板基类和模块初始化

**文件：**
- 创建：`gui/step_panels/__init__.py`

**说明：** 创建步骤面板基类 `StepConfigPanel`，定义统一接口和通用功能（延时配置、文件选择等），并导出所有面板类。

- [ ] **步骤 1：编写基类代码**

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox, QPushButton,
    QGroupBox, QFileDialog, QSlider, QRadioButton, QButtonGroup,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QIcon


class StepConfigPanel(QWidget):
    config_changed = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(12, 12, 12, 12)
        
        self.config = {}
        self.delay_widget = None
    
    def get_config(self):
        return self.config
    
    def set_config(self, config):
        self.config = config.copy()
    
    def add_section_title(self, text):
        label = QLabel(f"<b>{text}</b>")
        label.setStyleSheet("color: #2c3e50; font-size: 14px;")
        self.layout.addWidget(label)
    
    def add_line(self, label_text, widget, stretch=0):
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setFixedWidth(80)
        h_layout.addWidget(label)
        h_layout.addWidget(widget, stretch)
        self.layout.addLayout(h_layout)
        return widget
    
    def add_spinbox(self, label_text, min_val=0, max_val=99999, default=0, step=1):
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default)
        spinbox.setSingleStep(step)
        spinbox.setStyleSheet("QSpinBox { padding: 4px; border: 1px solid #ddd; border-radius: 4px; }")
        return self.add_line(label_text, spinbox)
    
    def add_double_spinbox(self, label_text, min_val=0, max_val=99999, default=0, decimals=2):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default)
        spinbox.setDecimals(decimals)
        spinbox.setStyleSheet("QDoubleSpinBox { padding: 4px; border: 1px solid #ddd; border-radius: 4px; }")
        return self.add_line(label_text, spinbox)
    
    def add_lineedit(self, label_text, default="", placeholder=""):
        lineedit = QLineEdit(default)
        lineedit.setPlaceholderText(placeholder)
        lineedit.setStyleSheet("QLineEdit { padding: 4px; border: 1px solid #ddd; border-radius: 4px; }")
        return self.add_line(label_text, lineedit, 1)
    
    def add_textedit(self, label_text, default="", placeholder=""):
        from PySide6.QtWidgets import QTextEdit
        label = QLabel(label_text)
        label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        textedit = QTextEdit(default)
        textedit.setPlaceholderText(placeholder)
        textedit.setStyleSheet("QTextEdit { padding: 4px; border: 1px solid #ddd; border-radius: 4px; }")
        textedit.setFixedHeight(100)
        self.layout.addWidget(label)
        self.layout.addWidget(textedit)
        return textedit
    
    def add_combobox(self, label_text, items, default_index=0):
        combobox = QComboBox()
        combobox.addItems(items)
        combobox.setCurrentIndex(default_index)
        combobox.setStyleSheet("QComboBox { padding: 4px; border: 1px solid #ddd; border-radius: 4px; }")
        return self.add_line(label_text, combobox)
    
    def add_checkbox(self, text, checked=False):
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        checkbox.setStyleSheet("QCheckBox { font-size: 12px; }")
        self.layout.addWidget(checkbox)
        return checkbox
    
    def add_radio_group(self, label_text, options, default_index=0):
        group = QGroupBox(label_text)
        group.setStyleSheet("QGroupBox { font-size: 12px; color: #7f8c8d; }")
        h_layout = QHBoxLayout(group)
        button_group = QButtonGroup(self)
        buttons = []
        for i, option in enumerate(options):
            radio = QRadioButton(option)
            radio.setStyleSheet("QRadioButton { font-size: 12px; }")
            h_layout.addWidget(radio)
            button_group.addButton(radio, i)
            buttons.append(radio)
            if i == default_index:
                radio.setChecked(True)
        self.layout.addWidget(group)
        return button_group, buttons
    
    def add_slider(self, label_text, min_val=0, max_val=100, default=50, suffix=""):
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        label.setFixedWidth(80)
        h_layout.addWidget(label)
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 6px; background: #ddd; border-radius: 3px; }
            QSlider::handle:horizontal { background: #27ae60; width: 16px; margin: -5px 0; border-radius: 8px; }
        """)
        h_layout.addWidget(slider, 1)
        
        value_label = QLabel(f"{default}{suffix}")
        value_label.setStyleSheet("font-size: 12px; color: #27ae60;")
        value_label.setFixedWidth(60)
        value_label.setAlignment(Qt.AlignRight)
        h_layout.addWidget(value_label)
        
        slider.valueChanged.connect(lambda v: value_label.setText(f"{v/100 if max_val == 100 else v}{suffix}"))
        self.layout.addLayout(h_layout)
        return slider, value_label
    
    def add_file_browser(self, label_text, file_filter="All Files (*.*)", default_path=""):
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        label.setFixedWidth(80)
        h_layout.addWidget(label)
        
        lineedit = QLineEdit(default_path)
        lineedit.setStyleSheet("QLineEdit { padding: 4px; border: 1px solid #ddd; border-radius: 4px; }")
        h_layout.addWidget(lineedit, 1)
        
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; background: #ecf0f1; border: none; border-radius: 4px; font-size: 12px; }
            QPushButton:hover { background: #bdc3c7; }
        """)
        
        def browse_file():
            path, _ = QFileDialog.getOpenFileName(self, "选择文件", lineedit.text(), file_filter)
            if path:
                lineedit.setText(path)
        
        browse_btn.clicked.connect(browse_file)
        h_layout.addWidget(browse_btn)
        self.layout.addLayout(h_layout)
        return lineedit, browse_btn
    
    def add_delay_section(self, default_delay=0):
        group = QGroupBox("延时设置")
        group.setStyleSheet("QGroupBox { font-size: 13px; font-weight: bold; color: #2c3e50; }")
        layout = QVBoxLayout(group)
        
        self.delay_widget = QDoubleSpinBox()
        self.delay_widget.setRange(0, 600)
        self.delay_widget.setValue(default_delay)
        self.delay_widget.setDecimals(2)
        self.delay_widget.setStyleSheet("QDoubleSpinBox { padding: 4px; border: 1px solid #ddd; border-radius: 4px; }")
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("延时(秒):"))
        h_layout.addWidget(self.delay_widget, 1)
        layout.addLayout(h_layout)
        self.layout.addWidget(group)
    
    def add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #ddd;")
        self.layout.addWidget(line)
    
    def add_buttons(self, confirm_callback, cancel_callback):
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        
        confirm_btn = QPushButton("确定")
        confirm_btn.setStyleSheet("""
            QPushButton { padding: 6px 24px; background: #27ae60; color: white; border: none; border-radius: 4px; font-size: 13px; }
            QPushButton:hover { background: #2ecc71; }
        """)
        confirm_btn.clicked.connect(confirm_callback)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton { padding: 6px 24px; background: #ecf0f1; border: none; border-radius: 4px; font-size: 13px; }
            QPushButton:hover { background: #bdc3c7; }
        """)
        cancel_btn.clicked.connect(cancel_callback)
        
        h_layout.addWidget(confirm_btn)
        h_layout.addWidget(cancel_btn)
        self.layout.addLayout(h_layout)


from .mouse_panel import MouseClickPanel, MouseMovePanel, MouseDragPanel, MouseScrollPanel
from .keyboard_panel import KeyboardTypePanel, KeyboardPressPanel, KeyboardHotkeyPanel
from .image_panel import ImageFindPanel, ImageClickPanel, ImageExistsPanel
from .window_panel import WindowFindPanel, WindowActivatePanel, WindowClosePanel, WindowPositionPanel
from .excel_panel import ExcelReadPanel
from .control_panel import WaitPanel, IfElsePanel, LoopPanel, LogPanel, LabelPanel, GotoPanel
from .variable_panel import SetVariablePanel, GetVariablePanel


PANEL_MAP = {
    "mouse_click": MouseClickPanel,
    "mouse_move": MouseMovePanel,
    "mouse_drag": MouseDragPanel,
    "mouse_scroll": MouseScrollPanel,
    "keyboard_type": KeyboardTypePanel,
    "keyboard_press": KeyboardPressPanel,
    "keyboard_hotkey": KeyboardHotkeyPanel,
    "image_find": ImageFindPanel,
    "image_click": ImageClickPanel,
    "image_exists": ImageExistsPanel,
    "window_find": WindowFindPanel,
    "window_activate": WindowActivatePanel,
    "window_close": WindowClosePanel,
    "window_position": WindowPositionPanel,
    "excel_read": ExcelReadPanel,
    "wait": WaitPanel,
    "if_else": IfElsePanel,
    "loop": LoopPanel,
    "log": LogPanel,
    "label": LabelPanel,
    "goto": GotoPanel,
    "set_variable": SetVariablePanel,
    "get_variable": GetVariablePanel,
}


def get_panel_class(step_type):
    return PANEL_MAP.get(step_type)
```

- [ ] **步骤 2：验证文件创建**

运行：`python -c "from gui.step_panels import StepConfigPanel; print('Base class imported successfully')"`
预期：成功输出 "Base class imported successfully"

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/__init__.py
git commit -m "feat: 添加步骤面板基类和模块初始化"
```

---

### 任务 2：创建鼠标操作配置面板

**文件：**
- 创建：`gui/step_panels/mouse_panel.py`

**说明：** 实现鼠标点击、鼠标移动、鼠标拖拽、鼠标滚动四种步骤类型的配置面板

- [ ] **步骤 1：编写鼠标点击面板**

```python
from . import StepConfigPanel


class MouseClickPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("鼠标点击配置")
        
        self.click_type = self.add_combobox("点击类型", ["左键单击", "左键双击", "右键单击", "中键单击"])
        
        self.pos_group, self.pos_buttons = self.add_radio_group("点击位置", ["当前位置", "屏幕坐标", "图片位置", "相对坐标"])
        
        self.screen_widgets = []
        h_layout = self.add_line("屏幕坐标", self._create_screen_coords())
        self.screen_widgets.append(h_layout.parentWidget() if h_layout.parentWidget() else h_layout)
        
        self.image_widgets = []
        self.image_path, _ = self.add_file_browser("图片路径", "图片文件 (*.png *.jpg *.bmp *.gif)")
        self.image_widgets.append(self.image_path.parentWidget())
        
        self.similarity, _ = self.add_slider("相似度", 0, 100, 90, "")
        self.find_range = self.add_combobox("查找范围", ["全屏", "当前窗口", "自定义区域"])
        self.offset_x = self.add_spinbox("相对偏移X", -9999, 9999, 0)
        self.offset_y = self.add_spinbox("相对偏移Y", -9999, 9999, 0)
        
        self.relative_widgets = []
        self.relative_base = self.add_combobox("相对基准", ["上一次点击位置", "屏幕左上角"])
        self.relative_x = self.add_spinbox("X偏移", -9999, 9999, 0)
        self.relative_y = self.add_spinbox("Y偏移", -9999, 9999, 0)
        
        self.random_offset = self.add_checkbox("随机偏移")
        self.random_range = self.add_spinbox("随机范围", 1, 100, 5)
        
        self.add_delay_section()
        
        self._connect_signals()
        self._update_visibility()
    
    def _create_screen_coords(self):
        from PySide6.QtWidgets import QWidget, QHBoxLayout
        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.x_coord = self.add_spinbox("X", -9999, 9999, 0)
        self.y_coord = self.add_spinbox("Y", -9999, 9999, 0)
        return widget
    
    def _connect_signals(self):
        self.pos_group.buttonClicked.connect(self._update_visibility)
        self.random_offset.stateChanged.connect(lambda s: self.random_range.setEnabled(s == 2))
    
    def _update_visibility(self):
        index = self.pos_group.checkedId()
        for w in self.screen_widgets:
            w.setVisible(index == 1)
        for w in self.image_widgets:
            w.setVisible(index == 2)
        for w in self.relative_widgets:
            w.setVisible(index == 3)
    
    def get_config(self):
        pos_type = ["current", "screen", "image", "relative"][self.pos_group.checkedId()]
        config = {
            "click_type": ["left_single", "left_double", "right_single", "middle_single"][self.click_type.currentIndex()],
            "position_type": pos_type,
            "random_offset": self.random_offset.isChecked(),
            "offset_range": self.random_range.value(),
        }
        
        if pos_type == "screen":
            config["x"] = self.x_coord.value()
            config["y"] = self.y_coord.value()
        elif pos_type == "image":
            config["image_path"] = self.image_path.text()
            config["similarity"] = self.similarity.value() / 100
            config["find_range"] = ["full", "window", "custom"][self.find_range.currentIndex()]
            config["offset_x"] = self.offset_x.value()
            config["offset_y"] = self.offset_y.value()
        elif pos_type == "relative":
            config["base"] = ["last_click", "screen_top"][self.relative_base.currentIndex()]
            config["x_offset"] = self.relative_x.value()
            config["y_offset"] = self.relative_y.value()
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        click_types = ["left_single", "left_double", "right_single", "middle_single"]
        if "click_type" in config:
            self.click_type.setCurrentIndex(click_types.index(config["click_type"]))
        
        pos_types = ["current", "screen", "image", "relative"]
        if "position_type" in config:
            self.pos_group.button(pos_types.index(config["position_type"])).setChecked(True)
        
        if "x" in config:
            self.x_coord.setValue(config["x"])
        if "y" in config:
            self.y_coord.setValue(config["y"])
        if "image_path" in config:
            self.image_path.setText(config["image_path"])
        if "similarity" in config:
            self.similarity.setValue(int(config["similarity"] * 100))
        if "random_offset" in config:
            self.random_offset.setChecked(config["random_offset"])
        if "offset_range" in config:
            self.random_range.setValue(config["offset_range"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
        
        self._update_visibility()


class MouseMovePanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("鼠标移动配置")
        
        self.move_type = self.add_combobox("移动方式", ["直线移动", "缓动移动", "随机路径"])
        self.duration = self.add_double_spinbox("移动时长", 0, 60, 0.5)
        
        self.pos_group, self.pos_buttons = self.add_radio_group("移动位置", ["屏幕坐标", "图片位置", "相对坐标"])
        
        self.x_coord = self.add_spinbox("X坐标", -9999, 9999, 0)
        self.y_coord = self.add_spinbox("Y坐标", -9999, 9999, 0)
        
        self.image_path, _ = self.add_file_browser("图片路径", "图片文件 (*.png *.jpg *.bmp *.gif)")
        self.similarity, _ = self.add_slider("相似度", 0, 100, 90, "")
        
        self.smooth_curve = self.add_checkbox("平滑曲线移动")
        
        self.add_delay_section()
        
        self._connect_signals()
        self._update_visibility()
    
    def _connect_signals(self):
        self.pos_group.buttonClicked.connect(self._update_visibility)
    
    def _update_visibility(self):
        index = self.pos_group.checkedId()
        self.x_coord.parentWidget().setVisible(index == 0)
        self.y_coord.parentWidget().setVisible(index == 0)
        self.image_path.parentWidget().setVisible(index == 1)
    
    def get_config(self):
        pos_type = ["screen", "image", "relative"][self.pos_group.checkedId()]
        config = {
            "move_type": ["linear", "ease", "random"][self.move_type.currentIndex()],
            "duration": self.duration.value(),
            "position_type": pos_type,
            "smooth_curve": self.smooth_curve.isChecked(),
        }
        
        if pos_type == "screen":
            config["x"] = self.x_coord.value()
            config["y"] = self.y_coord.value()
        elif pos_type == "image":
            config["image_path"] = self.image_path.text()
            config["similarity"] = self.similarity.value() / 100
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "move_type" in config:
            types = ["linear", "ease", "random"]
            self.move_type.setCurrentIndex(types.index(config["move_type"]))
        if "duration" in config:
            self.duration.setValue(config["duration"])
        if "x" in config:
            self.x_coord.setValue(config["x"])
        if "y" in config:
            self.y_coord.setValue(config["y"])
        if "image_path" in config:
            self.image_path.setText(config["image_path"])
        if "smooth_curve" in config:
            self.smooth_curve.setChecked(config["smooth_curve"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
        self._update_visibility()


class MouseDragPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("鼠标拖拽配置")
        
        self.drag_button = self.add_combobox("拖拽按钮", ["左键", "右键", "中键"])
        
        self.start_group, _ = self.add_radio_group("起点类型", ["屏幕坐标", "图片位置"])
        self.start_x = self.add_spinbox("起点X", -9999, 9999, 0)
        self.start_y = self.add_spinbox("起点Y", -9999, 9999, 0)
        self.start_image, _ = self.add_file_browser("起点图片", "图片文件 (*.png *.jpg *.bmp *.gif)")
        
        self.end_group, _ = self.add_radio_group("终点类型", ["屏幕坐标", "图片位置", "相对起点"])
        self.end_x = self.add_spinbox("终点X", -9999, 9999, 0)
        self.end_y = self.add_spinbox("终点Y", -9999, 9999, 0)
        self.end_image, _ = self.add_file_browser("终点图片", "图片文件 (*.png *.jpg *.bmp *.gif)")
        
        self.duration = self.add_double_spinbox("拖拽时长", 0, 60, 1.0)
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.start_group.buttonClicked.connect(self._update_start_visibility)
        self.end_group.buttonClicked.connect(self._update_end_visibility)
    
    def _update_start_visibility(self):
        index = self.start_group.checkedId()
        self.start_x.parentWidget().setVisible(index == 0)
        self.start_y.parentWidget().setVisible(index == 0)
        self.start_image.parentWidget().setVisible(index == 1)
    
    def _update_end_visibility(self):
        index = self.end_group.checkedId()
        self.end_x.parentWidget().setVisible(index == 0 or index == 2)
        self.end_y.parentWidget().setVisible(index == 0 or index == 2)
        self.end_image.parentWidget().setVisible(index == 1)
    
    def get_config(self):
        config = {
            "drag_button": ["left", "right", "middle"][self.drag_button.currentIndex()],
            "start_type": ["screen", "image"][self.start_group.checkedId()],
            "end_type": ["screen", "image", "relative"][self.end_group.checkedId()],
            "duration": self.duration.value(),
        }
        
        if config["start_type"] == "screen":
            config["start_x"] = self.start_x.value()
            config["start_y"] = self.start_y.value()
        else:
            config["start_image"] = self.start_image.text()
        
        if config["end_type"] == "screen":
            config["end_x"] = self.end_x.value()
            config["end_y"] = self.end_y.value()
        elif config["end_type"] == "image":
            config["end_image"] = self.end_image.text()
        else:
            config["end_x"] = self.end_x.value()
            config["end_y"] = self.end_y.value()
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "start_x" in config:
            self.start_x.setValue(config["start_x"])
        if "start_y" in config:
            self.start_y.setValue(config["start_y"])
        if "end_x" in config:
            self.end_x.setValue(config["end_x"])
        if "end_y" in config:
            self.end_y.setValue(config["end_y"])
        if "duration" in config:
            self.duration.setValue(config["duration"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class MouseScrollPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("鼠标滚动配置")
        
        self.scroll_direction = self.add_combobox("滚动方向", ["向上", "向下", "向左", "向右"])
        self.scroll_times = self.add_spinbox("滚动次数", 1, 100, 1)
        self.scroll_amount = self.add_spinbox("每次滚动量", 1, 1000, 100)
        self.scroll_interval = self.add_double_spinbox("滚动间隔", 0, 10, 0.1)
        
        self.add_delay_section()
    
    def get_config(self):
        config = {
            "direction": ["up", "down", "left", "right"][self.scroll_direction.currentIndex()],
            "times": self.scroll_times.value(),
            "amount": self.scroll_amount.value(),
            "interval": self.scroll_interval.value(),
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "times" in config:
            self.scroll_times.setValue(config["times"])
        if "amount" in config:
            self.scroll_amount.setValue(config["amount"])
        if "interval" in config:
            self.scroll_interval.setValue(config["interval"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
```

- [ ] **步骤 2：验证鼠标面板导入**

运行：`python -c "from gui.step_panels.mouse_panel import MouseClickPanel; print('MouseClickPanel imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/mouse_panel.py
git commit -m "feat: 添加鼠标操作配置面板（点击、移动、拖拽、滚动）"
```

---

### 任务 3：创建键盘操作配置面板

**文件：**
- 创建：`gui/step_panels/keyboard_panel.py`

**说明：** 实现键盘输入、按键操作、快捷键三种步骤类型的配置面板

- [ ] **步骤 1：编写键盘面板代码**

```python
from . import StepConfigPanel


class KeyboardTypePanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("键盘输入配置")
        
        self.content = self.add_textedit("输入内容", placeholder="请输入要输入的文本内容")
        
        self.input_type = self.add_combobox("输入方式", ["逐字输入", "剪贴板粘贴"])
        
        self.interval = self.add_double_spinbox("输入间隔", 0, 1, 0.05)
        
        self.random_interval = self.add_checkbox("随机间隔")
        self.range_interval = self.add_double_spinbox("间隔范围", 0, 0.5, 0.02)
        
        self.simulate_human = self.add_checkbox("模拟人类输入（随机停顿、错误修正）")
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.random_interval.stateChanged.connect(lambda s: self.range_interval.setEnabled(s == 2))
    
    def get_config(self):
        config = {
            "content": self.content.toPlainText(),
            "input_type": ["typing", "clipboard"][self.input_type.currentIndex()],
            "interval": self.interval.value(),
            "random_interval": self.random_interval.isChecked(),
            "interval_range": self.range_interval.value() if self.random_interval.isChecked() else 0,
            "simulate_human": self.simulate_human.isChecked(),
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "content" in config:
            self.content.setPlainText(config["content"])
        if "input_type" in config:
            types = ["typing", "clipboard"]
            self.input_type.setCurrentIndex(types.index(config["input_type"]))
        if "interval" in config:
            self.interval.setValue(config["interval"])
        if "random_interval" in config:
            self.random_interval.setChecked(config["random_interval"])
        if "simulate_human" in config:
            self.simulate_human.setChecked(config["simulate_human"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class KeyboardPressPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("按键操作配置")
        
        self.key_name = self.add_combobox("按键", [
            "ENTER", "TAB", "SPACE", "BACKSPACE", "DELETE", "INSERT",
            "HOME", "END", "PAGE_UP", "PAGE_DOWN",
            "UP", "DOWN", "LEFT", "RIGHT",
            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        ])
        
        self.hold_time = self.add_double_spinbox("按住时长", 0, 10, 0.1)
        self.repeat_times = self.add_spinbox("重复次数", 1, 100, 1)
        self.repeat_interval = self.add_double_spinbox("重复间隔", 0, 10, 0.2)
        
        self.add_delay_section()
    
    def get_config(self):
        config = {
            "key": self.key_name.currentText(),
            "hold_time": self.hold_time.value(),
            "repeat_times": self.repeat_times.value(),
            "repeat_interval": self.repeat_interval.value(),
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "key" in config:
            index = self.key_name.findText(config["key"])
            if index >= 0:
                self.key_name.setCurrentIndex(index)
        if "hold_time" in config:
            self.hold_time.setValue(config["hold_time"])
        if "repeat_times" in config:
            self.repeat_times.setValue(config["repeat_times"])
        if "repeat_interval" in config:
            self.repeat_interval.setValue(config["repeat_interval"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class KeyboardHotkeyPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("快捷键配置")
        
        self.ctrl_check = self.add_checkbox("Ctrl")
        self.alt_check = self.add_checkbox("Alt")
        self.shift_check = self.add_checkbox("Shift")
        self.win_check = self.add_checkbox("Win")
        
        self.main_key = self.add_combobox("主按键", [
            "ENTER", "TAB", "SPACE", "BACKSPACE", "DELETE",
            "UP", "DOWN", "LEFT", "RIGHT",
            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        ])
        
        self.hold_time = self.add_double_spinbox("按住时长", 0, 10, 0.1)
        
        self.preview_label = QLabel("预览: ")
        self.preview_label.setStyleSheet("font-size: 12px; color: #27ae60;")
        self.layout.addWidget(self.preview_label)
        
        self.add_delay_section()
        
        self._connect_signals()
        self._update_preview()
    
    def _connect_signals(self):
        self.ctrl_check.stateChanged.connect(self._update_preview)
        self.alt_check.stateChanged.connect(self._update_preview)
        self.shift_check.stateChanged.connect(self._update_preview)
        self.win_check.stateChanged.connect(self._update_preview)
        self.main_key.currentIndexChanged.connect(self._update_preview)
    
    def _update_preview(self):
        keys = []
        if self.ctrl_check.isChecked():
            keys.append("Ctrl")
        if self.alt_check.isChecked():
            keys.append("Alt")
        if self.shift_check.isChecked():
            keys.append("Shift")
        if self.win_check.isChecked():
            keys.append("Win")
        keys.append(self.main_key.currentText())
        self.preview_label.setText(f"预览: {' + '.join(keys)}")
    
    def get_config(self):
        config = {
            "ctrl": self.ctrl_check.isChecked(),
            "alt": self.alt_check.isChecked(),
            "shift": self.shift_check.isChecked(),
            "win": self.win_check.isChecked(),
            "main_key": self.main_key.currentText(),
            "hold_time": self.hold_time.value(),
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "ctrl" in config:
            self.ctrl_check.setChecked(config["ctrl"])
        if "alt" in config:
            self.alt_check.setChecked(config["alt"])
        if "shift" in config:
            self.shift_check.setChecked(config["shift"])
        if "win" in config:
            self.win_check.setChecked(config["win"])
        if "main_key" in config:
            index = self.main_key.findText(config["main_key"])
            if index >= 0:
                self.main_key.setCurrentIndex(index)
        if "hold_time" in config:
            self.hold_time.setValue(config["hold_time"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
```

- [ ] **步骤 2：验证键盘面板导入**

运行：`python -c "from gui.step_panels.keyboard_panel import KeyboardTypePanel; print('KeyboardTypePanel imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/keyboard_panel.py
git commit -m "feat: 添加键盘操作配置面板（输入、按键、快捷键）"
```

---

### 任务 4：创建图像操作配置面板

**文件：**
- 创建：`gui/step_panels/image_panel.py`

**说明：** 实现查找图片、点击图片、图片存在判断三种步骤类型的配置面板

- [ ] **步骤 1：编写图像面板代码**

```python
from . import StepConfigPanel
from PySide6.QtWidgets import QLabel, QVBoxLayout


class ImageFindPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("查找图片配置")
        
        self.image_path, _ = self.add_file_browser("图片路径", "图片文件 (*.png *.jpg *.bmp *.gif)")
        
        self.preview_label = QLabel("图片预览")
        self.preview_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        self.layout.addWidget(self.preview_label)
        
        self.image_preview = QLabel()
        self.image_preview.setStyleSheet("border: 1px solid #ddd; background: #f8f9fa;")
        self.image_preview.setFixedSize(150, 100)
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_preview)
        
        self.find_range = self.add_combobox("查找范围", ["全屏", "当前窗口", "自定义区域"])
        self.similarity, _ = self.add_slider("相似度", 0, 100, 90, "")
        
        self.grayscale = self.add_checkbox("灰度匹配（提高匹配成功率）")
        
        self.wait_find = self.add_checkbox("等待找到图片")
        self.timeout = self.add_spinbox("超时时间", 1, 600, 10)
        
        self.after_action = self.add_combobox("找到后动作", ["继续执行", "点击", "移动到位置"])
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.image_path.textChanged.connect(self._update_preview)
        self.wait_find.stateChanged.connect(lambda s: self.timeout.setEnabled(s == 2))
    
    def _update_preview(self):
        path = self.image_path.text()
        if path:
            from PySide6.QtGui import QPixmap
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(self.image_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_preview.setPixmap(pixmap)
                return
        self.image_preview.clear()
        self.image_preview.setText("预览区域")
    
    def get_config(self):
        config = {
            "image_path": self.image_path.text(),
            "find_range": ["full", "window", "custom"][self.find_range.currentIndex()],
            "similarity": self.similarity.value() / 100,
            "grayscale": self.grayscale.isChecked(),
            "wait_find": self.wait_find.isChecked(),
            "timeout": self.timeout.value() if self.wait_find.isChecked() else 0,
            "after_action": ["continue", "click", "move"][self.after_action.currentIndex()],
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "image_path" in config:
            self.image_path.setText(config["image_path"])
        if "similarity" in config:
            self.similarity.setValue(int(config["similarity"] * 100))
        if "grayscale" in config:
            self.grayscale.setChecked(config["grayscale"])
        if "wait_find" in config:
            self.wait_find.setChecked(config["wait_find"])
        if "timeout" in config:
            self.timeout.setValue(config["timeout"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class ImageClickPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("点击图片配置")
        
        self.image_path, _ = self.add_file_browser("图片路径", "图片文件 (*.png *.jpg *.bmp *.gif)")
        
        self.find_range = self.add_combobox("查找范围", ["全屏", "当前窗口", "自定义区域"])
        self.similarity, _ = self.add_slider("相似度", 0, 100, 90, "")
        
        self.click_type = self.add_combobox("点击类型", ["左键单击", "左键双击", "右键单击"])
        
        self.click_position = self.add_combobox("点击位置", ["图片中心", "左上角", "右上角", "左下角", "右下角", "自定义偏移"])
        
        self.offset_x = self.add_spinbox("相对偏移X", -9999, 9999, 0)
        self.offset_y = self.add_spinbox("相对偏移Y", -9999, 9999, 0)
        
        self.random_offset = self.add_checkbox("随机偏移")
        self.random_range = self.add_spinbox("随机范围", 1, 100, 5)
        
        self.wait_find = self.add_checkbox("等待找到图片")
        self.timeout = self.add_spinbox("超时时间", 1, 600, 10)
        
        self.not_found_action = self.add_combobox("未找到时", ["继续执行", "跳过", "报错"])
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.click_position.currentIndexChanged.connect(
            lambda i: self._toggle_offset(i == 5)
        )
        self.wait_find.stateChanged.connect(lambda s: self.timeout.setEnabled(s == 2))
        self.random_offset.stateChanged.connect(lambda s: self.random_range.setEnabled(s == 2))
    
    def _toggle_offset(self, show):
        self.offset_x.parentWidget().setVisible(show)
        self.offset_y.parentWidget().setVisible(show)
    
    def get_config(self):
        config = {
            "image_path": self.image_path.text(),
            "find_range": ["full", "window", "custom"][self.find_range.currentIndex()],
            "similarity": self.similarity.value() / 100,
            "click_type": ["left_single", "left_double", "right_single"][self.click_type.currentIndex()],
            "click_position": ["center", "top_left", "top_right", "bottom_left", "bottom_right", "custom"][self.click_position.currentIndex()],
            "offset_x": self.offset_x.value(),
            "offset_y": self.offset_y.value(),
            "random_offset": self.random_offset.isChecked(),
            "random_range": self.random_range.value() if self.random_offset.isChecked() else 0,
            "wait_find": self.wait_find.isChecked(),
            "timeout": self.timeout.value() if self.wait_find.isChecked() else 0,
            "not_found_action": ["continue", "skip", "error"][self.not_found_action.currentIndex()],
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "image_path" in config:
            self.image_path.setText(config["image_path"])
        if "similarity" in config:
            self.similarity.setValue(int(config["similarity"] * 100))
        if "click_type" in config:
            types = ["left_single", "left_double", "right_single"]
            self.click_type.setCurrentIndex(types.index(config["click_type"]))
        if "click_position" in config:
            positions = ["center", "top_left", "top_right", "bottom_left", "bottom_right", "custom"]
            self.click_position.setCurrentIndex(positions.index(config["click_position"]))
        if "offset_x" in config:
            self.offset_x.setValue(config["offset_x"])
        if "offset_y" in config:
            self.offset_y.setValue(config["offset_y"])
        if "random_offset" in config:
            self.random_offset.setChecked(config["random_offset"])
        if "wait_find" in config:
            self.wait_find.setChecked(config["wait_find"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class ImageExistsPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("图片存在判断配置")
        
        self.image_path, _ = self.add_file_browser("图片路径", "图片文件 (*.png *.jpg *.bmp *.gif)")
        
        self.find_range = self.add_combobox("查找范围", ["全屏", "当前窗口", "自定义区域"])
        self.similarity, _ = self.add_slider("相似度", 0, 100, 90, "")
        
        self.result_var = self.add_lineedit("匹配结果变量", "image_found")
        
        self.exist_action = self.add_combobox("存在时执行", ["继续执行", "跳转到标记"])
        self.not_exist_action = self.add_combobox("不存在时执行", ["继续执行", "跳转到标记"])
        
        self.exist_label = self.add_lineedit("存在跳转标记", "")
        self.not_exist_label = self.add_lineedit("不存在跳转标记", "")
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.exist_action.currentIndexChanged.connect(
            lambda i: self.exist_label.setEnabled(i == 1)
        )
        self.not_exist_action.currentIndexChanged.connect(
            lambda i: self.not_exist_label.setEnabled(i == 1)
        )
    
    def get_config(self):
        config = {
            "image_path": self.image_path.text(),
            "find_range": ["full", "window", "custom"][self.find_range.currentIndex()],
            "similarity": self.similarity.value() / 100,
            "result_var": self.result_var.text(),
            "exist_action": ["continue", "goto"][self.exist_action.currentIndex()],
            "not_exist_action": ["continue", "goto"][self.not_exist_action.currentIndex()],
            "exist_label": self.exist_label.text(),
            "not_exist_label": self.not_exist_label.text(),
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "image_path" in config:
            self.image_path.setText(config["image_path"])
        if "similarity" in config:
            self.similarity.setValue(int(config["similarity"] * 100))
        if "result_var" in config:
            self.result_var.setText(config["result_var"])
        if "exist_label" in config:
            self.exist_label.setText(config["exist_label"])
        if "not_exist_label" in config:
            self.not_exist_label.setText(config["not_exist_label"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
```

- [ ] **步骤 2：验证图像面板导入**

运行：`python -c "from gui.step_panels.image_panel import ImageFindPanel; print('ImageFindPanel imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/image_panel.py
git commit -m "feat: 添加图像操作配置面板（查找图片、点击图片、图片存在）"
```

---

### 任务 5：创建窗口操作配置面板

**文件：**
- 创建：`gui/step_panels/window_panel.py`

**说明：** 实现查找窗口、激活窗口、关闭窗口、窗口位置四种步骤类型的配置面板

- [ ] **步骤 1：编写窗口面板代码**

```python
from . import StepConfigPanel


class WindowFindPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("查找窗口配置")
        
        self.window_title = self.add_lineedit("窗口标题", placeholder="窗口标题，支持通配符")
        
        self.match_type = self.add_combobox("查找方式", ["精确匹配", "包含匹配", "正则匹配"])
        
        self.handle_var = self.add_lineedit("窗口句柄变量", "window_handle")
        
        self.wait_window = self.add_checkbox("等待窗口出现")
        self.timeout = self.add_spinbox("超时时间", 1, 600, 10)
        
        self.not_found_action = self.add_combobox("未找到时", ["继续执行", "跳过", "报错"])
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.wait_window.stateChanged.connect(lambda s: self.timeout.setEnabled(s == 2))
    
    def get_config(self):
        config = {
            "window_title": self.window_title.text(),
            "match_type": ["exact", "contains", "regex"][self.match_type.currentIndex()],
            "handle_var": self.handle_var.text(),
            "wait_window": self.wait_window.isChecked(),
            "timeout": self.timeout.value() if self.wait_window.isChecked() else 0,
            "not_found_action": ["continue", "skip", "error"][self.not_found_action.currentIndex()],
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "window_title" in config:
            self.window_title.setText(config["window_title"])
        if "handle_var" in config:
            self.handle_var.setText(config["handle_var"])
        if "wait_window" in config:
            self.wait_window.setChecked(config["wait_window"])
        if "timeout" in config:
            self.timeout.setValue(config["timeout"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class WindowActivatePanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("激活窗口配置")
        
        self.activate_type = self.add_combobox("激活方式", ["通过标题", "通过句柄变量"])
        
        self.window_title = self.add_lineedit("窗口标题", placeholder="目标窗口标题")
        self.handle_var = self.add_lineedit("窗口句柄变量", "window_handle")
        
        self.wait_activate = self.add_checkbox("等待窗口激活")
        self.timeout = self.add_spinbox("超时时间", 1, 60, 5)
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.activate_type.currentIndexChanged.connect(self._update_visibility)
        self.wait_activate.stateChanged.connect(lambda s: self.timeout.setEnabled(s == 2))
    
    def _update_visibility(self):
        index = self.activate_type.currentIndex()
        self.window_title.parentWidget().setVisible(index == 0)
        self.handle_var.parentWidget().setVisible(index == 1)
    
    def get_config(self):
        config = {
            "activate_type": ["by_title", "by_handle"][self.activate_type.currentIndex()],
            "wait_activate": self.wait_activate.isChecked(),
            "timeout": self.timeout.value() if self.wait_activate.isChecked() else 0,
        }
        
        if self.activate_type.currentIndex() == 0:
            config["window_title"] = self.window_title.text()
        else:
            config["handle_var"] = self.handle_var.text()
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "activate_type" in config:
            types = ["by_title", "by_handle"]
            self.activate_type.setCurrentIndex(types.index(config["activate_type"]))
        if "window_title" in config:
            self.window_title.setText(config["window_title"])
        if "handle_var" in config:
            self.handle_var.setText(config["handle_var"])
        if "wait_activate" in config:
            self.wait_activate.setChecked(config["wait_activate"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class WindowClosePanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("关闭窗口配置")
        
        self.close_type = self.add_combobox("关闭方式", ["通过标题", "通过句柄变量"])
        
        self.window_title = self.add_lineedit("窗口标题", placeholder="目标窗口标题")
        self.handle_var = self.add_lineedit("窗口句柄变量", "window_handle")
        
        self.force_close = self.add_checkbox("强制关闭（结束进程）")
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.close_type.currentIndexChanged.connect(self._update_visibility)
    
    def _update_visibility(self):
        index = self.close_type.currentIndex()
        self.window_title.parentWidget().setVisible(index == 0)
        self.handle_var.parentWidget().setVisible(index == 1)
    
    def get_config(self):
        config = {
            "close_type": ["by_title", "by_handle"][self.close_type.currentIndex()],
            "force_close": self.force_close.isChecked(),
        }
        
        if self.close_type.currentIndex() == 0:
            config["window_title"] = self.window_title.text()
        else:
            config["handle_var"] = self.handle_var.text()
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "close_type" in config:
            types = ["by_title", "by_handle"]
            self.close_type.setCurrentIndex(types.index(config["close_type"]))
        if "window_title" in config:
            self.window_title.setText(config["window_title"])
        if "handle_var" in config:
            self.handle_var.setText(config["handle_var"])
        if "force_close" in config:
            self.force_close.setChecked(config["force_close"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class WindowPositionPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("窗口位置配置")
        
        self.window_title = self.add_lineedit("窗口标题", placeholder="目标窗口标题")
        
        self.x_coord = self.add_spinbox("X坐标", -9999, 9999, 0)
        self.y_coord = self.add_spinbox("Y坐标", -9999, 9999, 0)
        self.width = self.add_spinbox("宽度", 100, 9999, 800)
        self.height = self.add_spinbox("高度", 100, 9999, 600)
        
        self.maximize = self.add_checkbox("最大化窗口")
        self.minimize = self.add_checkbox("最小化窗口")
        
        self.add_delay_section()
    
    def get_config(self):
        config = {
            "window_title": self.window_title.text(),
            "x": self.x_coord.value(),
            "y": self.y_coord.value(),
            "width": self.width.value(),
            "height": self.height.value(),
            "maximize": self.maximize.isChecked(),
            "minimize": self.minimize.isChecked(),
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "window_title" in config:
            self.window_title.setText(config["window_title"])
        if "x" in config:
            self.x_coord.setValue(config["x"])
        if "y" in config:
            self.y_coord.setValue(config["y"])
        if "width" in config:
            self.width.setValue(config["width"])
        if "height" in config:
            self.height.setValue(config["height"])
        if "maximize" in config:
            self.maximize.setChecked(config["maximize"])
        if "minimize" in config:
            self.minimize.setChecked(config["minimize"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
```

- [ ] **步骤 2：验证窗口面板导入**

运行：`python -c "from gui.step_panels.window_panel import WindowFindPanel; print('WindowFindPanel imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/window_panel.py
git commit -m "feat: 添加窗口操作配置面板（查找、激活、关闭、位置）"
```

---

### 任务 6：创建Excel操作配置面板

**文件：**
- 创建：`gui/step_panels/excel_panel.py`

**说明：** 实现读取Excel步骤类型的配置面板

- [ ] **步骤 1：编写Excel面板代码**

```python
from . import StepConfigPanel


class ExcelReadPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("Excel读取配置")
        
        self.file_path, _ = self.add_file_browser("文件路径", "Excel文件 (*.xlsx *.xls)")
        
        self.sheet_name = self.add_lineedit("工作表", "Sheet1")
        
        self.read_range_group, self.read_range_buttons = self.add_radio_group(
            "读取范围", ["单元格", "行", "列", "区域"]
        )
        
        self.cell_address = self.add_lineedit("单元格地址", "A1")
        
        self.row_num = self.add_spinbox("行号", 1, 99999, 1)
        self.col_num = self.add_spinbox("列号", 1, 999, 1)
        
        self.start_cell = self.add_lineedit("起始单元格", "A1")
        self.end_cell = self.add_lineedit("结束单元格", "A1")
        
        self.output_var = self.add_lineedit("输出变量", "excel_result")
        self.output_format = self.add_combobox("变量格式", ["字符串", "数字", "列表"])
        
        self.add_delay_section()
        
        self._connect_signals()
        self._update_visibility()
    
    def _connect_signals(self):
        self.read_range_group.buttonClicked.connect(self._update_visibility)
    
    def _update_visibility(self):
        index = self.read_range_group.checkedId()
        self.cell_address.parentWidget().setVisible(index == 0)
        self.row_num.parentWidget().setVisible(index == 1)
        self.col_num.parentWidget().setVisible(index == 1 or index == 2)
        self.start_cell.parentWidget().setVisible(index == 3)
        self.end_cell.parentWidget().setVisible(index == 3)
    
    def get_config(self):
        range_type = ["cell", "row", "column", "range"][self.read_range_group.checkedId()]
        config = {
            "file_path": self.file_path.text(),
            "sheet_name": self.sheet_name.text(),
            "read_range": range_type,
            "output_var": self.output_var.text(),
            "output_format": ["string", "number", "list"][self.output_format.currentIndex()],
        }
        
        if range_type == "cell":
            config["cell_address"] = self.cell_address.text()
        elif range_type == "row":
            config["row_num"] = self.row_num.value()
        elif range_type == "column":
            config["col_num"] = self.col_num.value()
        elif range_type == "range":
            config["start_cell"] = self.start_cell.text()
            config["end_cell"] = self.end_cell.text()
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "file_path" in config:
            self.file_path.setText(config["file_path"])
        if "sheet_name" in config:
            self.sheet_name.setText(config["sheet_name"])
        if "read_range" in config:
            types = ["cell", "row", "column", "range"]
            self.read_range_group.button(types.index(config["read_range"])).setChecked(True)
        if "cell_address" in config:
            self.cell_address.setText(config["cell_address"])
        if "row_num" in config:
            self.row_num.setValue(config["row_num"])
        if "col_num" in config:
            self.col_num.setValue(config["col_num"])
        if "start_cell" in config:
            self.start_cell.setText(config["start_cell"])
        if "end_cell" in config:
            self.end_cell.setText(config["end_cell"])
        if "output_var" in config:
            self.output_var.setText(config["output_var"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
        self._update_visibility()
```

- [ ] **步骤 2：验证Excel面板导入**

运行：`python -c "from gui.step_panels.excel_panel import ExcelReadPanel; print('ExcelReadPanel imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/excel_panel.py
git commit -m "feat: 添加Excel操作配置面板（读取Excel）"
```

---

### 任务 7：创建控制操作配置面板

**文件：**
- 创建：`gui/step_panels/control_panel.py`

**说明：** 实现等待、条件判断、循环、日志、标记、跳转六种步骤类型的配置面板

- [ ] **步骤 1：编写控制面板代码**

```python
from . import StepConfigPanel


class WaitPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("等待配置")
        
        self.wait_type = self.add_combobox("等待类型", ["固定时间", "随机时间", "条件等待"])
        
        self.fixed_time = self.add_double_spinbox("等待时间", 0, 600, 1)
        
        self.min_time = self.add_double_spinbox("最小时间", 0, 600, 1)
        self.max_time = self.add_double_spinbox("最大时间", 0, 600, 3)
        
        self.wait_condition = self.add_combobox("等待条件", ["图片出现", "文字出现", "窗口出现"])
        self.condition_param, _ = self.add_file_browser("条件参数", "图片文件 (*.png *.jpg *.bmp *.gif)")
        self.timeout = self.add_spinbox("超时时间", 1, 600, 30)
        
        self._connect_signals()
        self._connect_signals()
        self._update_visibility()
    
    def _connect_signals(self):
        self.wait_type.currentIndexChanged.connect(self._update_visibility)
    
    def _update_visibility(self):
        index = self.wait_type.currentIndex()
        self.fixed_time.parentWidget().setVisible(index == 0)
        self.min_time.parentWidget().setVisible(index == 1)
        self.max_time.parentWidget().setVisible(index == 1)
        self.wait_condition.parentWidget().setVisible(index == 2)
        self.condition_param.parentWidget().setVisible(index == 2)
        self.timeout.parentWidget().setVisible(index == 2)
    
    def get_config(self):
        config = {
            "wait_type": ["fixed", "random", "condition"][self.wait_type.currentIndex()],
        }
        
        if self.wait_type.currentIndex() == 0:
            config["fixed_time"] = self.fixed_time.value()
        elif self.wait_type.currentIndex() == 1:
            config["min_time"] = self.min_time.value()
            config["max_time"] = self.max_time.value()
        elif self.wait_type.currentIndex() == 2:
            config["condition"] = ["image", "text", "window"][self.wait_condition.currentIndex()]
            config["param"] = self.condition_param.text()
            config["timeout"] = self.timeout.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "wait_type" in config:
            types = ["fixed", "random", "condition"]
            self.wait_type.setCurrentIndex(types.index(config["wait_type"]))
        if "fixed_time" in config:
            self.fixed_time.setValue(config["fixed_time"])
        if "min_time" in config:
            self.min_time.setValue(config["min_time"])
        if "max_time" in config:
            self.max_time.setValue(config["max_time"])
        self._update_visibility()


class IfElsePanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("条件判断配置")
        
        self.condition_type = self.add_combobox("条件类型", ["值比较", "图片存在", "文字存在", "窗口存在"])
        
        self.var_name = self.add_lineedit("变量名", placeholder="要比较的变量")
        self.compare_op = self.add_combobox("比较操作", ["==", "!=", "<", "<=", ">", ">="])
        self.compare_value = self.add_lineedit("比较值", placeholder="比较目标值")
        
        self.image_path, _ = self.add_file_browser("图片路径", "图片文件 (*.png *.jpg *.bmp *.gif)")
        self.similarity, _ = self.add_slider("相似度", 0, 100, 90, "")
        
        self.text_content = self.add_lineedit("文字内容", placeholder="目标文字")
        self.window_title = self.add_lineedit("窗口标题", placeholder="目标窗口标题")
        
        self.true_action = self.add_combobox("条件成立时", ["继续执行", "跳转到标记"])
        self.false_action = self.add_combobox("条件不成立时", ["继续执行", "跳转到标记"])
        
        self.true_label = self.add_lineedit("成立跳转标记", "")
        self.false_label = self.add_lineedit("不成立跳转标记", "")
        
        self.add_delay_section()
        
        self._connect_signals()
        self._update_visibility()
    
    def _connect_signals(self):
        self.condition_type.currentIndexChanged.connect(self._update_visibility)
        self.true_action.currentIndexChanged.connect(lambda i: self.true_label.setEnabled(i == 1))
        self.false_action.currentIndexChanged.connect(lambda i: self.false_label.setEnabled(i == 1))
    
    def _update_visibility(self):
        index = self.condition_type.currentIndex()
        self.var_name.parentWidget().setVisible(index == 0)
        self.compare_op.parentWidget().setVisible(index == 0)
        self.compare_value.parentWidget().setVisible(index == 0)
        self.image_path.parentWidget().setVisible(index == 1)
        self.similarity.parentWidget().setVisible(index == 1)
        self.text_content.parentWidget().setVisible(index == 2)
        self.window_title.parentWidget().setVisible(index == 3)
    
    def get_config(self):
        config = {
            "condition_type": ["value", "image", "text", "window"][self.condition_type.currentIndex()],
            "true_action": ["continue", "goto"][self.true_action.currentIndex()],
            "false_action": ["continue", "goto"][self.false_action.currentIndex()],
            "true_label": self.true_label.text(),
            "false_label": self.false_label.text(),
        }
        
        if self.condition_type.currentIndex() == 0:
            config["var_name"] = self.var_name.text()
            config["compare_op"] = self.compare_op.currentText()
            config["compare_value"] = self.compare_value.text()
        elif self.condition_type.currentIndex() == 1:
            config["image_path"] = self.image_path.text()
            config["similarity"] = self.similarity.value() / 100
        elif self.condition_type.currentIndex() == 2:
            config["text_content"] = self.text_content.text()
        elif self.condition_type.currentIndex() == 3:
            config["window_title"] = self.window_title.text()
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "condition_type" in config:
            types = ["value", "image", "text", "window"]
            self.condition_type.setCurrentIndex(types.index(config["condition_type"]))
        if "var_name" in config:
            self.var_name.setText(config["var_name"])
        if "compare_value" in config:
            self.compare_value.setText(config["compare_value"])
        if "image_path" in config:
            self.image_path.setText(config["image_path"])
        if "text_content" in config:
            self.text_content.setText(config["text_content"])
        if "window_title" in config:
            self.window_title.setText(config["window_title"])
        if "true_label" in config:
            self.true_label.setText(config["true_label"])
        if "false_label" in config:
            self.false_label.setText(config["false_label"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
        self._update_visibility()


class LoopPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("循环配置")
        
        self.loop_type = self.add_combobox("循环类型", ["次数循环", "条件循环", "遍历列表"])
        
        self.loop_times = self.add_spinbox("循环次数", 1, 99999, 10)
        self.loop_var = self.add_lineedit("循环变量", "loop_index")
        self.start_value = self.add_spinbox("起始值", 0, 99999, 0)
        self.step_value = self.add_spinbox("步长", -999, 999, 1)
        
        self.cond_var = self.add_lineedit("条件变量", placeholder="条件变量名")
        self.cond_op = self.add_combobox("条件操作", ["!=", "==", "<", "<=", ">", ">="])
        self.cond_value = self.add_lineedit("条件值", placeholder="条件目标值")
        
        self.list_var = self.add_lineedit("列表变量", placeholder="要遍历的列表变量")
        self.item_var = self.add_lineedit("元素变量", "item")
        
        self.loop_interval = self.add_double_spinbox("循环间隔", 0, 60, 0)
        
        self.add_delay_section()
        
        self._connect_signals()
        self._update_visibility()
    
    def _connect_signals(self):
        self.loop_type.currentIndexChanged.connect(self._update_visibility)
    
    def _update_visibility(self):
        index = self.loop_type.currentIndex()
        self.loop_times.parentWidget().setVisible(index == 0)
        self.loop_var.parentWidget().setVisible(index == 0)
        self.start_value.parentWidget().setVisible(index == 0)
        self.step_value.parentWidget().setVisible(index == 0)
        self.cond_var.parentWidget().setVisible(index == 1)
        self.cond_op.parentWidget().setVisible(index == 1)
        self.cond_value.parentWidget().setVisible(index == 1)
        self.list_var.parentWidget().setVisible(index == 2)
        self.item_var.parentWidget().setVisible(index == 2)
    
    def get_config(self):
        config = {
            "loop_type": ["times", "condition", "iterate"][self.loop_type.currentIndex()],
            "loop_interval": self.loop_interval.value(),
        }
        
        if self.loop_type.currentIndex() == 0:
            config["loop_times"] = self.loop_times.value()
            config["loop_var"] = self.loop_var.text()
            config["start_value"] = self.start_value.value()
            config["step_value"] = self.step_value.value()
        elif self.loop_type.currentIndex() == 1:
            config["cond_var"] = self.cond_var.text()
            config["cond_op"] = self.cond_op.currentText()
            config["cond_value"] = self.cond_value.text()
        elif self.loop_type.currentIndex() == 2:
            config["list_var"] = self.list_var.text()
            config["item_var"] = self.item_var.text()
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "loop_type" in config:
            types = ["times", "condition", "iterate"]
            self.loop_type.setCurrentIndex(types.index(config["loop_type"]))
        if "loop_times" in config:
            self.loop_times.setValue(config["loop_times"])
        if "loop_var" in config:
            self.loop_var.setText(config["loop_var"])
        if "cond_var" in config:
            self.cond_var.setText(config["cond_var"])
        if "list_var" in config:
            self.list_var.setText(config["list_var"])
        if "item_var" in config:
            self.item_var.setText(config["item_var"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
        self._update_visibility()


class LogPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("日志配置")
        
        self.log_level = self.add_combobox("日志级别", ["调试", "信息", "警告", "错误"])
        
        self.log_content = self.add_textedit("日志内容", placeholder="日志内容，支持变量引用 ${var}")
        
        self.output_to_file = self.add_checkbox("输出到文件")
        self.file_path, _ = self.add_file_browser("文件路径", "日志文件 (*.log)")
        
        self.add_delay_section()
        
        self._connect_signals()
    
    def _connect_signals(self):
        self.output_to_file.stateChanged.connect(lambda s: self.file_path.parentWidget().setEnabled(s == 2))
    
    def get_config(self):
        config = {
            "log_level": ["debug", "info", "warning", "error"][self.log_level.currentIndex()],
            "content": self.log_content.toPlainText(),
            "output_to_file": self.output_to_file.isChecked(),
            "file_path": self.file_path.text() if self.output_to_file.isChecked() else "",
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "log_level" in config:
            levels = ["debug", "info", "warning", "error"]
            self.log_level.setCurrentIndex(levels.index(config["log_level"]))
        if "content" in config:
            self.log_content.setPlainText(config["content"])
        if "output_to_file" in config:
            self.output_to_file.setChecked(config["output_to_file"])
        if "file_path" in config:
            self.file_path.setText(config["file_path"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class LabelPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("标记配置")
        
        self.label_name = self.add_lineedit("标记名称", placeholder="用于跳转的标记名称")
    
    def get_config(self):
        return {"label_name": self.label_name.text()}
    
    def set_config(self, config):
        super().set_config(config)
        if "label_name" in config:
            self.label_name.setText(config["label_name"])


class GotoPanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("跳转配置")
        
        self.target_label = self.add_lineedit("目标标记", placeholder="要跳转的标记名称")
        
        self.add_delay_section()
    
    def get_config(self):
        config = {"target_label": self.target_label.text()}
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "target_label" in config:
            self.target_label.setText(config["target_label"])
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
```

- [ ] **步骤 2：验证控制面板导入**

运行：`python -c "from gui.step_panels.control_panel import WaitPanel, IfElsePanel; print('Control panels imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/control_panel.py
git commit -m "feat: 添加控制操作配置面板（等待、条件判断、循环、日志、标记、跳转）"
```

---

### 任务 8：创建变量操作配置面板

**文件：**
- 创建：`gui/step_panels/variable_panel.py`

**说明：** 实现设置变量、获取变量两种步骤类型的配置面板

- [ ] **步骤 1：编写变量面板代码**

```python
from . import StepConfigPanel


class SetVariablePanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("设置变量配置")
        
        self.var_name = self.add_lineedit("变量名", placeholder="变量名称")
        
        self.var_value = self.add_lineedit("变量值", placeholder="变量值，支持表达式和变量引用")
        
        self.value_type = self.add_combobox("值类型", ["字符串", "数字", "布尔值", "列表", "字典"])
        
        self.add_delay_section()
    
    def get_config(self):
        config = {
            "var_name": self.var_name.text(),
            "var_value": self.var_value.text(),
            "value_type": ["string", "number", "bool", "list", "dict"][self.value_type.currentIndex()],
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "var_name" in config:
            self.var_name.setText(config["var_name"])
        if "var_value" in config:
            self.var_value.setText(config["var_value"])
        if "value_type" in config:
            types = ["string", "number", "bool", "list", "dict"]
            self.value_type.setCurrentIndex(types.index(config["value_type"]))
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])


class GetVariablePanel(StepConfigPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.add_section_title("获取变量配置")
        
        self.var_name = self.add_lineedit("变量名", placeholder="要获取的变量名称")
        
        self.output_mode = self.add_combobox("输出方式", ["输出日志", "弹窗显示", "复制到剪贴板"])
        
        self.add_delay_section()
    
    def get_config(self):
        config = {
            "var_name": self.var_name.text(),
            "output_mode": ["log", "popup", "clipboard"][self.output_mode.currentIndex()],
        }
        
        if self.delay_widget:
            config["delay"] = self.delay_widget.value()
        
        return config
    
    def set_config(self, config):
        super().set_config(config)
        if "var_name" in config:
            self.var_name.setText(config["var_name"])
        if "output_mode" in config:
            modes = ["log", "popup", "clipboard"]
            self.output_mode.setCurrentIndex(modes.index(config["output_mode"]))
        if "delay" in config and self.delay_widget:
            self.delay_widget.setValue(config["delay"])
```

- [ ] **步骤 2：验证变量面板导入**

运行：`python -c "from gui.step_panels.variable_panel import SetVariablePanel; print('Variable panels imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/variable_panel.py
git commit -m "feat: 添加变量操作配置面板（设置变量、获取变量）"
```

---

### 任务 9：创建步骤编辑器对话框

**文件：**
- 创建：`gui/step_editor.py`

**说明：** 创建步骤编辑器对话框主类，根据步骤类型动态切换配置面板，管理数据保存和编辑流程

- [ ] **步骤 1：编写步骤编辑器代码**

```python
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QStackedWidget, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from gui.step_panels import PANEL_MAP, get_panel_class


class StepEditorDialog(QDialog):
    step_saved = Signal(dict)
    
    def __init__(self, step_type=None, step_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("步骤配置")
        self.setMinimumSize(600, 500)
        self.resize(650, 600)
        
        self.step_type = step_type
        self.step_data = step_data or {}
        
        self.setup_ui()
        
        if step_type:
            self.type_combo.setCurrentText(step_type)
            self._switch_panel(step_type)
        
        if step_data:
            self._load_step_data(step_data)
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)
        
        header_layout = QHBoxLayout()
        
        self.type_label = QLabel("步骤类型:")
        self.type_label.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        header_layout.addWidget(self.type_label)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(list(PANEL_MAP.keys()))
        self.type_combo.setStyleSheet("QComboBox { padding: 4px; border: 1px solid #ddd; border-radius: 4px; min-width: 150px; }")
        header_layout.addWidget(self.type_combo)
        
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #ddd;")
        main_layout.addWidget(line)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("QStackedWidget { border: 1px solid #ddd; border-radius: 4px; }")
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.stacked_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        main_layout.addWidget(scroll_area, 1)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.confirm_btn = QPushButton("确定")
        self.confirm_btn.setStyleSheet("""
            QPushButton { padding: 6px 24px; background: #27ae60; color: white; border: none; border-radius: 4px; font-size: 13px; }
            QPushButton:hover { background: #2ecc71; }
        """)
        self.confirm_btn.clicked.connect(self._on_confirm)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton { padding: 6px 24px; background: #ecf0f1; border: none; border-radius: 4px; font-size: 13px; }
            QPushButton:hover { background: #bdc3c7; }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.confirm_btn)
        button_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(button_layout)
        
        self._connect_signals()
        self._initialize_panels()
    
    def _connect_signals(self):
        self.type_combo.currentTextChanged.connect(self._switch_panel)
    
    def _initialize_panels(self):
        self.panel_instances = {}
        for step_type, panel_class in PANEL_MAP.items():
            panel = panel_class()
            self.stacked_widget.addWidget(panel)
            self.panel_instances[step_type] = panel
    
    def _switch_panel(self, step_type):
        self.step_type = step_type
        panel = self.panel_instances.get(step_type)
        if panel:
            index = self.stacked_widget.indexOf(panel)
            self.stacked_widget.setCurrentIndex(index)
    
    def _load_step_data(self, step_data):
        if "type" in step_data:
            self.step_type = step_data["type"]
            self.type_combo.setCurrentText(step_data["type"])
        
        panel = self.panel_instances.get(self.step_type)
        if panel and "config" in step_data:
            panel.set_config(step_data["config"])
        
        if "delay" in step_data:
            for p in self.panel_instances.values():
                if p.delay_widget:
                    p.delay_widget.setValue(step_data["delay"])
    
    def _on_confirm(self):
        panel = self.panel_instances.get(self.step_type)
        if not panel:
            self.reject()
            return
        
        config = panel.get_config()
        delay = config.pop("delay", 0) if "delay" in config else 0
        
        step_data = {
            "type": self.step_type,
            "name": self._get_step_name(self.step_type),
            "description": self._get_step_description(self.step_type),
            "config": config,
            "delay": delay,
            "params": self._format_params(self.step_type, config),
        }
        
        self.step_saved.emit(step_data)
        self.accept()
    
    def _get_step_name(self, step_type):
        name_map = {
            "mouse_click": "鼠标点击",
            "mouse_move": "鼠标移动",
            "mouse_drag": "鼠标拖拽",
            "mouse_scroll": "鼠标滚动",
            "keyboard_type": "键盘输入",
            "keyboard_press": "按键操作",
            "keyboard_hotkey": "快捷键",
            "image_find": "查找图片",
            "image_click": "点击图片",
            "image_exists": "图片存在判断",
            "window_find": "查找窗口",
            "window_activate": "激活窗口",
            "window_close": "关闭窗口",
            "window_position": "窗口位置",
            "excel_read": "读取Excel",
            "wait": "等待",
            "if_else": "条件判断",
            "loop": "循环",
            "log": "日志",
            "label": "标记",
            "goto": "跳转",
            "set_variable": "设置变量",
            "get_variable": "获取变量",
        }
        return name_map.get(step_type, step_type)
    
    def _get_step_description(self, step_type):
        desc_map = {
            "mouse_click": "在指定位置执行鼠标点击",
            "mouse_move": "将鼠标移动到指定位置",
            "mouse_drag": "从起点拖拽到终点",
            "mouse_scroll": "执行鼠标滚轮滚动",
            "keyboard_type": "在当前焦点输入框中输入文本",
            "keyboard_press": "按下并释放单个按键",
            "keyboard_hotkey": "同时按下多个按键组合",
            "image_find": "在屏幕上查找指定图片",
            "image_click": "查找图片并点击",
            "image_exists": "判断图片是否存在于屏幕上",
            "window_find": "查找指定标题的窗口",
            "window_activate": "激活指定窗口",
            "window_close": "关闭指定窗口",
            "window_position": "设置窗口位置和大小",
            "excel_read": "从Excel文件中读取数据",
            "wait": "等待指定时间或条件",
            "if_else": "根据条件执行不同的分支",
            "loop": "执行循环操作",
            "log": "输出日志信息",
            "label": "定义跳转标记点",
            "goto": "跳转到指定标记",
            "set_variable": "设置变量值",
            "get_variable": "获取变量值并输出",
        }
        return desc_map.get(step_type, "")
    
    def _format_params(self, step_type, config):
        params = []
        
        if step_type == "mouse_click":
            click_types = {"left_single": "左键单击", "left_double": "左键双击", "right_single": "右键单击"}
            params.append(f"点击类型: {click_types.get(config.get('click_type'), config.get('click_type'))}")
            if config.get("position_type") == "screen":
                params.append(f"位置: ({config.get('x', 0)}, {config.get('y', 0)})")
            elif config.get("position_type") == "image":
                params.append(f"图片: {config.get('image_path', '')}")
        
        elif step_type == "keyboard_type":
            content = config.get("content", "")[:30]
            if len(content) < len(config.get("content", "")):
                content += "..."
            params.append(f"文本: {content}")
        
        elif step_type == "keyboard_hotkey":
            keys = []
            if config.get("ctrl"):
                keys.append("Ctrl")
            if config.get("alt"):
                keys.append("Alt")
            if config.get("shift"):
                keys.append("Shift")
            if config.get("win"):
                keys.append("Win")
            keys.append(config.get("main_key", ""))
            params.append(f"快捷键: {'+'.join(keys)}")
        
        elif step_type == "image_find" or step_type == "image_click":
            params.append(f"图片: {config.get('image_path', '')}")
            params.append(f"相似度: {config.get('similarity', 0.9):.2f}")
        
        elif step_type == "wait":
            if config.get("wait_type") == "fixed":
                params.append(f"等待时间: {config.get('fixed_time', 1)}秒")
            elif config.get("wait_type") == "random":
                params.append(f"等待时间: {config.get('min_time', 1)}-{config.get('max_time', 3)}秒")
        
        elif step_type == "if_else":
            types = {"value": "值比较", "image": "图片存在", "text": "文字存在", "window": "窗口存在"}
            params.append(f"条件类型: {types.get(config.get('condition_type'), '')}")
        
        elif step_type == "loop":
            types = {"times": "次数循环", "condition": "条件循环", "iterate": "遍历列表"}
            params.append(f"循环类型: {types.get(config.get('loop_type'), '')}")
            if config.get("loop_type") == "times":
                params.append(f"循环次数: {config.get('loop_times', 10)}")
        
        elif step_type == "set_variable":
            params.append(f"变量: {config.get('var_name', '')}")
        
        elif step_type == "log":
            levels = {"debug": "调试", "info": "信息", "warning": "警告", "error": "错误"}
            params.append(f"级别: {levels.get(config.get('log_level'), '')}")
        
        elif step_type == "label":
            params.append(f"标记: {config.get('label_name', '')}")
        
        elif step_type == "goto":
            params.append(f"跳转: {config.get('target_label', '')}")
        
        elif step_type == "excel_read":
            params.append(f"文件: {config.get('file_path', '')}")
        
        return ", ".join(params)
```

- [ ] **步骤 2：验证步骤编辑器导入**

运行：`python -c "from gui.step_editor import StepEditorDialog; print('StepEditorDialog imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/step_editor.py
git commit -m "feat: 创建步骤编辑器对话框主类"
```

---

### 任务 10：集成步骤编辑器到主窗口

**文件：**
- 修改：`gui/main_window.py`

**说明：** 修改主窗口中的添加/编辑步骤逻辑，使用新的步骤编辑器对话框

- [ ] **步骤 1：修改添加步骤方法**

修改 `add_step` 方法，替换原来的简单逻辑：

```python
def add_step(self):
    dialog = StepEditorDialog(parent=self)
    if dialog.exec() == QDialog.Accepted:
        dialog.step_saved.connect(self._on_step_saved)
        dialog.step_saved.emit(dialog.step_data)
```

- [ ] **步骤 2：修改编辑步骤方法**

修改 `edit_step` 方法，传递步骤数据到编辑器：

```python
def edit_step(self):
    current_row = self.step_table.currentRow()
    if current_row < 0:
        QMessageBox.warning(self, "提示", "请先选择要编辑的步骤")
        return
    
    step_type = self.step_table.item(current_row, 0).text()
    step_data = self._get_step_data_from_table(current_row)
    
    dialog = StepEditorDialog(step_type=step_type, step_data=step_data, parent=self)
    if dialog.exec() == QDialog.Accepted:
        dialog.step_saved.connect(self._on_step_saved)
        dialog.step_saved.emit(dialog.step_data)
```

- [ ] **步骤 3：添加步骤保存回调**

添加 `_on_step_saved` 方法处理保存的步骤数据：

```python
def _on_step_saved(self, step_data):
    current_row = self.step_table.currentRow()
    if current_row >= 0:
        self._update_step_in_table(current_row, step_data)
    else:
        self._add_step_to_table(step_data)
```

- [ ] **步骤 4：添加辅助方法**

添加 `_get_step_data_from_table` 和 `_add_step_to_table`、`_update_step_in_table` 方法。

- [ ] **步骤 5：验证集成**

运行：`python main.py`
预期：应用正常启动，点击"添加步骤"弹出步骤编辑器对话框

- [ ] **步骤 6：Commit**

```bash
git add gui/main_window.py
git commit -m "feat: 集成步骤编辑器到主窗口"
```

---

## 自检

### 规格覆盖度

| 规格需求 | 对应任务 |
|----------|----------|
| 鼠标点击配置面板 | 任务 2 |
| 鼠标移动配置面板 | 任务 2 |
| 鼠标拖拽配置面板 | 任务 2 |
| 鼠标滚动配置面板 | 任务 2 |
| 键盘输入配置面板 | 任务 3 |
| 按键操作配置面板 | 任务 3 |
| 快捷键配置面板 | 任务 3 |
| 查找图片配置面板 | 任务 4 |
| 点击图片配置面板 | 任务 4 |
| 图片存在判断配置面板 | 任务 4 |
| 窗口操作配置面板 | 任务 5 |
| Excel读取配置面板 | 任务 6 |
| 等待配置面板 | 任务 7 |
| 条件判断配置面板 | 任务 7 |
| 循环配置面板 | 任务 7 |
| 日志/标记/跳转配置面板 | 任务 7 |
| 变量操作配置面板 | 任务 8 |
| 步骤编辑器对话框 | 任务 9 |
| 主窗口集成 | 任务 10 |

### 类型一致性

- 所有面板类继承自 `StepConfigPanel`
- 统一使用 `get_config()` 和 `set_config(config)` 接口
- 步骤类型 ID 与设计文档保持一致

---

## 执行交接

计划已完成并保存到 `docs/superpowers/plans/2026-07-10-step-editor-implementation.md`。两种执行方式：

**1. 子代理驱动（推荐）** - 每个任务调度一个新的子代理，任务间进行审查，快速迭代

**2. 内联执行** - 在当前会话中使用 executing-plans 执行任务，批量执行并设有检查点

**选哪种方式？"