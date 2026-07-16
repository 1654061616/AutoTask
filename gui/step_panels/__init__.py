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
    config_changed = Signal(dict)

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(6, 6, 6, 6)
        self.main_layout.setSpacing(6)
        self.setLayout(self.main_layout)
        self._config = {}
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-size: 13px;
            }
        """)

    def _start_capture_coordinate(self, callback):
        app = QApplication.instance()
        
        windows_to_minimize = []
        for widget in app.topLevelWidgets():
            if hasattr(widget, 'windowTitle'):
                title = widget.windowTitle()
                if "AutoFlow" in title or "节点编辑器" in title:
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
                if "AutoFlow" in title or "节点编辑器" in title:
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
                if "AutoFlow" in title or "节点编辑器" in title:
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
        label.setStyleSheet("""
            QLabel {
                color: #27ae60;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 0 4px 0;
                border-bottom: 1px solid #e0e0e0;
                margin-bottom: 4px;
            }
        """)
        self.main_layout.addWidget(label)
        return label

    def add_line(self, label_text, widget, stretch=0):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(6)

        label = QLabel(f"{label_text}:")
        label.setStyleSheet("""
            QLabel {
                color: #555;
                font-size: 13px;
                min-width: 70px;
                max-width: 90px;
            }
        """)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        row_layout.addWidget(label)

        widget.setStyleSheet("""
            QWidget {
                font-size: 13px;
            }
        """)
        row_layout.addWidget(widget, 1)

        self.main_layout.addLayout(row_layout)
        return widget

    def add_spinbox(self, label_text, min_val, max_val, default, step=1):
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default)
        spinbox.setSingleStep(step)
        spinbox.setStyleSheet("""
            QSpinBox {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 13px;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #3498db;
                outline: none;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
            }
        """)
        return self.add_line(label_text, spinbox)

    def add_double_spinbox(self, label_text, min_val, max_val, default, decimals=2):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default)
        spinbox.setDecimals(decimals)
        spinbox.setStyleSheet("""
            QDoubleSpinBox {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 13px;
                min-width: 80px;
            }
            QDoubleSpinBox:focus {
                border-color: #3498db;
                outline: none;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                width: 20px;
            }
        """)
        return self.add_line(label_text, spinbox)

    def add_lineedit(self, label_text, default="", placeholder=""):
        lineedit = QLineEdit()
        lineedit.setText(default)
        lineedit.setPlaceholderText(placeholder)
        lineedit.setStyleSheet("""
            QLineEdit {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
        """)
        return self.add_line(label_text, lineedit)

    def add_textedit(self, label_text, default="", placeholder=""):
        textedit = QTextEdit()
        textedit.setPlaceholderText(placeholder)
        if default:
            textedit.setText(default)
        textedit.setStyleSheet("""
            QTextEdit {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 13px;
                min-height: 60px;
            }
            QTextEdit:focus {
                border-color: #3498db;
                outline: none;
            }
        """)
        return self.add_line(label_text, textedit)

    def add_combobox(self, label_text, items, default_index=0):
        combobox = QComboBox()
        combobox.addItems(items)
        if 0 <= default_index < len(items):
            combobox.setCurrentIndex(default_index)
        combobox.setStyleSheet("""
            QComboBox {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 13px;
                min-width: 100px;
                color: #333333;
                background-color: #ffffff;
            }
            QComboBox:focus {
                border-color: #3498db;
                outline: none;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #d0d0d0;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
        """)
        
        list_view = QListView()
        list_view.setStyleSheet("""
            QListView {
                color: #333333;
                background-color: #ffffff;
                font-size: 13px;
            }
            QListView::item {
                padding: 6px 10px;
                height: 28px;
            }
            QListView::item:selected {
                color: #ffffff;
                background-color: #3498db;
            }
            QListView::item:hover {
                color: #ffffff;
                background-color: #3498db;
            }
        """)
        combobox.setView(list_view)
        
        return self.add_line(label_text, combobox)

    def add_checkbox(self, text, checked=False):
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        self.main_layout.addWidget(checkbox)
        return checkbox

    def add_radio_group(self, label_text, options, default_index=0):
        group_box = QGroupBox(label_text)
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #555;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 6px;
                padding-top: 8px;
                padding-left: 8px;
                padding-right: 8px;
                padding-bottom: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
                font-size: 12px;
                color: #666;
            }
        """)
        group_layout = QVBoxLayout(group_box)
        group_layout.setSpacing(4)
        group_layout.setContentsMargins(4, 4, 4, 4)

        buttons = []
        for i, option in enumerate(options):
            radio_btn = QRadioButton(option)
            radio_btn.setStyleSheet("""
                QRadioButton {
                    font-size: 12px;
                    color: #555;
                }
                QRadioButton::indicator {
                    width: 14px;
                    height: 14px;
                    border-radius: 7px;
                    border: 2px solid #d0d0d0;
                }
                QRadioButton::indicator:checked {
                    border-color: #3498db;
                    background-color: #3498db;
                }
            """)
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
        label.setStyleSheet("color: #555; font-size: 13px;")
        slider_layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #e0e0e0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                width: 14px;
                height: 14px;
                background: #3498db;
                border-radius: 7px;
                margin: -5px 0;
                border: 2px solid white;
            }
        """)

        value_label = QLabel(f"{default}{suffix}")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("color: #27ae60; font-weight: bold; font-size: 12px;")

        slider.valueChanged.connect(lambda val: value_label.setText(f"{val}{suffix}"))

        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)

        self.main_layout.addLayout(slider_layout)
        return slider

    def add_file_browser(self, label_text, file_filter="All Files (*)", default_path=""):
        file_layout = QHBoxLayout()
        file_layout.setSpacing(4)

        label = QLabel(f"{label_text}:")
        label.setStyleSheet("""
            QLabel {
                color: #555;
                font-size: 13px;
                min-width: 70px;
                max-width: 90px;
            }
        """)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        file_layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setText(default_path)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
        """)

        browse_btn = QPushButton("...")
        browse_btn.setStyleSheet("""
            QPushButton {
                padding: 4px 8px;
                border-radius: 3px;
                border: 1px solid #d0d0d0;
                background-color: #ffffff;
                font-size: 12px;
                min-width: 28px;
                max-width: 28px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

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

    def add_delay_section(self, default_delay=0):
        delay_group = QGroupBox("延时设置")
        delay_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #555;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 6px;
                padding-top: 8px;
                padding-left: 8px;
                padding-right: 8px;
                padding-bottom: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
                font-size: 12px;
                color: #666;
            }
        """)
        delay_layout = QFormLayout(delay_group)
        delay_layout.setSpacing(4)

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 3600)
        self.delay_spin.setValue(default_delay)
        self.delay_spin.setStyleSheet("""
            QSpinBox {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 13px;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #3498db;
                outline: none;
            }
        """)

        delay_label = QLabel("执行后延时(秒):")
        delay_label.setStyleSheet("font-size: 12px; color: #666;")
        delay_layout.addRow(delay_label, self.delay_spin)

        self.main_layout.addWidget(delay_group)
        return self.delay_spin

    def add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #e0e0e0;")
        self.main_layout.addWidget(separator)
        return separator

    def add_buttons(self, confirm_callback, cancel_callback):
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        btn_layout.addStretch()

        confirm_btn = QPushButton("确定")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 5px 16px;
                border-radius: 3px;
                border: none;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 5px 16px;
                border-radius: 3px;
                border: none;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        confirm_btn.clicked.connect(confirm_callback)
        cancel_btn.clicked.connect(cancel_callback)

        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)

        self.main_layout.addLayout(btn_layout)
        return confirm_btn, cancel_btn


class CoordOverlay(QDialog):
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
        painter.drawText(self.rect(), Qt.AlignCenter, "点击鼠标左键确认拾取 | 按 ESC 取消")

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
        painter.drawText(self.rect(), Qt.AlignCenter, "拖拽选择区域 | 松开鼠标完成截图 | 按 ESC 取消")

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
        painter.drawText(self.rect(), Qt.AlignCenter, "拖拽选择区域 | 松开鼠标完成 | 按 ESC 取消")

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
