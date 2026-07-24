"""
窗口步骤配置面板 — 查找窗口、激活窗口、关闭窗口、设置窗口位置
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QLineEdit, QComboBox, QCheckBox,
                               QRadioButton, QGroupBox)
from PySide6.QtCore import Qt, Signal
from . import StepConfigPanel
from gui.styles import Styles


class WindowFindPanel(StepConfigPanel):
    """窗口查找步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.window_title_edit = self.add_lineedit("窗口标题", placeholder="支持通配符 * 和 ?")

        self.match_type_combo = self.add_combobox("查找方式", ["精确匹配", "包含匹配", "正则匹配"])

        self.handle_var_edit = self.add_lineedit("窗口句柄变量", placeholder="存储窗口句柄的变量名")

        self.wait_check = QCheckBox("等待窗口出现")
        self.main_layout.addWidget(self.wait_check)

        self.wait_timeout_group = QGroupBox("超时设置")
        wait_layout = QFormLayout(self.wait_timeout_group)
        self.wait_timeout_spin = QSpinBox()
        self.wait_timeout_spin.setRange(1, 300)
        self.wait_timeout_spin.setValue(30)
        self.wait_timeout_spin.setStyleSheet(Styles.spin_box())
        wait_layout.addRow("超时时间(秒):", self.wait_timeout_spin)
        self.main_layout.addWidget(self.wait_timeout_group)

        self.not_found_combo = self.add_combobox("未找到时", ["继续执行", "跳过", "报错"])

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_wait_visibility()

    def _connect_signals(self):
        self.wait_check.stateChanged.connect(self._update_wait_visibility)

    def _update_wait_visibility(self):
        self.wait_timeout_group.setVisible(self.wait_check.isChecked())

    def get_config(self):
        return {
            "window_title": self.window_title_edit.text(),
            "match_type": ["exact", "contains", "regex"][self.match_type_combo.currentIndex()],
            "handle_var": self.handle_var_edit.text(),
            "wait_for_window": self.wait_check.isChecked(),
            "wait_timeout": self.wait_timeout_spin.value(),
            "not_found_action": ["continue", "skip", "error"][self.not_found_combo.currentIndex()],
            "wait_before": self.get_wait_before(), "wait_after": self.get_wait_after()
        }

    def set_config(self, config):
        self.window_title_edit.setText(config.get("window_title", ""))

        match_type_map = {"exact": 0, "contains": 1, "regex": 2}
        self.match_type_combo.setCurrentIndex(match_type_map.get(config.get("match_type", "contains"), 1))

        self.handle_var_edit.setText(config.get("handle_var", ""))
        self.wait_check.setChecked(config.get("wait_for_window", False))
        self.wait_timeout_spin.setValue(config.get("wait_timeout", 30))

        not_found_map = {"continue": 0, "skip": 1, "error": 2}
        self.not_found_combo.setCurrentIndex(not_found_map.get(config.get("not_found_action", "continue"), 0))

        self.set_wait_before(config.get("wait_before", {"type": "fixed", "value": 0.5}))
        self.set_wait_after(config.get("wait_after", {"type": "fixed", "value": 0.5}))

        self._update_wait_visibility()


