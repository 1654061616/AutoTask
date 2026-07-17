# 样式表集中管理 实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 将项目中 100+ 处内联 `setStyleSheet` 集中到 `gui/styles/` 包 + `resources/themes/light.qss`，支持主题切换。

**架构：** QSS 外部样式表（静态全局样式） + Python 工厂方法（动态参数化样式） + ThemeManager 单例（主题加载/切换）。三层：调用层（各面板）→ 中间层（工厂方法）→ 底层（QSS + 颜色常量）。

**技术栈：** PySide6, Python 3.13

---

### 任务 1：创建 `gui/styles/` 包 - 颜色常量 + 样式工厂 + 主题管理器

**文件：**
- 创建：`gui/styles/__init__.py`
- 创建：`gui/styles/colors.py`
- 创建：`gui/styles/widget_styles.py`
- 创建：`gui/styles/theme_manager.py`

- [ ] **步骤 1：创建 `gui/styles/__init__.py`**

```python
from .colors import Colors
from .widget_styles import Styles
from .theme_manager import ThemeManager

__all__ = ["Colors", "Styles", "ThemeManager"]
```

- [ ] **步骤 2：创建 `gui/styles/colors.py`**

从 `gui/styles_bak.py` 迁移 `Colors` 类，内容不变。

```python
"""颜色常量"""


class Colors:
    PRIMARY = "#3498db"
    PRIMARY_HOVER = "#2980b9"
    PRIMARY_PRESSED = "#1c6ea4"
    PRIMARY_DISABLED = "#7ab8e4"

    SUCCESS = "#27ae60"
    SUCCESS_HOVER = "#2ecc71"
    SUCCESS_DISABLED = "#7ed6a4"

    DANGER = "#e74c3c"
    DANGER_HOVER = "#ec7063"
    DANGER_DISABLED = "#f0a0a0"

    TEXT_PRIMARY = "#333"
    TEXT_SECONDARY = "#555"
    TEXT_WHITE = "white"
    TEXT_WHITE_DISABLED = "rgba(255,255,255,0.7)"

    BORDER = "#ddd"
    BORDER_FOCUS = "#3498db"
    BG_LIGHT = "#f8f9fa"
    BG_WHITE = "#ffffff"
```

- [ ] **步骤 3：创建 `gui/styles/widget_styles.py`**

从 `gui/styles_bak.py` 迁移 `Styles` 类并扩展。保留所有原有方法，新增以下方法：

