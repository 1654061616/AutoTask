"""应用程序统一样式管理模块"""

from PySide6.QtGui import QColor


class Colors:
    """颜色常量"""

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


class Styles:
    """样式片段和工厂方法"""

    # ---- 输入框 ----
    INPUT_BASE = (
        "border: 1px solid #ddd; border-radius: 4px; padding: 4px 8px;"
        "background: white; color: #333;"
    )

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

    # ---- 标签 ----
    LABEL_SECONDARY = f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;"
    LABEL_SECTION = f"color: {Colors.TEXT_SECONDARY}; font-size: 13px; min-width: 70px; max-width: 90px;"

    @staticmethod
    def status_label(color):
        return f"color: {color}; font-weight: bold;"

    # ---- 按钮 ----
    @staticmethod
    def button(color, padding="8px 20px", hover_color=None, pressed_color=None, disabled_color=None, font_weight="bold"):
        """生成完整按钮样式，含 hover / pressed / disabled 状态"""
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

    # ---- 工具栏按钮（小尺寸，无状态）----
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

    # ---- 分组框 ----
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

    # ---- 预览文本 ----
    @staticmethod
    def preview_text():
        return f"""
            QLabel {{
                background: {Colors.BG_LIGHT}; border: 1px solid {Colors.BORDER};
                border-radius: 4px; padding: 8px; color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
            }}
        """

    # ---- 主窗口全局 ----
    @staticmethod
    def main_window_global():
        return f"""
            QMainWindow {{
                background-color: #f5f7fa;
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 2px;
                padding: 0 2px 0 2px;
            }}
            QPushButton {{
                padding: 5px 15px;
                border-radius: 4px;
                border: 1px solid #ccc;
                background-color: #ffffff;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            QTreeWidget {{
                border: 1px solid #ddd;
                border-radius: 4px;
                alternate-background-color: #f9f9f9;
                show-decoration-selected: 1;
            }}
            QTreeWidget::item {{
                padding: 6px 4px;
                height: 28px;
            }}
            QTreeWidget::item:edit {{
                background-color: #ffffff;
                color: #000000;
            }}
            QTreeWidget::item:selected {{
                background-color: #3498db;
                color: white;
            }}
            QTreeWidget::item:selected:edit {{
                background-color: #ffffff;
                color: #000000;
            }}
            QTreeWidget QLineEdit {{
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #3498db;
                padding: 2px;
                margin: 1px;
            }}
            QHeaderView::section {{
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #ddd;
            }}
            QTextEdit {{
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }}
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border-color: #3498db;
            }}
        """