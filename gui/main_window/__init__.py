"""
文件名: main_window
功能: 主窗口界面包，包含 MainWindow 类和所有功能 Mixin 模块
所属模块: GUI层 - gui包
"""

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

import sys
import os

from core.engine import FlowEngine
from utils.resource_path import get_resource_path

from .ui_builder import UIBuilderMixin
from .task_manager import TaskManagerMixin
from .task_executor import TaskExecutorMixin
from .schedule_handler import ScheduleHandlerMixin
from .node_handler import NodeHandlerMixin


class MainWindow(QMainWindow,
                 UIBuilderMixin,
                 TaskManagerMixin,
                 TaskExecutorMixin,
                 ScheduleHandlerMixin,
                 NodeHandlerMixin):
    """
    主窗口类: 整个软件的界面主体
    
    继承自 QMainWindow 和多个功能 Mixin:
    - UIBuilderMixin: 界面构建（菜单栏、状态栏、中央区域、样式表）
    - TaskManagerMixin: 任务管理（新建、复制、删除、打开、保存、重命名）
    - TaskExecutorMixin: 任务执行（启动、停止、日志、进度）
    - ScheduleHandlerMixin: 定时任务（启停、配置加载）
    - NodeHandlerMixin: 节点图处理（编辑步骤、加载节点）
    """
    
    flow_loaded = Signal(dict)       # 未使用 流程加载完成，传递流程数据字典
    step_selected = Signal(dict)    # 未使用 画布中选中了某个步骤节点，传递步骤数据字典
    flow_started = Signal()         # 未使用 流程开始执行
    flow_stopped = Signal()         # 未使用 流程已停止
    log_received = Signal(str)      # 收到引擎日志，传递日志文本
    task_completed = Signal(bool, str)  # 任务执行完成，传递(是否成功, 错误信息)
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("AutoFlow")
        
        icon_path = get_resource_path("icons/icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setGeometry(100, 100, 1400, 900)
        
        self.flows = []
        self.current_flow = None
        
        self.engine = FlowEngine()
        
        self.log_received.connect(self._on_log_received)
        self.engine.logger.add_callback(self._on_engine_log)
        self.task_completed.connect(self._on_task_completed_slot)
        
        self.init_ui()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()