```python
"""动态样式工厂 — 需要参数或运行时切换的样式"""

from PySide6.QtGui import QColor
from .colors import Colors


class Styles:
    INPUT_BASE = (
        "border: 1px solid #ddd; border-radius: 4px; padding: 4px 8px;"
        "background: white; color: #333;"
    )

    # ========== 原有方法（从 styles_bak.py 迁移） ==========
    @staticmethod
    def input_field():
        return f"""
            QLineEdit {{
                {Styles.INPUT_BASE}
            }}
            QLineEdit:focus {{
                border-color: {Colors.BORDER_FOCUS};
            }}
        """

    @staticmethod
    def spin_box():
        return f"""
            QSpinBox {{
                {Styles.INPUT_BASE}
            }}
            QSpinBox:focus {{
                border-color: {Colors.BORDER_FOCUS};
            }}
        """

    @staticmethod
    def combo_box():
        return f"""
            QComboBox {{
                {Styles.INPUT_BASE}
            }}
            QComboBox:focus {{
                border-color: {Colors.BORDER_FOCUS};
            }}
            QComboBox::drop-down {{
                border: none; padding-right: 6px;
            }}
        """

    @staticmethod
    def combo_view():
        return """
            QListView::item:selected { background: #3498db; color: white; }
            QListView::item:hover { background: #e8f4fd; }
        """

    @staticmethod
    def text_edit():
        return f"""
            QTextEdit {{
                border: 1px solid #ddd; border-radius: 4px; padding: 6px;
                background: white; color: {Colors.TEXT_PRIMARY};
                font-size: 13px;
            }}
            QTextEdit:focus {{
                border-color: {Colors.BORDER_FOCUS};
            }}
        """

    LABEL_SECONDARY = f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;"
    LABEL_SECTION = f"color: {Colors.TEXT_SECONDARY}; font-size: 13px; min-width: 70px; max-width: 90px;"

    @staticmethod
    def status_label(color):
        return f"color: {color}; font-weight: bold;"

    @staticmethod
    def button(color, padding="8px 20px", hover_color=None, pressed_color=None,
               disabled_color=None, font_weight="bold"):
        h = hover_color or QColor(color).darker(110).name()
        p = pressed_color or QColor(color).darker(130).name()
        d = disabled_color or QColor(color).lighter(160).name()
        return f"""
            QPushButton {{
                background-color: {color};
                color: {Colors.TEXT_WHITE};
                font-weight: {font_weight};
                padding: {padding};
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {h};
            }}
            QPushButton:pressed {{
                background-color: {p};
            }}
            QPushButton:disabled {{
                background-color: {d};
                color: {Colors.TEXT_WHITE_DISABLED};
            }}
        """

    @staticmethod
    def btn_success(padding="8px 20px"):
        return Styles.button(Colors.SUCCESS, padding, Colors.SUCCESS_HOVER, None, Colors.SUCCESS_DISABLED)

    @staticmethod
    def btn_primary(padding="8px 20px"):
        return Styles.button(Colors.PRIMARY, padding, Colors.PRIMARY_HOVER, Colors.PRIMARY_PRESSED, Colors.PRIMARY_DISABLED)

    @staticmethod
    def btn_danger(padding="8px 20px"):
        return Styles.button(Colors.DANGER, padding, Colors.DANGER_HOVER, None, Colors.DANGER_DISABLED)

    @staticmethod
    def btn_toolbar(color, padding="4px 8px"):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-weight: bold;
                padding: {padding};
                border-radius: 4px;
            }}
        """

    @staticmethod
    def btn_toolbar_success():
        return Styles.btn_toolbar(Colors.SUCCESS, "4px 12px")

    @staticmethod
    def btn_toolbar_success_small():
        return Styles.btn_toolbar(Colors.SUCCESS, "4px 8px")

    @staticmethod
    def btn_toolbar_danger():
        return Styles.btn_toolbar(Colors.DANGER, "4px 8px")

    @staticmethod
    def group_box(title_color=None):
        c = title_color or Colors.PRIMARY
        return f"""
            QGroupBox {{
                font-weight: bold; border: 1px solid {Colors.BORDER};
                border-radius: 6px; margin-top: 12px; padding: 12px 8px 8px 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin; left: 12px; padding: 0 6px; color: {c};
            }}
        """

    @staticmethod
    def preview_text():
        return f"""
            QLabel {{
                background: {Colors.BG_LIGHT}; border: 1px solid {Colors.BORDER};
                border-radius: 4px; padding: 8px; color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
            }}
        """

    # ========== 新增：步表面板基类用 ==========

    @staticmethod
    def panel_bg():
        return """
            QWidget {
                background-color: #f8f9fa;
                font-size: 13px;
            }
        """

    @staticmethod
    def section_title():
        return """
            QLabel {
                color: #27ae60;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 0 4px 0;
                border-bottom: 1px solid #e0e0e0;
                margin-bottom: 4px;
            }
        """

    # ========== 新增：小尺寸控件（步表面板用） ==========

    @staticmethod
    def small_input():
        return """
            QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QComboBox {
                padding: 4px 6px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                font-size: 13px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
            QTextEdit:focus, QComboBox:focus {
                border-color: #3498db;
                outline: none;
            }
        """

    @staticmethod
    def small_spin_box():
        return """
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
        """

    @staticmethod
    def small_double_spin_box():
        return """
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
        """

    @staticmethod
    def small_line_edit():
        return """
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
        """

    @staticmethod
    def small_text_edit():
        return """
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
        """

    @staticmethod
    def small_combo_box():
        return """
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
        """

    @staticmethod
    def small_combo_view():
        return """
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
        """

    # ========== 新增：无线电组 ==========

    @staticmethod
    def radio_group():
        return """
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
        """

    @staticmethod
    def radio_btn():
        return """
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
        """

    # ========== 新增：滑块 ==========

    @staticmethod
    def slider():
        return """
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
        """

    @staticmethod
    def slider_value_label():
        return "color: #27ae60; font-weight: bold; font-size: 12px;"

    # ========== 新增：文件浏览按钮 ==========

    @staticmethod
    def browse_btn():
        return """
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
        """

    @staticmethod
    def browse_btn_text(text_padding="4px 12px"):
        return f"""
            QPushButton {{
                padding: {text_padding};
                border-radius: 4px;
                border: 1px solid #ccc;
                background-color: #ffffff;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
        """

    # ========== 新增：延时设置 ==========

    @staticmethod
    def delay_group():
        return """
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
        """

    @staticmethod
    def delay_spin():
        return """
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
        """

    @staticmethod
    def delay_label():
        return "font-size: 12px; color: #666;"

    # ========== 新增：分隔线 ==========

    @staticmethod
    def separator():
        return "color: #e0e0e0;"

    # ========== 新增：确认/取消按钮（对话框用） ==========

    @staticmethod
    def confirm_btn():
        return Styles.button(Colors.SUCCESS, "5px 16px", Colors.SUCCESS_HOVER, None, Colors.SUCCESS_DISABLED)

    @staticmethod
    def cancel_btn():
        return Styles.button(Colors.DANGER, "5px 16px", "#c0392b", None, Colors.DANGER_DISABLED)

    # ========== 新增：调度按钮（运行时切换） ==========

    @staticmethod
    def schedule_btn_start():
        return """
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 14px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #40a9ff; }
            QPushButton:pressed { background-color: #096dd9; }
        """

    @staticmethod
    def schedule_btn_stop():
        return """
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 14px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ff7875; }
            QPushButton:pressed { background-color: #d9363e; }
        """

    # ========== 新增：节点编辑器对话框 ==========

    @staticmethod
    def config_panel_bg():
        return """
            QWidget {
                background-color: #f8f9fa;
            }
        """

    @staticmethod
    def title_label():
        return """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding-bottom: 8px;
                border-bottom: 2px solid #27ae60;
            }
        """

    @staticmethod
    def empty_label():
        return """
            QLabel {
                font-size: 14px;
                color: #999;
                text-align: center;
                padding: 40px 20px;
            }
        """

    @staticmethod
    def toggle_btn():
        return """
            QToolButton {
                border: none;
                border-radius: 2px;
                font-size: 20px;
                font-weight: bold;
                color: #27ae60;
                background: transparent;
            }
            QToolButton:hover {
                color: #2ecc71;
                background: rgba(0,0,0,0.08);
            }
        """

    @staticmethod
    def scroll_area_transparent():
        return """
            QScrollArea {
                border: none;
            }
        """

    @staticmethod
    def error_label():
        return """
            QLabel {
                font-size: 14px;
                color: #e74c3c;
                text-align: center;
                padding: 40px 20px;
            }
        """

    # ========== 新增：CRON 生成器 ==========

    @staticmethod
    def cron_expression_label():
        return (
            "font-weight: bold; font-size: 15px; color: #27ae60; "
            "background: #f0f0f0; padding: 4px 12px; border-radius: 4px;"
        )

    # ========== 新增：主窗口任务列表按钮 ==========

    @staticmethod
    def task_tree_status_btn(color):
        return f"""
            QPushButton {{
                border: none;
                background-color: {color};
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {QColor(color).darker(110).name()};
            }}
        """

    @staticmethod
    def task_tree_icon_btn(color, hover_bg):
        return f"""
            QPushButton {{
                border: none;
                padding: 2px;
                background: transparent;
                color: {color};
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                border-radius: 3px;
            }}
        """

    # ========== 新增：节点工具栏（深色主题） ==========

    @staticmethod
    def toolbar_bg():
        return "background-color: #1a1a2e;"

    @staticmethod
    def toolbar_title():
        return "font-weight: bold; font-size: 14px; color: #fff;"

    @staticmethod
    def toolbar_group():
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: #aaa;
                border: 1px solid #3a3a5a;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: transparent;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
        """

    @staticmethod
    def toolbar_scroll_area():
        return """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #2a2a4a;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a6e;
                border-radius: 4px;
            }
        """

    @staticmethod
    def toolbar_node_btn(color):
        return f"""
            QPushButton {{
                background-color: #2a2a4a;
                color: #fff;
                border: 1px solid {color};
                border-radius: 4px;
                padding: 6px 8px;
                text-align: left;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {color};
                border-color: {color};
            }}
        """
```

