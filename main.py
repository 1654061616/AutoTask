"""
文件名: main.py
功能: 程序入口文件，负责启动整个AutoFlow自动化操作软件
所属模块: 项目根目录
依赖: 
    - sys: Python内置模块，用于处理命令行参数和程序退出
    - PySide6.QtWidgets.QApplication: Qt框架的应用程序类，管理GUI应用的生命周期
    - gui.main_window.MainWindow: 自定义的主窗口类，包含所有界面元素

执行流程:
    1. 创建QApplication对象（必须在创建任何GUI控件之前）
    2. 设置界面样式为Fusion（跨平台统一风格）
    3. 创建主窗口对象
    4. 显示主窗口
    5. 进入Qt事件循环，等待用户操作
"""

import sys
import traceback
import logging
import ctypes
import platform

if platform.system() == "Windows":
    try:
        DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = 0x00000022
        ctypes.windll.user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
    except:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autoflow_error.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def excepthook(exc_type, exc_value, exc_traceback):
    logging.error('=' * 80)
    logging.error('UNHANDLED EXCEPTION:')
    logging.error('=' * 80)
    exc_info = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.error(exc_info)
    logging.error('=' * 80)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = excepthook

from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """
    主函数: 程序的入口点
    作用: 初始化并启动整个GUI应用程序
    """
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"主程序启动失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
