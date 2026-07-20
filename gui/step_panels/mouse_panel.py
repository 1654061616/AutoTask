"""
鼠标步骤配置面板 — 点击、移动、拖拽、滚动
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QDoubleSpinBox, QLineEdit,
                               QComboBox, QCheckBox, QRadioButton, QSlider,
                               QPushButton, QFileDialog, QGroupBox, QFrame,
                               QListView)
from PySide6.QtCore import Qt, Signal
from . import StepConfigPanel
from gui.styles import Styles


class MouseClickPanel(StepConfigPanel):
    """鼠标点击步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.click_type_combo = self.add_combobox("点击类型", ["左键单击", "左键双击", "右键单击", "中键单击"])
        self.click_type_combo.setMaximumWidth(150)

        self.position_radio_group = QGroupBox("点击位置")
        position_layout = QVBoxLayout(self.position_radio_group)
        self.position_radios = []
        position_options = ["当前位置", "屏幕坐标", "相对坐标"]
        for i, option in enumerate(position_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.position_radios.append(radio)
            position_layout.addWidget(radio)
        self.main_layout.addWidget(self.position_radio_group)

        self.screen_coord_group = QGroupBox("屏幕坐标")
        screen_layout = QVBoxLayout(self.screen_coord_group)
        
        x_layout = QHBoxLayout()
        x_label = QLabel("X坐标:")
        x_label.setFixedWidth(50)
        x_layout.addWidget(x_label)
        self.screen_x_spin = QSpinBox()
        self.screen_x_spin.setRange(0, 4000)
        self.screen_x_spin.setValue(0)
        self.screen_x_spin.setStyleSheet(Styles.spin_box())
        x_layout.addWidget(self.screen_x_spin)
        screen_layout.addLayout(x_layout)
        
        y_layout = QHBoxLayout()
        y_label = QLabel("Y坐标:")
        y_label.setFixedWidth(50)
        y_layout.addWidget(y_label)
        self.screen_y_spin = QSpinBox()
        self.screen_y_spin.setRange(0, 4000)
        self.screen_y_spin.setValue(0)
        self.screen_y_spin.setStyleSheet(Styles.spin_box())
        y_layout.addWidget(self.screen_y_spin)
        screen_layout.addLayout(y_layout)
        
        select_btn = QPushButton("选择坐标")
        select_btn.setStyleSheet(Styles.btn_primary("4px 12px"))
        select_btn.clicked.connect(self._select_screen_coordinate)
        screen_layout.addWidget(select_btn)
        self.main_layout.addWidget(self.screen_coord_group)

        self.relative_group = QGroupBox("相对坐标")
        relative_layout = QVBoxLayout(self.relative_group)
        self.relative_base_combo = QComboBox()
        self.relative_base_combo.addItems(["上一次点击位置", "上一次移动位置", "当前鼠标位置"])
        self.relative_base_combo.setStyleSheet(Styles.combo_box())
        rel_base_view = QListView()
        rel_base_view.setStyleSheet(Styles.combo_view())
        self.relative_base_combo.setView(rel_base_view)
        relative_layout.addWidget(self.relative_base_combo)

        rel_offset_layout = QHBoxLayout()
        rel_offset_layout.setSpacing(8)
        rel_offset_label = QLabel("偏移量:")
        rel_offset_label.setFixedWidth(60)
        rel_offset_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        rel_offset_layout.addWidget(rel_offset_label)
        self.relative_x_spin = QSpinBox()
        self.relative_x_spin.setRange(-4000, 4000)
        self.relative_x_spin.setValue(0)
        self.relative_x_spin.setStyleSheet(Styles.spin_box())
        self.relative_y_spin = QSpinBox()
        self.relative_y_spin.setRange(-4000, 4000)
        self.relative_y_spin.setValue(0)
        self.relative_y_spin.setStyleSheet(Styles.spin_box())
        rel_offset_layout.addWidget(QLabel("X"))
        rel_offset_layout.addWidget(self.relative_x_spin)
        rel_offset_layout.addWidget(QLabel("Y"))
        rel_offset_layout.addWidget(self.relative_y_spin)
        relative_layout.addLayout(rel_offset_layout)
        self.main_layout.addWidget(self.relative_group)

        random_layout = QHBoxLayout()
        random_layout.setSpacing(8)
        self.random_offset_check = QCheckBox("随机偏移")
        random_layout.addWidget(self.random_offset_check)
        random_layout.addWidget(QLabel("范围:"))
        self.random_range_spin = QSpinBox()
        self.random_range_spin.setRange(1, 50)
        self.random_range_spin.setValue(5)
        self.random_range_spin.setStyleSheet(Styles.spin_box())
        random_layout.addWidget(self.random_range_spin)
        random_layout.addWidget(QLabel("像素"))
        random_layout.addStretch()
        self.main_layout.addLayout(random_layout)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_position_visibility()

    def _connect_signals(self):
        for radio in self.position_radios:
            radio.toggled.connect(self._update_position_visibility)

    def _update_position_visibility(self):
        selected_index = -1
        for i, radio in enumerate(self.position_radios):
            if radio.isChecked():
                selected_index = i
                break

        self.screen_coord_group.setVisible(selected_index == 1)
        self.relative_group.setVisible(selected_index == 2)

    def _select_screen_coordinate(self):
        def on_coordinate_selected(x, y):
            self.screen_x_spin.setValue(x)
            self.screen_y_spin.setValue(y)
        self._start_capture_coordinate(on_coordinate_selected)

    def get_config(self):
        position_type = self.position_radios.index([r for r in self.position_radios if r.isChecked()][0])
        position_types = ["current", "screen", "relative"]

        config = {
            "click_type": ["left_single", "left_double", "right_single", "middle_single"][self.click_type_combo.currentIndex()],
            "position_type": position_types[position_type],
            "random_offset": self.random_offset_check.isChecked(),
            "random_range": self.random_range_spin.value(),
            "delay": self.delay_spin.value()
        }

        if position_type == 1:
            config["x"] = self.screen_x_spin.value()
            config["y"] = self.screen_y_spin.value()
        elif position_type == 2:
            config["relative_base"] = ["last_click", "last_move", "current"][self.relative_base_combo.currentIndex()]
            config["relative_x"] = self.relative_x_spin.value()
            config["relative_y"] = self.relative_y_spin.value()

        return config

    def set_config(self, config):
        click_type_map = {"left_single": 0, "left_double": 1, "right_single": 2, "middle_single": 3}
        self.click_type_combo.setCurrentIndex(click_type_map.get(config.get("click_type", "left_single"), 0))

        position_type_map = {"current": 0, "screen": 1, "relative": 2}
        position_type = position_type_map.get(config.get("position_type", "current"), 0)
        self.position_radios[position_type].setChecked(True)

        self.random_offset_check.setChecked(config.get("random_offset", False))
        self.random_range_spin.setValue(config.get("random_range", 5))
        self.delay_spin.setValue(config.get("delay", 0))

        self.screen_x_spin.setValue(config.get("x", 0))
        self.screen_y_spin.setValue(config.get("y", 0))

        relative_base_map = {"last_click": 0, "last_move": 1, "current": 2}
        self.relative_base_combo.setCurrentIndex(relative_base_map.get(config.get("relative_base", "last_click"), 0))
        self.relative_x_spin.setValue(config.get("relative_x", 0))
        self.relative_y_spin.setValue(config.get("relative_y", 0))

        self._update_position_visibility()


class MouseMovePanel(StepConfigPanel):
    """鼠标移动步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.move_type_combo = self.add_combobox("移动方式", ["直线移动", "缓动移动", "随机路径"])

        self.duration_spin = self.add_double_spinbox("移动时长", 0, 10, 0.5, 2)

        self.position_radio_group = QGroupBox("移动位置")
        position_layout = QVBoxLayout(self.position_radio_group)
        self.position_radios = []
        position_options = ["屏幕坐标", "相对坐标"]
        for i, option in enumerate(position_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.position_radios.append(radio)
            position_layout.addWidget(radio)
        self.main_layout.addWidget(self.position_radio_group)

        self.screen_coord_group = QGroupBox("屏幕坐标")
        screen_layout = QVBoxLayout(self.screen_coord_group)
        
        x_layout = QHBoxLayout()
        x_label = QLabel("X坐标:")
        x_label.setFixedWidth(50)
        x_layout.addWidget(x_label)
        self.screen_x_spin = QSpinBox()
        self.screen_x_spin.setRange(0, 4000)
        self.screen_x_spin.setValue(0)
        self.screen_x_spin.setStyleSheet(Styles.spin_box())
        x_layout.addWidget(self.screen_x_spin)
        screen_layout.addLayout(x_layout)
        
        y_layout = QHBoxLayout()
        y_label = QLabel("Y坐标:")
        y_label.setFixedWidth(50)
        y_layout.addWidget(y_label)
        self.screen_y_spin = QSpinBox()
        self.screen_y_spin.setRange(0, 4000)
        self.screen_y_spin.setValue(0)
        self.screen_y_spin.setStyleSheet(Styles.spin_box())
        y_layout.addWidget(self.screen_y_spin)
        screen_layout.addLayout(y_layout)
        
        select_btn = QPushButton("选择坐标")
        select_btn.setStyleSheet(Styles.btn_primary("4px 12px"))
        select_btn.clicked.connect(self._select_screen_coordinate)
        screen_layout.addWidget(select_btn)
        self.main_layout.addWidget(self.screen_coord_group)

        self.relative_group = QGroupBox("相对坐标")
        relative_layout = QVBoxLayout(self.relative_group)
        self.relative_base_combo = QComboBox()
        self.relative_base_combo.addItems(["上一次点击位置", "上一次移动位置", "当前鼠标位置"])
        self.relative_base_combo.setStyleSheet(Styles.combo_box())
        rel_base_view = QListView()
        rel_base_view.setStyleSheet(Styles.combo_view())
        self.relative_base_combo.setView(rel_base_view)
        relative_layout.addWidget(self.relative_base_combo)

        rel_offset_layout = QHBoxLayout()
        rel_offset_layout.setSpacing(8)
        rel_offset_label = QLabel("偏移量:")
        rel_offset_label.setFixedWidth(60)
        rel_offset_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        rel_offset_layout.addWidget(rel_offset_label)
        self.relative_x_spin = QSpinBox()
        self.relative_x_spin.setRange(-4000, 4000)
        self.relative_x_spin.setValue(0)
        self.relative_x_spin.setStyleSheet(Styles.spin_box())
        self.relative_y_spin = QSpinBox()
        self.relative_y_spin.setRange(-4000, 4000)
        self.relative_y_spin.setValue(0)
        self.relative_y_spin.setStyleSheet(Styles.spin_box())
        rel_offset_layout.addWidget(QLabel("X"))
        rel_offset_layout.addWidget(self.relative_x_spin)
        rel_offset_layout.addWidget(QLabel("Y"))
        rel_offset_layout.addWidget(self.relative_y_spin)
        relative_layout.addLayout(rel_offset_layout)
        self.main_layout.addWidget(self.relative_group)

        self.smooth_curve_check = self.add_checkbox("平滑曲线移动", checked=True)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_position_visibility()

    def _connect_signals(self):
        for radio in self.position_radios:
            radio.toggled.connect(self._update_position_visibility)

    def _update_position_visibility(self):
        selected_index = -1
        for i, radio in enumerate(self.position_radios):
            if radio.isChecked():
                selected_index = i
                break

        self.screen_coord_group.setVisible(selected_index == 0)
        self.relative_group.setVisible(selected_index == 1)

    def _select_screen_coordinate(self):
        def on_coordinate_selected(x, y):
            self.screen_x_spin.setValue(x)
            self.screen_y_spin.setValue(y)
        self._start_capture_coordinate(on_coordinate_selected)

    def get_config(self):
        position_type = self.position_radios.index([r for r in self.position_radios if r.isChecked()][0])
        position_types = ["screen", "relative"]

        config = {
            "move_type": ["linear", "ease", "random"][self.move_type_combo.currentIndex()],
            "duration": self.duration_spin.value(),
            "position_type": position_types[position_type],
            "smooth_curve": self.smooth_curve_check.isChecked(),
            "delay": self.delay_spin.value()
        }

        if position_type == 0:
            config["x"] = self.screen_x_spin.value()
            config["y"] = self.screen_y_spin.value()
        elif position_type == 1:
            config["relative_base"] = ["last_click", "last_move", "current"][self.relative_base_combo.currentIndex()]
            config["relative_x"] = self.relative_x_spin.value()
            config["relative_y"] = self.relative_y_spin.value()

        return config

    def set_config(self, config):
        move_type_map = {"linear": 0, "ease": 1, "random": 2}
        self.move_type_combo.setCurrentIndex(move_type_map.get(config.get("move_type", "linear"), 0))

        self.duration_spin.setValue(config.get("duration", 0.5))

        position_type_map = {"screen": 0, "relative": 1}
        position_type = position_type_map.get(config.get("position_type", "screen"), 0)
        self.position_radios[position_type].setChecked(True)

        self.smooth_curve_check.setChecked(config.get("smooth_curve", True))
        self.delay_spin.setValue(config.get("delay", 0))

        self.screen_x_spin.setValue(config.get("x", 0))
        self.screen_y_spin.setValue(config.get("y", 0))

        relative_base_map = {"last_click": 0, "last_move": 1, "current": 2}
        self.relative_base_combo.setCurrentIndex(relative_base_map.get(config.get("relative_base", "last_click"), 0))
        self.relative_x_spin.setValue(config.get("relative_x", 0))
        self.relative_y_spin.setValue(config.get("relative_y", 0))

        self._update_position_visibility()


class MouseDragPanel(StepConfigPanel):
    """鼠标拖拽步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.drag_button_combo = self.add_combobox("拖拽按钮", ["左键", "右键", "中键"])

        self.start_screen_group = QGroupBox("起点坐标")
        start_screen_layout = QVBoxLayout(self.start_screen_group)
        
        sx_layout = QHBoxLayout()
        sx_label = QLabel("起点X:")
        sx_label.setFixedWidth(55)
        sx_layout.addWidget(sx_label)
        self.start_x_spin = QSpinBox()
        self.start_x_spin.setRange(0, 4000)
        self.start_x_spin.setValue(0)
        self.start_x_spin.setStyleSheet(Styles.spin_box())
        sx_layout.addWidget(self.start_x_spin)
        start_screen_layout.addLayout(sx_layout)
        
        sy_layout = QHBoxLayout()
        sy_label = QLabel("起点Y:")
        sy_label.setFixedWidth(55)
        sy_layout.addWidget(sy_label)
        self.start_y_spin = QSpinBox()
        self.start_y_spin.setRange(0, 4000)
        self.start_y_spin.setValue(0)
        self.start_y_spin.setStyleSheet(Styles.spin_box())
        sy_layout.addWidget(self.start_y_spin)
        start_screen_layout.addLayout(sy_layout)
        
        start_select_btn = QPushButton("选择起点")
        start_select_btn.setStyleSheet(Styles.btn_primary("4px 12px"))
        start_select_btn.clicked.connect(self._select_start_coordinate)
        start_screen_layout.addWidget(start_select_btn)
        self.main_layout.addWidget(self.start_screen_group)

        self.end_radio_group = QGroupBox("终点类型")
        end_layout = QVBoxLayout(self.end_radio_group)
        self.end_radios = []
        end_options = ["屏幕坐标", "相对起点"]
        for i, option in enumerate(end_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.end_radios.append(radio)
            end_layout.addWidget(radio)
        self.main_layout.addWidget(self.end_radio_group)

        self.end_screen_group = QGroupBox("终点坐标")
        end_screen_layout = QVBoxLayout(self.end_screen_group)
        
        ex_layout = QHBoxLayout()
        ex_label = QLabel("终点X:")
        ex_label.setFixedWidth(55)
        ex_layout.addWidget(ex_label)
        self.end_x_spin = QSpinBox()
        self.end_x_spin.setRange(0, 4000)
        self.end_x_spin.setValue(0)
        self.end_x_spin.setStyleSheet(Styles.spin_box())
        ex_layout.addWidget(self.end_x_spin)
        end_screen_layout.addLayout(ex_layout)
        
        ey_layout = QHBoxLayout()
        ey_label = QLabel("终点Y:")
        ey_label.setFixedWidth(55)
        ey_layout.addWidget(ey_label)
        self.end_y_spin = QSpinBox()
        self.end_y_spin.setRange(0, 4000)
        self.end_y_spin.setValue(0)
        self.end_y_spin.setStyleSheet(Styles.spin_box())
        ey_layout.addWidget(self.end_y_spin)
        end_screen_layout.addLayout(ey_layout)
        
        end_select_btn = QPushButton("选择终点")
        end_select_btn.setStyleSheet(Styles.btn_primary("4px 12px"))
        end_select_btn.clicked.connect(self._select_end_coordinate)
        end_screen_layout.addWidget(end_select_btn)
        self.main_layout.addWidget(self.end_screen_group)

        self.end_relative_group = QGroupBox("相对起点")
        end_relative_layout = QHBoxLayout(self.end_relative_group)
        end_relative_layout.setSpacing(8)
        rel_label = QLabel("偏移量:")
        rel_label.setFixedWidth(60)
        rel_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        end_relative_layout.addWidget(rel_label)
        self.end_relative_x_spin = QSpinBox()
        self.end_relative_x_spin.setRange(-4000, 4000)
        self.end_relative_x_spin.setValue(0)
        self.end_relative_x_spin.setStyleSheet(Styles.spin_box())
        self.end_relative_y_spin = QSpinBox()
        self.end_relative_y_spin.setRange(-4000, 4000)
        self.end_relative_y_spin.setValue(0)
        self.end_relative_y_spin.setStyleSheet(Styles.spin_box())
        end_relative_layout.addWidget(QLabel("X"))
        end_relative_layout.addWidget(self.end_relative_x_spin)
        end_relative_layout.addWidget(QLabel("Y"))
        end_relative_layout.addWidget(self.end_relative_y_spin)
        self.main_layout.addWidget(self.end_relative_group)

        self.drag_duration_spin = self.add_double_spinbox("拖拽时长", 0, 10, 1.0, 2)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_visibility()

    def _connect_signals(self):
        for radio in self.end_radios:
            radio.toggled.connect(self._update_visibility)

    def _update_visibility(self):
        end_index = self.end_radios.index([r for r in self.end_radios if r.isChecked()][0])

        self.end_screen_group.setVisible(end_index == 0)
        self.end_relative_group.setVisible(end_index == 1)

    def _select_start_coordinate(self):
        def on_coordinate_selected(x, y):
            self.start_x_spin.setValue(x)
            self.start_y_spin.setValue(y)
        self._start_capture_coordinate(on_coordinate_selected)

    def _select_end_coordinate(self):
        def on_coordinate_selected(x, y):
            self.end_x_spin.setValue(x)
            self.end_y_spin.setValue(y)
        self._start_capture_coordinate(on_coordinate_selected)

    def get_config(self):
        end_type = self.end_radios.index([r for r in self.end_radios if r.isChecked()][0])

        config = {
            "button": ["left", "right", "middle"][self.drag_button_combo.currentIndex()],
            "start_type": "screen",
            "end_type": ["screen", "relative"][end_type],
            "duration": self.drag_duration_spin.value(),
            "delay": self.delay_spin.value()
        }

        config["start_x"] = self.start_x_spin.value()
        config["start_y"] = self.start_y_spin.value()

        if end_type == 0:
            config["end_x"] = self.end_x_spin.value()
            config["end_y"] = self.end_y_spin.value()
        elif end_type == 1:
            config["relative_x"] = self.end_relative_x_spin.value()
            config["relative_y"] = self.end_relative_y_spin.value()

        return config

    def set_config(self, config):
        button_map = {"left": 0, "right": 1, "middle": 2}
        self.drag_button_combo.setCurrentIndex(button_map.get(config.get("button", "left"), 0))

        end_type_map = {"screen": 0, "relative": 1}
        end_type = end_type_map.get(config.get("end_type", "screen"), 0)
        self.end_radios[end_type].setChecked(True)

        self.drag_duration_spin.setValue(config.get("duration", 1.0))
        self.delay_spin.setValue(config.get("delay", 0))

        self.start_x_spin.setValue(config.get("start_x", 0))
        self.start_y_spin.setValue(config.get("start_y", 0))

        self.end_x_spin.setValue(config.get("end_x", 0))
        self.end_y_spin.setValue(config.get("end_y", 0))
        self.end_relative_x_spin.setValue(config.get("relative_x", 0))
        self.end_relative_y_spin.setValue(config.get("relative_y", 0))

        self._update_visibility()


class MouseScrollPanel(StepConfigPanel):
    """鼠标滚轮步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.direction_combo = self.add_combobox("滚动方向", ["向上", "向下", "向左", "向右"])

        self.scroll_count_spin = self.add_spinbox("滚动次数", 1, 100, 1)

        self.scroll_amount_spin = self.add_spinbox("每次滚动量", 1, 1000, 100)

        self.scroll_interval_spin = self.add_double_spinbox("滚动间隔", 0, 5, 0.1, 2)

        self.add_separator()
        self.add_delay_section()

    def get_config(self):
        return {
            "direction": ["up", "down", "left", "right"][self.direction_combo.currentIndex()],
            "count": self.scroll_count_spin.value(),
            "amount": self.scroll_amount_spin.value(),
            "interval": self.scroll_interval_spin.value(),
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        direction_map = {"up": 0, "down": 1, "left": 2, "right": 3}
        self.direction_combo.setCurrentIndex(direction_map.get(config.get("direction", "up"), 0))
        self.scroll_count_spin.setValue(config.get("count", 1))
        self.scroll_amount_spin.setValue(config.get("amount", 100))
        self.scroll_interval_spin.setValue(config.get("interval", 0.1))
        self.delay_spin.setValue(config.get("delay", 0))