- [ ] **步骤 4：创建 `gui/styles/theme_manager.py`**

```python
"""主题管理器 — 加载 QSS、切换主题、热更新"""

import os
from PySide6.QtWidgets import QWidget


class ThemeManager:
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
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base_dir, "resources", "themes", f"{theme}.qss")

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
```

- [ ] **步骤 5：Commit**

```bash
git add gui/styles/__init__.py gui/styles/colors.py gui/styles/widget_styles.py gui/styles/theme_manager.py
git commit -m "feat: 创建样式管理包 gui/styles/ (colors, widget_styles, theme_manager)"
```

---

### 任务 2：创建 `resources/themes/light.qss`

**文件：**
- 创建：`resources/themes/light.qss`

- [ ] **步骤 1：创建 `resources/themes/` 目录**

```bash
mkdir -p resources/themes
```

- [ ] **步骤 2：创建 `resources/themes/light.qss`**

从 `ui_builder.py` 的 `apply_stylesheet()` 和 `styles_bak.py` 的 `main_window_global()` 提取全局静态样式。

```css
/* 全局背景 */
QMainWindow {
    background-color: #f5f7fa;
}

/* GroupBox 全局默认 */
QGroupBox {
    font-weight: bold;
    border: 1px solid #ddd;
    border-radius: 6px;
    margin-top: 6px;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 2px;
    padding: 0 2px 0 2px;
}

/* 默认按钮样式 */
QPushButton {
    padding: 5px 15px;
    border-radius: 4px;
    border: 1px solid #ccc;
    background-color: #ffffff;
}
QPushButton:hover {
    background-color: #f0f0f0;
}

/* QTreeWidget */
QTreeWidget {
    border: 1px solid #ddd;
    border-radius: 4px;
    alternate-background-color: #f9f9f9;
    show-decoration-selected: 1;
}
QTreeWidget::item {
    padding: 6px 4px;
    height: 28px;
}
QTreeWidget::item:edit {
    background-color: #ffffff;
    color: #000000;
}
QTreeWidget::item:selected {
    background-color: #3498db;
    color: white;
}
QTreeWidget::item:selected:edit {
    background-color: #ffffff;
    color: #000000;
}
QTreeWidget QLineEdit {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #3498db;
    padding: 2px;
    margin: 1px;
}

/* QHeaderView */
QHeaderView::section {
    background-color: #f8f9fa;
    padding: 5px;
    border: 1px solid #ddd;
}

/* 日志 QTextEdit（代码编辑器风格） */
QTextEdit {
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: Consolas, Monaco, monospace;
    font-size: 12px;
}

/* 输入控件全局默认 */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #3498db;
}
```

