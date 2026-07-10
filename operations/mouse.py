import pyautogui
import random
import time

class MouseOperations:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05
    
    def click(self, x: int = None, y: int = None, button: str = "left", clicks: int = 1, interval: float = 0.2):
        if x is not None and y is not None:
            self.move(x, y)
        pyautogui.click(button=button, clicks=clicks, interval=interval)
    
    def move(self, x: int, y: int, duration: float = 0.5, easing: bool = True):
        if easing:
            start_x, start_y = pyautogui.position()
            steps = 30
            for i in range(steps + 1):
                t = i / steps
                eased = self._ease_in_out_cubic(t)
                current_x = start_x + (x - start_x) * eased
                current_y = start_y + (y - start_y) * eased
                pyautogui.moveTo(current_x, current_y, duration=0)
                time.sleep(duration / steps)
        else:
            pyautogui.moveTo(x, y, duration=duration)
    
    def _ease_in_out_cubic(self, t: float) -> float:
        if t < 0.5:
            return 4 * t * t * t
        return 1 - (-2 * t + 2) ** 3 / 2
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5):
        pyautogui.moveTo(start_x, start_y)
        pyautogui.dragTo(end_x, end_y, duration=duration)
    
    def scroll(self, amount: int, x: int = None, y: int = None):
        if x is not None and y is not None:
            pyautogui.moveTo(x, y)
        pyautogui.scroll(amount)
    
    def right_click(self, x: int = None, y: int = None):
        self.click(x, y, button="right")
    
    def double_click(self, x: int = None, y: int = None):
        self.click(x, y, clicks=2)
    
    def get_position(self) -> tuple:
        return pyautogui.position()
    
    def random_move(self, max_distance: int = 100):
        current_x, current_y = self.get_position()
        new_x = current_x + random.randint(-max_distance, max_distance)
        new_y = current_y + random.randint(-max_distance, max_distance)
        self.move(new_x, new_y)
    
    def click_random(self):
        self.random_move()
        self.click()
    
    def human_like_click(self, x: int, y: int):
        self.move(x, y, duration=random.uniform(0.3, 0.8))
        time.sleep(random.uniform(0.1, 0.3))
        self.click()
        time.sleep(random.uniform(0.1, 0.3))