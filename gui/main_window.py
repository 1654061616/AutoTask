"""
文件名: main_window.py
功能: 主窗口界面，包含任务列表、执行日志、任务信息、定时设置、节点图预览等所有界面元素
所属模块: GUI层 - gui包
依赖: 
    - PySide6.QtWidgets: Qt的所有窗口控件（按钮、输入框、表格、对话框等）
    - PySide6.QtGui: Qt的图形相关类（图标、字体、颜色等）
    - PySide6.QtCore: Qt的核心类（信号、槽、枚举等）
    - sys, os, uuid, json: Python内置模块
    - .step_editor: 步骤编辑器对话框
    - .node_graph: 节点图相关类（画布、视图、工具栏）
    - .node_editor_dialog: 节点编辑器对话框

界面布局:
    主窗口分为左右两部分（通过QSplitter分隔，可拖拽调整宽度）:
    ┌─────────────────────────┬─────────────────────────────────────┐
    │ 左侧面板 (约400px)      │ 右侧面板 (约1000px)                  │
    │ ┌─────────────────────┐ │ ┌─────────────────────────────────┐ │
    │ │ 任务列表            │ │ │ 任务信息                        │ │
    │ │ (新建/导入/复制按钮) │ │ │ 定时设置                        │ │
    │ │ (任务树:名称+操作)  │ │ │ 执行步骤查看(节点图)             │ │
    │ └─────────────────────┘ │ │ 操作按钮(开始/停止/编辑/保存)    │ │
    │ ┌─────────────────────┐ │ └─────────────────────────────────┘ │
    │ │ 执行日志            │ │                                     │
    │ │ (清空日志按钮)      │ │                                     │
    │ └─────────────────────┘ │                                     │
    └─────────────────────────┴─────────────────────────────────────┘
"""

# 从PySide6.QtWidgets模块导入所有需要的窗口控件类
# QMainWindow: 主窗口类，提供菜单栏、工具栏、状态栏等
# QWidget: 基础控件类，所有可见控件的基类
# QVBoxLayout/QHBoxLayout: 垂直/水平布局管理器，用于排列控件
# QPushButton: 按钮控件
# QToolBar: 工具栏
# QStatusBar: 状态栏
# QSplitter: 分隔器，允许用户拖拽调整子控件大小
# QTreeWidget: 树形控件，用于显示任务列表
# QTreeWidgetItem: 树形控件中的一个项目
# QTableWidget: 表格控件
# QTableWidgetItem: 表格中的一个单元格
# QTextEdit: 文本编辑控件（这里用作日志显示）
# QLabel: 标签控件，用于显示文字
# QComboBox: 下拉选择框
# QLineEdit: 单行文本输入框
# QGroupBox: 分组框，用于组织相关控件
# QGridLayout/QFormLayout: 网格/表单布局管理器
# QSpinBox/QDoubleSpinBox: 整数/小数数字输入框
# QCheckBox: 复选框
# QFileDialog: 文件选择对话框
# QMessageBox: 消息对话框（提示、警告、确认等）
# QProgressBar: 进度条
# QInputDialog: 输入对话框
# QHeaderView: 表头视图，用于控制表格列的大小调整方式
# QDialog: 对话框基类
# QApplication: 应用程序类
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QToolBar, QStatusBar, QSplitter,
                               QTreeWidget, QTreeWidgetItem, QTableWidget,
                               QTableWidgetItem, QTextEdit, QLabel, QComboBox,
                               QLineEdit, QGroupBox, QGridLayout, QFormLayout,
                               QSpinBox, QDoubleSpinBox, QCheckBox,
                               QFileDialog, QMessageBox, QProgressBar,
                               QInputDialog, QHeaderView, QDialog, QApplication)

# 从PySide6.QtGui模块导入图形相关类
# QIcon: 图标类
# QAction: 动作类，用于菜单和工具栏
# QFont: 字体类
# QColor/QBrush: 颜色/画刷类，用于设置控件颜色
# QPainter: 画家类，用于绘制图形
from PySide6.QtGui import QIcon, QAction, QFont, QColor, QBrush, QPainter

# 从PySide6.QtCore模块导入核心类
# Qt: 包含所有Qt的枚举值和常量（如对齐方式、窗口标志等）
# QSize: 尺寸类
# Signal: 信号类，用于事件通知
# Slot: 槽装饰器，用于接收信号
from PySide6.QtCore import Qt, QSize, Signal, Slot

# Python内置模块
import sys      # 系统相关功能（命令行参数、退出等）
import os       # 文件和目录操作
import uuid     # 生成唯一标识符
import json     # JSON数据处理

# 导入自定义模块
from .step_editor import StepEditorDialog, STEP_TYPE_MAP  # 步骤编辑器对话框和步骤类型映射
from .node_graph import GraphScene, GraphView, NodeToolbar  # 节点图相关类
from .node_editor_dialog import NodeEditorDialog  # 节点编辑器对话框
from core.engine import FlowEngine  # 执行引擎
from utils.resource_path import get_resource_path, get_resources_dir, ensure_resources_dir  # 资源路径管理
from gui.widgets.schedule_panel import SchedulePanel