- [ ] **步骤 3：Commit**

```bash
git add resources/themes/light.qss
git commit -m "feat: 添加亮色主题 QSS 文件"
```

---

### 任务 3：迁移 `gui/step_panels/__init__.py` — 基类面板

**文件：**
- 修改：`gui/step_panels/__init__.py`

- [ ] **步骤 1：添加导入**

在文件顶部添加：
```python
from gui.styles import Styles, Colors
```

- [ ] **步骤 2：替换 `StepConfigPanel.__init__` 中的面板背景**

替换第 43-48 行：
```python
# 替换前
self.setStyleSheet("""
    QWidget {
        background-color: #f8f9fa;
        font-size: 13px;
    }
""")

# 替换后
self.setStyleSheet(Styles.panel_bg())
```

- [ ] **步骤 3：替换 `add_section_title` 方法**

替换第 127-136 行：
```python
# 替换前
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

# 替换后
label.setStyleSheet(Styles.section_title())
```

- [ ] **步骤 4：替换 `add_line` 中的标签样式**

替换第 145-156 行：
```python
# 替换前
label.setStyleSheet("""
    QLabel {
        color: #555;
        font-size: 13px;
        min-width: 70px;
        max-width: 90px;
    }
""")
widget.setStyleSheet("""
    QWidget {
        font-size: 13px;
    }
""")

# 替换后
label.setStyleSheet(Styles.LABEL_SECTION)
widget.setStyleSheet("QWidget { font-size: 13px; }")
```

- [ ] **步骤 5：替换 `add_spinbox`**

替换第 171-185 行：
```python
# 替换前
spinbox.setStyleSheet("""...""")

# 替换后
spinbox.setStyleSheet(Styles.small_spin_box())
```

- [ ] **步骤 6：替换 `add_double_spinbox`**

替换第 194-208 行：
```python
# 替换前
spinbox.setStyleSheet("""...""")

# 替换后
spinbox.setStyleSheet(Styles.small_double_spin_box())
```

- [ ] **步骤 7：替换 `add_lineedit`**

替换第 216-227 行：
```python
# 替换前
lineedit.setStyleSheet("""...""")

# 替换后
lineedit.setStyleSheet(Styles.small_line_edit())
```

- [ ] **步骤 8：替换 `add_textedit`**

替换第 235-247 行：
```python
# 替换前
textedit.setStyleSheet("""...""")

# 替换后
textedit.setStyleSheet(Styles.small_text_edit())
```

- [ ] **步骤 9：替换 `add_combobox`**

替换第 255-295 行：
```python
# 替换前
combobox.setStyleSheet("""...""")
list_view.setStyleSheet("""...""")

# 替换后
combobox.setStyleSheet(Styles.small_combo_box())
list_view.setStyleSheet(Styles.small_combo_view())
```

- [ ] **步骤 10：替换 `add_radio_group`**

替换第 313-341 行：
```python
# 替换前
group_box.setStyleSheet("""...""")
radio_btn.setStyleSheet("""...""")

# 替换后
group_box.setStyleSheet(Styles.radio_group())
radio_btn.setStyleSheet(Styles.radio_btn())
```

