"""
步骤面板模块 �?步骤配置面板基类和坐标截图工�?
"""
import os
import ctypes
import platform
from PIL import ImageGrab
import pyautogui
from utils.resource_path import ensure_image_dir
from PySide6.QtWidgets import (QWidget, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QDoubleSpinBox, QLineEdit,
                               QTextEdit, QComboBox, QCheckBox, QRadioButton,
                               QSlider, QPushButton, QFileDialog, QGroupBox,
                               QFrame, QListView, QApplication)
from PySide6.QtCore import Qt, Signal, QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QCursor
from gui.styles import Styles, Colors

user32 = ctypes.windll.user32


def get_virtual_screen_geometry():
    try:
        return (
            user32.GetSystemMetrics(76),
            user32.GetSystemMetrics(77),
            user32.GetSystemMetrics(78),
            user32.GetSystemMetrics(79)
        )
    except:
        return 0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


VX, VY, VW, VH = get_virtual_screen_geometry()


class StepConfigPanel(QWidget):
    """步骤配置面板基类，提供通用的控件构建方法"""

    config_changed = Signal(dict)

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(6, 6, 6, 6)
        self.main_layout.setSpacing(6)
        self.setLayout(self.main_layout)
        self._config = {}
        self.setStyleSheet(Styles.panel_bg())

    def _start_capture_coordinate(self, callback):
        app = QApplication.instance()
        
        windows_to_minimize = []
        for widget in app.topLevelWidgets():
            if hasattr(widget, 'windowTitle'):
                title = widget.windowTitle()
                if "AutoFlow" in title or "节点编辑" in title:
                    windows_to_minimize.append(widget)
        
        for w in windows_to_minimize:
            w.showMinimized()

        self._coord_callback = callback
        self._coord_overlay = CoordOverlay(windows_to_minimize)
        self._coord_overlay.coordinate_selected.connect(self._on_coordinate_selected)
        self._coord_overlay.exec()

    def _on_coordinate_selected(self, x, y):
        if self._coord_callback:
            self._coord_callback(x, y)
        self._coord_overlay = None

    def _start_capture_screenshot(self, callback):
        app = QApplication.instance()
        
        windows_to_minimize = []
        for widget in app.topLevelWidgets():
            if hasattr(widget, 'windowTitle'):
                title = widget.windowTitle()
                if "AutoFlow" in title or "节点编辑" in title:
                    windows_to_minimize.append(widget)
        
        for w in windows_to_minimize:
            w.showMinimized()

        self._screenshot_callback = callback
        self._screenshot_overlay = ScreenshotOverlay(windows_to_minimize)
        self._screenshot_overlay.screenshot_taken.connect(self._on_screenshot_taken)
        self._screenshot_overlay.exec()

    def _on_screenshot_taken(self, image_path):
        if self._screenshot_callback:
            self._screenshot_callback(image_path)
        self._screenshot_overlay = None

    def _start_capture_region(self, callback):
        app = QApplication.instance()
        
        windows_to_minimize = []
        for widget in app.topLevelWidgets():
            if hasattr(widget, 'windowTitle'):
                title = widget.windowTitle()
                if "AutoFlow" in title or "节点编辑" in title:
                    windows_to_minimize.append(widget)
        
        for w in windows_to_minimize:
            w.showMinimized()

        self._region_callback = callback
        self._region_overlay = RegionOverlay(windows_to_minimize)
        self._region_overlay.region_selected.connect(self._on_region_selected)
        self._region_overlay.exec()

    def _on_region_selected(self, x, y, width, height):
        if self._region_callback:
            self._region_callback(x, y, width, height)
        self._region_overlay = None

    def get_config(self):
        raise NotImplementedError("Subclasses must implement get_config()")

    def set_config(self, config):
        raise NotImplementedError("Subclasses must implement set_config(config)")

    def add_section_title(self, text):
        label = QLabel(f"<b>{text}</b>")
        label.setStyleSheet(Styles.section_title())
        self.main_layout.addWidget(label)
        return label

    def add_line(self, label_text, widget, stretch=0):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(6)

        label = QLabel(f"{label_text}:")
        label.setStyleSheet(Styles.LABEL_SECTION)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        row_layout.addWidget(label)

        widget.setStyleSheet(Styles.widget_font())
        row_layout.addWidget(widget, 1)

        self.main_layout.addLayout(row_layout)
        return widget

    def add_spinbox(self, label_text, min_val, max_val, default, step=1):
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default)
        spinbox.setSingleStep(step)
        spinbox.setStyleSheet(Styles.small_spin_box())
        return self.add_line(label_text, spinbox)

    def add_double_spinbox(self, label_text, min_val, max_val, default, decimals=2):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default)
        spinbox.setDecimals(decimals)
        spinbox.setStyleSheet(Styles.small_double_spin_box())
        return self.add_line(label_text, spinbox)

    def add_lineedit(self, label_text, default="", placeholder=""):
        lineedit = QLineEdit()
        lineedit.setText(default)
        lineedit.setPlaceholderText(placeholder)
        lineedit.setStyleSheet(Styles.small_line_edit())
        return self.add_line(label_text, lineedit)

    def add_textedit(self, label_text, default="", placeholder=""):
        textedit = QTextEdit()
        textedit.setPlaceholderText(placeholder)
        if default:
            textedit.setText(default)
        textedit.setStyleSheet(Styles.small_text_edit())
        return self.add_line(label_text, textedit)

    def add_combobox(self, label_text, items, default_index=0):
        combobox = QComboBox()
        combobox.addItems(items)
        if 0 <= default_index < len(items):
            combobox.setCurrentIndex(default_index)
        combobox.setStyleSheet(Styles.small_combo_box())
        
        list_view = QListView()
        list_view.setStyleSheet(Styles.small_combo_view())
        combobox.setView(list_view)
        
        return self.add_line(label_text, combobox)

    def add_checkbox(self, text, checked=False):
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        self.main_layout.addWidget(checkbox)
        return checkbox

    def add_radio_group(self, label_text, options, default_index=0):
        group_box = QGroupBox(label_text)
        group_box.setStyleSheet(Styles.radio_group())
        group_layout = QVBoxLayout(group_box)
        group_layout.setSpacing(4)
        group_layout.setContentsMargins(4, 4, 4, 4)

        buttons = []
        for i, option in enumerate(options):
            radio_btn = QRadioButton(option)
            radio_btn.setStyleSheet(Styles.radio_btn())
            if i == default_index:
                radio_btn.setChecked(True)
            buttons.append(radio_btn)
            group_layout.addWidget(radio_btn)

        self.main_layout.addWidget(group_box)
        return buttons

    def add_slider(self, label_text, min_val, max_val, default, suffix=""):
        slider_layout = QVBoxLayout()
        slider_layout.setSpacing(3)

        label = QLabel(f"{label_text}:")
        label.setStyleSheet(Styles.LABEL_SECONDARY)
        slider_layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.setStyleSheet(Styles.slider())

        value_label = QLabel(f"{default}{suffix}")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(Styles.slider_value_label())

        slider.valueChanged.connect(lambda val: value_label.setText(f"{val}{suffix}"))

        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)

        self.main_layout.addLayout(slider_layout)
        return slider

    def add_file_browser(self, label_text, file_filter="All Files (*)", default_path=""):
        file_layout = QHBoxLayout()
        file_layout.setSpacing(4)

        label = QLabel(f"{label_text}:")
        label.setStyleSheet(Styles.LABEL_SECTION)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        file_layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setText(default_path)
        line_edit.setStyleSheet(Styles.small_line_edit())

        browse_btn = QPushButton("...")
        browse_btn.setStyleSheet(Styles.browse_btn())

        def browse_file():
            start_dir = ""
            if "图片" in file_filter or "png" in file_filter.lower() or "jpg" in file_filter.lower():
                image_dir = ensure_image_dir()
                if os.path.exists(image_dir):
                    start_dir = image_dir
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", start_dir, file_filter)
            if file_path:
                line_edit.setText(file_path)

        browse_btn.clicked.connect(browse_file)

        file_layout.addWidget(line_edit, 1)
        file_layout.addWidget(browse_btn)

        self.main_layout.addLayout(file_layout)
        return line_edit

    def add_delay_section(self, default_before=None, default_after=None):
        if default_before is None:
            default_before = {"type": "fixed", "value": 0.5}
        if default_after is None:
            default_after = {"type": "fixed", "value": 0.5}

        self.wait_before_widgets = self._make_wait_row("步骤前等待", default_before)
        self.wait_after_widgets = self._make_wait_row("步骤后等待", default_after)

    def _make_wait_row(self, label_text, default_config):
        group = QGroupBox(label_text)
        group.setStyleSheet(Styles.delay_group())
        group.setFixedHeight(80)
        layout = QHBoxLayout(group)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(6)

        type_label = QLabel("类型:")
        type_label.setStyleSheet(Styles.delay_label())
        layout.addWidget(type_label)

        type_combo = QComboBox()
        type_combo.addItems(["固定", "随机"])
        type_combo.setStyleSheet(Styles.small_combo_box())
        layout.addWidget(type_combo)

        fixed_spin = QDoubleSpinBox()
        fixed_spin.setRange(0.0, 3600.0)
        fixed_spin.setDecimals(1)
        fixed_spin.setSingleStep(0.1)
        fixed_spin.setSuffix(" 秒")
        fixed_spin.setStyleSheet(Styles.delay_spin())
        layout.addWidget(fixed_spin)

        min_spin = QDoubleSpinBox()
        min_spin.setRange(0.0, 3600.0)
        min_spin.setDecimals(1)
        min_spin.setSingleStep(0.1)
        min_spin.setSuffix(" 秒")
        min_spin.setStyleSheet(Styles.delay_spin())
        min_spin.setVisible(False)
        layout.addWidget(min_spin)

        max_label = QLabel(" ~ ")
        max_label.setStyleSheet(Styles.delay_label())
        max_label.setVisible(False)
        layout.addWidget(max_label)

        max_spin = QDoubleSpinBox()
        max_spin.setRange(0.0, 3600.0)
        max_spin.setDecimals(1)
        max_spin.setSingleStep(0.1)
        max_spin.setSuffix(" 秒")
        max_spin.setStyleSheet(Styles.delay_spin())
        max_spin.setVisible(False)
        layout.addWidget(max_spin)

        layout.addStretch()

        def on_type_changed(idx):
            is_fixed = (idx == 0)
            fixed_spin.setVisible(is_fixed)
            min_spin.setVisible(not is_fixed)
            max_label.setVisible(not is_fixed)
            max_spin.setVisible(not is_fixed)

        type_combo.currentIndexChanged.connect(on_type_changed)

        if default_config.get("type") == "random":
            type_combo.setCurrentIndex(1)
            min_spin.setValue(default_config.get("min", 1.0))
            max_spin.setValue(default_config.get("max", 3.0))
        else:
            type_combo.setCurrentIndex(0)
            fixed_spin.setValue(default_config.get("value", 0.5))

        self.main_layout.addWidget(group)
        return (type_combo, fixed_spin, min_spin, max_spin)

    def _get_wait_from_widgets(self, widgets):
        type_combo, fixed_spin, min_spin, max_spin = widgets
        if type_combo.currentIndex() == 0:
            return {"type": "fixed", "value": round(fixed_spin.value(), 1)}
        else:
            return {"type": "random", "min": round(min_spin.value(), 1), "max": round(max_spin.value(), 1)}

    def _set_wait_to_widgets(self, widgets, config):
        type_combo, fixed_spin, min_spin, max_spin = widgets
        if config.get("type") == "random":
            type_combo.setCurrentIndex(1)
            min_spin.setValue(config.get("min", 1.0))
            max_spin.setValue(config.get("max", 3.0))
        else:
            type_combo.setCurrentIndex(0)
            fixed_spin.setValue(config.get("value", 0.5))

    def get_wait_before(self):
        return self._get_wait_from_widgets(self.wait_before_widgets)

    def get_wait_after(self):
        return self._get_wait_from_widgets(self.wait_after_widgets)

    def set_wait_before(self, config):
        self._set_wait_to_widgets(self.wait_before_widgets, config)

    def set_wait_after(self, config):
        self._set_wait_to_widgets(self.wait_after_widgets, config)

    def add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(Styles.separator())
        self.main_layout.addWidget(separator)
        return separator

    def add_buttons(self, confirm_callback, cancel_callback):
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        btn_layout.addStretch()

        confirm_btn = QPushButton("确定")
        confirm_btn.setStyleSheet(Styles.confirm_btn())

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet(Styles.cancel_btn())

        confirm_btn.clicked.connect(confirm_callback)
        cancel_btn.clicked.connect(cancel_callback)

        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)

        self.main_layout.addLayout(btn_layout)
        return confirm_btn, cancel_btn


