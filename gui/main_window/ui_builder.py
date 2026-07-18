from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QToolBar, QStatusBar, QSplitter,
                               QTreeWidget, QTreeWidgetItem,
                               QTextEdit, QLabel,
                               QLineEdit, QGroupBox, QGridLayout, QFormLayout,
                               QSpinBox, QDoubleSpinBox, QCheckBox,
                               QFileDialog, QMessageBox, QProgressBar,
                               QInputDialog, QHeaderView, QDialog, QApplication)
from PySide6.QtGui import QIcon, QAction, QFont, QPainter, QPixmap, QColor, QPen, QBrush, QPainterPath
from PySide6.QtCore import Qt, QSize, Signal, Slot, QPointF

from ..node_graph import GraphScene, GraphView, NodeToolbar

from core.engine import FlowEngine
from utils.resource_path import get_resource_path, get_resources_dir, ensure_resources_dir
from .schedule_panel import SchedulePanel
from gui.styles import Styles, ThemeManager


class UIBuilderMixin:
    """界面构建 Mixin：菜单栏、状态栏、中央区域、样式表"""

    def init_ui(self):
        self.create_menu_bar()
        self.create_status_bar()
        self.create_central_widget()
        self.apply_stylesheet()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setFixedHeight(25)
        file_menu = menu_bar.addMenu("文件(&F)")

        new_action = QAction("新建任务", self)
        open_action = QAction("打开任务", self)
        save_action = QAction("保存任务", self)
        save_as_action = QAction("另存为", self)
        exit_action = QAction("退出", self)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        new_action.triggered.connect(self.on_new_flow)
        open_action.triggered.connect(self.on_open_flow)
        save_action.triggered.connect(lambda checked: self.on_save_flow())
        exit_action.triggered.connect(self.close)

        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(22, 22)
        self.theme_btn.setIcon(self._create_theme_icon("light"))
        self.theme_btn.setIconSize(QSize(18, 18))
        self.theme_btn.setStyleSheet(Styles.theme_btn())
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.clicked.connect(self._on_theme_changed)
        menu_bar.setCornerWidget(self.theme_btn, Qt.TopRightCorner)

    def create_tool_bar(self):
        tool_bar = QToolBar("主工具栏")
        tool_bar.setIconSize(QSize(24, 24))
        self.addToolBar(tool_bar)

        new_icon = QIcon.fromTheme("document-new")
        open_icon = QIcon.fromTheme("document-open")
        save_icon = QIcon.fromTheme("document-save")
        run_icon = QIcon.fromTheme("media-play")
        stop_icon = QIcon.fromTheme("media-stop")

        tool_bar.addAction(new_icon, "新建", self.on_new_flow)
        tool_bar.addAction(open_icon, "打开", self.on_open_flow)
        tool_bar.addAction(save_icon, "保存", lambda checked: self.on_save_flow())
        tool_bar.addSeparator()
        tool_bar.addAction(run_icon, "运行", self.on_run_flow)
        tool_bar.addAction(stop_icon, "停止", self.on_stop_flow)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.hide()
        self.status_bar.addPermanentWidget(self.progress_bar)

    def create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Horizontal)

        # ==================== 左侧面板 ====================
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        btn_style = "background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;"

        self.new_task_btn = QPushButton("新建")
        self.new_task_btn.setStyleSheet(Styles.btn_toolbar_success())
        self.open_task_btn = QPushButton("导入")
        self.open_task_btn.setStyleSheet(Styles.btn_toolbar_success())
        self.save_task_btn = QPushButton("保存")
        self.save_task_btn.setStyleSheet(Styles.btn_toolbar_success())
        self.copy_task_btn = QPushButton("复制")
        self.copy_task_btn.setStyleSheet(Styles.btn_toolbar_success())
        self.delete_task_btn = QPushButton("删除")
        self.delete_task_btn.setStyleSheet(Styles.btn_toolbar_danger())

        self.task_list_group = QGroupBox("任务列表")
        task_list_layout = QVBoxLayout(self.task_list_group)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.new_task_btn)
        btn_layout.addWidget(self.open_task_btn)
        btn_layout.addWidget(self.copy_task_btn)
        task_list_layout.addLayout(btn_layout)

        self.task_tree = QTreeWidget()
        self.task_tree.setHeaderLabels(["任务名称", "任务状态"])
        self.task_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.task_tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        task_list_layout.addWidget(self.task_tree)
        left_layout.addWidget(self.task_list_group)

        self.log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(self.log_group)

        log_header_layout = QHBoxLayout()
        log_header_layout.addWidget(QLabel("执行日志"))
        log_header_layout.addStretch()
        self.clear_log_btn = QPushButton("清空日志")
        log_header_layout.addWidget(self.clear_log_btn)
        log_layout.addLayout(log_header_layout)

        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setPlaceholderText("运行日志将显示在这里...")
        log_layout.addWidget(self.log_panel)
        left_layout.addWidget(self.log_group)

        self.splitter.addWidget(left_panel)

        # ==================== 右侧面板 ====================
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.task_info_group = QGroupBox("任务信息")
        task_info_layout = QFormLayout(self.task_info_group)

        self.task_name_edit = QLineEdit()
        self.task_name_edit.setPlaceholderText("输入任务名称")
        task_info_layout.addRow("任务名称:", self.task_name_edit)

        self.task_status_label = QLabel("已停止")
        self.task_status_label.setStyleSheet(Styles.status_label("#e74c3c"))
        task_info_layout.addRow("当前状态:", self.task_status_label)
        right_layout.addWidget(self.task_info_group)

        # -------------------- 定时设置 --------------------
        self.schedule_group = QGroupBox("定时设置")
        schedule_layout = QVBoxLayout(self.schedule_group)
        self.schedule_panel = SchedulePanel()
        self.schedule_panel.start_scheduled.connect(self._on_start_scheduled)
        schedule_layout.addWidget(self.schedule_panel)
        right_layout.addWidget(self.schedule_group)

        # -------------------- 执行步骤查看 --------------------
        self.step_view_group = QGroupBox("执行步骤查看")
        step_view_layout = QVBoxLayout(self.step_view_group)
        self.graph_scene = GraphScene()
        self.graph_view = GraphView(self.graph_scene)
        step_view_layout.addWidget(self.graph_view)
        right_layout.addWidget(self.step_view_group)

        # -------------------- 操作按钮组 --------------------
        action_btn_layout = QHBoxLayout()
        action_btn_layout.addStretch()

        self.start_task_btn = QPushButton("开始当前任务")
        self.start_task_btn.setStyleSheet(Styles.btn_success("8px 20px"))

        self.stop_task_btn = QPushButton("停止当前任务")
        self.stop_task_btn.setStyleSheet(Styles.btn_danger("8px 20px"))
        self.stop_task_btn.setEnabled(False)

        self.edit_steps_btn = QPushButton("编辑执行步骤")
        self.edit_steps_btn.setStyleSheet(Styles.btn_primary("8px 20px"))
        self.save_config_btn = QPushButton("保存配置")
        self.save_config_btn.setStyleSheet(Styles.btn_primary("8px 20px"))

        action_btn_layout.addWidget(self.start_task_btn)
        action_btn_layout.addWidget(self.stop_task_btn)
        action_btn_layout.addWidget(self.edit_steps_btn)
        action_btn_layout.addStretch()
        action_btn_layout.addWidget(self.save_config_btn)
        right_layout.addLayout(action_btn_layout)

        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([400, 1000])
        main_layout.addWidget(self.splitter)

        # ==================== 信号与槽连接 ====================
        self.new_task_btn.clicked.connect(self.on_new_flow)
        self.open_task_btn.clicked.connect(self.on_open_flow)
        self.save_task_btn.clicked.connect(lambda checked: self.on_save_flow())
        self.copy_task_btn.clicked.connect(self.on_copy_task)
        self.delete_task_btn.clicked.connect(self.on_delete_task)
        self.clear_log_btn.clicked.connect(self.on_clear_log)

        self.task_tree.itemClicked.connect(self.on_task_selected)
        self.task_tree.itemChanged.connect(self.on_task_name_changed)

        self.start_task_btn.clicked.connect(self.on_run_flow)
        self.stop_task_btn.clicked.connect(self.on_stop_flow)
        self.edit_steps_btn.clicked.connect(self.on_edit_steps)
        self.save_config_btn.clicked.connect(lambda checked: self.on_save_flow())

        self.load_default_tasks()

    def apply_stylesheet(self):
        self.setStyleSheet(Styles.main_window_qss())

    def _create_theme_icon(self, theme="light"):
        import math
        size = 18
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor("#ff8c00")

        if theme == "light":
            # 太阳：中心圆 + 8 条射线
            cx, cy, r = size / 2, size / 2, 4
            painter.setPen(QPen(color, 1.5))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPointF(cx, cy), r, r)
            painter.setPen(QPen(color, 2))
            painter.setBrush(Qt.NoBrush)
            for i in range(8):
                rad = (i * 45) * math.pi / 180
                x1 = cx + (r + 2) * math.cos(rad)
                y1 = cy + (r + 2) * math.sin(rad)
                x2 = cx + (r + 4) * math.cos(rad)
                y2 = cy + (r + 4) * math.sin(rad)
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        else:
            # 月亮：月牙形（用 QPainterPath 差集）
            painter.setPen(QPen(color, 1.5))
            painter.setBrush(QBrush(color))
            outer = QPainterPath()
            outer.addEllipse(QPointF(size / 2, size / 2), 5, 5)
            inner = QPainterPath()
            inner.addEllipse(QPointF(size / 2 + 2.5, size / 2 - 2.5), 4, 4)
            crescent = outer.subtracted(inner)
            painter.drawPath(crescent)

        painter.end()
        return QIcon(pixmap)

    def _on_theme_changed(self):
        current = ThemeManager.instance().current_theme
        theme = "dark" if current == "light" else "light"
        ThemeManager.instance().switch_theme(theme)
        self.setStyleSheet(Styles.main_window_qss())
        self.theme_btn.setStyleSheet(Styles.theme_btn(theme))
        self.theme_btn.setIcon(self._create_theme_icon(theme))