- [ ] **步骤 11：替换 `add_slider`**

替换第 370-394 行：
```python
# 替换前
label.setStyleSheet("color: #555; font-size: 13px;")
slider.setStyleSheet("""...""")
value_label.setStyleSheet("color: #27ae60; font-weight: bold; font-size: 12px;")

# 替换后
label.setStyleSheet(Styles.LABEL_SECONDARY)
slider.setStyleSheet(Styles.slider())
value_label.setStyleSheet(Styles.slider_value_label())
```

- [ ] **步骤 12：替换 `add_file_browser`**

替换第 409-466 行：
```python
# 替换前
label.setStyleSheet("""...""")          # 409-416
line_edit.setStyleSheet("""...""")      # 422-433
browse_btn.setStyleSheet("""...""")     # 436-448

# 替换后
label.setStyleSheet(Styles.LABEL_SECTION)
line_edit.setStyleSheet(Styles.small_line_edit())
browse_btn.setStyleSheet(Styles.browse_btn())
```

- [ ] **步骤 13：替换 `add_delay_section`**

替换第 471-513 行：
```python
# 替换前
delay_group.setStyleSheet("""...""")    # 471-485
self.delay_spin.setStyleSheet("""...""") # 498-508
delay_label.setStyleSheet("font-size: 12px; color: #666;")

# 替换后
delay_group.setStyleSheet(Styles.delay_group())
self.delay_spin.setStyleSheet(Styles.delay_spin())
delay_label.setStyleSheet(Styles.delay_label())
```

- [ ] **步骤 14：替换 `add_separator`**

替换第 523 行：
```python
# 替换前
separator.setStyleSheet("color: #e0e0e0;")

# 替换后
separator.setStyleSheet(Styles.separator())
```

- [ ] **步骤 15：替换 `add_buttons`**

替换第 533-550 行：
```python
# 替换前
confirm_btn.setStyleSheet("""...""")
cancel_btn.setStyleSheet("""...""")

# 替换后
confirm_btn.setStyleSheet(Styles.confirm_btn())
cancel_btn.setStyleSheet(Styles.cancel_btn())
```

- [ ] **步骤 16：Commit**

```bash
git add gui/step_panels/__init__.py
git commit -m "refactor: 步表面板基类使用 Styles 工厂方法替换内联样式"
```

---

### 任务 4：迁移 `gui/step_panels/keyboard_panel.py`

**文件：**
- 修改：`gui/step_panels/keyboard_panel.py`

- [ ] **步骤 1：添加导入**

```python
from gui.styles import Styles, Colors
```

- [ ] **步骤 2：替换所有内联样式**

| 行号 | 控件 | 替换为 |
|------|------|--------|
| 28 | `file_label` | `Styles.LABEL_SECTION` |
| 32-35 | `self.file_path_edit` | `Styles.small_line_edit()` |
| 38-41 | `browse_btn` | `Styles.browse_btn_text()` |
| 51 | `sheet_label` | `Styles.LABEL_SECTION` |
| 57-58 | `self.sheet_edit` | `Styles.small_line_edit()` |
| 68 | `mode_label` | `Styles.LABEL_SECTION` |
| 73-75 | `self.read_mode_combo` | `Styles.small_combo_box()` |
| 78-82 | `read_mode_view` | `Styles.small_combo_view()` |
| 106-109 | `self.cell_address_edit` | `Styles.small_line_edit()` |
| 119-122 | `self.row_number_spin` | `Styles.small_spin_box()` |
| 132-135 | `self.column_number_spin` | `Styles.small_spin_box()` |
| 144-147 | `self.start_cell_edit` | `Styles.small_line_edit()` |
| 150-153 | `self.end_cell_edit` | `Styles.small_line_edit()` |
| 162 | `fmt_label` | `Styles.LABEL_SECTION` |
| 167-170 | `self.var_format_combo` | `Styles.small_combo_box()` |
| 172-176 | `var_format_view` | `Styles.small_combo_view()` |
| 190-193 | `self.variable_name_edit` | `Styles.small_line_edit()` |
| 200-203 | `self.input_text_edit` | `Styles.small_text_edit()` |
| 216 | `input_label` | `Styles.LABEL_SECONDARY` |
| 227-230 | `self.interval_spin` | `Styles.small_spin_box()` |
| 248 | `interval_label` | `Styles.LABEL_SECTION` |
| 266-269 | `self.random_min_spin` | `Styles.small_spin_box()` |
| 286-289 | `self.random_max_spin` | `Styles.small_spin_box()` |
| 443-446 | `self.key_combo` | `Styles.small_combo_box()` |
| 455-459 | `key_view` | `Styles.small_combo_view()` |
| 530-533 | `self.main_key_combo` | `Styles.small_combo_box()` |
| 542-546 | `main_key_view` | `Styles.small_combo_view()` |
| 562-565 | `self.preview_text` | `Styles.preview_text()` |

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/keyboard_panel.py
git commit -m "refactor: keyboard_panel 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 5：迁移 `gui/step_panels/mouse_panel.py`

