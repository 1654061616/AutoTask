import pyautogui
import pyperclip
import random
import time

class KeyboardOperations:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05
    
    def type(self, text: str, interval: float = 0.05, human_like: bool = False):
        if human_like:
            self._human_type(text)
        else:
            pyautogui.typewrite(text, interval=interval)
    
    def _human_type(self, text: str):
        for char in text:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.02, 0.15))
            if random.random() < 0.05:
                time.sleep(random.uniform(0.1, 0.3))
    
    def press(self, key: str):
        pyautogui.press(key)
    
    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
    
    def hold(self, key: str, duration: float = 1.0):
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
    
    def copy(self):
        pyautogui.hotkey('ctrl', 'c')
    
    def paste(self):
        pyautogui.hotkey('ctrl', 'v')
    
    def cut(self):
        pyautogui.hotkey('ctrl', 'x')
    
    def select_all(self):
        pyautogui.hotkey('ctrl', 'a')
    
    def delete(self, times: int = 1):
        for _ in range(times):
            pyautogui.press('delete')
    
    def backspace(self, times: int = 1):
        for _ in range(times):
            pyautogui.press('backspace')
    
    def enter(self, times: int = 1):
        for _ in range(times):
            pyautogui.press('enter')
    
    def tab(self, times: int = 1):
        for _ in range(times):
            pyautogui.press('tab')
    
    def clipboard_copy(self, text: str):
        pyperclip.copy(text)
    
    def clipboard_paste(self) -> str:
        return pyperclip.paste()
    
    def input_text(self, text: str, method: str = "direct"):
        if method == "clipboard":
            self.clipboard_copy(text)
            self.paste()
        elif method == "human":
            self._human_type(text)
        else:
            self.type(text)