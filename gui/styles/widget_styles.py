"""动态样式工厂 — 需要参数或运行时切换的样式"""

from PySide6.QtGui import QColor
from .colors import Colors


class Styles:
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

    # ========== 步表面板基类用 ==========

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

    # ========== 小尺寸控件（步表面板用） ==========

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

    # ========== 无线电组 ==========

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

    # ========== 滑块 ==========

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

    # ========== 文件浏览按钮 ==========

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

    # ========== 延时设置 ==========

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

    # ========== 分隔线 ==========

    @staticmethod
    def separator():
        return "color: #e0e0e0;"

    # ========== 确认/取消按钮（对话框用） ==========

    @staticmethod
    def confirm_btn():
        return Styles.button(Colors.SUCCESS, "5px 16px", Colors.SUCCESS_HOVER, None, Colors.SUCCESS_DISABLED)

    @staticmethod
    def cancel_btn():
        return Styles.button(Colors.DANGER, "5px 16px", "#c0392b", None, Colors.DANGER_DISABLED)

    # ========== 调度按钮（运行时切换） ==========

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

    # ========== 节点编辑器对话框 ==========

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

    # ========== CRON 生成器 ==========

    @staticmethod
    def cron_expression_label():
        return (
            "font-weight: bold; font-size: 15px; color: #27ae60; "
            "background: #f0f0f0; padding: 4px 12px; border-radius: 4px;"
        )

    # ========== 主窗口任务列表按钮 ==========

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

    # ========== 节点工具栏（深色主题） ==========

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