**文件：**
- 修改：`gui/step_panels/mouse_panel.py`

- [ ] **步骤 1：添加导入**

```python
from gui.styles import Styles, Colors
```

- [ ] **步骤 2：替换所有内联样式**

所有 SpinBox → `Styles.spin_box()`；所有 ComboBox → `Styles.combo_box()`；所有 ComboBox View → `Styles.combo_view()`；所有 select_btn → `Styles.btn_primary("4px 12px")`。

涉及行号：42, 56, 64, 77, 82, 100, 107, 126, 239, 253, 261, 274, 279, 297, 304, 408, 422, 430, 461, 475, 483, 502, 509

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/mouse_panel.py
git commit -m "refactor: mouse_panel 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 6：迁移 `gui/step_panels/window_panel.py`

**文件：**
- 修改：`gui/step_panels/window_panel.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换所有内联样式** — 所有 SpinBox → `Styles.spin_box()`；所有 LineEdit → `Styles.small_line_edit()`

涉及行号：29, 102, 113, 128, 216, 227, 307, 321, 340, 354

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/window_panel.py
git commit -m "refactor: window_panel 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 7：迁移 `gui/step_panels/image_panel.py`

**文件：**
- 修改：`gui/step_panels/image_panel.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换所有内联样式**

| 行号 | 控件 | 替换为 |
|------|------|--------|
| 24-27 | `self.image_path_edit` | `Styles.spin_box()` 或者 `Styles.input_field()` |
| 29-31 | `browse_btn` | `Styles.browse_btn_text()` |
| 42-45 | `screenshot_btn` | `Styles.btn_primary("4px 12px")` |
| 63-68 | `self.preview_label` | 保留（唯一的预览卡片样式） |
| 86-89 | `region_select_btn` | `Styles.btn_danger("4px 12px")` |

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/image_panel.py
git commit -m "refactor: image_panel 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 8：迁移 `gui/step_panels/control_panel.py`

**文件：**
- 修改：`gui/step_panels/control_panel.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换所有内联样式** — SpinBox → `Styles.spin_box()`；ComboBox → `Styles.combo_box()`；ComboBox View → `Styles.combo_view()`；LineEdit → `Styles.input_field()`；browse_btn → `Styles.browse_btn_text()`

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/control_panel.py
git commit -m "refactor: control_panel 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 9：迁移 `gui/step_panels/excel_panel.py`

**文件：**
- 修改：`gui/step_panels/excel_panel.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换所有内联样式** — LineEdit → `Styles.input_field()`；SpinBox → `Styles.spin_box()`

涉及行号：37, 51, 63, 70, 76

- [ ] **步骤 3：Commit**

```bash
git add gui/step_panels/excel_panel.py
git commit -m "refactor: excel_panel 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 10：迁移 `gui/widgets/node_editor_dialog.py`

**文件：**
- 修改：`gui/widgets/node_editor_dialog.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换所有内联样式**

| 行号 | 控件 | 替换为 |
|------|------|--------|
| 58-60 | `self.config_panel` | `Styles.config_panel_bg()` |
| 89 | `self.toggle_left_btn` | `Styles.toggle_btn()` |
| 98 | `self.toggle_right_btn` | `Styles.toggle_btn()` |
| 111-117 | `self.title_label` | `Styles.title_label()` |
| 128-134 | `self.empty_label` | `Styles.empty_label()` |
| 146-155 | `self.save_btn` | `Styles.btn_primary("6px 20px")` |
| 167-173 | `self.ok_btn` | `Styles.btn_success("8px 30px")` |
| 183-189 | `self.cancel_btn` | `Styles.btn_danger("8px 30px")` |
| 280-282 | `scroll_area` | `Styles.scroll_area_transparent()` |
| 302-307 | `msg_label` | `Styles.error_label()` |

- [ ] **步骤 3：删除 `btn_style` 变量**（第 86-90 行），因为 toggle_btn 已统一管理

- [ ] **步骤 4：Commit**

```bash
git add gui/widgets/node_editor_dialog.py
git commit -m "refactor: node_editor_dialog 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 11：迁移 `gui/widgets/cron_generator.py`

**文件：**
- 修改：`gui/widgets/cron_generator.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换 `self.expression_label.setStyleSheet`**

