"""
键盘操作模块 — 封装 pyautogui 键盘操作，支持多种输入方式
"""
import pyautogui
import pyperclip
import random
import time

class KeyboardOperations:
    """键盘操作封装，支持输入、按键、快捷键、剪贴板等操作"""

    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

    def type(self, text: str, interval: float = 0.05, human_like: bool = False):
        """输入文本"""
        if human_like:
            self._human_type(text)
        else:
            pyautogui.typewrite(text, interval=interval)

    def _human_type(self, text: str):
        """拟人化输入：随机间隔 + 偶尔停顿"""
        for char in text:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.02, 0.15))
            if random.random() < 0.05:
                time.sleep(random.uniform(0.1, 0.3))

    def press(self, key: str, presses: int = 1):
        """按下指定按键"""
        for _ in range(presses):
            pyautogui.press(key)
            if presses > 1:
                time.sleep(0.1)

    def hotkey(self, *keys):
        """按下组合键"""
        pyautogui.hotkey(*keys)

    def hold(self, key: str, duration: float = 1.0):
        """按住按键一段时间"""
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)

    def copy(self):
        """Ctrl+C 复制"""
        pyautogui.hotkey('ctrl', 'c')

    def paste(self):
        """Ctrl+V 粘贴"""
        pyautogui.hotkey('ctrl', 'v')

    def cut(self):
        """Ctrl+X 剪切"""
        pyautogui.hotkey('ctrl', 'x')

    def select_all(self):
        """Ctrl+A 全选"""
        pyautogui.hotkey('ctrl', 'a')

    def delete(self, times: int = 1):
        """按 Delete 键"""
        for _ in range(times):
            pyautogui.press('delete')

    def backspace(self, times: int = 1):
        """按 Backspace 键"""
        for _ in range(times):
            pyautogui.press('backspace')

    def enter(self, times: int = 1):
        """按 Enter 键"""
        for _ in range(times):
            pyautogui.press('enter')

    def tab(self, times: int = 1):
        """按 Tab 键"""
        for _ in range(times):
            pyautogui.press('tab')

    def clipboard_copy(self, text: str):
        """将文本复制到剪贴板"""
        pyperclip.copy(text)

    def clipboard_paste(self) -> str:
        """从剪贴板获取文本"""
        return pyperclip.paste()

    def input_text(self, text: str, method: str = "direct"):
        """按指定方法输入文本：direct / clipboard / human"""
        if method == "clipboard":
            self.clipboard_copy(text)
            self.paste()
        elif method == "human":
            self._human_type(text)
        else:
            self.type(text)