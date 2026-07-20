"""
流程控制步骤配置面板 — 等待、条件判断、循环、日志、标签、跳转
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QLineEdit, QTextEdit,
                               QComboBox, QCheckBox, QRadioButton, QSlider,
                               QPushButton, QFileDialog, QGroupBox, QListView)
from PySide6.QtCore import Qt, Signal
from . import StepConfigPanel
from gui.styles import Styles


class WaitPanel(StepConfigPanel):
    """等待步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.wait_type_combo = self.add_combobox("等待类型", ["固定时间", "随机时间", "条件等待"])

        self.fixed_group = QGroupBox("固定时间")
        fixed_layout = QFormLayout(self.fixed_group)
        self.fixed_time_spin = QSpinBox()
        self.fixed_time_spin.setRange(0, 3600)
        self.fixed_time_spin.setValue(1)
        self.fixed_time_spin.setStyleSheet(Styles.spin_box())
        fixed_layout.addRow("等待时间(秒):", self.fixed_time_spin)
        self.main_layout.addWidget(self.fixed_group)

        self.random_group = QGroupBox("随机时间")
        random_layout = QFormLayout(self.random_group)
        self.min_time_spin = QSpinBox()
        self.min_time_spin.setRange(0, 3600)
        self.min_time_spin.setValue(1)
        self.min_time_spin.setStyleSheet(Styles.spin_box())
        self.max_time_spin = QSpinBox()
        self.max_time_spin.setRange(0, 3600)
        self.max_time_spin.setValue(5)
        self.max_time_spin.setStyleSheet(Styles.spin_box())
        random_layout.addRow("最小时间(秒):", self.min_time_spin)
        random_layout.addRow("最大时间(秒):", self.max_time_spin)
        self.main_layout.addWidget(self.random_group)

        self.condition_group = QGroupBox("条件等待")
        condition_layout = QVBoxLayout(self.condition_group)

        self.condition_type_combo = QComboBox()
        self.condition_type_combo.addItems(["图片出现", "文字出现", "窗口出现"])
        self.condition_type_combo.setStyleSheet(Styles.combo_box())
        cond_type_view = QListView()
        cond_type_view.setStyleSheet(Styles.combo_view())
        self.condition_type_combo.setView(cond_type_view)
        condition_layout.addWidget(self.condition_type_combo)

        self.condition_param_group = QGroupBox("条件参数")
        condition_param_layout = QVBoxLayout(self.condition_param_group)

        self.image_path_edit = QLineEdit()
        self.image_path_edit.setPlaceholderText("图片路径")
        self.image_path_edit.setStyleSheet(Styles.input_field())
        condition_param_layout.addWidget(self.image_path_edit)

        browse_layout = QHBoxLayout()
        browse_btn = QPushButton("浏览图片")
        browse_btn.setStyleSheet(Styles.browse_btn_text())

        def browse_image():
            file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                self.image_path_edit.setText(file_path)

        browse_btn.clicked.connect(browse_image)
        browse_layout.addWidget(browse_btn)
        browse_layout.addStretch()
        condition_param_layout.addLayout(browse_layout)

        self.similarity_slider = QSlider(Qt.Horizontal)
        self.similarity_slider.setRange(0, 100)
        self.similarity_slider.setValue(90)
        self.similarity_slider.setTickPosition(QSlider.TicksBelow)
        self.similarity_slider.setTickInterval(10)
        self.similarity_value_label = QLabel("0.90")
        self.similarity_value_label.setAlignment(Qt.AlignCenter)
        self.similarity_value_label.setStyleSheet(Styles.slider_value_label())
        self.similarity_slider.valueChanged.connect(
            lambda val: self.similarity_value_label.setText(f"{val / 100:.2f}")
        )
        condition_param_layout.addWidget(QLabel("相似度:"))
        condition_param_layout.addWidget(self.similarity_slider)
        condition_param_layout.addWidget(self.similarity_value_label)

        self.text_content_edit = QLineEdit()
        self.text_content_edit.setPlaceholderText("要查找的文字内容")
        self.text_content_edit.setStyleSheet(Styles.input_field())
        condition_param_layout.addWidget(self.text_content_edit)

        self.window_title_edit = QLineEdit()
        self.window_title_edit.setPlaceholderText("窗口标题（支持通配符）")
        self.window_title_edit.setStyleSheet(Styles.input_field())
        condition_param_layout.addWidget(self.window_title_edit)

        condition_layout.addWidget(self.condition_param_group)

        timeout_layout = QFormLayout()
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 300)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setStyleSheet(Styles.spin_box())
        timeout_layout.addRow("超时时间(秒):", self.timeout_spin)
        condition_layout.addLayout(timeout_layout)

        self.main_layout.addWidget(self.condition_group)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_wait_visibility()
        self._update_condition_param_visibility()

    def _connect_signals(self):
        self.wait_type_combo.currentIndexChanged.connect(self._update_wait_visibility)
        self.condition_type_combo.currentIndexChanged.connect(self._update_condition_param_visibility)

    def _update_wait_visibility(self):
        index = self.wait_type_combo.currentIndex()
        self.fixed_group.setVisible(index == 0)
        self.random_group.setVisible(index == 1)
        self.condition_group.setVisible(index == 2)

    def _update_condition_param_visibility(self):
        index = self.condition_type_combo.currentIndex()
        self.image_path_edit.setVisible(index == 0)
        self.similarity_slider.setVisible(index == 0)
        self.similarity_value_label.setVisible(index == 0)
        self.text_content_edit.setVisible(index == 1)
        self.window_title_edit.setVisible(index == 2)

    def get_config(self):
        wait_type = ["fixed", "random", "condition"][self.wait_type_combo.currentIndex()]
        config = {
            "wait_type": wait_type,
            "delay": self.delay_spin.value()
        }

        if wait_type == "fixed":
            config["time"] = self.fixed_time_spin.value()
        elif wait_type == "random":
            config["min_time"] = self.min_time_spin.value()
            config["max_time"] = self.max_time_spin.value()
        elif wait_type == "condition":
            condition_type = ["image", "text", "window"][self.condition_type_combo.currentIndex()]
            config["condition_type"] = condition_type
            config["timeout"] = self.timeout_spin.value()
            if condition_type == "image":
                config["image_path"] = self.image_path_edit.text()
                config["similarity"] = self.similarity_slider.value() / 100
            elif condition_type == "text":
                config["text"] = self.text_content_edit.text()
            elif condition_type == "window":
                config["window_title"] = self.window_title_edit.text()

        return config

    def set_config(self, config):
        wait_type_map = {"fixed": 0, "random": 1, "condition": 2}
        self.wait_type_combo.setCurrentIndex(wait_type_map.get(config.get("wait_type", "fixed"), 0))

        self.fixed_time_spin.setValue(config.get("time", 1))
        self.min_time_spin.setValue(config.get("min_time", 1))
        self.max_time_spin.setValue(config.get("max_time", 5))

        condition_type_map = {"image": 0, "text": 1, "window": 2}
        self.condition_type_combo.setCurrentIndex(condition_type_map.get(config.get("condition_type", "image"), 0))
        self.timeout_spin.setValue(config.get("timeout", 30))

        self.image_path_edit.setText(config.get("image_path", ""))
        self.similarity_slider.setValue(int(config.get("similarity", 0.9) * 100))
        self.text_content_edit.setText(config.get("text", ""))
        self.window_title_edit.setText(config.get("window_title", ""))

        self.delay_spin.setValue(config.get("delay", 0))

        self._update_wait_visibility()
        self._update_condition_param_visibility()