class CoordOverlay(QDialog):
    """坐标拾取覆盖层：全屏半透明覆盖，点击获取坐标"""
    coordinate_selected = Signal(int, int)

    def __init__(self, windows_to_restore=None):
        super().__init__()
        self.windows_to_restore = windows_to_restore or []
        self._init_ui()

    def _init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def showEvent(self, event):
        screens = QApplication.screens()
        min_x = min(s.geometry().left() for s in screens)
        min_y = min(s.geometry().top() for s in screens)
        max_x = max(s.geometry().right() for s in screens)
        max_y = max(s.geometry().bottom() for s in screens)
        self.setGeometry(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
        QApplication.setOverrideCursor(Qt.CrossCursor)
        super().showEvent(event)

    def hideEvent(self, event):
        QApplication.restoreOverrideCursor()
        super().hideEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 50))
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Microsoft YaHei", 13))
        painter.drawText(self.rect(), Qt.AlignCenter, "点击鼠标左键确认拾取 | �?ESC 取消")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x, y = pyautogui.position()
            self.coordinate_selected.emit(x, y)
            self._cleanup()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._cleanup()

    def _cleanup(self):
        self.reject()
        app = QApplication.instance()
        app.processEvents()
        for w in self.windows_to_restore:
            w.showNormal()


