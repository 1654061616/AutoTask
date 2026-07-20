"""
窗口操作模块 — 基于 win32gui 的 Windows 窗口管理
"""
import win32gui
import win32con
import win32api
from typing import List, Optional, Tuple
import psutil

class WindowOperations:
    """Windows 窗口管理器，支持查找、激活、关闭、移动、透明等操作"""

    def __init__(self):
        pass

    def get_all_windows(self) -> List[Tuple[int, str]]:
        """获取所有可见窗口的句柄和标题"""
        windows = []
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows.append((hwnd, title))
            return True
        win32gui.EnumWindows(callback, None)
        return windows

    def find_window(self, title: str) -> Optional[int]:
        """按标题模糊查找窗口，返回句柄"""
        windows = self.get_all_windows()
        for hwnd, window_title in windows:
            if title.lower() in window_title.lower():
                return hwnd
        return None

    def activate_window(self, hwnd: int):
        """激活窗口（置为前台）"""
        win32gui.SetForegroundWindow(hwnd)

    def close_window(self, hwnd: int):
        """发送关闭消息"""
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def minimize_window(self, hwnd: int):
        """最小化窗口"""
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize_window(self, hwnd: int):
        """最大化窗口"""
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def restore_window(self, hwnd: int):
        """还原窗口"""
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    def get_window_rect(self, hwnd: int) -> Tuple[int, int, int, int]:
        """获取窗口矩形坐标 (left, top, right, bottom)"""
        return win32gui.GetWindowRect(hwnd)

    def set_window_pos(self, hwnd: int, x: int, y: int, width: int, height: int):
        """设置窗口位置和大小"""
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOP,
            x, y, width, height,
            win32con.SWP_NOZORDER
        )

    def get_window_title(self, hwnd: int) -> str:
        """获取窗口标题"""
        return win32gui.GetWindowText(hwnd)

    def get_active_window(self) -> Optional[int]:
        """获取当前活动窗口句柄"""
        return win32gui.GetForegroundWindow()

    def set_window_transparency(self, hwnd: int, alpha: int):
        """设置窗口透明度（0-255）"""
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
        )
        win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)