from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QDoubleSpinBox, QLineEdit,
                               QComboBox, QCheckBox, QRadioButton, QSlider,
                               QPushButton, QFileDialog, QGroupBox, QFrame,
                               QListView)
from PySide6.QtCore import Qt, Signal
from . import StepConfigPanel


class MouseClickPanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("鼠标点击配置")

        self.click_type_combo = self.add_combobox("点击类型", ["左键单击", "左键双击", "右键单击", "中键单击"])

        self.position_radio_group = QGroupBox("点击位置")
        position_layout = QVBoxLayout(self.position_radio_group)
        self.position_radios = []
        position_options = ["当前位置", "屏幕坐标", "图片位置", "相对坐标"]
        for i, option in enumerate(position_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.position_radios.append(radio)
            position_layout.addWidget(radio)
        self.main_layout.addWidget(self.position_radio_group)

        self.screen_coord_group = QGroupBox("屏幕坐标")
        screen_layout = QFormLayout(self.screen_coord_group)
        self.screen_x_spin = QSpinBox()
        self.screen_x_spin.setRange(0, 4000)
        self.screen_x_spin.setValue(0)
        self.screen_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.screen_y_spin = QSpinBox()
        self.screen_y_spin.setRange(0, 4000)
        self.screen_y_spin.setValue(0)
        self.screen_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        screen_layout.addRow("X坐标:", self.screen_x_spin)
        screen_layout.addRow("Y坐标:", self.screen_y_spin)
        self.main_layout.addWidget(self.screen_coord_group)

        self.image_group = QGroupBox("图片位置")
        image_layout = QVBoxLayout(self.image_group)

        file_layout = QHBoxLayout()
        file_layout.setSpacing(8)
        file_label = QLabel("图片路径:")
        file_label.setFixedWidth(80)
        file_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        file_layout.addWidget(file_label)
        self.image_path_edit = QLineEdit()
        self.image_path_edit.setStyleSheet("""
            QLineEdit { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border-radius: 4px; border: 1px solid #ccc; background-color: #ffffff; }
            QPushButton:hover { background-color: #f0f0f0; }
        """)

        def browse_image():
            file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                self.image_path_edit.setText(file_path)

        browse_btn.clicked.connect(browse_image)
        file_layout.addWidget(self.image_path_edit)
        file_layout.addWidget(browse_btn)
        image_layout.addLayout(file_layout)

        slider_layout = QVBoxLayout()
        slider_label = QLabel("相似度:")
        slider_layout.addWidget(slider_label)
        self.similarity_slider = QSlider(Qt.Horizontal)
        self.similarity_slider.setRange(0, 100)
        self.similarity_slider.setValue(90)
        self.similarity_slider.setTickPosition(QSlider.TicksBelow)
        self.similarity_slider.setTickInterval(10)
        self.similarity_value_label = QLabel("0.90")
        self.similarity_value_label.setAlignment(Qt.AlignCenter)
        self.similarity_value_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.similarity_slider.valueChanged.connect(
            lambda val: self.similarity_value_label.setText(f"{val / 100:.2f}")
        )
        slider_layout.addWidget(self.similarity_slider)
        slider_layout.addWidget(self.similarity_value_label)
        image_layout.addLayout(slider_layout)

        self.find_range_combo = QComboBox()
        self.find_range_combo.addItems(["全屏", "当前窗口", "自定义区域"])
        self.find_range_combo.setStyleSheet("""
            QComboBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QComboBox:focus { border-color: #3498db; }
        """)
        range_list_view = QListView()
        range_list_view.setStyleSheet("""
            QListView { color: #333333; background-color: #ffffff; font-size: 13px; }
            QListView::item { padding: 6px 10px; height: 28px; }
            QListView::item:selected { color: #ffffff; background-color: #3498db; }
            QListView::item:hover { color: #ffffff; background-color: #3498db; }
        """)
        self.find_range_combo.setView(range_list_view)
        image_layout.addWidget(self.find_range_combo)

        offset_layout = QHBoxLayout()
        offset_layout.setSpacing(8)
        offset_label = QLabel("相对偏移:")
        offset_label.setFixedWidth(80)
        offset_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        offset_layout.addWidget(offset_label)
        self.image_offset_x_spin = QSpinBox()
        self.image_offset_x_spin.setRange(-1000, 1000)
        self.image_offset_x_spin.setValue(0)
        self.image_offset_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 80px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.image_offset_y_spin = QSpinBox()
        self.image_offset_y_spin.setRange(-1000, 1000)
        self.image_offset_y_spin.setValue(0)
        self.image_offset_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 80px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        offset_layout.addWidget(QLabel("X"))
        offset_layout.addWidget(self.image_offset_x_spin)
        offset_layout.addWidget(QLabel("Y"))
        offset_layout.addWidget(self.image_offset_y_spin)
        image_layout.addLayout(offset_layout)
        self.main_layout.addWidget(self.image_group)

        self.relative_group = QGroupBox("相对坐标")
        relative_layout = QVBoxLayout(self.relative_group)
        self.relative_base_combo = QComboBox()
        self.relative_base_combo.addItems(["上一次点击位置", "上一次移动位置", "当前鼠标位置"])
        self.relative_base_combo.setStyleSheet("""
            QComboBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QComboBox:focus { border-color: #3498db; }
        """)
        rel_base_view = QListView()
        rel_base_view.setStyleSheet("""
            QListView { color: #333333; background-color: #ffffff; font-size: 13px; }
            QListView::item { padding: 6px 10px; height: 28px; }
            QListView::item:selected { color: #ffffff; background-color: #3498db; }
            QListView::item:hover { color: #ffffff; background-color: #3498db; }
        """)
        self.relative_base_combo.setView(rel_base_view)
        relative_layout.addWidget(self.relative_base_combo)

        rel_offset_layout = QHBoxLayout()
        rel_offset_layout.setSpacing(8)
        rel_offset_label = QLabel("偏移量:")
        rel_offset_label.setFixedWidth(80)
        rel_offset_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        rel_offset_layout.addWidget(rel_offset_label)
        self.relative_x_spin = QSpinBox()
        self.relative_x_spin.setRange(-4000, 4000)
        self.relative_x_spin.setValue(0)
        self.relative_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 100px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.relative_y_spin = QSpinBox()
        self.relative_y_spin.setRange(-4000, 4000)
        self.relative_y_spin.setValue(0)
        self.relative_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 100px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        rel_offset_layout.addWidget(QLabel("X"))
        rel_offset_layout.addWidget(self.relative_x_spin)
        rel_offset_layout.addWidget(QLabel("Y"))
        rel_offset_layout.addWidget(self.relative_y_spin)
        relative_layout.addLayout(rel_offset_layout)
        self.main_layout.addWidget(self.relative_group)

        random_layout = QHBoxLayout()
        random_layout.setSpacing(8)
        self.random_offset_check = QCheckBox("随机偏移")
        self.random_offset_check.setStyleSheet("QCheckBox { spacing: 8px; }")
        random_layout.addWidget(self.random_offset_check)
        random_layout.addWidget(QLabel("范围:"))
        self.random_range_spin = QSpinBox()
        self.random_range_spin.setRange(1, 50)
        self.random_range_spin.setValue(5)
        self.random_range_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 80px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
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
        self.image_group.setVisible(selected_index == 2)
        self.relative_group.setVisible(selected_index == 3)

    def get_config(self):
        position_type = self.position_radios.index([r for r in self.position_radios if r.isChecked()][0])
        position_types = ["current", "screen", "image", "relative"]

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
            config["image_path"] = self.image_path_edit.text()
            config["similarity"] = self.similarity_slider.value() / 100
            config["find_range"] = self.find_range_combo.currentText()
            config["offset_x"] = self.image_offset_x_spin.value()
            config["offset_y"] = self.image_offset_y_spin.value()
        elif position_type == 3:
            config["relative_base"] = ["last_click", "last_move", "current"][self.relative_base_combo.currentIndex()]
            config["relative_x"] = self.relative_x_spin.value()
            config["relative_y"] = self.relative_y_spin.value()

        return config

    def set_config(self, config):
        click_type_map = {"left_single": 0, "left_double": 1, "right_single": 2, "middle_single": 3}
        self.click_type_combo.setCurrentIndex(click_type_map.get(config.get("click_type", "left_single"), 0))

        position_type_map = {"current": 0, "screen": 1, "image": 2, "relative": 3}
        position_type = position_type_map.get(config.get("position_type", "current"), 0)
        self.position_radios[position_type].setChecked(True)

        self.random_offset_check.setChecked(config.get("random_offset", False))
        self.random_range_spin.setValue(config.get("random_range", 5))
        self.delay_spin.setValue(config.get("delay", 0))

        self.screen_x_spin.setValue(config.get("x", 0))
        self.screen_y_spin.setValue(config.get("y", 0))

        self.image_path_edit.setText(config.get("image_path", ""))
        self.similarity_slider.setValue(int(config.get("similarity", 0.9) * 100))
        self.find_range_combo.setCurrentText(config.get("find_range", "全屏"))
        self.image_offset_x_spin.setValue(config.get("offset_x", 0))
        self.image_offset_y_spin.setValue(config.get("offset_y", 0))

        relative_base_map = {"last_click": 0, "last_move": 1, "current": 2}
        self.relative_base_combo.setCurrentIndex(relative_base_map.get(config.get("relative_base", "last_click"), 0))
        self.relative_x_spin.setValue(config.get("relative_x", 0))
        self.relative_y_spin.setValue(config.get("relative_y", 0))

        self._update_position_visibility()


class MouseMovePanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("鼠标移动配置")

        self.move_type_combo = self.add_combobox("移动方式", ["直线移动", "缓动移动", "随机路径"])

        self.duration_spin = self.add_double_spinbox("移动时长", 0, 10, 0.5, 2)

        self.position_radio_group = QGroupBox("移动位置")
        position_layout = QVBoxLayout(self.position_radio_group)
        self.position_radios = []
        position_options = ["屏幕坐标", "图片位置", "相对坐标"]
        for i, option in enumerate(position_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.position_radios.append(radio)
            position_layout.addWidget(radio)
        self.main_layout.addWidget(self.position_radio_group)

        self.screen_coord_group = QGroupBox("屏幕坐标")
        screen_layout = QFormLayout(self.screen_coord_group)
        self.screen_x_spin = QSpinBox()
        self.screen_x_spin.setRange(0, 4000)
        self.screen_x_spin.setValue(0)
        self.screen_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.screen_y_spin = QSpinBox()
        self.screen_y_spin.setRange(0, 4000)
        self.screen_y_spin.setValue(0)
        self.screen_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        screen_layout.addRow("X坐标:", self.screen_x_spin)
        screen_layout.addRow("Y坐标:", self.screen_y_spin)
        self.main_layout.addWidget(self.screen_coord_group)

        self.image_group = QGroupBox("图片位置")
        image_layout = QVBoxLayout(self.image_group)

        file_layout = QHBoxLayout()
        file_layout.setSpacing(8)
        file_label = QLabel("图片路径:")
        file_label.setFixedWidth(80)
        file_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        file_layout.addWidget(file_label)
        self.image_path_edit = QLineEdit()
        self.image_path_edit.setStyleSheet("""
            QLineEdit { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border-radius: 4px; border: 1px solid #ccc; background-color: #ffffff; }
            QPushButton:hover { background-color: #f0f0f0; }
        """)

        def browse_image():
            file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                self.image_path_edit.setText(file_path)

        browse_btn.clicked.connect(browse_image)
        file_layout.addWidget(self.image_path_edit)
        file_layout.addWidget(browse_btn)
        image_layout.addLayout(file_layout)

        slider_layout = QVBoxLayout()
        slider_label = QLabel("相似度:")
        slider_layout.addWidget(slider_label)
        self.similarity_slider = QSlider(Qt.Horizontal)
        self.similarity_slider.setRange(0, 100)
        self.similarity_slider.setValue(90)
        self.similarity_slider.setTickPosition(QSlider.TicksBelow)
        self.similarity_slider.setTickInterval(10)
        self.similarity_value_label = QLabel("0.90")
        self.similarity_value_label.setAlignment(Qt.AlignCenter)
        self.similarity_value_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.similarity_slider.valueChanged.connect(
            lambda val: self.similarity_value_label.setText(f"{val / 100:.2f}")
        )
        slider_layout.addWidget(self.similarity_slider)
        slider_layout.addWidget(self.similarity_value_label)
        image_layout.addLayout(slider_layout)
        self.main_layout.addWidget(self.image_group)

        self.relative_group = QGroupBox("相对坐标")
        relative_layout = QVBoxLayout(self.relative_group)
        self.relative_base_combo = QComboBox()
        self.relative_base_combo.addItems(["上一次点击位置", "上一次移动位置", "当前鼠标位置"])
        self.relative_base_combo.setStyleSheet("""
            QComboBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QComboBox:focus { border-color: #3498db; }
        """)
        rel_base_view = QListView()
        rel_base_view.setStyleSheet("""
            QListView { color: #333333; background-color: #ffffff; font-size: 13px; }
            QListView::item { padding: 6px 10px; height: 28px; }
            QListView::item:selected { color: #ffffff; background-color: #3498db; }
            QListView::item:hover { color: #ffffff; background-color: #3498db; }
        """)
        self.relative_base_combo.setView(rel_base_view)
        relative_layout.addWidget(self.relative_base_combo)

        rel_offset_layout = QHBoxLayout()
        rel_offset_layout.setSpacing(8)
        rel_offset_label = QLabel("偏移量:")
        rel_offset_label.setFixedWidth(80)
        rel_offset_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        rel_offset_layout.addWidget(rel_offset_label)
        self.relative_x_spin = QSpinBox()
        self.relative_x_spin.setRange(-4000, 4000)
        self.relative_x_spin.setValue(0)
        self.relative_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 100px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.relative_y_spin = QSpinBox()
        self.relative_y_spin.setRange(-4000, 4000)
        self.relative_y_spin.setValue(0)
        self.relative_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 100px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
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
        self.image_group.setVisible(selected_index == 1)
        self.relative_group.setVisible(selected_index == 2)

    def get_config(self):
        position_type = self.position_radios.index([r for r in self.position_radios if r.isChecked()][0])
        position_types = ["screen", "image", "relative"]

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
            config["image_path"] = self.image_path_edit.text()
            config["similarity"] = self.similarity_slider.value() / 100
        elif position_type == 2:
            config["relative_base"] = ["last_click", "last_move", "current"][self.relative_base_combo.currentIndex()]
            config["relative_x"] = self.relative_x_spin.value()
            config["relative_y"] = self.relative_y_spin.value()

        return config

    def set_config(self, config):
        move_type_map = {"linear": 0, "ease": 1, "random": 2}
        self.move_type_combo.setCurrentIndex(move_type_map.get(config.get("move_type", "linear"), 0))

        self.duration_spin.setValue(config.get("duration", 0.5))

        position_type_map = {"screen": 0, "image": 1, "relative": 2}
        position_type = position_type_map.get(config.get("position_type", "screen"), 0)
        self.position_radios[position_type].setChecked(True)

        self.smooth_curve_check.setChecked(config.get("smooth_curve", True))
        self.delay_spin.setValue(config.get("delay", 0))

        self.screen_x_spin.setValue(config.get("x", 0))
        self.screen_y_spin.setValue(config.get("y", 0))

        self.image_path_edit.setText(config.get("image_path", ""))
        self.similarity_slider.setValue(int(config.get("similarity", 0.9) * 100))

        relative_base_map = {"last_click": 0, "last_move": 1, "current": 2}
        self.relative_base_combo.setCurrentIndex(relative_base_map.get(config.get("relative_base", "last_click"), 0))
        self.relative_x_spin.setValue(config.get("relative_x", 0))
        self.relative_y_spin.setValue(config.get("relative_y", 0))

        self._update_position_visibility()


class MouseDragPanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("鼠标拖拽配置")

        self.drag_button_combo = self.add_combobox("拖拽按钮", ["左键", "右键", "中键"])

        self.start_radio_group = QGroupBox("起点类型")
        start_layout = QVBoxLayout(self.start_radio_group)
        self.start_radios = []
        start_options = ["屏幕坐标", "图片位置"]
        for i, option in enumerate(start_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.start_radios.append(radio)
            start_layout.addWidget(radio)
        self.main_layout.addWidget(self.start_radio_group)

        self.start_screen_group = QGroupBox("起点坐标")
        start_screen_layout = QFormLayout(self.start_screen_group)
        self.start_x_spin = QSpinBox()
        self.start_x_spin.setRange(0, 4000)
        self.start_x_spin.setValue(0)
        self.start_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.start_y_spin = QSpinBox()
        self.start_y_spin.setRange(0, 4000)
        self.start_y_spin.setValue(0)
        self.start_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        start_screen_layout.addRow("起点X:", self.start_x_spin)
        start_screen_layout.addRow("起点Y:", self.start_y_spin)
        self.main_layout.addWidget(self.start_screen_group)

        self.start_image_group = QGroupBox("起点图片")
        start_image_layout = QVBoxLayout(self.start_image_group)
        file_layout = QHBoxLayout()
        file_layout.setSpacing(8)
        file_label = QLabel("图片路径:")
        file_label.setFixedWidth(80)
        file_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        file_layout.addWidget(file_label)
        self.start_image_edit = QLineEdit()
        self.start_image_edit.setStyleSheet("""
            QLineEdit { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border-radius: 4px; border: 1px solid #ccc; background-color: #ffffff; }
            QPushButton:hover { background-color: #f0f0f0; }
        """)

        def browse_start_image():
            file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                self.start_image_edit.setText(file_path)

        browse_btn.clicked.connect(browse_start_image)
        file_layout.addWidget(self.start_image_edit)
        file_layout.addWidget(browse_btn)
        start_image_layout.addLayout(file_layout)

        start_slider_layout = QVBoxLayout()
        start_slider_label = QLabel("相似度:")
        start_slider_layout.addWidget(start_slider_label)
        self.start_similarity_slider = QSlider(Qt.Horizontal)
        self.start_similarity_slider.setRange(0, 100)
        self.start_similarity_slider.setValue(90)
        self.start_similarity_slider.setTickPosition(QSlider.TicksBelow)
        self.start_similarity_slider.setTickInterval(10)
        self.start_similarity_value_label = QLabel("0.90")
        self.start_similarity_value_label.setAlignment(Qt.AlignCenter)
        self.start_similarity_value_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.start_similarity_slider.valueChanged.connect(
            lambda val: self.start_similarity_value_label.setText(f"{val / 100:.2f}")
        )
        start_slider_layout.addWidget(self.start_similarity_slider)
        start_slider_layout.addWidget(self.start_similarity_value_label)
        start_image_layout.addLayout(start_slider_layout)
        self.main_layout.addWidget(self.start_image_group)

        self.end_radio_group = QGroupBox("终点类型")
        end_layout = QVBoxLayout(self.end_radio_group)
        self.end_radios = []
        end_options = ["屏幕坐标", "图片位置", "相对起点"]
        for i, option in enumerate(end_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.end_radios.append(radio)
            end_layout.addWidget(radio)
        self.main_layout.addWidget(self.end_radio_group)

        self.end_screen_group = QGroupBox("终点坐标")
        end_screen_layout = QFormLayout(self.end_screen_group)
        self.end_x_spin = QSpinBox()
        self.end_x_spin.setRange(0, 4000)
        self.end_x_spin.setValue(0)
        self.end_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.end_y_spin = QSpinBox()
        self.end_y_spin.setRange(0, 4000)
        self.end_y_spin.setValue(0)
        self.end_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        end_screen_layout.addRow("终点X:", self.end_x_spin)
        end_screen_layout.addRow("终点Y:", self.end_y_spin)
        self.main_layout.addWidget(self.end_screen_group)

        self.end_image_group = QGroupBox("终点图片")
        end_image_layout = QVBoxLayout(self.end_image_group)
        end_file_layout = QHBoxLayout()
        end_file_layout.setSpacing(8)
        end_file_label = QLabel("图片路径:")
        end_file_label.setFixedWidth(80)
        end_file_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        end_file_layout.addWidget(end_file_label)
        self.end_image_edit = QLineEdit()
        self.end_image_edit.setStyleSheet("""
            QLineEdit { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        end_browse_btn = QPushButton("浏览")
        end_browse_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border-radius: 4px; border: 1px solid #ccc; background-color: #ffffff; }
            QPushButton:hover { background-color: #f0f0f0; }
        """)

        def browse_end_image():
            file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                self.end_image_edit.setText(file_path)

        end_browse_btn.clicked.connect(browse_end_image)
        end_file_layout.addWidget(self.end_image_edit)
        end_file_layout.addWidget(end_browse_btn)
        end_image_layout.addLayout(end_file_layout)

        end_slider_layout = QVBoxLayout()
        end_slider_label = QLabel("相似度:")
        end_slider_layout.addWidget(end_slider_label)
        self.end_similarity_slider = QSlider(Qt.Horizontal)
        self.end_similarity_slider.setRange(0, 100)
        self.end_similarity_slider.setValue(90)
        self.end_similarity_slider.setTickPosition(QSlider.TicksBelow)
        self.end_similarity_slider.setTickInterval(10)
        self.end_similarity_value_label = QLabel("0.90")
        self.end_similarity_value_label.setAlignment(Qt.AlignCenter)
        self.end_similarity_value_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.end_similarity_slider.valueChanged.connect(
            lambda val: self.end_similarity_value_label.setText(f"{val / 100:.2f}")
        )
        end_slider_layout.addWidget(self.end_similarity_slider)
        end_slider_layout.addWidget(self.end_similarity_value_label)
        end_image_layout.addLayout(end_slider_layout)
        self.main_layout.addWidget(self.end_image_group)

        self.end_relative_group = QGroupBox("相对起点")
        end_relative_layout = QHBoxLayout(self.end_relative_group)
        end_relative_layout.setSpacing(8)
        rel_label = QLabel("偏移量:")
        rel_label.setFixedWidth(80)
        rel_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        end_relative_layout.addWidget(rel_label)
        self.end_relative_x_spin = QSpinBox()
        self.end_relative_x_spin.setRange(-4000, 4000)
        self.end_relative_x_spin.setValue(0)
        self.end_relative_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 100px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.end_relative_y_spin = QSpinBox()
        self.end_relative_y_spin.setRange(-4000, 4000)
        self.end_relative_y_spin.setValue(0)
        self.end_relative_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 100px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
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
        for radio in self.start_radios:
            radio.toggled.connect(self._update_visibility)
        for radio in self.end_radios:
            radio.toggled.connect(self._update_visibility)

    def _update_visibility(self):
        start_index = self.start_radios.index([r for r in self.start_radios if r.isChecked()][0])
        end_index = self.end_radios.index([r for r in self.end_radios if r.isChecked()][0])

        self.start_screen_group.setVisible(start_index == 0)
        self.start_image_group.setVisible(start_index == 1)
        self.end_screen_group.setVisible(end_index == 0)
        self.end_image_group.setVisible(end_index == 1)
        self.end_relative_group.setVisible(end_index == 2)

    def get_config(self):
        start_type = self.start_radios.index([r for r in self.start_radios if r.isChecked()][0])
        end_type = self.end_radios.index([r for r in self.end_radios if r.isChecked()][0])

        config = {
            "button": ["left", "right", "middle"][self.drag_button_combo.currentIndex()],
            "start_type": ["screen", "image"][start_type],
            "end_type": ["screen", "image", "relative"][end_type],
            "duration": self.drag_duration_spin.value(),
            "delay": self.delay_spin.value()
        }

        if start_type == 0:
            config["start_x"] = self.start_x_spin.value()
            config["start_y"] = self.start_y_spin.value()
        elif start_type == 1:
            config["start_image_path"] = self.start_image_edit.text()
            config["start_similarity"] = self.start_similarity_slider.value() / 100

        if end_type == 0:
            config["end_x"] = self.end_x_spin.value()
            config["end_y"] = self.end_y_spin.value()
        elif end_type == 1:
            config["end_image_path"] = self.end_image_edit.text()
            config["end_similarity"] = self.end_similarity_slider.value() / 100
        elif end_type == 2:
            config["relative_x"] = self.end_relative_x_spin.value()
            config["relative_y"] = self.end_relative_y_spin.value()

        return config

    def set_config(self, config):
        button_map = {"left": 0, "right": 1, "middle": 2}
        self.drag_button_combo.setCurrentIndex(button_map.get(config.get("button", "left"), 0))

        start_type_map = {"screen": 0, "image": 1}
        start_type = start_type_map.get(config.get("start_type", "screen"), 0)
        self.start_radios[start_type].setChecked(True)

        end_type_map = {"screen": 0, "image": 1, "relative": 2}
        end_type = end_type_map.get(config.get("end_type", "screen"), 0)
        self.end_radios[end_type].setChecked(True)

        self.drag_duration_spin.setValue(config.get("duration", 1.0))
        self.delay_spin.setValue(config.get("delay", 0))

        self.start_x_spin.setValue(config.get("start_x", 0))
        self.start_y_spin.setValue(config.get("start_y", 0))
        self.start_image_edit.setText(config.get("start_image_path", ""))
        self.start_similarity_slider.setValue(int(config.get("start_similarity", 0.9) * 100))

        self.end_x_spin.setValue(config.get("end_x", 0))
        self.end_y_spin.setValue(config.get("end_y", 0))
        self.end_image_edit.setText(config.get("end_image_path", ""))
        self.end_similarity_slider.setValue(int(config.get("end_similarity", 0.9) * 100))
        self.end_relative_x_spin.setValue(config.get("relative_x", 0))
        self.end_relative_y_spin.setValue(config.get("relative_y", 0))

        self._update_visibility()


class MouseScrollPanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("鼠标滚动配置")

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