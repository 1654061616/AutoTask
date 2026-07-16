from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QDoubleSpinBox, QLineEdit,
                               QComboBox, QCheckBox, QRadioButton, QSlider,
                               QPushButton, QFileDialog, QGroupBox, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QImage
from . import StepConfigPanel
import os


class ImageFindPanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("查找图片配置")

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
        
        screenshot_btn = QPushButton("截图")
        screenshot_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border-radius: 4px; border: 1px solid #3498db; 
                          background-color: #3498db; color: white; font-size: 12px; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        
        def capture_screenshot():
            def on_screenshot_taken(image_path):
                self.image_path_edit.setText(image_path)
            self._start_capture_screenshot(on_screenshot_taken)
        
        screenshot_btn.clicked.connect(capture_screenshot)
        
        file_layout.addWidget(self.image_path_edit)
        file_layout.addWidget(browse_btn)
        file_layout.addWidget(screenshot_btn)
        self.main_layout.addLayout(file_layout)

        preview_group = QGroupBox("图片预览")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_label = QLabel()
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px dashed #ddd;
                border-radius: 4px;
                min-height: 120px;
            }
        """)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setText("请选择图片")
        preview_layout.addWidget(self.preview_label)
        self.main_layout.addWidget(preview_group)

        self.find_range_combo = self.add_combobox("查找范围", ["全屏", "当前窗口", "自定义区域"])

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
        self.main_layout.addLayout(slider_layout)

        self.grayscale_check = self.add_checkbox("灰度匹配")

        self.algorithm_combo = self.add_combobox("匹配算法", ["模板匹配", "AKAZE特征匹配"])

        wait_layout = QHBoxLayout()
        wait_layout.setSpacing(8)
        self.wait_find_check = QCheckBox("等待找到图片")
        self.wait_find_check.setStyleSheet("QCheckBox { spacing: 8px; }")
        wait_layout.addWidget(self.wait_find_check)
        wait_layout.addWidget(QLabel("超时时间:"))
        self.wait_timeout_spin = QSpinBox()
        self.wait_timeout_spin.setRange(1, 300)
        self.wait_timeout_spin.setValue(10)
        self.wait_timeout_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 80px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        wait_layout.addWidget(self.wait_timeout_spin)
        wait_layout.addWidget(QLabel("秒"))
        wait_layout.addStretch()
        self.main_layout.addLayout(wait_layout)

        self.find_action_combo = self.add_combobox("找到后动作", ["继续执行", "点击", "移动到位置"])

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_wait_timeout_visibility()

    def _connect_signals(self):
        self.image_path_edit.textChanged.connect(self._update_preview)
        self.wait_find_check.toggled.connect(self._update_wait_timeout_visibility)

    def _update_preview(self):
        image_path = self.image_path_edit.text()
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.preview_label.setPixmap(pixmap)
                self.preview_label.setText("")
            else:
                self.preview_label.setText("图片加载失败")
        else:
            self.preview_label.setText("请选择图片")
            self.preview_label.setPixmap(QPixmap())

    def _update_wait_timeout_visibility(self):
        self.wait_timeout_spin.setVisible(self.wait_find_check.isChecked())

    def get_config(self):
        return {
            "image_path": self.image_path_edit.text(),
            "find_range": self.find_range_combo.currentText(),
            "similarity": self.similarity_slider.value() / 100,
            "grayscale_match": self.grayscale_check.isChecked(),
            "algorithm": ["template", "akaze"][self.algorithm_combo.currentIndex()],
            "wait_find": self.wait_find_check.isChecked(),
            "wait_timeout": self.wait_timeout_spin.value(),
            "find_action": ["continue", "click", "move"][self.find_action_combo.currentIndex()],
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        self.image_path_edit.setText(config.get("image_path", ""))
        self.find_range_combo.setCurrentText(config.get("find_range", "全屏"))
        self.similarity_slider.setValue(int(config.get("similarity", 0.9) * 100))
        self.grayscale_check.setChecked(config.get("grayscale_match", False))
        
        algorithm_map = {"template": 0, "akaze": 1}
        self.algorithm_combo.setCurrentIndex(algorithm_map.get(config.get("algorithm", "template"), 0))
        
        self.wait_find_check.setChecked(config.get("wait_find", False))
        self.wait_timeout_spin.setValue(config.get("wait_timeout", 10))

        find_action_map = {"continue": 0, "click": 1, "move": 2}
        self.find_action_combo.setCurrentIndex(find_action_map.get(config.get("find_action", "continue"), 0))

        self.delay_spin.setValue(config.get("delay", 0))
        self._update_preview()
        self._update_wait_timeout_visibility()


class ImageClickPanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("点击图片配置")

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
        
        screenshot_btn = QPushButton("截图")
        screenshot_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border-radius: 4px; border: 1px solid #3498db; 
                          background-color: #3498db; color: white; font-size: 12px; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        
        def capture_screenshot():
            def on_screenshot_taken(image_path):
                self.image_path_edit.setText(image_path)
            self._start_capture_screenshot(on_screenshot_taken)
        
        screenshot_btn.clicked.connect(capture_screenshot)
        
        file_layout.addWidget(self.image_path_edit)
        file_layout.addWidget(browse_btn)
        file_layout.addWidget(screenshot_btn)
        self.main_layout.addLayout(file_layout)

        self.find_range_combo = self.add_combobox("查找范围", ["全屏", "当前窗口", "自定义区域"])

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
        self.main_layout.addLayout(slider_layout)

        self.algorithm_combo = self.add_combobox("匹配算法", ["模板匹配", "AKAZE特征匹配"])

        self.click_type_combo = self.add_combobox("点击类型", ["左键单击", "左键双击", "右键单击"])

        position_group = QGroupBox("点击位置")
        position_layout = QVBoxLayout(position_group)
        self.position_radios = []
        position_options = ["图片中心", "左上角", "右上角", "左下角", "右下角", "自定义偏移"]
        for i, option in enumerate(position_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.position_radios.append(radio)
            position_layout.addWidget(radio)
        self.main_layout.addWidget(position_group)

        offset_layout = QHBoxLayout()
        offset_layout.setSpacing(8)
        offset_label = QLabel("相对偏移:")
        offset_label.setFixedWidth(80)
        offset_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        offset_layout.addWidget(offset_label)
        self.offset_x_spin = QSpinBox()
        self.offset_x_spin.setRange(-1000, 1000)
        self.offset_x_spin.setValue(0)
        self.offset_x_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 80px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        self.offset_y_spin = QSpinBox()
        self.offset_y_spin.setRange(-1000, 1000)
        self.offset_y_spin.setValue(0)
        self.offset_y_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 80px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        offset_layout.addWidget(QLabel("X"))
        offset_layout.addWidget(self.offset_x_spin)
        offset_layout.addWidget(QLabel("Y"))
        offset_layout.addWidget(self.offset_y_spin)
        offset_layout.addStretch()
        self.main_layout.addLayout(offset_layout)

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

        wait_layout = QHBoxLayout()
        wait_layout.setSpacing(8)
        self.wait_find_check = QCheckBox("等待找到图片")
        self.wait_find_check.setStyleSheet("QCheckBox { spacing: 8px; }")
        wait_layout.addWidget(self.wait_find_check)
        wait_layout.addWidget(QLabel("超时时间:"))
        self.wait_timeout_spin = QSpinBox()
        self.wait_timeout_spin.setRange(1, 300)
        self.wait_timeout_spin.setValue(10)
        self.wait_timeout_spin.setStyleSheet("""
            QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 80px; }
            QSpinBox:focus { border-color: #3498db; }
        """)
        wait_layout.addWidget(self.wait_timeout_spin)
        wait_layout.addWidget(QLabel("秒"))
        wait_layout.addStretch()
        self.main_layout.addLayout(wait_layout)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_visibility()

    def _connect_signals(self):
        for radio in self.position_radios:
            radio.toggled.connect(self._update_visibility)
        self.wait_find_check.toggled.connect(self._update_wait_timeout_visibility)

    def _update_visibility(self):
        selected_index = -1
        for i, radio in enumerate(self.position_radios):
            if radio.isChecked():
                selected_index = i
                break
        self.offset_x_spin.setVisible(selected_index == 5)
        self.offset_y_spin.setVisible(selected_index == 5)

    def _update_wait_timeout_visibility(self):
        self.wait_timeout_spin.setVisible(self.wait_find_check.isChecked())

    def get_config(self):
        position_type = self.position_radios.index([r for r in self.position_radios if r.isChecked()][0])
        position_types = ["center", "top_left", "top_right", "bottom_left", "bottom_right", "custom"]

        return {
            "image_path": self.image_path_edit.text(),
            "find_range": self.find_range_combo.currentText(),
            "similarity": self.similarity_slider.value() / 100,
            "algorithm": ["template", "akaze"][self.algorithm_combo.currentIndex()],
            "click_type": ["left_single", "left_double", "right_single"][self.click_type_combo.currentIndex()],
            "click_position": position_types[position_type],
            "offset_x": self.offset_x_spin.value(),
            "offset_y": self.offset_y_spin.value(),
            "random_offset": self.random_offset_check.isChecked(),
            "random_range": self.random_range_spin.value(),
            "wait_find": self.wait_find_check.isChecked(),
            "wait_timeout": self.wait_timeout_spin.value(),
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        self.image_path_edit.setText(config.get("image_path", ""))
        self.find_range_combo.setCurrentText(config.get("find_range", "全屏"))
        self.similarity_slider.setValue(int(config.get("similarity", 0.9) * 100))
        
        algorithm_map = {"template": 0, "akaze": 1}
        self.algorithm_combo.setCurrentIndex(algorithm_map.get(config.get("algorithm", "template"), 0))

        click_type_map = {"left_single": 0, "left_double": 1, "right_single": 2}
        self.click_type_combo.setCurrentIndex(click_type_map.get(config.get("click_type", "left_single"), 0))

        position_type_map = {"center": 0, "top_left": 1, "top_right": 2,
                            "bottom_left": 3, "bottom_right": 4, "custom": 5}
        position_type = position_type_map.get(config.get("click_position", "center"), 0)
        self.position_radios[position_type].setChecked(True)

        self.offset_x_spin.setValue(config.get("offset_x", 0))
        self.offset_y_spin.setValue(config.get("offset_y", 0))

        self.random_offset_check.setChecked(config.get("random_offset", False))
        self.random_range_spin.setValue(config.get("random_range", 5))

        self.wait_find_check.setChecked(config.get("wait_find", False))
        self.wait_timeout_spin.setValue(config.get("wait_timeout", 10))

        self.delay_spin.setValue(config.get("delay", 0))
        self._update_visibility()
        self._update_wait_timeout_visibility()


class ImageExistsPanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.add_section_title("图片存在判断配置")

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
        
        screenshot_btn = QPushButton("截图")
        screenshot_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border-radius: 4px; border: 1px solid #3498db; 
                          background-color: #3498db; color: white; font-size: 12px; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        
        def capture_screenshot():
            def on_screenshot_taken(image_path):
                self.image_path_edit.setText(image_path)
            self._start_capture_screenshot(on_screenshot_taken)
        
        screenshot_btn.clicked.connect(capture_screenshot)
        
        file_layout.addWidget(self.image_path_edit)
        file_layout.addWidget(browse_btn)
        file_layout.addWidget(screenshot_btn)
        self.main_layout.addLayout(file_layout)

        self.find_range_combo = self.add_combobox("查找范围", ["全屏", "当前窗口", "自定义区域"])

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
        self.main_layout.addLayout(slider_layout)

        self.algorithm_combo = self.add_combobox("匹配算法", ["模板匹配", "AKAZE特征匹配"])

        self.result_var_edit = self.add_lineedit("匹配结果变量", default="image_found", placeholder="变量名")

        self.exists_action_combo = self.add_combobox("存在时执行", ["继续执行", "跳转到标记"])

        self.not_exists_action_combo = self.add_combobox("不存在时执行", ["继续执行", "跳转到标记"])

        jump_layout = QHBoxLayout()
        jump_layout.setSpacing(8)
        jump_label = QLabel("跳转标记:")
        jump_label.setFixedWidth(80)
        jump_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        jump_layout.addWidget(jump_label)
        self.jump_mark_edit = QLineEdit()
        self.jump_mark_edit.setPlaceholderText("标记名称")
        self.jump_mark_edit.setStyleSheet("""
            QLineEdit { padding: 5px; border: 1px solid #ddd; border-radius: 4px; }
            QLineEdit:focus { border-color: #3498db; }
        """)
        jump_layout.addWidget(self.jump_mark_edit)
        jump_layout.addStretch()
        self.main_layout.addLayout(jump_layout)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_jump_mark_visibility()

    def _connect_signals(self):
        self.exists_action_combo.currentTextChanged.connect(self._update_jump_mark_visibility)
        self.not_exists_action_combo.currentTextChanged.connect(self._update_jump_mark_visibility)

    def _update_jump_mark_visibility(self):
        exists_jump = self.exists_action_combo.currentText() == "跳转到标记"
        not_exists_jump = self.not_exists_action_combo.currentText() == "跳转到标记"
        self.jump_mark_edit.setVisible(exists_jump or not_exists_jump)

    def get_config(self):
        return {
            "image_path": self.image_path_edit.text(),
            "find_range": self.find_range_combo.currentText(),
            "similarity": self.similarity_slider.value() / 100,
            "algorithm": ["template", "akaze"][self.algorithm_combo.currentIndex()],
            "result_variable": self.result_var_edit.text(),
            "exists_action": ["continue", "jump"][self.exists_action_combo.currentIndex()],
            "not_exists_action": ["continue", "jump"][self.not_exists_action_combo.currentIndex()],
            "jump_mark": self.jump_mark_edit.text(),
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        self.image_path_edit.setText(config.get("image_path", ""))
        self.find_range_combo.setCurrentText(config.get("find_range", "全屏"))
        self.similarity_slider.setValue(int(config.get("similarity", 0.9) * 100))
        
        algorithm_map = {"template": 0, "akaze": 1}
        self.algorithm_combo.setCurrentIndex(algorithm_map.get(config.get("algorithm", "template"), 0))
        
        self.result_var_edit.setText(config.get("result_variable", "image_found"))

        exists_action_map = {"continue": 0, "jump": 1}
        self.exists_action_combo.setCurrentIndex(exists_action_map.get(config.get("exists_action", "continue"), 0))

        not_exists_action_map = {"continue": 0, "jump": 1}
        self.not_exists_action_combo.setCurrentIndex(not_exists_action_map.get(config.get("not_exists_action", "continue"), 0))

        self.jump_mark_edit.setText(config.get("jump_mark", ""))
        self.delay_spin.setValue(config.get("delay", 0))
        self._update_jump_mark_visibility()