class IfElsePanel(StepConfigPanel):
    """条件判断步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.condition_type_combo = self.add_combobox("条件类型", ["值比较", "图片存在", "文字存在", "窗口存在"])

        self.value_compare_group = QGroupBox("值比较")
        value_layout = QFormLayout(self.value_compare_group)

        self.var_name_edit = QLineEdit()
        self.var_name_edit.setPlaceholderText("变量名")
        self.var_name_edit.setStyleSheet(Styles.input_field())
        value_layout.addRow("变量名:", self.var_name_edit)

        self.compare_op_combo = QComboBox()
        self.compare_op_combo.addItems(["==", "!=", "<", "<=", ">", ">="])
        self.compare_op_combo.setStyleSheet(Styles.combo_box())
        compare_op_view = QListView()
        compare_op_view.setStyleSheet(Styles.combo_view())
        self.compare_op_combo.setView(compare_op_view)
        value_layout.addRow("比较操作:", self.compare_op_combo)

        self.compare_value_edit = QLineEdit()
        self.compare_value_edit.setPlaceholderText("比较值")
        self.compare_value_edit.setStyleSheet(Styles.input_field())
        value_layout.addRow("比较值:", self.compare_value_edit)
        self.main_layout.addWidget(self.value_compare_group)

        self.image_exists_group = QGroupBox("图片存在")
        image_layout = QVBoxLayout(self.image_exists_group)

        image_path_layout = QHBoxLayout()
        image_path_layout.setSpacing(8)
        image_label = QLabel("图片路径:")
        image_label.setFixedWidth(80)
        image_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        image_path_layout.addWidget(image_label)
        self.image_path_edit = QLineEdit()
        self.image_path_edit.setPlaceholderText("选择图片")
        self.image_path_edit.setStyleSheet(Styles.input_field())
        image_path_layout.addWidget(self.image_path_edit)
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet(Styles.browse_btn())

        def browse_image():
            file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                self.image_path_edit.setText(file_path)

        browse_btn.clicked.connect(browse_image)
        image_path_layout.addWidget(browse_btn)
        image_layout.addLayout(image_path_layout)

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
        self.similarity_value_label.setStyleSheet(Styles.slider_value_label())
        self.similarity_slider.valueChanged.connect(
            lambda val: self.similarity_value_label.setText(f"{val / 100:.2f}")
        )
        slider_layout.addWidget(self.similarity_slider)
        slider_layout.addWidget(self.similarity_value_label)
        image_layout.addLayout(slider_layout)
        self.main_layout.addWidget(self.image_exists_group)

        self.text_exists_group = QGroupBox("文字存在")
        text_layout = QFormLayout(self.text_exists_group)
        self.text_content_edit = QLineEdit()
        self.text_content_edit.setPlaceholderText("要查找的文字")
        self.text_content_edit.setStyleSheet(Styles.input_field())
        text_layout.addRow("文字内容:", self.text_content_edit)
        self.main_layout.addWidget(self.text_exists_group)

        self.window_exists_group = QGroupBox("窗口存在")
        window_layout = QFormLayout(self.window_exists_group)
        self.window_title_edit = QLineEdit()
        self.window_title_edit.setPlaceholderText("窗口标题（支持通配符）")
        self.window_title_edit.setStyleSheet(Styles.input_field())
        window_layout.addRow("窗口标题:", self.window_title_edit)
        self.main_layout.addWidget(self.window_exists_group)

        self.add_separator()

        self.true_action_combo = self.add_combobox("条件成立时", ["继续执行", "跳转到标记"])
        self.true_goto_edit = QLineEdit()
        self.true_goto_edit.setPlaceholderText("目标标记名称")
        self.true_goto_edit.setStyleSheet(Styles.input_field())
        self.add_line("跳转标记", self.true_goto_edit)

        self.false_action_combo = self.add_combobox("条件不成立时", ["继续执行", "跳转到标记"])
        self.false_goto_edit = QLineEdit()
        self.false_goto_edit.setPlaceholderText("目标标记名称")
        self.false_goto_edit.setStyleSheet(Styles.input_field())
        self.add_line("跳转标记", self.false_goto_edit)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_condition_visibility()
        self._update_goto_visibility()

    def _connect_signals(self):
        self.condition_type_combo.currentIndexChanged.connect(self._update_condition_visibility)
        self.true_action_combo.currentIndexChanged.connect(self._update_goto_visibility)
        self.false_action_combo.currentIndexChanged.connect(self._update_goto_visibility)

    def _update_condition_visibility(self):
        index = self.condition_type_combo.currentIndex()
        self.value_compare_group.setVisible(index == 0)
        self.image_exists_group.setVisible(index == 1)
        self.text_exists_group.setVisible(index == 2)
        self.window_exists_group.setVisible(index == 3)

    def _update_goto_visibility(self):
        self.true_goto_edit.setVisible(self.true_action_combo.currentIndex() == 1)
        self.false_goto_edit.setVisible(self.false_action_combo.currentIndex() == 1)

    def get_config(self):
        condition_type = ["value_compare", "image_exists", "text_exists", "window_exists"][
            self.condition_type_combo.currentIndex()]
        true_action = ["continue", "goto"][self.true_action_combo.currentIndex()]
        false_action = ["continue", "goto"][self.false_action_combo.currentIndex()]

        config = {
            "condition_type": condition_type,
            "true_action": true_action,
            "false_action": false_action,
            "delay": self.delay_spin.value()
        }

        if condition_type == "value_compare":
            config["var_name"] = self.var_name_edit.text()
            config["compare_op"] = self.compare_op_combo.currentText()
            config["compare_value"] = self.compare_value_edit.text()
        elif condition_type == "image_exists":
            config["image_path"] = self.image_path_edit.text()
            config["similarity"] = self.similarity_slider.value() / 100
        elif condition_type == "text_exists":
            config["text"] = self.text_content_edit.text()
        elif condition_type == "window_exists":
            config["window_title"] = self.window_title_edit.text()

        if true_action == "goto":
            config["true_goto"] = self.true_goto_edit.text()
        if false_action == "goto":
            config["false_goto"] = self.false_goto_edit.text()

        return config

    def set_config(self, config):
        condition_type_map = {"value_compare": 0, "image_exists": 1, "text_exists": 2, "window_exists": 3}
        self.condition_type_combo.setCurrentIndex(condition_type_map.get(config.get("condition_type", "value_compare"), 0))

        self.var_name_edit.setText(config.get("var_name", ""))
        compare_op_index = self.compare_op_combo.findText(config.get("compare_op", "=="))
        if compare_op_index >= 0:
            self.compare_op_combo.setCurrentIndex(compare_op_index)
        self.compare_value_edit.setText(config.get("compare_value", ""))

        self.image_path_edit.setText(config.get("image_path", ""))
        self.similarity_slider.setValue(int(config.get("similarity", 0.9) * 100))

        self.text_content_edit.setText(config.get("text", ""))
        self.window_title_edit.setText(config.get("window_title", ""))

        true_action_map = {"continue": 0, "goto": 1}
        self.true_action_combo.setCurrentIndex(true_action_map.get(config.get("true_action", "continue"), 0))
        false_action_map = {"continue": 0, "goto": 1}
        self.false_action_combo.setCurrentIndex(false_action_map.get(config.get("false_action", "continue"), 0))

        self.true_goto_edit.setText(config.get("true_goto", ""))
        self.false_goto_edit.setText(config.get("false_goto", ""))

        self.delay_spin.setValue(config.get("delay", 0))

        self._update_condition_visibility()
        self._update_goto_visibility()


class LoopPanel(StepConfigPanel):
    """循环步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.loop_type_combo = self.add_combobox("循环类型", ["次数循环", "条件循环", "遍历列表"])

        self.count_group = QGroupBox("次数循环")
        count_layout = QFormLayout(self.count_group)

        self.loop_count_spin = QSpinBox()
        self.loop_count_spin.setRange(1, 10000)
        self.loop_count_spin.setValue(10)
        self.loop_count_spin.setStyleSheet(Styles.spin_box())
        count_layout.addRow("循环次数:", self.loop_count_spin)

        self.loop_var_edit = QLineEdit()
        self.loop_var_edit.setPlaceholderText("循环变量名（可选）")
        self.loop_var_edit.setStyleSheet(Styles.input_field())
        count_layout.addRow("循环变量:", self.loop_var_edit)

        self.start_value_spin = QSpinBox()
        self.start_value_spin.setRange(-1000000, 1000000)
        self.start_value_spin.setValue(0)
        self.start_value_spin.setStyleSheet(Styles.spin_box())
        count_layout.addRow("起始值:", self.start_value_spin)

        self.step_spin = QSpinBox()
        self.step_spin.setRange(1, 10000)
        self.step_spin.setValue(1)
        self.step_spin.setStyleSheet(Styles.spin_box())
        count_layout.addRow("步长:", self.step_spin)
        self.main_layout.addWidget(self.count_group)

        self.condition_group = QGroupBox("条件循环")
        condition_layout = QFormLayout(self.condition_group)

        self.condition_var_edit = QLineEdit()
        self.condition_var_edit.setPlaceholderText("条件变量名")
        self.condition_var_edit.setStyleSheet(Styles.input_field())
        condition_layout.addRow("条件变量:", self.condition_var_edit)

        self.condition_op_combo = QComboBox()
        self.condition_op_combo.addItems(["==", "!=", "<", "<=", ">", ">=", "exists", "not_exists"])
        self.condition_op_combo.setStyleSheet(Styles.combo_box())
        cond_op_view = QListView()
        cond_op_view.setStyleSheet(Styles.combo_view())
        self.condition_op_combo.setView(cond_op_view)
        condition_layout.addRow("条件操作:", self.condition_op_combo)

        self.condition_value_edit = QLineEdit()
        self.condition_value_edit.setPlaceholderText("条件值")
        self.condition_value_edit.setStyleSheet(Styles.input_field())
        condition_layout.addRow("条件值:", self.condition_value_edit)
        self.main_layout.addWidget(self.condition_group)

        self.iterate_group = QGroupBox("遍历列表")
        iterate_layout = QFormLayout(self.iterate_group)

        self.list_var_edit = QLineEdit()
        self.list_var_edit.setPlaceholderText("列表变量名")
        self.list_var_edit.setStyleSheet(Styles.input_field())
        iterate_layout.addRow("列表变量:", self.list_var_edit)

        self.element_var_edit = QLineEdit()
        self.element_var_edit.setPlaceholderText("元素变量名")
        self.element_var_edit.setStyleSheet(Styles.input_field())
        iterate_layout.addRow("元素变量:", self.element_var_edit)
        self.main_layout.addWidget(self.iterate_group)

        self.loop_interval_spin = self.add_double_spinbox("循环间隔(秒)", 0, 60, 0.5, 2)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_loop_visibility()

    def _connect_signals(self):
        self.loop_type_combo.currentIndexChanged.connect(self._update_loop_visibility)

    def _update_loop_visibility(self):
        index = self.loop_type_combo.currentIndex()
        self.count_group.setVisible(index == 0)
        self.condition_group.setVisible(index == 1)
        self.iterate_group.setVisible(index == 2)

    def get_config(self):
        loop_type = ["count", "condition", "iterate"][self.loop_type_combo.currentIndex()]

        config = {
            "loop_type": loop_type,
            "loop_interval": self.loop_interval_spin.value(),
            "delay": self.delay_spin.value()
        }

        if loop_type == "count":
            config["count"] = self.loop_count_spin.value()
            config["loop_var"] = self.loop_var_edit.text()
            config["start_value"] = self.start_value_spin.value()
            config["step"] = self.step_spin.value()
        elif loop_type == "condition":
            config["condition_var"] = self.condition_var_edit.text()
            config["condition_op"] = self.condition_op_combo.currentText()
            config["condition_value"] = self.condition_value_edit.text()
        elif loop_type == "iterate":
            config["list_var"] = self.list_var_edit.text()
            config["element_var"] = self.element_var_edit.text()

        return config

    def set_config(self, config):
        loop_type_map = {"count": 0, "condition": 1, "iterate": 2}
        self.loop_type_combo.setCurrentIndex(loop_type_map.get(config.get("loop_type", "count"), 0))

        self.loop_count_spin.setValue(config.get("count", 10))
        self.loop_var_edit.setText(config.get("loop_var", ""))
        self.start_value_spin.setValue(config.get("start_value", 0))
        self.step_spin.setValue(config.get("step", 1))

        self.condition_var_edit.setText(config.get("condition_var", ""))
        condition_op_index = self.condition_op_combo.findText(config.get("condition_op", "=="))
        if condition_op_index >= 0:
            self.condition_op_combo.setCurrentIndex(condition_op_index)
        self.condition_value_edit.setText(config.get("condition_value", ""))

        self.list_var_edit.setText(config.get("list_var", ""))
        self.element_var_edit.setText(config.get("element_var", ""))

        self.loop_interval_spin.setValue(config.get("loop_interval", 0.5))
        self.delay_spin.setValue(config.get("delay", 0))

        self._update_loop_visibility()


