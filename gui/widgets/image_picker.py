from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QLineEdit, QFileDialog, QMessageBox,
                               QSizePolicy, QScrollArea)
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QCursor
from PySide6.QtCore import Qt, Signal, QRect, QPoint
import os
import sys
from utils.resource_path import ensure_image_dir

try:
    import mss
    HAS_MSS = True
except ImportError:
    HAS_MSS = False

try:
    from PIL import Image as PILImage
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class ImagePicker(QWidget):
    image_selected = Signal(str)
    image_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._image_path = ""
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("图片路径")
        self.path_edit.setReadOnly(True)
        layout.addWidget(self.path_edit)

        btn_layout = QHBoxLayout()
        
        self.browse_btn = QPushButton("浏览图片")
        self.browse_btn.clicked.connect(self._browse_image)
        
        self.capture_btn = QPushButton("截取屏幕")
        self.capture_btn.clicked.connect(self._capture_screen)
        
        btn_layout.addWidget(self.browse_btn)
        btn_layout.addWidget(self.capture_btn)
        layout.addLayout(btn_layout)

        preview_group = QWidget()
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_label = QLabel("图片预览")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ddd;
                border-radius: 6px;
                background-color: #fafafa;
                min-height: 150px;
                color: #999;
                font-size: 14px;
            }
        """)
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        preview_layout.addWidget(self.preview_label)
        layout.addWidget(preview_group)

        info_layout = QHBoxLayout()
        self.size_label = QLabel("")
        self.size_label.setStyleSheet("color: #666; font-size: 12px;")
        info_layout.addWidget(self.size_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)

    def _browse_image(self):
        image_dir = ensure_image_dir()
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", image_dir, 
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*)"
        )
        if file_path:
            self.set_image_path(file_path)

    def _capture_screen(self):
        if not HAS_MSS and not HAS_PIL:
            QMessageBox.warning(self, "截图失败", 
                "需要安装 mss 或 Pillow 库来支持截图功能\n请运行: pip install mss Pillow")
            return

        try:
            with mss.mss() as sct:
                monitor = sct.monitors[0]
                screenshot = sct.grab(monitor)
                
                image_dir = ensure_image_dir()
                os.makedirs(image_dir, exist_ok=True)
                
                import time
                timestamp = int(time.time())
                screenshot_path = os.path.join(image_dir, f"screenshot_{timestamp}.png")
                
                img = PILImage.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                img.save(screenshot_path, "PNG")
                
                self.set_image_path(screenshot_path)
                
        except Exception as e:
            QMessageBox.warning(self, "截图失败", f"无法截取屏幕: {str(e)}")

    def set_image_path(self, path: str):
        if os.path.exists(path):
            self._image_path = path
            self.path_edit.setText(path)
            self._update_preview(path)
            self.image_selected.emit(path)
            self.image_changed.emit(path)
        else:
            QMessageBox.warning(self, "文件不存在", f"图片文件不存在: {path}")

    def get_image_path(self) -> str:
        return self._image_path

    def _update_preview(self, path: str):
        try:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                self.preview_label.setText("无法加载图片")
                self.size_label.setText("")
                return

            original_size = pixmap.size()
            
            max_width = self.preview_label.width() - 20
            max_height = self.preview_label.height() - 20
            
            scaled_pixmap = pixmap.scaled(
                max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            self.preview_label.setPixmap(scaled_pixmap)
            
            self.size_label.setText(
                f"尺寸: {original_size.width()} x {original_size.height()} "
                f"| 文件: {os.path.getsize(path) / 1024:.1f} KB"
            )
            
        except Exception as e:
            self.preview_label.setText(f"预览失败: {str(e)}")
            self.size_label.setText("")

    def clear(self):
        self._image_path = ""
        self.path_edit.clear()
        self.preview_label.setText("图片预览")
        self.size_label.setText("")

    def set_enabled(self, enabled: bool):
        self.browse_btn.setEnabled(enabled)
        self.capture_btn.setEnabled(enabled)
        self.path_edit.setEnabled(enabled)


class ImagePreviewDialog(QWidget):
    def __init__(self, image_path: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图片预览")
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        scroll_area.setWidget(self.image_label)
        layout.addWidget(scroll_area)
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
            self.resize(pixmap.width() + 40, pixmap.height() + 80)
        else:
            self.image_label.setText("无法加载图片")