class WindowActivatePanel(StepConfigPanel):
    """窗口激活步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.activate_type_radio_group = QGroupBox("激活方式")
        activate_layout = QVBoxLayout(self.activate_type_radio_group)
        self.activate_radios = []
        activate_options = ["通过标题", "通过句柄变量"]
        for i, option in enumerate(activate_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.activate_radios.append(radio)
            activate_layout.addWidget(radio)
        self.main_layout.addWidget(self.activate_type_radio_group)

        self.title_group = QGroupBox("窗口标题")
        title_layout = QFormLayout(self.title_group)
        self.window_title_edit = QLineEdit()
        self.window_title_edit.setPlaceholderText("输入窗口标题")
        self.window_title_edit.setStyleSheet(Styles.small_line_edit())
        title_layout.addRow("标题:", self.window_title_edit)
        self.main_layout.addWidget(self.title_group)

        self.handle_group = QGroupBox("窗口句柄变量")
        handle_layout = QFormLayout(self.handle_group)
        self.handle_var_edit = QLineEdit()
        self.handle_var_edit.setPlaceholderText("存储窗口句柄的变量名")
        self.handle_var_edit.setStyleSheet(Styles.small_line_edit())
        handle_layout.addRow("变量名:", self.handle_var_edit)
        self.main_layout.addWidget(self.handle_group)

        self.wait_check = QCheckBox("等待窗口激活")
        self.main_layout.addWidget(self.wait_check)

        self.wait_timeout_group = QGroupBox("超时设置")
        wait_layout = QFormLayout(self.wait_timeout_group)
        self.wait_timeout_spin = QSpinBox()
        self.wait_timeout_spin.setRange(1, 300)
        self.wait_timeout_spin.setValue(30)
        self.wait_timeout_spin.setStyleSheet(Styles.spin_box())
        wait_layout.addRow("超时时间(秒):", self.wait_timeout_spin)
        self.main_layout.addWidget(self.wait_timeout_group)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_visibility()

    def _connect_signals(self):
        for radio in self.activate_radios:
            radio.toggled.connect(self._update_visibility)
        self.wait_check.stateChanged.connect(self._update_wait_visibility)

    def _update_visibility(self):
        selected_index = -1
        for i, radio in enumerate(self.activate_radios):
            if radio.isChecked():
                selected_index = i
                break

        self.title_group.setVisible(selected_index == 0)
        self.handle_group.setVisible(selected_index == 1)
        self._update_wait_visibility()

    def _update_wait_visibility(self):
        self.wait_timeout_group.setVisible(self.wait_check.isChecked())

    def get_config(self):
        activate_type = self.activate_radios.index([r for r in self.activate_radios if r.isChecked()][0])

        config = {
            "activate_type": ["title", "handle_var"][activate_type],
            "wait_for_activate": self.wait_check.isChecked(),
            "wait_timeout": self.wait_timeout_spin.value(),
            "wait_before": self.get_wait_before(), "wait_after": self.get_wait_after()
        }

        if activate_type == 0:
            config["window_title"] = self.window_title_edit.text()
        else:
            config["handle_var"] = self.handle_var_edit.text()

        return config

    def set_config(self, config):
        activate_type_map = {"title": 0, "handle_var": 1}
        activate_type = activate_type_map.get(config.get("activate_type", "title"), 0)
        self.activate_radios[activate_type].setChecked(True)

        self.window_title_edit.setText(config.get("window_title", ""))
        self.handle_var_edit.setText(config.get("handle_var", ""))

        self.wait_check.setChecked(config.get("wait_for_activate", False))
        self.wait_timeout_spin.setValue(config.get("wait_timeout", 30))

        self.set_wait_before(config.get("wait_before", {"type": "fixed", "value": 0.5}))
        self.set_wait_after(config.get("wait_after", {"type": "fixed", "value": 0.5}))

        self._update_visibility()


class WindowClosePanel(StepConfigPanel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.close_type_radio_group = QGroupBox("关闭方式")
        close_layout = QVBoxLayout(self.close_type_radio_group)
        self.close_radios = []
        close_options = ["通过标题", "通过句柄变量"]
        for i, option in enumerate(close_options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            self.close_radios.append(radio)
            close_layout.addWidget(radio)
        self.main_layout.addWidget(self.close_type_radio_group)

        self.title_group = QGroupBox("窗口标题")
        title_layout = QFormLayout(self.title_group)
        self.window_title_edit = QLineEdit()
        self.window_title_edit.setPlaceholderText("输入窗口标题")
        self.window_title_edit.setStyleSheet(Styles.small_line_edit())
        title_layout.addRow("标题:", self.window_title_edit)
        self.main_layout.addWidget(self.title_group)

        self.handle_group = QGroupBox("窗口句柄变量")
        handle_layout = QFormLayout(self.handle_group)
        self.handle_var_edit = QLineEdit()
        self.handle_var_edit.setPlaceholderText("存储窗口句柄的变量名")
        self.handle_var_edit.setStyleSheet(Styles.small_line_edit())
        handle_layout.addRow("变量名:", self.handle_var_edit)
        self.main_layout.addWidget(self.handle_group)

        self.force_close_check = QCheckBox("强制关闭（结束进程）")
        self.main_layout.addWidget(self.force_close_check)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()
        self._update_visibility()

    def _connect_signals(self):
        for radio in self.close_radios:
            radio.toggled.connect(self._update_visibility)

    def _update_visibility(self):
        selected_index = -1
        for i, radio in enumerate(self.close_radios):
            if radio.isChecked():
                selected_index = i
                break

        self.title_group.setVisible(selected_index == 0)
        self.handle_group.setVisible(selected_index == 1)

    def get_config(self):
        close_type = self.close_radios.index([r for r in self.close_radios if r.isChecked()][0])

        config = {
            "close_type": ["title", "handle_var"][close_type],
            "force_close": self.force_close_check.isChecked(),
            "wait_before": self.get_wait_before(), "wait_after": self.get_wait_after()
        }

        if close_type == 0:
            config["window_title"] = self.window_title_edit.text()
        else:
            config["handle_var"] = self.handle_var_edit.text()

        return config

    def set_config(self, config):
        close_type_map = {"title": 0, "handle_var": 1}
        close_type = close_type_map.get(config.get("close_type", "title"), 0)
        self.close_radios[close_type].setChecked(True)

        self.window_title_edit.setText(config.get("window_title", ""))
        self.handle_var_edit.setText(config.get("handle_var", ""))

        self.force_close_check.setChecked(config.get("force_close", False))
        self.set_wait_before(config.get("wait_before", {"type": "fixed", "value": 0.5}))
        self.set_wait_after(config.get("wait_after", {"type": "fixed", "value": 0.5}))

        self._update_visibility()


class WindowPositionPanel(StepConfigPanel):
    """窗口位置设置步骤配置面板"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.window_title_edit = self.add_lineedit("窗口标题", placeholder="输入窗口标题")

        pos_layout = QHBoxLayout()
        pos_layout.setSpacing(8)

        x_label = QLabel("X坐标:")
        x_label.setFixedWidth(60)
        x_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        pos_layout.addWidget(x_label)

        self.x_spin = QSpinBox()
        self.x_spin.setRange(-10000, 10000)
        self.x_spin.setValue(0)
        self.x_spin.setStyleSheet(Styles.spin_box())
        pos_layout.addWidget(self.x_spin)

        y_label = QLabel("Y坐标:")
        y_label.setFixedWidth(60)
        y_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        pos_layout.addWidget(y_label)

        self.y_spin = QSpinBox()
        self.y_spin.setRange(-10000, 10000)
        self.y_spin.setValue(0)
        self.y_spin.setStyleSheet(Styles.spin_box())
        pos_layout.addWidget(self.y_spin)

        self.main_layout.addLayout(pos_layout)

        size_layout = QHBoxLayout()
        size_layout.setSpacing(8)

        width_label = QLabel("宽度:")
        width_label.setFixedWidth(60)
        width_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        size_layout.addWidget(width_label)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 10000)
        self.width_spin.setValue(800)
        self.width_spin.setStyleSheet(Styles.spin_box())
        size_layout.addWidget(self.width_spin)

        height_label = QLabel("高度:")
        height_label.setFixedWidth(60)
        height_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        size_layout.addWidget(height_label)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(0, 10000)
        self.height_spin.setValue(600)
        self.height_spin.setStyleSheet(Styles.spin_box())
        size_layout.addWidget(self.height_spin)

        self.main_layout.addLayout(size_layout)

        self.maximize_check = QCheckBox("最大化窗口")
        self.main_layout.addWidget(self.maximize_check)

        self.minimize_check = QCheckBox("最小化窗口")
        self.main_layout.addWidget(self.minimize_check)

        self.add_separator()
        self.add_delay_section()

        self._connect_signals()

    def _connect_signals(self):
        self.maximize_check.stateChanged.connect(self._update_size_visibility)
        self.minimize_check.stateChanged.connect(self._update_size_visibility)

    def _update_size_visibility(self):
        is_maximized = self.maximize_check.isChecked()
        is_minimized = self.minimize_check.isChecked()
        self.x_spin.setEnabled(not (is_maximized or is_minimized))
        self.y_spin.setEnabled(not (is_maximized or is_minimized))
        self.width_spin.setEnabled(not (is_maximized or is_minimized))
        self.height_spin.setEnabled(not (is_maximized or is_minimized))

    def get_config(self):
        return {
            "window_title": self.window_title_edit.text(),
            "x": self.x_spin.value(),
            "y": self.y_spin.value(),
            "width": self.width_spin.value(),
            "height": self.height_spin.value(),
            "maximize": self.maximize_check.isChecked(),
            "minimize": self.minimize_check.isChecked(),
            "wait_before": self.get_wait_before(), "wait_after": self.get_wait_after()
        }

    def set_config(self, config):
        self.window_title_edit.setText(config.get("window_title", ""))
        self.x_spin.setValue(config.get("x", 0))
        self.y_spin.setValue(config.get("y", 0))
        self.width_spin.setValue(config.get("width", 800))
        self.height_spin.setValue(config.get("height", 600))
        self.maximize_check.setChecked(config.get("maximize", False))
        self.minimize_check.setChecked(config.get("minimize", False))
        self.set_wait_before(config.get("wait_before", {"type": "fixed", "value": 0.5}))
        self.set_wait_after(config.get("wait_after", {"type": "fixed", "value": 0.5}))

        self._update_size_visibility()