class LogPanel(StepConfigPanel):
    """日志输出步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.log_level_combo = self.add_combobox("日志级别", ["调试", "信息", "警告", "错误"])

        self.log_content_edit = QTextEdit()
        self.log_content_edit.setPlaceholderText("日志内容（支持变量引用 ${var}）")
        self.log_content_edit.setStyleSheet(Styles.text_edit())
        self.add_line("日志内容", self.log_content_edit)

        self.output_to_file_check = QCheckBox("输出到文件")
        self.main_layout.addWidget(self.output_to_file_check)

        self.file_path_group = QGroupBox("文件路径")
        file_layout = QHBoxLayout(self.file_path_group)
        file_layout.setSpacing(8)

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("日志文件路径")
        self.file_path_edit.setStyleSheet(Styles.input_field())
        file_layout.addWidget(self.file_path_edit)

        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet(Styles.browse_btn())

        def browse_file():
            file_path, _ = QFileDialog.getSaveFileName(self, "选择日志文件", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                self.file_path_edit.setText(file_path)

        browse_btn.clicked.connect(browse_file)
        file_layout.addWidget(browse_btn)
        self.main_layout.addWidget(self.file_path_group)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_file_visibility()

    def _connect_signals(self):
        self.output_to_file_check.stateChanged.connect(self._update_file_visibility)

    def _update_file_visibility(self):
        self.file_path_group.setVisible(self.output_to_file_check.isChecked())

    def get_config(self):
        log_level = ["debug", "info", "warning", "error"][self.log_level_combo.currentIndex()]

        config = {
            "log_level": log_level,
            "content": self.log_content_edit.toPlainText(),
            "output_to_file": self.output_to_file_check.isChecked(),
            "delay": self.delay_spin.value()
        }

        if self.output_to_file_check.isChecked():
            config["file_path"] = self.file_path_edit.text()

        return config

    def set_config(self, config):
        log_level_map = {"debug": 0, "info": 1, "warning": 2, "error": 3}
        self.log_level_combo.setCurrentIndex(log_level_map.get(config.get("log_level", "info"), 1))

        self.log_content_edit.setText(config.get("content", ""))
        self.output_to_file_check.setChecked(config.get("output_to_file", False))
        self.file_path_edit.setText(config.get("file_path", ""))

        self.delay_spin.setValue(config.get("delay", 0))

        self._update_file_visibility()


class LabelPanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.label_name_edit = QLineEdit()
        self.label_name_edit.setPlaceholderText("标记名称")
        self.label_name_edit.setStyleSheet(Styles.input_field())
        self.add_line("标记名称", self.label_name_edit)

    def get_config(self):
        return {
            "label_name": self.label_name_edit.text()
        }

    def set_config(self, config):
        self.label_name_edit.setText(config.get("label_name", ""))


class GotoPanel(StepConfigPanel):
    """跳转步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.target_label_edit = QLineEdit()
        self.target_label_edit.setPlaceholderText("目标标记名称")
        self.target_label_edit.setStyleSheet(Styles.input_field())
        self.add_line("目标标记", self.target_label_edit)

        self.add_separator()
        self.add_delay_section()

    def get_config(self):
        return {
            "target_label": self.target_label_edit.text(),
            "delay": self.delay_spin.value()
        }

    def set_config(self, config):
        self.target_label_edit.setText(config.get("target_label", ""))
        self.delay_spin.setValue(config.get("delay", 0))