from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QPushButton, QLabel, QWidget, QComboBox, QDoubleSpinBox)


class GlobalConfigDialog(QDialog):
    """全局配置弹窗，包含等待时间等设置"""

    def __init__(self, wait_config: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("全局等待设置")
        self.setMinimumWidth(360)
        self._wait_config = wait_config
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)

        self._before_widgets = self._make_wait_row("步骤前等待:", layout, self._wait_config["wait_before"])
        self._after_widgets = self._make_wait_row("步骤后等待:", layout, self._wait_config["wait_after"])

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        ok_btn = QPushButton("确定")
        cancel_btn = QPushButton("取消")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

    def _make_wait_row(self, label: str, layout: QFormLayout, config: dict):
        container = QWidget()
        h = QHBoxLayout(container)
        h.setContentsMargins(0, 0, 0, 0)

        type_combo = QComboBox()
        type_combo.addItems(["固定", "随机"])

        fixed_spin = QDoubleSpinBox()
        fixed_spin.setRange(0.1, 60.0)
        fixed_spin.setSingleStep(0.1)
        fixed_spin.setSuffix(" 秒")

        min_spin = QDoubleSpinBox()
        min_spin.setRange(0.1, 60.0)
        min_spin.setSingleStep(0.1)
        min_spin.setSuffix(" 秒")
        min_spin.setVisible(False)

        max_label = QLabel("~")
        max_label.setVisible(False)

        max_spin = QDoubleSpinBox()
        max_spin.setRange(0.1, 60.0)
        max_spin.setSingleStep(0.1)
        max_spin.setSuffix(" 秒")
        max_spin.setVisible(False)

        def on_type_changed(idx):
            is_fixed = (idx == 0)
            fixed_spin.setVisible(is_fixed)
            min_spin.setVisible(not is_fixed)
            max_label.setVisible(not is_fixed)
            max_spin.setVisible(not is_fixed)

        type_combo.currentIndexChanged.connect(on_type_changed)

        if config.get("type") == "random":
            type_combo.setCurrentIndex(1)
            min_spin.setValue(config.get("min", 1.0))
            max_spin.setValue(config.get("max", 3.0))
        else:
            type_combo.setCurrentIndex(0)
            fixed_spin.setValue(config.get("value", 0.5))

        h.addWidget(type_combo)
        h.addWidget(fixed_spin)
        h.addWidget(min_spin)
        h.addWidget(max_label)
        h.addWidget(max_spin)
        h.addStretch()

        layout.addRow(label, container)
        return type_combo, fixed_spin, min_spin, max_spin

    def get_wait_config(self):
        config = {}
        for key, widgets in [("wait_before", self._before_widgets),
                             ("wait_after", self._after_widgets)]:
            combo, fixed_spin, min_spin, max_spin = widgets
            if combo.currentIndex() == 0:
                config[key] = {"type": "fixed", "value": fixed_spin.value()}
            else:
                config[key] = {"type": "random", "min": min_spin.value(), "max": max_spin.value()}
        return config