class ScreenshotOverlay(QDialog):
    """截图覆盖层：全屏覆盖，框选区域截图"""
    screenshot_taken = Signal(str)

    def __init__(self, windows_to_restore=None):
        super().__init__()
        self.windows_to_restore = windows_to_restore or []
        self.start_draw_pos = None
        self.end_draw_pos = None
        self.start_screen_pos = None
        self.is_dragging = False
        self._init_ui()

    def _init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def showEvent(self, event):
        screens = QApplication.screens()
        min_x = min(s.geometry().left() for s in screens)
        min_y = min(s.geometry().top() for s in screens)
        max_x = max(s.geometry().right() for s in screens)
        max_y = max(s.geometry().bottom() for s in screens)
        self.setGeometry(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
        QApplication.setOverrideCursor(Qt.CrossCursor)
        super().showEvent(event)

    def hideEvent(self, event):
        QApplication.restoreOverrideCursor()
        super().hideEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 50))

        if self.is_dragging and self.start_draw_pos and self.end_draw_pos:
            x1 = min(self.start_draw_pos.x(), self.end_draw_pos.x())
            y1 = min(self.start_draw_pos.y(), self.end_draw_pos.y())
            x2 = max(self.start_draw_pos.x(), self.end_draw_pos.x())
            y2 = max(self.start_draw_pos.y(), self.end_draw_pos.y())
            draw_rect = QRect(x1, y1, x2 - x1, y2 - y1)
            
            painter.fillRect(draw_rect, QColor(255, 255, 255, 50))
            
            pen = QPen(QColor(0, 150, 255), 2)
            painter.setPen(pen)
            painter.drawRect(draw_rect)

            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Microsoft YaHei", 12))
            width = draw_rect.width()
            height = draw_rect.height()
            painter.drawText(draw_rect.topRight() + QPoint(5, 15), f"{width} x {height}")

        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Microsoft YaHei", 13))
        painter.drawText(self.rect(), Qt.AlignCenter, "拖拽选择区域 | 松开鼠标完成截图 | �?ESC 取消")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_draw_pos = event.pos()
            self.start_screen_pos = self._get_cursor_pos()
            self.is_dragging = True

    def mouseMoveEvent(self, event):
        if self.is_dragging and self.start_draw_pos:
            self.end_draw_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_dragging:
            self.is_dragging = False
            if self.start_screen_pos:
                end_screen_pos = self._get_cursor_pos()
                x1 = min(self.start_screen_pos.x(), end_screen_pos.x())
                y1 = min(self.start_screen_pos.y(), end_screen_pos.y())
                x2 = max(self.start_screen_pos.x(), end_screen_pos.x())
                y2 = max(self.start_screen_pos.y(), end_screen_pos.y())
                
                if (x2 - x1) > 10 and (y2 - y1) > 10:
                    self._take_screenshot(QRect(x1, y1, x2 - x1, y2 - y1))
                else:
                    self.start_draw_pos = None
                    self.end_draw_pos = None
                    self.start_screen_pos = None
                    self.update()
            self.start_draw_pos = None
            self.end_draw_pos = None
            self.start_screen_pos = None

    def _get_cursor_pos(self):
        try:
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            
            pt = POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            return QPoint(pt.x, pt.y)
        except:
            return QPoint(0, 0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._cleanup()

    def _take_screenshot(self, rect):
        screenshot = ImageGrab.grab(bbox=(rect.left(), rect.top(), rect.right(), rect.bottom()))
        
        save_dir = ensure_image_dir()
        
        timestamp = os.path.getmtime(__file__)
        import time
        timestamp = int(time.time())
        filename = f"screenshot_{timestamp}.png"
        save_path = os.path.join(save_dir, filename)
        
        screenshot.save(save_path)
        
        self.screenshot_taken.emit(save_path)
        self._cleanup()

    def _cleanup(self):
        self.reject()
        app = QApplication.instance()
        app.processEvents()
        for w in self.windows_to_restore:
            w.showNormal()


class RegionOverlay(QDialog):
    """区域选择覆盖层：全屏覆盖，框选区域获取坐标范围"""
    region_selected = Signal(int, int, int, int)

    def __init__(self, windows_to_restore=None):
        super().__init__()
        self.windows_to_restore = windows_to_restore or []
        self.start_draw_pos = None
        self.end_draw_pos = None
        self.start_screen_pos = None
        self.is_dragging = False
        self._init_ui()

    def _init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def showEvent(self, event):
        screens = QApplication.screens()
        min_x = min(s.geometry().left() for s in screens)
        min_y = min(s.geometry().top() for s in screens)
        max_x = max(s.geometry().right() for s in screens)
        max_y = max(s.geometry().bottom() for s in screens)
        self.setGeometry(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
        QApplication.setOverrideCursor(Qt.CrossCursor)
        super().showEvent(event)

    def hideEvent(self, event):
        QApplication.restoreOverrideCursor()
        super().hideEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 50))

        if self.is_dragging and self.start_draw_pos and self.end_draw_pos:
            x1 = min(self.start_draw_pos.x(), self.end_draw_pos.x())
            y1 = min(self.start_draw_pos.y(), self.end_draw_pos.y())
            x2 = max(self.start_draw_pos.x(), self.end_draw_pos.x())
            y2 = max(self.start_draw_pos.y(), self.end_draw_pos.y())
            draw_rect = QRect(x1, y1, x2 - x1, y2 - y1)
            
            painter.fillRect(draw_rect, QColor(255, 255, 255, 50))
            
            pen = QPen(QColor(0, 150, 255), 2)
            painter.setPen(pen)
            painter.drawRect(draw_rect)

            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Microsoft YaHei", 12))
            width = draw_rect.width()
            height = draw_rect.height()
            painter.drawText(draw_rect.topRight() + QPoint(5, 15), f"{width} x {height}")

        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Microsoft YaHei", 13))
        painter.drawText(self.rect(), Qt.AlignCenter, "拖拽选择区域 | 松开鼠标完成 | �?ESC 取消")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_draw_pos = event.pos()
            self.start_screen_pos = self._get_cursor_pos()
            self.is_dragging = True

    def mouseMoveEvent(self, event):
        if self.is_dragging and self.start_draw_pos:
            self.end_draw_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_dragging:
            self.is_dragging = False
            if self.start_screen_pos:
                end_screen_pos = self._get_cursor_pos()
                x1 = min(self.start_screen_pos.x(), end_screen_pos.x())
                y1 = min(self.start_screen_pos.y(), end_screen_pos.y())
                x2 = max(self.start_screen_pos.x(), end_screen_pos.x())
                y2 = max(self.start_screen_pos.y(), end_screen_pos.y())
                
                if (x2 - x1) > 10 and (y2 - y1) > 10:
                    self.region_selected.emit(x1, y1, x2 - x1, y2 - y1)
                    self._cleanup()
                else:
                    self.start_draw_pos = None
                    self.end_draw_pos = None
                    self.start_screen_pos = None
                    self.update()
            self.start_draw_pos = None
            self.end_draw_pos = None
            self.start_screen_pos = None

    def _get_cursor_pos(self):
        try:
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            
            pt = POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            return QPoint(pt.x, pt.y)
        except:
            return QPoint(0, 0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._cleanup()

    def _cleanup(self):
        self.reject()
        app = QApplication.instance()
        app.processEvents()
        for w in self.windows_to_restore:
            w.showNormal()


from .mouse_panel import (MouseClickPanel, MouseMovePanel, 
                          MouseDragPanel, MouseScrollPanel)
from .keyboard_panel import (KeyboardTypePanel, KeyboardPressPanel, 
                            KeyboardHotkeyPanel)
from .image_panel import (ImageFindPanel, ImageClickPanel, ImageExistsPanel)
from .window_panel import (WindowFindPanel, WindowActivatePanel, 
                          WindowClosePanel, WindowPositionPanel)
from .excel_panel import ExcelReadPanel
from .control_panel import (WaitPanel, IfElsePanel, LoopPanel, 
                           LogPanel, LabelPanel, GotoPanel)
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