class MainWindow(QMainWindow):
    """
    主窗口类: 整个软件的界面主体
    
    继承自QMainWindow，拥有以下特性:
    - 菜单栏: 文件菜单（新建、打开、保存、退出）
    - 状态栏: 显示程序状态和进度
    - 中央区域: 左右分栏布局
    
    信号定义:
        flow_loaded: 当一个流程被加载时发出
        step_selected: 当一个步骤被选中时发出
        flow_started: 当流程开始执行时发出
        flow_stopped: 当流程停止执行时发出
    
    主要属性:
        flows: 存储所有任务流程的列表
        current_flow: 当前选中的任务流程
        task_tree: 任务列表树形控件
        log_panel: 执行日志显示区域
        task_name_edit: 任务名称输入框
        graph_scene/graph_view: 节点图场景和视图
    """
    
    # 定义Qt信号，用于跨组件通信
    # Signal(dict)表示这个信号会携带一个字典类型的数据
    flow_loaded = Signal(dict)    # 流程加载完成信号
    step_selected = Signal(dict)  # 步骤选中信号
    flow_started = Signal()       # 流程开始执行信号
    flow_stopped = Signal()       # 流程停止执行信号
    log_received = Signal(str)    # 日志接收信号，用于从后台线程更新GUI日志
    task_completed = Signal(bool, str)  # 任务完成信号，参数：success(是否成功), error_message(错误信息)
    
    def __init__(self):
        """
        初始化方法: 创建主窗口时自动调用
        
        执行流程:
            1. 调用父类QMainWindow的初始化方法
            2. 设置窗口标题
            3. 设置窗口初始大小和位置
            4. 初始化任务列表和当前任务变量
            5. 调用init_ui()创建界面
        """
        # 调用父类的构造方法，这是必须的
        super().__init__()
        
        # 设置窗口标题，显示在标题栏上
        self.setWindowTitle("AutoFlow")
        
        icon_path = get_resource_path("icons/Icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 设置窗口的初始位置和大小
        # 参数: (x坐标, y坐标, 宽度, 高度)
        # x=100, y=100: 窗口左上角距离屏幕左上角的距离
        # 1400x900: 窗口的宽和高
        self.setGeometry(100, 100, 1400, 900)
        
        # 初始化任务列表，用于存储所有打开的任务
        self.flows = []
        
        # 当前选中的任务，初始为None（没有选中任何任务）
        self.current_flow = None
        
        # 初始化执行引擎
        self.engine = FlowEngine()
        
        # 连接日志信号到GUI日志面板（通过信号机制安全地从后台线程更新GUI）
        self.log_received.connect(self._on_log_received)
        
        # 注册日志回调函数到执行引擎的logger
        self.engine.logger.add_callback(self._on_engine_log)
        
        # 连接任务完成信号到槽方法
        self.task_completed.connect(self._on_task_completed_slot)
        
        # 创建界面的所有控件
        self.init_ui()
    
    def init_ui(self):
        """
        创建界面方法: 统一管理所有界面元素的创建
        
        调用以下子方法:
            create_menu_bar(): 创建菜单栏
            create_status_bar(): 创建状态栏
            create_central_widget(): 创建中央区域（主要内容）
            apply_stylesheet(): 应用样式表（美化界面）
        """
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏（当前被注释掉了，因为功能已经集成到界面按钮中）
        # self.create_tool_bar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 创建中央区域（最重要的部分，包含所有主要控件）
        self.create_central_widget()
        
        # 应用样式表，让界面看起来更美观
        self.apply_stylesheet()
    
    def create_menu_bar(self):
        """
        创建菜单栏方法
        
        创建"文件"菜单，包含以下菜单项:
            新建任务: 创建一个新的自动化任务
            打开任务: 从文件加载已保存的任务
            保存任务: 保存当前任务到文件
            另存为: 将当前任务另存为新文件
            退出: 关闭程序
        """
        # 获取主窗口的菜单栏对象（QMainWindow自带的）
        menu_bar = self.menuBar()
        
        # 创建"文件"菜单，"(&F)"表示可以用Alt+F快捷键打开
        file_menu = menu_bar.addMenu("文件(&F)")
        
        # 创建菜单项（QAction对象）
        new_action = QAction("新建任务", self)     # 新建任务
        open_action = QAction("打开任务", self)    # 打开任务
        save_action = QAction("保存任务", self)    # 保存任务
        save_as_action = QAction("另存为", self)   # 另存为
        exit_action = QAction("退出", self)        # 退出
        
        # 将菜单项添加到文件菜单中
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        
        # 添加分隔线（视觉上分开不同类别的菜单项）
        file_menu.addSeparator()
        
        # 添加退出菜单项
        file_menu.addAction(exit_action)
        
        # 连接信号和槽：当菜单项被点击时，执行对应的方法
        # triggered是QAction的信号，当用户点击菜单项时发出
        new_action.triggered.connect(self.on_new_flow)    # 点击"新建任务"执行on_new_flow
        open_action.triggered.connect(self.on_open_flow)  # 点击"打开任务"执行on_open_flow
        save_action.triggered.connect(lambda checked: self.on_save_flow())  # 点击"保存任务"执行on_save_flow
        exit_action.triggered.connect(self.close)         # 点击"退出"执行close（关闭窗口）
    
    def create_tool_bar(self):
        """
        创建工具栏方法（当前未使用）
        
        工具栏包含以下按钮:
            新建: 创建新任务
            打开: 打开已有任务
            保存: 保存当前任务
            运行: 开始执行任务
            停止: 停止执行任务
        """
        # 创建工具栏对象，参数是工具栏的名称
        tool_bar = QToolBar("主工具栏")
        
        # 设置工具栏图标的大小为24x24像素
        tool_bar.setIconSize(QSize(24, 24))
        
        # 将工具栏添加到主窗口
        self.addToolBar(tool_bar)
        
        # 创建图标，使用系统主题图标
        # QIcon.fromTheme()会从系统主题中查找图标，如果找不到则使用默认图标
        new_icon = QIcon.fromTheme("document-new")   # 新建图标
        open_icon = QIcon.fromTheme("document-open") # 打开图标
        save_icon = QIcon.fromTheme("document-save") # 保存图标
        run_icon = QIcon.fromTheme("media-play")     # 播放/运行图标
        stop_icon = QIcon.fromTheme("media-stop")    # 停止图标
        
        # 添加工具栏按钮
        # 参数: 图标, 提示文字, 点击后执行的方法
        tool_bar.addAction(new_icon, "新建", self.on_new_flow)
        tool_bar.addAction(open_icon, "打开", self.on_open_flow)
        tool_bar.addAction(save_icon, "保存", lambda checked: self.on_save_flow())
        
        # 添加分隔线
        tool_bar.addSeparator()
        
        # 添加运行和停止按钮
        tool_bar.addAction(run_icon, "运行", self.on_run_flow)
        tool_bar.addAction(stop_icon, "停止", self.on_stop_flow)
    
    def create_status_bar(self):
        """
        创建状态栏方法
        
        状态栏包含:
            状态标签: 显示当前程序状态（就绪、运行中、已停止等）
            进度条: 显示任务执行进度（默认隐藏，执行时显示）
        """
        # 创建状态栏对象
        self.status_bar = QStatusBar()
        
        # 将状态栏设置到主窗口
        self.setStatusBar(self.status_bar)
        
        # 创建状态标签，初始显示"就绪"
        self.status_label = QLabel("就绪")
        
        # 将状态标签添加到状态栏（左侧）
        self.status_bar.addWidget(self.status_label)
        
        # 创建进度条，用于显示任务执行进度
        self.progress_bar = QProgressBar()
        
        # 设置进度条固定宽度为200像素
        self.progress_bar.setFixedWidth(200)
        
        # 默认隐藏进度条，只有在任务执行时才显示
        self.progress_bar.hide()
        
        # 将进度条添加到状态栏（右侧，永久显示）
        # addPermanentWidget会把控件放在状态栏的最右侧
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def create_central_widget(self):
        """
        创建中央区域方法: 包含主窗口的所有主要内容
        
        布局结构:
            主窗口 → QSplitter(水平分隔)
              ├── 左侧面板(QWidget)
              │     ├── 任务列表(QGroupBox)
              │     │     ├── 按钮组(新建/导入/复制)
              │     │     └── 任务树(QTreeWidget)
              │     └── 执行日志(QGroupBox)
              │           ├── 标题栏(标签+清空按钮)
              │           └── 日志面板(QTextEdit)
              └── 右侧面板(QWidget)
                    ├── 任务信息(QGroupBox)
                    ├── 定时设置(QGroupBox)
                    ├── 执行步骤查看(QGroupBox)
                    └── 操作按钮组(开始/停止/编辑/保存)
        """
        # 创建中央控件，作为主窗口的中心区域
        # QMainWindow必须有一个central widget
        central_widget = QWidget()
        
        # 将中央控件设置到主窗口
        self.setCentralWidget(central_widget)
        
        # 创建主布局（水平布局），用于放置左右两个面板
        main_layout = QHBoxLayout(central_widget)
        
        # 设置布局的外边距为5像素（上下左右各5px）
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 设置布局中控件之间的间距为0
        main_layout.setSpacing(0)
        
        # 创建QSplitter（水平分隔器），允许用户拖拽调整左右面板宽度
        self.splitter = QSplitter(Qt.Horizontal)
        
        # ==================== 左侧面板 ====================
        
        # 创建左侧面板容器
        left_panel = QWidget()
        
        # 创建左侧面板的布局（垂直布局）
        left_layout = QVBoxLayout(left_panel)
        
        # 定义按钮样式（绿色背景、白色文字、粗体、圆角）
        # 这里定义了一个变量但没有使用，实际样式直接写在每个按钮上
        btn_style = "background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;"
        
        # 创建"新建"按钮，用于创建新任务
        self.new_task_btn = QPushButton("新建")
        self.new_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 12px; border-radius: 4px;")
        
        # 创建"导入"按钮，用于从文件导入任务
        self.open_task_btn = QPushButton("导入")
        self.open_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 12px; border-radius: 4px;")
        
        # 创建"保存"按钮，用于保存当前任务
        self.save_task_btn = QPushButton("保存")
        self.save_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
        
        # 创建"复制"按钮，用于复制当前任务
        self.copy_task_btn = QPushButton("复制")
        self.copy_task_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
        
        # 创建"删除"按钮，用于删除选中任务（红色背景表示危险操作）
        self.delete_task_btn = QPushButton("删除")
        self.delete_task_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
        
        # 创建"任务列表"分组框，用于组织任务相关控件
        self.task_list_group = QGroupBox("任务列表")
        task_list_layout = QVBoxLayout(self.task_list_group)
        
        # 创建按钮布局（水平布局），放置新建、导入、复制按钮
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.new_task_btn)      # 添加新建按钮
        btn_layout.addWidget(self.open_task_btn)     # 添加导入按钮
        btn_layout.addWidget(self.copy_task_btn)     # 添加复制按钮
        
        # 将按钮布局添加到任务列表分组框
        task_list_layout.addLayout(btn_layout)
        
        # 创建任务树形控件，用于显示任务列表
        self.task_tree = QTreeWidget()
        
        # 设置树形控件的列标题为["任务名称", "任务状态"]
        # 任务状态列包含状态图标、保存图标、删除图标
        self.task_tree.setHeaderLabels(["任务名称", "任务状态"])
        
        # 设置第0列（任务名称）自动拉伸，填充可用空间
        self.task_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        
        # 设置第1列（操作）根据内容自动调整宽度
        self.task_tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        
        # 将任务树添加到任务列表分组框
        task_list_layout.addWidget(self.task_tree)
        
        # 将任务列表分组框添加到左侧面板布局
        left_layout.addWidget(self.task_list_group)
        
        # 创建"执行日志"分组框
        self.log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(self.log_group)
        
        # 创建日志标题栏布局（水平布局）
        log_header_layout = QHBoxLayout()
        
        # 添加"执行日志"标签
        log_header_layout.addWidget(QLabel("执行日志"))
        
        # 添加弹簧，将清空按钮推到右侧
        log_header_layout.addStretch()
        
        # 创建"清空日志"按钮
        self.clear_log_btn = QPushButton("清空日志")
        
        # 将清空按钮添加到标题栏布局
        log_header_layout.addWidget(self.clear_log_btn)
        
        # 将标题栏布局添加到日志分组框
        log_layout.addLayout(log_header_layout)
        
        # 创建日志显示面板（QTextEdit）
        self.log_panel = QTextEdit()
        
        # 设置日志面板为只读模式，用户不能编辑日志内容
        self.log_panel.setReadOnly(True)
        
        # 设置占位符文本，提示用户日志会显示在这里
        self.log_panel.setPlaceholderText("运行日志将显示在这里...")
        
        # 将日志面板添加到日志分组框
        log_layout.addWidget(self.log_panel)
        
        # 将日志分组框添加到左侧面板布局
        left_layout.addWidget(self.log_group)
        
        # 将左侧面板添加到分隔器
        self.splitter.addWidget(left_panel)

        # ==================== 右侧面板 ====================
        
        # 创建右侧面板容器
        right_panel = QWidget()
        
        # 创建右侧面板的布局（垂直布局）
        right_layout = QVBoxLayout(right_panel)
        
        # -------------------- 任务信息分组框 --------------------
        
        # 创建"任务信息"分组框
        self.task_info_group = QGroupBox("任务信息")
        
        # 使用表单布局（QFormLayout），适合标签+控件的配对显示
        task_info_layout = QFormLayout(self.task_info_group)
        
        # 创建任务名称输入框
        self.task_name_edit = QLineEdit()
        
        # 设置占位符文本，提示用户输入任务名称
        self.task_name_edit.setPlaceholderText("输入任务名称")
        
        # 将任务名称输入框添加到表单布局（标签在前，控件在后）
        task_info_layout.addRow("任务名称:", self.task_name_edit)
        
        # 创建任务状态标签，初始显示"已停止"
        self.task_status_label = QLabel("已停止")
        
        # 设置状态标签样式（红色文字、粗体）
        self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        
        # 将状态标签添加到表单布局
        task_info_layout.addRow("当前状态:", self.task_status_label)
        
        # 将任务信息分组框添加到右侧面板布局
        right_layout.addWidget(self.task_info_group)
        
        # -------------------- 定时设置分组框 --------------------
        self.schedule_group = QGroupBox("定时设置")
        schedule_layout = QVBoxLayout(self.schedule_group)
        self.schedule_panel = SchedulePanel()
        self.schedule_panel.start_scheduled.connect(self._on_start_scheduled)
        schedule_layout.addWidget(self.schedule_panel)
        right_layout.addWidget(self.schedule_group)
        
        # -------------------- 执行步骤查看分组框 --------------------
        
        # 创建"执行步骤查看"分组框
        self.step_view_group = QGroupBox("执行步骤查看")
        step_view_layout = QVBoxLayout(self.step_view_group)
        
        # 创建节点图场景（GraphScene），用于管理节点和连线
        self.graph_scene = GraphScene()
        
        # 创建节点图视图（GraphView），用于显示场景内容
        self.graph_view = GraphView(self.graph_scene)
        
        # 将节点图视图添加到分组框
        step_view_layout.addWidget(self.graph_view)
        
        # 将执行步骤查看分组框添加到右侧面板布局
        right_layout.addWidget(self.step_view_group)
        
        # -------------------- 操作按钮组 --------------------
        
        # 创建操作按钮布局（水平布局）
        action_btn_layout = QHBoxLayout()
        
        # 添加弹簧，将按钮推到右侧
        action_btn_layout.addStretch()
        
        # 创建"开始当前任务"按钮（绿色背景）
        self.start_task_btn = QPushButton("开始当前任务")
        self.start_task_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #bdc3c7;
                font-weight: normal;
            }
        """)
        
        # 创建"停止当前任务"按钮（红色背景）
        self.stop_task_btn = QPushButton("停止当前任务")
        self.stop_task_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #ec7063;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #bdc3c7;
                font-weight: normal;
            }
        """)
        self.stop_task_btn.setEnabled(False)  # 初始状态禁用，任务未执行时不能停止
        
        # 创建"编辑执行步骤"按钮（蓝色背景）
        self.edit_steps_btn = QPushButton("编辑执行步骤")
        self.edit_steps_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 8px 20px;")
        
        # 创建"保存配置"按钮（蓝色背景）
        self.save_config_btn = QPushButton("保存配置")
        self.save_config_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 8px 20px;")
        
        # 将按钮添加到布局
        action_btn_layout.addWidget(self.start_task_btn)    # 开始按钮
        action_btn_layout.addWidget(self.stop_task_btn)     # 停止按钮
        action_btn_layout.addWidget(self.edit_steps_btn)    # 编辑步骤按钮
        
        # 添加弹簧，将保存按钮与其他按钮分开
        action_btn_layout.addStretch()
        
        action_btn_layout.addWidget(self.save_config_btn)   # 保存配置按钮
        
        # 将操作按钮布局添加到右侧面板布局
        right_layout.addLayout(action_btn_layout)
        
        # -------------------- 完成布局设置 --------------------
        
        # 将右侧面板添加到分隔器
        self.splitter.addWidget(right_panel)
        
        # 设置分隔器的初始宽度比例：左侧400px，右侧1000px
        self.splitter.setSizes([400, 1000])
        
        # 将分隔器添加到主布局
        main_layout.addWidget(self.splitter)
        
        # ==================== 信号与槽连接 ====================
        
        # 左侧面板按钮的信号连接
        self.new_task_btn.clicked.connect(self.on_new_flow)        # 新建任务
        self.open_task_btn.clicked.connect(self.on_open_flow)      # 打开任务
        self.save_task_btn.clicked.connect(lambda checked: self.on_save_flow())      # 保存任务
        self.copy_task_btn.clicked.connect(self.on_copy_task)      # 复制任务
        self.delete_task_btn.clicked.connect(self.on_delete_task)  # 删除任务
        self.clear_log_btn.clicked.connect(self.on_clear_log)      # 清空日志
        
        # 任务树的信号连接
        self.task_tree.itemClicked.connect(self.on_task_selected)       # 点击任务项
        self.task_tree.itemChanged.connect(self.on_task_name_changed)   # 任务名称修改
        
        # 右侧面板按钮的信号连接
        self.start_task_btn.clicked.connect(self.on_run_flow)    # 开始任务
        self.stop_task_btn.clicked.connect(self.on_stop_flow)    # 停止任务
        self.edit_steps_btn.clicked.connect(self.on_edit_steps)  # 编辑步骤
        self.save_config_btn.clicked.connect(lambda checked: self.on_save_flow())  # 保存配置
        
        # 加载默认任务（从resources目录读取保存的任务文件）
        self.load_default_tasks()
    
    def load_default_tasks(self):
        """
        加载默认任务方法: 从resources目录读取保存的任务文件
        
        执行流程:
            1. 确定resources目录路径（项目根目录下的resources文件夹）
            2. 如果目录不存在，创建目录并返回
            3. 遍历目录中所有.json文件
            4. 读取每个文件的内容，解析为任务数据
            5. 调用add_task_to_tree()将任务添加到任务列表
        """
        resources_dir = ensure_resources_dir()
        
        # 遍历resources目录中的所有文件
        for filename in os.listdir(resources_dir):
            # 只处理.json文件
            if filename.endswith(".json"):
                # 拼接文件的完整路径
                file_path = os.path.join(resources_dir, filename)
                
                try:
                    # 打开文件并读取内容
                    # 使用utf-8编码，确保中文正确显示
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # 将JSON字符串解析为Python字典
                        flow_data = json.load(f)
                    
                    # 构建任务字典，提取关键信息
                    task = {
                        "id": flow_data.get("id", str(uuid.uuid4())[:8]),  # 任务ID，取uuid的前8位
                        "name": flow_data.get("name", os.path.splitext(filename)[0]),  # 任务名称，默认使用文件名（不含扩展名）
                        "status": flow_data.get("status", "已停止"),  # 任务状态
                        "nodes": flow_data.get("nodes", []),  # 节点列表
                        "edges": flow_data.get("edges", []),  # 连线列表
                        "schedule": flow_data.get("schedule", {}),
                        "file_path": file_path  # 文件路径，用于保存时使用
                    }
                    
                    # 将任务添加到任务列表树中
                    self.add_task_to_tree(task)
                except Exception as e:
                    # 如果加载失败，打印错误信息（不中断程序）
                    print(f"加载任务文件失败: {filename} - {str(e)}")
    
    def add_task_to_tree(self, task):
        """
        添加任务到任务树方法: 创建任务列表项并显示在任务树中
        
        每个任务项包含:
            第0列: 任务名称（可编辑）
            第1列: 操作按钮组（状态图标、保存图标、删除图标）
        
        参数:
            task: 任务字典，包含任务的所有信息
        """
        # 创建一个树形控件项（QTreeWidgetItem）
        # 这个项会显示在task_tree中
        item = QTreeWidgetItem(self.task_tree)
        
        # 设置第0列的文本为任务名称
        item.setText(0, task["name"])
        
        # 将任务字典存储到项的Qt.UserRole中
        # Qt.UserRole是一个自定义数据角色，用于存储额外的数据
        # 这样在需要时可以通过item.data(0, Qt.UserRole)获取完整的任务数据
        item.setData(0, Qt.UserRole, task)
        
        # 设置项的标志，添加Qt.ItemIsEditable标志
        # 这样用户可以双击任务名称进行编辑
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        
        # 获取任务状态
        status = task["status"]
        
        # ==================== 创建操作列的控件 ====================
        
        # 创建一个容器控件，用于放置操作按钮组
        widget = QWidget()
        
        # 创建水平布局，用于排列操作按钮
        widget_layout = QHBoxLayout(widget)
        
        # 设置布局的外边距为2像素
        widget_layout.setContentsMargins(2, 2, 2, 2)
        
        # 设置按钮之间的间距为2像素
        widget_layout.setSpacing(2)
        
        # -------------------- 状态按钮（圆形图标） --------------------
        
        # 创建状态按钮，用于显示任务状态并控制执行/停止
        status_btn = QPushButton()
        
        # 设置按钮固定大小为20x20像素，做成圆形
        status_btn.setFixedSize(20, 20)
        
        # 根据任务状态设置按钮样式
        if "执行中" in status:
            # 执行中状态：绿色圆形
            status_btn.setStyleSheet("""
                QPushButton {
                    border: none;              /* 无边框 */
                    background-color: #4caf50; /* 绿色背景 */
                    border-radius: 10px;       /* 圆角半径为10，即圆形 */
                }
                QPushButton:hover {
                    background-color: #45a049; /* 鼠标悬停时颜色稍深 */
                }
            """)
            # 设置鼠标悬停提示
            status_btn.setToolTip("点击停止任务")
        else:
            # 非执行中状态：红色圆形
            status_btn.setStyleSheet("""
                QPushButton {
                    border: none;              /* 无边框 */
                    background-color: #e74c3c; /* 红色背景 */
                    border-radius: 10px;       /* 圆角半径为10，即圆形 */
                }
                QPushButton:hover {
                    background-color: #c0392b; /* 鼠标悬停时颜色稍深 */
                }
            """)
            # 设置鼠标悬停提示
            status_btn.setToolTip("点击执行任务")
        
        # 连接状态按钮的点击信号到on_toggle_task方法
        # 使用lambda表达式传递task参数
        status_btn.clicked.connect(lambda checked, t=task: self.on_toggle_task(t))
        
        # -------------------- 保存按钮（图标） --------------------
        
        # 创建保存按钮
        save_btn = QPushButton()
        
        # 设置按钮图标为"document-save"（系统主题中的保存图标）
        # 如果系统中没有这个图标，则使用空图标
        save_btn.setIcon(QIcon.fromTheme("document-save", QIcon()))
        
        # 设置按钮样式（透明背景，鼠标悬停时显示浅蓝色背景）
        save_btn.setStyleSheet("""
            QPushButton {
                border: none;              /* 无边框 */
                padding: 2px;              /* 内边距 */
                background: transparent;   /* 透明背景 */
                color: #3498db;            /* 蓝色文字（如果有） */
            }
            QPushButton:hover {
                background-color: #e8f4fd; /* 鼠标悬停时浅蓝色背景 */
                border-radius: 3px;        /* 圆角 */
            }
        """)
        
        # 设置鼠标悬停提示
        save_btn.setToolTip("保存任务")
        
        # 连接保存按钮的点击信号到on_save_flow方法
        save_btn.clicked.connect(lambda checked, t=task: self.on_save_flow(t))
        
        # -------------------- 删除按钮（图标） --------------------
        
        # 创建删除按钮
        delete_btn = QPushButton()
        
        # 设置按钮图标为"edit-delete"（系统主题中的删除图标）
        delete_btn.setIcon(QIcon.fromTheme("edit-delete", QIcon()))
        
        # 设置按钮样式（透明背景，鼠标悬停时显示浅红色背景）
        delete_btn.setStyleSheet("""
            QPushButton {
                border: none;              /* 无边框 */
                padding: 2px;              /* 内边距 */
                background: transparent;   /* 透明背景 */
                color: #e74c3c;            /* 红色文字（如果有） */
            }
            QPushButton:hover {
                background-color: #fce4ec; /* 鼠标悬停时浅红色背景 */
                border-radius: 3px;        /* 圆角 */
            }
        """)
        
        # 设置鼠标悬停提示
        delete_btn.setToolTip("删除任务")
        
        # 连接删除按钮的点击信号到on_delete_task方法
        delete_btn.clicked.connect(lambda checked, t=task: self.on_delete_task(t))
        
        # ==================== 将按钮添加到布局 ====================
        
        # 将三个按钮添加到操作列的布局中
        widget_layout.addWidget(status_btn)  # 状态按钮（最左边）
        widget_layout.addWidget(save_btn)    # 保存按钮
        widget_layout.addWidget(delete_btn)  # 删除按钮（最右边）
        
        # 将操作列的容器控件设置到树形控件的第1列
        # 参数: (项, 列索引, 控件)
        self.task_tree.setItemWidget(item, 1, widget)
    
    def apply_stylesheet(self):
        """
        应用样式表方法: 为整个主窗口设置统一的视觉风格
        
        样式表使用Qt的样式表语法（类似CSS），定义了以下控件的外观:
            - QMainWindow: 主窗口背景色
            - QGroupBox: 分组框样式（边框、圆角、标题位置）
            - QPushButton: 按钮样式（默认状态和悬停状态）
            - QTreeWidget: 树形控件样式（边框、行高、选中状态等）
            - QTableWidget: 表格控件样式（边框、单元格、选中状态）
            - QHeaderView: 表头样式（背景色、边框）
            - QTextEdit: 文本编辑控件样式（深色背景，类似终端）
        """
        self.setStyleSheet("""
            /* 主窗口样式 */
            QMainWindow {
                background-color: #f5f7fa;  /* 浅灰色背景 */
            }
            /* 分组框样式 */
            QGroupBox {
                font-weight: bold;           /* 标题加粗 */
                border: 1px solid #ddd;      /* 灰色边框 */
                border-radius: 6px;          /* 圆角 */
                margin-top: 6px;             /* 顶部外边距 */
                padding-top: 10px;           /* 顶部内边距 */
            }
            /* 分组框标题样式 */
            QGroupBox::title {
                subcontrol-origin: margin;   /* 从外边距开始定位 */
                left: 2px;                  /* 距离左边2像素 */
                padding: 0 2px 0 2px;       /* 左右各2像素内边距 */
            }
            /* 按钮样式 */
            QPushButton {
                padding: 5px 15px;          /* 内边距（上下5px，左右15px） */
                border-radius: 4px;          /* 圆角 */
                border: 1px solid #ccc;      /* 灰色边框 */
                background-color: #ffffff;   /* 白色背景 */
            }
            /* 按钮悬停样式 */
            QPushButton:hover {
                background-color: #f0f0f0;  /* 浅灰色背景 */
            }
            /* 树形控件样式 */
            QTreeWidget {
                border: 1px solid #ddd;      /* 灰色边框 */
                border-radius: 4px;          /* 圆角 */
                alternate-background-color: #f9f9f9;  /* 交替行背景色 */
                show-decoration-selected: 1;  /* 选中时显示装饰 */
            }
            /* 树形控件项样式 */
            QTreeWidget::item {
                padding: 6px 4px;           /* 内边距 */
                height: 28px;               /* 行高 */
            }
            /* 树形控件项编辑状态样式 */
            QTreeWidget::item:edit {
                background-color: #ffffff;   /* 白色背景 */
                color: #000000;              /* 黑色文字 */
            }
            /* 树形控件项选中状态样式 */
            QTreeWidget::item:selected {
                background-color: #3498db;   /* 蓝色背景 */
                color: white;                /* 白色文字 */
            }
            /* 树形控件项选中且编辑状态样式 */
            QTreeWidget::item:selected:edit {
                background-color: #ffffff;   /* 白色背景（编辑时不显示选中色） */
                color: #000000;              /* 黑色文字 */
            }
            /* 树形控件中的输入框样式 */
            QTreeWidget QLineEdit {
                background-color: #ffffff;   /* 白色背景 */
                color: #000000;              /* 黑色文字 */
                border: 1px solid #3498db;   /* 蓝色边框 */
                padding: 2px;               /* 内边距 */
                margin: 1px;                /* 外边距 */
            }
            /* 表格控件样式 */
            QTableWidget {
                border: 1px solid #ddd;      /* 灰色边框 */
                border-radius: 4px;          /* 圆角 */
                gridline-color: #eee;        /* 网格线颜色 */
            }
            /* 表格单元格样式 */
            QTableWidget::item {
                padding: 5px;               /* 内边距 */
            }
            /* 表格单元格选中样式 */
            QTableWidget::item:selected {
                background-color: #3498db;   /* 蓝色背景 */
                color: white;                /* 白色文字 */
            }
            /* 表头样式 */
            QHeaderView::section {
                background-color: #f8f9fa;   /* 浅灰色背景 */
                padding: 5px;               /* 内边距 */
                border: 1px solid #ddd;      /* 灰色边框 */
            }
            /* 文本编辑控件样式（用于日志显示） */
            QTextEdit {
                border: 1px solid #ddd;      /* 灰色边框 */
                border-radius: 4px;          /* 圆角 */
                background-color: #1e1e1e;   /* 深色背景（类似终端） */
                color: #d4d4d4;              /* 浅色文字 */
                font-family: Consolas, Monaco, monospace;  /* 等宽字体 */
                font-size: 12px;             /* 字体大小 */
            }
            /* 输入控件样式（输入框、下拉框、数字输入框） */
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 5px;               /* 内边距 */
                border: 1px solid #ddd;      /* 灰色边框 */
                border-radius: 4px;          /* 圆角 */
            }
            /* 输入控件获得焦点时的样式 */
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #3498db;       /* 蓝色边框 */
            }
        """)
    
    @Slot()
    def on_new_flow(self):
        """
        新建任务方法: 创建一个新的自动化任务
        
        执行流程:
            1. 弹出输入对话框，让用户输入任务名称
            2. 如果用户输入了名称，使用用户输入的名称
            3. 如果用户取消或未输入，自动生成名称（如"任务_1"）
            4. 创建任务字典
            5. 将任务添加到任务树
            6. 自动选中新创建的任务
            7. 更新状态栏和日志
        """
        # 弹出输入对话框，让用户输入任务名称
        # 参数: (父窗口, 对话框标题, 提示文字)
        # 返回值: (用户输入的文本, 是否点击了确定按钮)
        flow_name, ok = QInputDialog.getText(self, "新建任务", "输入任务名称:")
        
        # 判断用户是否点击了确定且输入了内容
        if ok and flow_name.strip():
            # 使用用户输入的名称（去除首尾空格）
            name = flow_name.strip()
        else:
            # 如果用户取消或未输入，自动生成名称
            # 计算当前任务树中的任务数量，生成"任务_1"、"任务_2"等
            name = f"任务_{len(self.task_tree.findItems('', Qt.MatchContains)) + 1}"
        
        # 创建任务字典
        task = {
            "id": str(uuid.uuid4())[:8],  # 生成唯一ID（取uuid前8位）
            "name": name,                  # 任务名称
            "status": "已停止",             # 初始状态为"已停止"
            "steps": [],                   # 步骤列表（初始为空）
            "file_path": None              # 文件路径（尚未保存，为None）
        }
        
        # 将任务添加到任务树
        self.add_task_to_tree(task)
        
        # 自动选中新创建的任务
        # topLevelItemCount()获取顶层项数量，-1表示最后一个
        self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
        
        # 更新状态栏显示
        self.status_label.setText(f"已新建任务: {name}")
        
        # 在日志面板中添加记录
        self.log_panel.append(f"新建任务: {name}")
    
    @Slot()
    def on_copy_task(self):
        """
        复制任务方法: 复制当前选中的任务
        
        执行流程:
            1. 获取当前选中的任务项
            2. 如果没有选中任务，弹出警告
            3. 获取原任务的数据
            4. 创建新任务（ID不同，名称加"(复制)"后缀）
            5. 将新任务添加到任务树
            6. 自动选中新复制的任务
            7. 更新状态栏和日志
        """
        # 获取当前选中的任务项
        current_item = self.task_tree.currentItem()
        
        # 如果没有选中任何任务，弹出警告对话框
        if not current_item:
            QMessageBox.warning(self, "复制失败", "请先选择一个任务")
            return
        
        # 获取原任务的数据（从Qt.UserRole中取出）
        task = current_item.data(0, Qt.UserRole)
        
        # 创建新任务，复制原任务的所有数据
        new_task = {
            "id": str(uuid.uuid4())[:8],              # 生成新的唯一ID
            "name": task["name"] + " (复制)",          # 名称加上"(复制)"后缀
            "status": "已停止",                        # 新任务初始状态为"已停止"
            "steps": [dict(s) for s in task.get("steps", [])],  # 深拷贝步骤列表
            "file_path": None                         # 新任务尚未保存
        }
        
        # 将新任务添加到任务树
        self.add_task_to_tree(new_task)
        
        # 自动选中新复制的任务
        self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
        
        # 更新状态栏显示
        self.status_label.setText(f"已复制任务: {new_task['name']}")
        
        # 在日志面板中添加记录
        self.log_panel.append(f"复制任务: {new_task['name']}")
    
    @Slot()
    def on_delete_task(self, task=None):
        """
        删除任务方法: 删除指定的任务
        
        参数:
            task: 可选参数，如果提供则删除该任务；如果为None则删除当前选中的任务
        
        执行流程:
            1. 如果没有提供task参数，获取当前选中的任务
            2. 如果提供了task参数，在任务树中查找对应的项
            3. 如果没有找到任务，弹出警告
            4. 弹出确认对话框，让用户确认是否删除
            5. 如果用户确认，删除任务并更新界面
        """
        # 判断是否提供了task参数
        if task is None:
            # 没有提供task参数，获取当前选中的任务项
            current_item = self.task_tree.currentItem()
            
            # 如果没有选中任何任务，弹出警告
            if not current_item:
                QMessageBox.warning(self, "删除失败", "请先选择一个任务")
                return
            
            # 获取任务数据
            task = current_item.data(0, Qt.UserRole)
        else:
            # 提供了task参数，需要在任务树中查找对应的项
            current_item = None
            
            # 遍历所有顶层项，查找匹配的任务
            for i in range(self.task_tree.topLevelItemCount()):
                item = self.task_tree.topLevelItem(i)
                if item.data(0, Qt.UserRole) == task:
                    current_item = item
                    break
            
            # 如果没有找到匹配的任务，弹出警告
            if not current_item:
                QMessageBox.warning(self, "删除失败", "未找到任务")
                return
        
        # 弹出确认对话框，让用户确认是否删除
        # 参数: (父窗口, 标题, 提示文字, 按钮选项, 默认按钮)
        reply = QMessageBox.question(
            self, "确认删除", f"确定要删除任务 '{task['name']}' 吗？",
            QMessageBox.Yes | QMessageBox.No,  # 显示"是"和"否"按钮
            QMessageBox.No                     # 默认选中"否"按钮
        )
        
        # 如果用户点击了"是"按钮
        if reply == QMessageBox.Yes:
            # 获取任务项在任务树中的索引
            index = self.task_tree.indexOfTopLevelItem(current_item)
            
            # 如果索引有效（不是-1）
            if index != -1:
                # 从任务树中移除该项
                self.task_tree.takeTopLevelItem(index)
                
                # 更新状态栏显示
                self.status_label.setText(f"已删除任务: {task['name']}")
                
                # 在日志面板中添加记录
                self.log_panel.append(f"删除任务: {task['name']}")
                
                # 清空节点图场景
                self.graph_scene.clear_all()
                
                # 清空任务名称输入框
                self.task_name_edit.clear()
                
                # 重置任务状态标签
                self.task_status_label.setText("已停止")
                self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
    
    @Slot(QTreeWidgetItem, int)
    def on_task_name_changed(self, item, column):
        """
        任务名称修改方法: 当用户编辑任务名称后自动同步更新
        
        触发时机: 当用户双击任务名称进行编辑并按下回车键时触发
        
        参数:
            item: 被修改的树形控件项
            column: 被修改的列索引（0表示任务名称列）
        """
        # 只处理第0列（任务名称列）的修改
        if column == 0:
            # 获取任务数据
            task = item.data(0, Qt.UserRole)
            
            if task:
                # 保存旧名称
                old_name = task["name"]
                
                # 获取新名称（从树形控件项的文本）
                new_name = item.text(0)
                
                # 更新任务字典中的名称
                task["name"] = new_name
                
                # 将更新后的任务数据重新存储到树形控件项中
                item.setData(0, Qt.UserRole, task)
                
                # 在日志面板中添加记录
                self.log_panel.append(f"任务重命名: {old_name} -> {new_name}")
                
                # 如果右侧面板中的任务名称输入框显示的是旧名称，同步更新为新名称
                if self.task_name_edit.text() == old_name:
                    self.task_name_edit.setText(new_name)
    
    @Slot()
    def on_open_flow(self):
        """
        打开任务方法: 从文件加载已保存的任务
        
        执行流程:
            1. 确定resources目录路径
            2. 如果目录不存在，创建目录
            3. 弹出文件选择对话框，让用户选择JSON文件
            4. 如果用户选择了文件，读取文件内容
            5. 解析JSON数据，创建任务字典
            6. 将任务添加到任务树
            7. 加载节点图和定时设置
            8. 更新状态栏和日志
        """
        resources_dir = ensure_resources_dir()
        
        # 弹出文件选择对话框
        # 参数: (父窗口, 对话框标题, 默认目录, 文件过滤器)
        # 返回值: (选中的文件路径, 文件过滤器)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开任务文件", resources_dir, "JSON文件 (*.json)"
        )
        
        # 如果用户选择了文件
        if file_path:
            try:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    # 将JSON字符串解析为Python字典
                    flow_data = json.load(f)
                
                # 获取任务名称（优先使用文件中保存的名称，否则使用文件名）
                flow_name = flow_data.get("name", os.path.basename(file_path))
                
                # 创建任务字典
                task = {
                    "id": flow_data.get("id", str(uuid.uuid4())[:8]),           # 任务ID
                    "name": flow_name,                                           # 任务名称
                    "status": "已停止",                                           # 初始状态
                    "nodes": flow_data.get("nodes", []),                         # 节点列表
                    "edges": flow_data.get("edges", []),                         # 连线列表
                    "schedule": flow_data.get("schedule", {}),
                    "file_path": file_path                                       # 文件路径
                }
                
                # 将任务添加到任务树
                self.add_task_to_tree(task)
                
                # 自动选中新打开的任务
                self.task_tree.setCurrentItem(self.task_tree.topLevelItem(self.task_tree.topLevelItemCount() - 1))
                
                # 更新右侧面板的任务名称输入框
                self.task_name_edit.setText(flow_name)
                
                # 加载节点图数据到场景中
                self.load_nodes_from_flow(flow_data)
                
                # 加载定时设置到右侧面板
                self.load_schedule_settings(task)
                
                # 更新状态栏显示
                self.status_label.setText(f"打开任务: {flow_name}")
                
                # 在日志面板中添加记录
                self.log_panel.append(f"打开任务: {flow_name}")
            except Exception as e:
                # 如果打开失败，弹出警告对话框
                QMessageBox.warning(self, "打开失败", f"无法打开任务文件: {str(e)}")

    def load_schedule_settings(self, task):
        schedule_config = task.get("schedule", {})
        self.schedule_panel.load_config(schedule_config)
    
    @Slot()
    def on_save_flow(self, task=None):
        """
        保存任务方法: 将任务保存到JSON文件
        
        参数:
            task: 可选参数，如果提供则保存该任务；如果为None则保存当前选中的任务
        
        执行流程:
            1. 如果没有提供task参数，获取当前选中的任务
            2. 如果提供了task参数，在任务树中查找对应的项
            3. 获取任务的文件路径
            4. 如果没有文件路径（新任务），弹出保存对话框
            5. 将任务数据（节点图、定时设置等）保存到文件
            6. 更新任务信息和界面
        """
        # 判断是否提供了task参数
        if task is None:
            # 没有提供task参数，获取当前选中的任务项
            current_item = self.task_tree.currentItem()
            
            # 如果没有选中任何任务，尝试使用当前流程
            if not current_item:
                if self.current_flow:
                    task = self.current_flow
                    # 尝试在任务树中查找对应的项
                    for i in range(self.task_tree.topLevelItemCount()):
                        item = self.task_tree.topLevelItem(i)
                        if item.data(0, Qt.UserRole) == task:
                            current_item = item
                            break
                else:
                    QMessageBox.warning(self, "保存失败", "请先选择一个任务")
                    return
            
            # 获取任务数据
            task = current_item.data(0, Qt.UserRole) if current_item else self.current_flow
        else:
            # 提供了task参数，需要在任务树中查找对应的项
            current_item = None
            
            # 遍历所有顶层项，查找匹配的任务
            for i in range(self.task_tree.topLevelItemCount()):
                item = self.task_tree.topLevelItem(i)
                if item.data(0, Qt.UserRole) == task:
                    current_item = item
                    break
        
        # 如果仍然没有找到任务，弹出警告
        if not task:
            QMessageBox.warning(self, "保存失败", "未找到任务数据")
            return
        
        # 获取任务的文件路径
        file_path = task.get("file_path")
        
        # 如果任务还没有文件路径（新创建的任务）
        if not file_path:
            resources_dir = ensure_resources_dir()
            
            # 确定默认文件名（优先使用右侧面板中的名称）
            default_name = self.task_name_edit.text() or task.get("name", "未命名任务")
            
            # 构建默认文件路径
            default_path = os.path.join(resources_dir, f"{default_name}.json")
            
            # 弹出保存对话框，让用户选择保存位置
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存任务文件", default_path, "JSON文件 (*.json)"
            )
        
        # 如果用户选择了文件路径
        if file_path:
            try:
                # 始终从 graph_scene 获取最新的节点和连线数据
                # 这样可以确保保存的是用户通过节点编辑器修改后的最新配置
                nodes = []
                edges = []
                
                if hasattr(self, 'graph_scene') and self.graph_scene:
                    graph_data = self.graph_scene.to_json()
                    if isinstance(graph_data, dict):
                        nodes = graph_data.get("nodes", [])
                        edges = graph_data.get("edges", [])
                
                # 如果 graph_scene 为空，回退到 task 中的数据
                if not nodes:
                    nodes = task.get("nodes", [])
                if not edges:
                    edges = task.get("edges", [])
                
                # 构建保存数据字典
                save_data = {
                    "id": task.get("id", ""),                              # 任务ID
                    "name": self.task_name_edit.text() or task.get("name", ""),  # 任务名称（优先使用右侧面板中的名称）
                    "version": "1.0",                                      # 版本号
                    "status": task.get("status", "已停止"),                  # 任务状态
                    "nodes": nodes,                                        # 节点列表
                    "edges": edges,                                        # 连线列表
                    "schedule": self.schedule_panel.get_config()
                }
                
                # 打开文件并写入内容
                # indent=2: 格式化输出，每个层级缩进2个空格
                # ensure_ascii=False: 保留中文，不转义为ASCII编码
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, indent=2, ensure_ascii=False)
                
                # 更新任务字典中的信息
                task["file_path"] = file_path  # 更新文件路径
                task["name"] = save_data["name"]  # 更新名称
                task["nodes"] = save_data["nodes"]  # 更新节点
                task["edges"] = save_data["edges"]  # 更新连线
                
                # 如果有对应的任务树项，更新任务树中的显示
                if current_item:
                    # 更新任务树中的任务名称显示
                    current_item.setText(0, save_data["name"])
                    
                    # 将更新后的任务数据重新存储到树形控件项中
                    current_item.setData(0, Qt.UserRole, task)
                
                # 更新状态栏显示
                self.status_label.setText(f"已保存: {os.path.basename(file_path)}")
                
                # 在日志面板中添加记录
                self.log_panel.append(f"保存任务: {save_data['name']}")
            except Exception as e:
                # 如果保存失败，弹出警告对话框
                QMessageBox.warning(self, "保存失败", f"无法保存任务文件: {str(e)}")
    
    @Slot()
    def on_run_flow(self):
        """
        运行任务方法: 开始执行当前选中的任务
        
        执行流程:
            1. 获取当前选中的任务项
            2. 如果没有选中任务，弹出警告
            3. 获取任务数据
            4. 调用_start_task()开始执行任务
        """
        # 获取当前选中的任务项
        current_item = self.task_tree.currentItem()
        
        # 如果没有选中任何任务，弹出警告
        if not current_item:
            QMessageBox.warning(self, "运行失败", "请先选择一个任务")
            return
        
        # 获取任务数据
        task = current_item.data(0, Qt.UserRole)
        
        # 调用_start_task()方法开始执行任务
        self._start_task(task, current_item)
    
    def _start_task(self, task, item=None):
        """
        启动任务方法: 内部方法，设置任务为执行状态并调用执行引擎
        
        参数:
            task: 任务字典
            item: 任务树中的项（可选）
        
        执行流程:
            1. 如果没有提供item参数，获取当前选中的任务项
            2. 更新任务状态为"执行中"
            3. 更新任务树中的状态图标
            4. 更新右侧面板的状态显示
            5. 更新状态栏和日志
            6. 加载任务数据到执行引擎并启动执行
            7. 发出flow_started信号
        """
        # 如果没有提供item参数，获取当前选中的任务项
        if item is None:
            item = self.task_tree.currentItem()
            if not item:
                return
        
        # 更新任务状态为"执行中"
        task["status"] = "执行中"
        
        # 更新当前选中的任务
        self.current_flow = task
        
        # 将更新后的任务数据重新存储到树形控件项中
        item.setData(0, Qt.UserRole, task)
        
        # 更新任务树中的状态图标（绿色圆形）
        self._update_status_widget(item, "执行中")
        
        # 更新右侧面板的任务状态标签
        self.task_status_label.setText("执行中")
        self.task_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")  # 绿色文字
        
        # 更新状态栏显示
        self.status_label.setText("运行中...")
        
        # 在日志面板中添加记录
        self.log_panel.append(f"开始执行任务: {task['name']}")
        
        # 禁用开始按钮，启用停止按钮
        self.start_task_btn.setEnabled(False)
        self.stop_task_btn.setEnabled(True)
        
        # 构建完整的flow数据（节点图格式）
        flow_data = {
            "id": task["id"],
            "name": task["name"],
            "version": task.get("version", "1.0"),
            "nodes": task.get("nodes", []),
            "edges": task.get("edges", []),
            "schedule": task.get("schedule", {})
        }
        
        # 加载任务数据到执行引擎
        self.engine.load_flow(flow_data)
        
        # 注册任务完成回调
        self.engine.add_completed_callback(self._on_task_completed)
        
        # 启动执行引擎（在后台线程中执行）
        self.engine.run()
        
        # 发出flow_started信号，通知其他组件任务已开始执行
        self.flow_started.emit()
    
    def _on_engine_log(self, log_entry: str):
        """
        引擎日志回调方法: 当执行引擎产生日志时被调用
        
        参数:
            log_entry: 日志条目字符串
            
        注意: 此方法在后台线程中执行，不能直接更新GUI控件
              需要通过Qt信号机制切换到主线程更新GUI
        """
        # 通过信号机制将日志传递到主线程
        self.log_received.emit(log_entry)
    
    @Slot(str)
    def _on_log_received(self, log_entry: str):
        """
        日志接收槽方法: 在主线程中更新GUI日志面板
        
        参数:
            log_entry: 日志条目字符串
            
        注意: 此方法通过Qt信号机制在主线程中执行，可以安全地更新GUI控件
        """
        # 将日志添加到日志面板
        self.log_panel.append(log_entry)
    
    def _on_task_completed(self, success: bool, error_message: str):
        """
        任务完成回调方法: 当执行引擎任务完成时被调用
        
        参数:
            success: 是否执行成功
            error_message: 错误信息（如果失败）
            
        注意: 此方法在后台线程中执行，不能直接更新GUI控件
              需要通过Qt信号机制切换到主线程更新GUI
        """
        # 通过信号机制将任务完成通知传递到主线程
        self.task_completed.emit(success, error_message)
    
    @Slot(bool, str)
    def _on_task_completed_slot(self, success: bool, error_message: str):
        """
        任务完成槽方法: 在主线程中处理任务完成逻辑
        
        参数:
            success: 是否执行成功
            error_message: 错误信息（如果失败）
            
        注意: 此方法通过Qt信号机制在主线程中执行，可以安全地更新GUI控件
        """
        # 如果有当前任务，更新状态为"已停止"
        if self.current_flow:
            current_item = None
            # 查找当前任务在任务树中的项
            for i in range(self.task_tree.topLevelItemCount()):
                item = self.task_tree.topLevelItem(i)
                if item.data(0, Qt.UserRole) == self.current_flow:
                    current_item = item
                    break
            
            if current_item:
                # 更新任务状态为"已停止"
                self.current_flow["status"] = "已停止"
                current_item.setData(0, Qt.UserRole, self.current_flow)
                
                # 更新任务树中的状态图标（红色圆形）
                self._update_status_widget(current_item, "已停止")
                
                # 更新右侧面板的任务状态标签
                self.task_status_label.setText("已停止")
                self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        
        # 更新状态栏显示
        if success:
            self.status_label.setText("任务执行完成")
            self.log_panel.append("任务执行完成")
        else:
            self.status_label.setText("任务执行异常")
            self.log_panel.append(f"任务执行异常: {error_message}")
        
        # 启用开始按钮，禁用停止按钮
        self.start_task_btn.setEnabled(True)
        self.stop_task_btn.setEnabled(False)
        
        # 发出flow_stopped信号，通知其他组件任务已停止
        self.flow_stopped.emit()
    
    @Slot()
    def _on_start_scheduled(self):
        """
        启动定时任务：读取 SchedulePanel 配置，加入 TaskScheduler 执行
        """
        from core.scheduler import TaskScheduler

        if self.current_flow is None:
            QMessageBox.warning(self, "启动失败", "请先选择一个任务")
            return

        config = self.schedule_panel.get_config()
        if config is None:
            return

        trigger_type = config["trigger_type"]
        params = config["params"]

        if trigger_type == "immediate":
            QMessageBox.information(self, "定时任务", "立即执行任务已启动")
            self.on_run_flow()
            return

        self.scheduler = TaskScheduler()
        self.scheduler.add_task(
            task_id=self.current_flow.get("id", "scheduled"),
            name=self.current_flow.get("name", "定时任务"),
            trigger_type=trigger_type,
            func=lambda: self.on_run_flow(),
            **params
        )
        self.scheduler.start()
        self.log_panel.append(f"定时任务已启动: {trigger_type}")
        self.task_status_label.setText("定时中")

        self.start_scheduled_btn = self.schedule_panel.start_scheduled_btn
        self.start_scheduled_btn.setText("■ 停止定时")
        self.start_scheduled_btn.setStyleSheet(
            "QPushButton {"
            "  background-color: #ff4d4f; color: white; border: none;"
            "  border-radius: 4px; padding: 4px 14px; font-size: 13px;"
            "  font-weight: bold;"
            "}"
            "QPushButton:hover { background-color: #ff7875; }"
            "QPushButton:pressed { background-color: #d9363e; }"
        )
        self.start_scheduled_btn.clicked.disconnect()
        self.start_scheduled_btn.clicked.connect(self._on_stop_scheduled)

    def _on_stop_scheduled(self):
        """停止定时任务"""
        if hasattr(self, 'scheduler') and self.scheduler:
            self.scheduler.stop()
            self.scheduler = None
        self.log_panel.append("定时任务已停止")
        self.task_status_label.setText("已停止")

        self.start_scheduled_btn = self.schedule_panel.start_scheduled_btn
        self.start_scheduled_btn.setText("▶ 开始定时")
        self.start_scheduled_btn.setStyleSheet(
            "QPushButton {"
            "  background-color: #1890ff; color: white; border: none;"
            "  border-radius: 4px; padding: 4px 14px; font-size: 13px;"
            "  font-weight: bold;"
            "}"
            "QPushButton:hover { background-color: #40a9ff; }"
            "QPushButton:pressed { background-color: #096dd9; }"
        )
        self.start_scheduled_btn.clicked.disconnect()
        self.start_scheduled_btn.clicked.connect(lambda: self.schedule_panel.start_scheduled.emit())

    @Slot()
    def on_stop_flow(self):
        """
        停止任务方法: 停止当前选中的任务
        
        执行流程:
            1. 获取当前选中的任务项
            2. 如果有选中的任务，获取任务数据
            3. 调用_stop_task()停止任务
        """
        # 获取当前选中的任务项
        current_item = self.task_tree.currentItem()
        
        # 如果有选中的任务
        if current_item:
            # 获取任务数据
            task = current_item.data(0, Qt.UserRole)
            
            # 调用_stop_task()方法停止任务
            self._stop_task(task, current_item)
    
    def _stop_task(self, task, item=None):
        """
        停止任务方法: 内部方法，设置任务为停止状态并调用执行引擎停止
        
        参数:
            task: 任务字典
            item: 任务树中的项（可选）
        
        执行流程:
            1. 如果没有提供item参数，获取当前选中的任务项
            2. 调用执行引擎停止执行
            3. 更新任务状态为"已停止"
            4. 更新任务树中的状态图标
            5. 更新右侧面板的状态显示
            6. 更新状态栏和日志
            7. 发出flow_stopped信号
        """
        # 如果没有提供item参数，获取当前选中的任务项
        if item is None:
            item = self.task_tree.currentItem()
            if not item:
                return
        
        # 调用执行引擎停止执行
        self.engine.stop()
        
        # 更新任务状态为"已停止"
        task["status"] = "已停止"
        
        # 将更新后的任务数据重新存储到树形控件项中
        item.setData(0, Qt.UserRole, task)
        
        # 更新任务树中的状态图标（红色圆形）
        self._update_status_widget(item, "已停止")
        
        # 更新右侧面板的任务状态标签
        self.task_status_label.setText("已停止")
        self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")  # 红色文字
        
        # 更新状态栏显示
        self.status_label.setText("已停止")
        
        # 在日志面板中添加记录
        self.log_panel.append(f"停止任务: {task['name']}")
        
        # 启用开始按钮，禁用停止按钮
        self.start_task_btn.setEnabled(True)
        self.stop_task_btn.setEnabled(False)
        
        # 发出flow_stopped信号，通知其他组件任务已停止
        self.flow_stopped.emit()
    
    def _update_status_widget(self, item, status):
        """
        更新状态控件方法: 更新任务树中操作列的状态图标
        
        参数:
            item: 任务树中的项
            status: 任务状态（"执行中"或"已停止"）
        
        执行流程:
            1. 获取操作列的容器控件
            2. 查找状态按钮（第一个QPushButton）
            3. 根据状态设置按钮样式（绿色圆形或红色圆形）
            4. 更新按钮的提示文字
        """
        # 获取操作列（第1列）的容器控件
        widget = self.task_tree.itemWidget(item, 1)
        
        # 如果找到了控件
        if widget:
            # 查找第一个QPushButton（即状态按钮）
            btn = widget.findChild(QPushButton)
            
            # 如果找到了状态按钮
            if btn:
                # 根据状态设置按钮样式
                if "执行中" in status:
                    # 执行中状态：绿色圆形
                    btn.setStyleSheet("""
                        QPushButton {
                            border: none;              /* 无边框 */
                            background-color: #4caf50; /* 绿色背景 */
                            border-radius: 10px;       /* 圆角半径为10，即圆形 */
                        }
                        QPushButton:hover {
                            background-color: #45a049; /* 鼠标悬停时颜色稍深 */
                        }
                    """)
                    # 更新按钮提示文字
                    btn.setToolTip("点击停止任务")
                else:
                    # 非执行中状态：红色圆形
                    btn.setStyleSheet("""
                        QPushButton {
                            border: none;              /* 无边框 */
                            background-color: #e74c3c; /* 红色背景 */
                            border-radius: 10px;       /* 圆角半径为10，即圆形 */
                        }
                        QPushButton:hover {
                            background-color: #c0392b; /* 鼠标悬停时颜色稍深 */
                        }
                    """)
                    # 更新按钮提示文字
                    btn.setToolTip("点击执行任务")
    
    @Slot()
    def on_toggle_task(self, task):
        """
        切换任务状态方法: 根据当前状态切换任务的执行/停止
        
        参数:
            task: 任务字典
        
        执行流程:
            1. 在任务树中查找对应的任务项
            2. 如果没有找到，直接返回
            3. 如果任务正在执行，调用_stop_task()停止任务
            4. 如果任务已停止，调用_start_task()开始执行任务
        """
        # 初始化任务项为None
        item = None
        
        # 遍历所有顶层项，查找匹配的任务
        for i in range(self.task_tree.topLevelItemCount()):
            tree_item = self.task_tree.topLevelItem(i)
            if tree_item.data(0, Qt.UserRole) == task:
                item = tree_item
                break
        
        # 如果没有找到匹配的任务，直接返回
        if not item:
            return
        
        # 判断任务当前状态
        if "执行中" in task.get("status", ""):
            # 如果任务正在执行，调用_stop_task()停止任务
            self._stop_task(task, item)
            # 更新右侧面板的状态显示
            self.task_status_label.setText("已停止")
            self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.status_label.setText("已停止")
            self.log_panel.append(f"停止执行任务: {task['name']}")
        else:
            self._start_task(task, item)
    
    @Slot(QTreeWidgetItem, int)
    def on_task_selected(self, item, column):
        """
        任务选中方法: 当用户点击任务列表中的任务时触发
        
        触发时机: 用户在任务树中点击某个任务项时触发
        
        参数:
            item: 被点击的任务项
            column: 被点击的列索引
        
        执行流程:
            1. 获取任务数据
            2. 更新当前选中的任务
            3. 更新右侧面板的任务名称和状态显示
            4. 根据状态设置状态标签颜色
            5. 加载节点图和定时设置
            6. 在日志中添加记录
        """
        # 获取任务数据
        task = item.data(0, Qt.UserRole)
        
        # 如果任务数据存在
        if task:
            # 更新当前选中的任务
            self.current_flow = task
            
            # 更新右侧面板的任务名称输入框
            self.task_name_edit.setText(task.get("name", ""))
            
            # 更新右侧面板的任务状态标签
            self.task_status_label.setText(task.get("status", "已停止"))
            
            # 获取任务状态
            status = task.get("status", "")
            
            # 根据状态设置状态标签的颜色
            if "执行中" in status:
                # 执行中：绿色文字
                self.task_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
            else:
                # 已停止：红色文字
                self.task_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            
            # 加载节点图数据到场景中
            self.load_nodes_from_flow(task)
            
            # 加载定时设置到右侧面板
            self.load_schedule_settings(task)
            
            # 在日志面板中添加记录
            self.log_panel.append(f"选择任务: {task['name']}")
    
    def load_steps_to_table(self, steps):
        """
        加载步骤到表格方法: 将步骤列表显示到步骤表格中（当前未使用）
        
        参数:
            steps: 步骤列表，每个步骤是一个字典
        
        执行流程:
            1. 清空表格所有行
            2. 遍历每个步骤，创建表格行
            3. 设置步骤类型、描述、参数、延迟等列的内容
            4. 应用步骤行的样式（根据类型显示不同颜色）
        """
        # 清空表格所有行
        self.step_table.setRowCount(0)
        
        # 遍历步骤列表
        for step in steps:
            # 获取当前表格行数（即新行的索引）
            row = self.step_table.rowCount()
            
            # 在表格中插入新行
            self.step_table.insertRow(row)
            
            # 获取步骤类型
            step_type = step.get("type", "")
            
            # 获取步骤类型的中文名称（从STEP_TYPE_MAP中查找）
            step_name = STEP_TYPE_MAP.get(step_type, step_type)
            
            # 获取步骤描述
            description = step.get("description", "")
            
            # 获取步骤参数
            params = step.get("params", {})
            
            # 处理参数和延迟时间
            if isinstance(params, dict):
                params_str = str(params)           # 将参数转换为字符串
                delay = params.get("delay", 0)     # 从参数中获取延迟时间
            else:
                params_str = str(params)           # 将参数转换为字符串
                delay = step.get("delay", 0)       # 从步骤中直接获取延迟时间
            
            # 创建表格单元格项
            type_item = QTableWidgetItem(step_name)    # 步骤类型
            desc_item = QTableWidgetItem(description)  # 步骤描述
            params_item = QTableWidgetItem(params_str) # 步骤参数
            delay_item = QTableWidgetItem(str(delay))  # 延迟时间
            
            # 设置单元格内容居中对齐
            type_item.setTextAlignment(Qt.AlignCenter)
            delay_item.setTextAlignment(Qt.AlignCenter)
            
            # 将步骤类型存储到单元格的Qt.UserRole中，供样式设置使用
            type_item.setData(Qt.UserRole, step_type)
            
            # 将单元格项设置到表格的对应位置
            self.step_table.setItem(row, 0, type_item)   # 第0列：步骤类型
            self.step_table.setItem(row, 1, desc_item)   # 第1列：步骤描述
            self.step_table.setItem(row, 2, params_item) # 第2列：步骤参数
            self.step_table.setItem(row, 3, delay_item)  # 第3列：延迟时间
            
            # 根据步骤类型应用行样式（不同类型显示不同颜色）
            self.apply_step_row_style(row)
    
    def apply_step_row_style(self, row):
        """
        应用步骤行样式方法: 根据步骤类型设置表格行的背景颜色（当前未使用）
        
        参数:
            row: 表格行索引
        
        颜色映射:
            - 鼠标操作（mouse_*）: 浅蓝色 (#b3e5fc)
            - 键盘输入（keyboard_type）: 浅绿色 (#c8e6c9)
            - 键盘按键（keyboard_press/hotkey）: 粉色 (#f8bbd9)
            - 图像操作（image_*）: 紫色 (#e1bee7)
            - 窗口操作（window_*）: 青色 (#b2dfdb)
            - Excel操作（excel_read）: 橙色 (#ffcc80)
            - 等待（wait）: 黄色 (#fff9c4)
            - 条件分支（if_else）: 红色 (#ffcdd2)
            - 循环（loop）: 灰色 (#e0e0e0)
            - 日志（log）: 浅灰色 (#f5f5f5)
            - 标签/跳转（label/goto）: 灰色 (#e0e0e0)
            - 变量操作（set/get_variable）: 蓝色 (#bbdefb)
        """
        # 获取第0列的单元格项（步骤类型）
        type_item = self.step_table.item(row, 0)
        
        # 获取步骤类型（从Qt.UserRole中取出）
        step_type = type_item.data(Qt.UserRole) if type_item else ""
        
        # 定义步骤类型到颜色的映射字典
        type_colors = {
            "mouse_click": "#b3e5fc",      # 鼠标点击 - 浅蓝色
            "mouse_move": "#b3e5fc",       # 鼠标移动 - 浅蓝色
            "mouse_drag": "#b3e5fc",       # 鼠标拖拽 - 浅蓝色
            "mouse_scroll": "#b3e5fc",     # 鼠标滚动 - 浅蓝色
            "keyboard_type": "#c8e6c9",    # 键盘输入 - 浅绿色
            "keyboard_press": "#f8bbd9",   # 按键按下 - 粉色
            "keyboard_hotkey": "#f8bbd9",  # 快捷键 - 粉色
            "image_find": "#e1bee7",       # 查找图片 - 紫色
            "image_click": "#e1bee7",      # 点击图片 - 紫色
            "image_exists": "#e1bee7",     # 图片存在判断 - 紫色
            "window_find": "#b2dfdb",      # 查找窗口 - 青色
            "window_activate": "#b2dfdb",  # 激活窗口 - 青色
            "window_close": "#b2dfdb",     # 关闭窗口 - 青色
            "window_position": "#b2dfdb",  # 窗口位置 - 青色
            "excel_read": "#ffcc80",       # 读取Excel - 橙色
            "wait": "#fff9c4",             # 等待 - 黄色
            "if_else": "#ffcdd2",          # 条件分支 - 红色
            "loop": "#e0e0e0",             # 循环 - 灰色
            "log": "#f5f5f5",              # 日志 - 浅灰色
            "label": "#e0e0e0",            # 标签 - 灰色
            "goto": "#e0e0e0",             # 跳转 - 灰色
            "set_variable": "#bbdefb",     # 设置变量 - 蓝色
            "get_variable": "#bbdefb",     # 获取变量 - 蓝色
        }
        
        # 获取对应的颜色（默认白色）
        color = type_colors.get(step_type, "#ffffff")
        
        # 遍历该行的所有列（共4列）
        for col in range(4):
            # 获取单元格项
            item = self.step_table.item(row, col)
            
            # 如果单元格项存在
            if item:
                # 设置单元格背景颜色
                item.setBackground(QBrush(QColor(color)))
    
    @Slot()
    def on_add_step(self):
        """
        添加步骤方法: 打开步骤编辑器对话框添加新步骤（当前未使用）
        
        执行流程:
            1. 创建步骤编辑器对话框
            2. 设置对话框标题为"添加步骤"
            3. 定义步骤保存后的回调函数
            4. 连接对话框的step_saved信号到回调函数
            5. 显示对话框（模态方式，阻塞当前窗口）
        
        回调函数 on_step_saved(step_data):
            1. 在表格末尾添加新行
            2. 从step_data中提取步骤信息
            3. 创建表格单元格项
            4. 设置单元格内容和样式
            5. 应用行样式
            6. 在日志中添加记录
        """
        # 创建步骤编辑器对话框
        dialog = StepEditorDialog(parent=self)
        
        # 设置对话框标题
        dialog.setWindowTitle("添加步骤")
        
        # 定义步骤保存后的回调函数
        def on_step_saved(step_data):
            # 获取当前表格行数（即新行的索引）
            row = self.step_table.rowCount()
            
            # 在表格中插入新行
            self.step_table.insertRow(row)
            
            # 从step_data中提取步骤信息
            step_type = step_data.get("type", "")
            step_name = STEP_TYPE_MAP.get(step_type, step_type)
            description = step_data.get("description", "")
            params = step_data.get("params", {})
            delay = params.get("delay", 0)
            
            # 创建表格单元格项
            type_item = QTableWidgetItem(step_name)
            desc_item = QTableWidgetItem(description)
            params_item = QTableWidgetItem(str(params))
            delay_item = QTableWidgetItem(str(delay))
            
            # 设置单元格内容居中对齐
            type_item.setTextAlignment(Qt.AlignCenter)
            delay_item.setTextAlignment(Qt.AlignCenter)
            
            # 将步骤类型存储到单元格的Qt.UserRole中
            type_item.setData(Qt.UserRole, step_type)
            
            # 将单元格项设置到表格的对应位置
            self.step_table.setItem(row, 0, type_item)
            self.step_table.setItem(row, 1, desc_item)
            self.step_table.setItem(row, 2, params_item)
            self.step_table.setItem(row, 3, delay_item)
            
            # 根据步骤类型应用行样式
            self.apply_step_row_style(row)
            
            # 在日志面板中添加记录
            self.log_panel.append(f"添加步骤: {step_name}")
        
        # 连接对话框的step_saved信号到回调函数
        dialog.step_saved.connect(on_step_saved)
        
        # 显示对话框（模态方式）
        dialog.exec()
    
    @Slot()
    def on_edit_step(self):
        """
        编辑步骤方法: 打开步骤编辑器对话框编辑选中的步骤（当前未使用）
        
        执行流程:
            1. 获取当前选中的行
            2. 如果没有选中行，弹出警告
            3. 从表格中提取步骤信息
            4. 创建步骤编辑器对话框（传入现有数据）
            5. 设置对话框标题为"编辑步骤"
            6. 定义步骤保存后的回调函数
            7. 连接对话框的step_saved信号到回调函数
            8. 显示对话框（模态方式）
        
        回调函数 on_step_saved(updated_data):
            1. 从updated_data中提取更新后的步骤信息
            2. 创建表格单元格项
            3. 更新表格中的单元格内容
            4. 应用行样式
            5. 在日志中添加记录
        """
        # 获取当前选中的行索引
        current_row = self.step_table.currentRow()
        
        # 如果没有选中任何行（索引为-1），弹出警告
        if current_row < 0:
            QMessageBox.warning(self, "编辑失败", "请先选择一个步骤")
            return
        
        # 从表格中提取步骤信息
        type_item = self.step_table.item(current_row, 0)
        step_type = type_item.data(Qt.UserRole) if type_item else ""
        description = self.step_table.item(current_row, 1).text() if self.step_table.item(current_row, 1) else ""
        params_text = self.step_table.item(current_row, 2).text() if self.step_table.item(current_row, 2) else ""
        delay = self.step_table.item(current_row, 3).text() if self.step_table.item(current_row, 3) else "0"
        
        # 将参数文本转换为字典
        # 使用eval()解析字符串，失败则返回空字典
        try:
            params = eval(params_text) if params_text else {}
        except:
            params = {}
        
        # 构建步骤数据字典
        step_data = {
            "type": step_type,
            "description": description,
            "params": params
        }
        
        # 创建步骤编辑器对话框（传入步骤类型和现有数据）
        dialog = StepEditorDialog(step_type=step_type, step_data=step_data, parent=self)
        
        # 设置对话框标题
        dialog.setWindowTitle("编辑步骤")
        
        # 定义步骤保存后的回调函数
        def on_step_saved(updated_data):
            # 从updated_data中提取更新后的步骤信息
            updated_type = updated_data.get("type", "")
            updated_name = STEP_TYPE_MAP.get(updated_type, updated_type)
            updated_desc = updated_data.get("description", "")
            updated_params_dict = updated_data.get("params", {})
            updated_params = str(updated_params_dict)
            updated_delay = updated_params_dict.get("delay", 0)
            
            # 创建更新后的表格单元格项
            type_item = QTableWidgetItem(updated_name)
            type_item.setTextAlignment(Qt.AlignCenter)
            type_item.setData(Qt.UserRole, updated_type)
            
            desc_item = QTableWidgetItem(updated_desc)
            params_item = QTableWidgetItem(updated_params)
            delay_item = QTableWidgetItem(str(updated_delay))
            delay_item.setTextAlignment(Qt.AlignCenter)
            
            # 更新表格中的单元格内容
            self.step_table.setItem(current_row, 0, type_item)
            self.step_table.setItem(current_row, 1, desc_item)
            self.step_table.setItem(current_row, 2, params_item)
            self.step_table.setItem(current_row, 3, delay_item)
            
            # 根据步骤类型应用行样式
            self.apply_step_row_style(current_row)
            
            # 在日志面板中添加记录
            self.log_panel.append(f"编辑步骤: {updated_name}")
        
        # 连接对话框的step_saved信号到回调函数
        dialog.step_saved.connect(on_step_saved)
        
        # 显示对话框（模态方式）
        dialog.exec()
    
    @Slot()
    def on_copy_step(self):
        """
        复制步骤方法: 复制当前选中的步骤（当前未使用）
        
        执行流程:
            1. 获取当前选中的行
            2. 如果没有选中行，弹出警告
            3. 从表格中提取步骤信息
            4. 在当前行下方插入新行
            5. 创建复制的步骤（名称加"(复制)"后缀）
            6. 应用行样式
            7. 在日志中添加记录
        """
        # 获取当前选中的行索引
        current_row = self.step_table.currentRow()
        
        # 如果没有选中任何行，弹出警告
        if current_row < 0:
            QMessageBox.warning(self, "复制失败", "请先选择一个步骤")
            return
        
        # 从表格中提取步骤信息
        step_type = self.step_table.item(current_row, 0).text()
        description = self.step_table.item(current_row, 1).text()
        params = self.step_table.item(current_row, 2).text()
        delay = self.step_table.item(current_row, 3).text()
        
        # 新行插入到当前行的下一行
        new_row = current_row + 1
        
        # 在表格中插入新行
        self.step_table.insertRow(new_row)
        
        # 创建复制的步骤（名称加"(复制)"后缀）
        type_item = QTableWidgetItem(step_type + " (复制)")
        desc_item = QTableWidgetItem(description)
        params_item = QTableWidgetItem(params)
        delay_item = QTableWidgetItem(delay)
        
        # 设置单元格内容居中对齐
        type_item.setTextAlignment(Qt.AlignCenter)
        delay_item.setTextAlignment(Qt.AlignCenter)
        
        # 将单元格项设置到表格的对应位置
        self.step_table.setItem(new_row, 0, type_item)
        self.step_table.setItem(new_row, 1, desc_item)
        self.step_table.setItem(new_row, 2, params_item)
        self.step_table.setItem(new_row, 3, delay_item)
        
        # 根据步骤类型应用行样式
        self.apply_step_row_style(new_row)
        
        # 在日志面板中添加记录
        self.log_panel.append(f"复制步骤: {step_type}")
    
    @Slot()
    def on_delete_step(self):
        """
        删除步骤方法: 删除当前选中的步骤（当前未使用）
        
        执行流程:
            1. 获取当前选中的行
            2. 如果没有选中行，弹出警告
            3. 从表格中提取步骤类型名称
            4. 弹出确认对话框，让用户确认是否删除
            5. 如果用户确认，删除该行
            6. 在日志中添加记录
        """
        # 获取当前选中的行索引
        current_row = self.step_table.currentRow()
        
        # 如果没有选中任何行，弹出警告
        if current_row < 0:
            QMessageBox.warning(self, "删除失败", "请先选择一个步骤")
            return
        
        # 获取步骤类型名称
        step_type = self.step_table.item(current_row, 0).text()
        
        # 弹出确认对话框，让用户确认是否删除
        reply = QMessageBox.question(
            self, "确认删除", f"确定要删除步骤 '{step_type}' 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        # 如果用户点击了"是"按钮
        if reply == QMessageBox.Yes:
            # 删除选中的行
            self.step_table.removeRow(current_row)
            
            # 在日志面板中添加记录
            self.log_panel.append(f"删除步骤: {step_type}")
    
    @Slot()
    def on_move_up(self):
        """
        上移步骤方法: 将选中的步骤向上移动一行（当前未使用）
        
        执行流程:
            1. 获取当前选中的行
            2. 如果不是第一行，执行上移操作
            3. 在当前行上方插入新行
            4. 将当前行的内容移动到新行
            5. 删除原来的行
            6. 更新选中行为上移后的行
        """
        # 获取当前选中的行索引
        current_row = self.step_table.currentRow()
        
        # 如果不是第一行（索引大于0），执行上移操作
        if current_row > 0:
            # 在当前行上方插入新行
            self.step_table.insertRow(current_row - 1)
            
            # 遍历所有列，将当前行的内容移动到新行
            for col in range(4):
                # 取出当前行的单元格项
                item = self.step_table.takeItem(current_row + 1, col)
                if item:
                    # 将单元格项设置到新行
                    self.step_table.setItem(current_row - 1, col, item)
            
            # 删除原来的行
            self.step_table.removeRow(current_row + 1)
            
            # 更新选中行为上移后的行
            self.step_table.setCurrentRow(current_row - 1)
    
    @Slot()
    def on_move_down(self):
        """
        下移步骤方法: 将选中的步骤向下移动一行（当前未使用）
        
        执行流程:
            1. 获取当前选中的行
            2. 如果不是最后一行，执行下移操作
            3. 在当前行下方两行处插入新行
            4. 将当前行的内容移动到新行
            5. 删除原来的行
            6. 更新选中行为下移后的行
        """
        # 获取当前选中的行索引
        current_row = self.step_table.currentRow()
        
        # 如果不是最后一行，执行下移操作
        if current_row < self.step_table.rowCount() - 1:
            # 在当前行下方两行处插入新行
            self.step_table.insertRow(current_row + 2)
            
            # 遍历所有列，将当前行的内容移动到新行
            for col in range(4):
                # 取出当前行的单元格项
                item = self.step_table.takeItem(current_row, col)
                if item:
                    # 将单元格项设置到新行
                    self.step_table.setItem(current_row + 2, col, item)
            
            # 删除原来的行
            self.step_table.removeRow(current_row)
            
            # 更新选中行为下移后的行
            self.step_table.setCurrentRow(current_row + 1)
    
    @Slot()
    def on_clear_log(self):
        """
        清空日志方法: 清空日志面板中的所有内容
        
        执行流程:
            1. 调用clear()方法清空日志面板
            2. 添加一条"日志已清空"的记录
        """
        # 清空日志面板中的所有内容
        self.log_panel.clear()
        
        # 添加一条"日志已清空"的记录
        self.log_panel.append("日志已清空")
    
    @Slot()
    def on_edit_steps(self):
        """
        编辑步骤方法: 打开节点编辑器对话框编辑执行步骤
        
        执行流程:
            1. 检查是否有当前选中的任务
            2. 如果没有选中任务，弹出警告
            3. 创建节点编辑器对话框（传入当前任务）
            4. 显示对话框（模态方式）
            5. 如果用户点击了"确定"按钮
            6. 获取节点图数据
            7. 更新当前任务的节点和连线数据
            8. 更新任务树中的任务数据
            9. 重新加载节点图到场景中
            10. 在日志中添加记录
        """
        # 检查是否有当前选中的任务
        if not self.current_flow:
            QMessageBox.warning(self, "编辑失败", "请先选择一个任务")
            return
        
        # 创建节点编辑器对话框（传入当前任务）
        dialog = NodeEditorDialog(self.current_flow, parent=self)
        
        # 显示对话框（模态方式），并判断用户是否点击了"确定"按钮
        try:
            if dialog.exec() == QDialog.Accepted:
                # 获取节点图数据
                graph_data = dialog.get_graph_data()
                
                # 更新当前任务的节点和连线数据
                self.current_flow["nodes"] = graph_data.get("nodes", [])
                self.current_flow["edges"] = graph_data.get("edges", [])
                
                # 获取当前选中的任务项
                current_item = self.task_tree.currentItem()
                if current_item:
                    # 更新任务树中的任务数据
                    current_item.setData(0, Qt.UserRole, self.current_flow)
                
                # 重新加载节点图到场景中
                self.load_nodes_from_flow(self.current_flow)
                
                # 在日志面板中添加记录
                self.log_panel.append(f"已更新执行步骤: {self.current_flow['name']}")
        finally:
            # 无论用户点击确定还是取消，都清理对话框资源
            try:
                dialog.cleanup()
            except Exception:
                pass
    
    def load_nodes_from_flow(self, flow_data):
        """
        从任务数据加载节点方法: 将任务中的节点和连线数据加载到节点图场景中
        
        参数:
            flow_data: 任务数据字典，包含nodes和edges字段
        
        执行流程:
            1. 清空节点图场景中的所有内容
            2. 提取节点列表和连线列表
            3. 创建节点映射字典（节点ID -> 节点对象）
            4. 遍历节点列表，创建节点并添加到场景中
            5. 遍历连线列表，根据节点ID查找对应的节点，创建连线
        """
        try:
            self.graph_scene.clear_all()
            
            nodes = flow_data.get("nodes", [])
            edges = flow_data.get("edges", [])
            
            node_map = {}
            
            for node_data in nodes:
                try:
                    node = self.graph_scene.add_node(
                        node_data.get("type", "wait"),
                        node_data.get("x", 0),
                        node_data.get("y", 0),
                        node_data.get("config", {})
                    )
                    
                    node.set_node_id(node_data.get("id", str(uuid.uuid4())))
                    node_map[node_data.get("id", "")] = node
                except Exception as e:
                    print(f"加载节点失败: {e}")
            
            for edge_data in edges:
                try:
                    source_node = node_map.get(edge_data["source_node"])
                    target_node = node_map.get(edge_data["target_node"])
                    
                    if source_node and target_node:
                        source_port = source_node.get_output_port(edge_data["source_port"])
                        target_port = target_node.get_input_port(edge_data["target_port"])
                        
                        if source_port and target_port:
                            self.graph_scene.add_edge(source_port, target_port)
                except Exception as e:
                    print(f"加载连线失败: {e}")
        except Exception as e:
            print(f"加载节点图失败: {e}")
    
    def add_log(self, message):
        """
        添加日志方法: 在日志面板中添加一条日志记录
        
        参数:
            message: 日志消息文本
        
        执行流程:
            1. 在日志面板中追加日志消息
            2. 将滚动条滚动到最底部，确保最新的日志可见
        """
        # 在日志面板中追加日志消息
        self.log_panel.append(message)
        
        # 将垂直滚动条滚动到最底部，确保最新的日志可见
        self.log_panel.verticalScrollBar().setValue(
            self.log_panel.verticalScrollBar().maximum()
        )
    
    def update_progress(self, value):
        """
        更新进度方法: 更新状态栏中的进度条
        
        参数:
            value: 进度值（0-100）
        
        执行流程:
            1. 显示进度条（如果之前是隐藏的）
            2. 设置进度条的值
        """
        # 显示进度条
        self.progress_bar.show()
        
        # 设置进度条的值（0-100）
        self.progress_bar.setValue(value)

def main():
    """
    主函数（备份）: 文件末尾的备用入口点
    
    注意: 这个main函数是备份，实际的入口点在项目根目录的main.py文件中
    """
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置界面样式为Fusion
    app.setStyle("Fusion")
    
    # 创建主窗口对象
    window = MainWindow()
    
    # 显示主窗口
    window.show()
    
    # 进入Qt事件循环
    sys.exit(app.exec())

if __name__ == "__main__":
    # 如果这个文件被直接运行，执行main函数
    # 实际项目中，应该通过项目根目录的main.py启动
    main()