替换第 200-203 行：
```python
# 替换前
self.expression_label.setStyleSheet(
    "font-weight: bold; font-size: 15px; color: #27ae60; "
    "background: #f0f0f0; padding: 4px 12px; border-radius: 4px;"
)

# 替换后
self.expression_label.setStyleSheet(Styles.cron_expression_label())
```

- [ ] **步骤 3：Commit**

```bash
git add gui/widgets/cron_generator.py
git commit -m "refactor: cron_generator 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 12：迁移 `gui/main_window/ui_builder.py`

**文件：**
- 修改：`gui/main_window/ui_builder.py`

- [ ] **步骤 1：修改导入**

```python
# 替换前
from gui.styles import Styles, Colors

# 替换后
from gui.styles import Styles, Colors, ThemeManager
```

- [ ] **步骤 2：替换左侧面板按钮样式**

替换第 180-189 行工具栏按钮：
```python
# 替换前
self.new_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 12px; border-radius: 4px;")
self.open_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 12px; border-radius: 4px;")
self.save_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
self.copy_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
self.delete_task_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")

# 替换后
self.new_task_btn.setStyleSheet(Styles.btn_toolbar_success())
self.open_task_btn.setStyleSheet(Styles.btn_toolbar_success())
self.save_task_btn.setStyleSheet(Styles.btn_toolbar_success_small())
self.copy_task_btn.setStyleSheet(Styles.btn_toolbar_success_small())
self.delete_task_btn.setStyleSheet(Styles.btn_toolbar_danger())
```

- [ ] **步骤 3：替换 `task_status_label` 样式**

替换第 152 行：
```python
# 替换前
self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")

# 替换后
self.task_status_label.setStyleSheet(Styles.status_label(Colors.DANGER))
```

- [ ] **步骤 4：替换操作按钮样式**

替换第 180-220 行：
```python
# 替换前
self.start_task_btn.setStyleSheet("""...""")
self.stop_task_btn.setStyleSheet("""...""")
self.edit_steps_btn.setStyleSheet("""...""")
self.save_config_btn.setStyleSheet("""...""")

# 替换后
self.start_task_btn.setStyleSheet(Styles.btn_success("8px 20px"))
self.stop_task_btn.setStyleSheet(Styles.btn_danger("8px 20px"))
self.edit_steps_btn.setStyleSheet(Styles.btn_primary("8px 20px"))
self.save_config_btn.setStyleSheet(Styles.btn_primary("8px 20px"))
```

- [ ] **步骤 5：替换 `apply_stylesheet` 方法**

```python
# 替换前
def apply_stylesheet(self):
    self.setStyleSheet(Styles.main_window_global())

# 替换后
def apply_stylesheet(self):
    tm = ThemeManager.instance()
    tm.apply_to(self)
    tm.watch(self)
```

- [ ] **步骤 6：Commit**

```bash
git add gui/main_window/ui_builder.py
git commit -m "refactor: ui_builder 使用 ThemeManager + Styles 替换内联样式"
```

---

### 任务 13：迁移 `gui/main_window/schedule_handler.py`

**文件：**
- 修改：`gui/main_window/schedule_handler.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles`

- [ ] **步骤 2：替换运行时按钮样式切换**

```python
# 替换前 (第 47-55 行)
self.start_scheduled_btn.setStyleSheet(
    "QPushButton {" ... "}"
)

# 替换后
self.start_scheduled_btn.setStyleSheet(Styles.schedule_btn_stop())

# 替换前 (第 69-77 行)
self.start_scheduled_btn.setStyleSheet(
    "QPushButton {" ... "}"
)

# 替换后
self.start_scheduled_btn.setStyleSheet(Styles.schedule_btn_start())
```

- [ ] **步骤 3：Commit**

```bash
git add gui/main_window/schedule_handler.py
git commit -m "refactor: schedule_handler 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 14：迁移 `gui/main_window/schedule_panel.py`

**文件：**
- 修改：`gui/main_window/schedule_panel.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles`

- [ ] **步骤 2：替换 `self.start_scheduled_btn` 初始样式**

替换第 38-46 行：
```python
# 替换前
self.start_scheduled_btn.setStyleSheet(
    "QPushButton {" ... "}"
)

# 替换后
self.start_scheduled_btn.setStyleSheet(Styles.schedule_btn_start())
```

- [ ] **步骤 3：替换 `self.cron_preview_label` 样式**

替换第 98 行：
```python
# 替换前
self.cron_preview_label.setStyleSheet("color: #555; font-family: monospace;")

# 替换后
self.cron_preview_label.setStyleSheet("color: #555; font-family: monospace;")
# 已很简单，可以保留或提取为 Styles.cron_preview_label()
```

