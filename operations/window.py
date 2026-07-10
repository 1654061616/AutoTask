import win32gui
import win32con
import win32api
from typing import List, Optional, Tuple
import psutil

class WindowOperations:
    def __init__(self):
        pass
    
    def get_all_windows(self) -> List[Tuple[int, str]]:
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
        windows = self.get_all_windows()
        for hwnd, window_title in windows:
            if title.lower() in window_title.lower():
                return hwnd
        return None
    
    def activate_window(self, hwnd: int):
        win32gui.SetForegroundWindow(hwnd)
    
    def close_window(self, hwnd: int):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    
    def minimize_window(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    
    def maximize_window(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    
    def restore_window(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    
    def get_window_rect(self, hwnd: int) -> Tuple[int, int, int, int]:
        return win32gui.GetWindowRect(hwnd)
    
    def set_window_pos(self, hwnd: int, x: int, y: int, width: int, height: int):
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOP,
            x, y, width, height,
            win32con.SWP_NOZORDER
        )
    
    def get_window_title(self, hwnd: int) -> str:
        return win32gui.GetWindowText(hwnd)
    
    def get_active_window(self) -> Optional[int]:
        return win32gui.GetForegroundWindow()
    
    def set_window_transparency(self, hwnd: int, alpha: int):
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
        )
        win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)