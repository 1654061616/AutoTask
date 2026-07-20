"""主题管理器 — 加载 QSS、切换主题、热更新"""

import os
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon
from utils.resource_path import get_resource_path


class ThemeManager:
    """主题管理器单例：加载 QSS、切换主题、热更新"""
    _instance = None
    _current_theme = "light"
    _watched_widgets: list[QWidget] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def instance(cls) -> "ThemeManager":
        return cls()

    @property
    def current_theme(self) -> str:
        return self._current_theme

    def _theme_path(self, theme: str) -> str:
        return get_resource_path(f"themes/{theme}.qss")

    def load_qss(self, theme: str = "light") -> str:
        path = self._theme_path(theme)
        if not os.path.exists(path):
            print(f"[ThemeManager] 主题文件不存在: {path}")
            return ""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def apply_to(self, widget: QWidget, theme: str = "light"):
        qss = self.load_qss(theme)
        if qss:
            widget.setStyleSheet(qss)
        self._current_theme = theme

    def watch(self, widget: QWidget):
        if widget not in self._watched_widgets:
            self._watched_widgets.append(widget)

    def unwatch(self, widget: QWidget):
        if widget in self._watched_widgets:
            self._watched_widgets.remove(widget)

    def switch_theme(self, theme: str):
        qss = self.load_qss(theme)
        if not qss:
            return
        self._current_theme = theme
        for widget in self._watched_widgets:
            try:
                widget.setStyleSheet(qss)
            except Exception as e:
                print(f"[ThemeManager] 切换主题失败: {e}")

    @staticmethod
    def load_icon(svg_filename, fallback_theme_name):
        """加载 SVG 图标，失败时回退到系统主题图标"""
        icon_path = get_resource_path(f"icons/{svg_filename}")
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon.fromTheme(fallback_theme_name)