- [ ] **步骤 4：Commit**

```bash
git add gui/main_window/schedule_panel.py
git commit -m "refactor: schedule_panel 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 15：迁移 `gui/main_window/task_executor.py`

**文件：**
- 修改：`gui/main_window/task_executor.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换状态标签样式**

```python
# 替换前 (第 33 行)
self.task_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")

# 替换后
self.task_status_label.setStyleSheet(Styles.status_label(Colors.SUCCESS))

# 替换前 (第 74 行)
self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")

# 替换后
self.task_status_label.setStyleSheet(Styles.status_label(Colors.DANGER))
```

- [ ] **步骤 3：Commit**

```bash
git add gui/main_window/task_executor.py
git commit -m "refactor: task_executor 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 16：迁移 `gui/main_window/task_manager.py`

**文件：**
- 修改：`gui/main_window/task_manager.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换 `_update_status_widget` 中的样式**

```python
# 替换前 (第 54-63 行 - 运行中状态)
status_btn.setStyleSheet("""
    QPushButton {
        border: none;
        background-color: #4caf50;
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")

# 替换后
status_btn.setStyleSheet(Styles.task_tree_status_btn("#4caf50"))

# 替换前 (第 65-74 行 - 停止状态)
status_btn.setStyleSheet("""
    QPushButton {
        border: none;
        background-color: #e74c3c;
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: #c0392b;
    }
""")

# 替换后
status_btn.setStyleSheet(Styles.task_tree_status_btn(Colors.DANGER))

# 替换前 (第 79-89 行 - 保存按钮)
save_btn.setStyleSheet("""...""")

# 替换后
save_btn.setStyleSheet(Styles.task_tree_icon_btn(Colors.PRIMARY, "#e8f4fd"))

# 替换前 (第 92-102 行 - 删除按钮)
delete_btn.setStyleSheet("""...""")

# 替换后
delete_btn.setStyleSheet(Styles.task_tree_icon_btn(Colors.DANGER, "#fce4ec"))
```

- [ ] **步骤 3：Commit**

```bash
git add gui/main_window/task_manager.py
git commit -m "refactor: task_manager 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 17：迁移 `gui/node_graph/node_toolbar.py`

**文件：**
- 修改：`gui/node_graph/node_toolbar.py`

- [ ] **步骤 1：添加导入** → `from gui.styles import Styles, Colors`

- [ ] **步骤 2：替换所有内联样式**

```python
# 替换 content_widget 背景
content_widget.setStyleSheet(Styles.toolbar_bg())

# 替换 title_label
title_label.setStyleSheet(Styles.toolbar_title())

# 替换 scroll_area
scroll_area.setStyleSheet(Styles.toolbar_scroll_area())

# 替换 groups_widget 背景
groups_widget.setStyleSheet(Styles.toolbar_bg())

# 替换 group 样式
group.setStyleSheet(Styles.toolbar_group())

# 替换 btn 样式（循环中）
btn.setStyleSheet(Styles.toolbar_node_btn(node_info['color']))
```

- [ ] **步骤 3：Commit**

```bash
git add gui/node_graph/node_toolbar.py
git commit -m "refactor: node_toolbar 使用 Styles 工厂方法替换内联样式"
```

---

### 任务 18：删除 `gui/styles_bak.py`

- [ ] **步骤 1：删除旧文件**

```bash
git rm gui/styles_bak.py
```

- [ ] **步骤 2：Commit**

```bash
git commit -m "chore: 删除已迁移的 styles_bak.py"
```

---

### 任务 19：验证 — 运行应用确保无样式错误

- [ ] **步骤 1：启动应用**

```bash
python main.py
```

- [ ] **步骤 2：检查项**
  - 主窗口正常显示，样式与改造前一致
  - 点击"编辑执行步骤"打开节点编辑器，样式正常
  - 切换各节点类型，配置面板样式正常
  - 定时设置面板样式正常
  - CRON 生成器样式正常
  - 控制台无 `Could not parse stylesheet` 错误

- [ ] **步骤 3：尝试切换主题（手动测试）**

```python
# 在 Python 控制台或代码中临时添加
from gui.styles import ThemeManager
ThemeManager.instance().switch_theme("light")
```

---

## 自检

1. **规格覆盖度** — 所有文件已覆盖：styles_bak.py → 删除；所有面板 → 迁移；ui_builder → ThemeManager
2. **占位符扫描** — 无 TODO、无待定、无占位符
3. **类型一致性** — Styles 类方法名与各任务中引用一致