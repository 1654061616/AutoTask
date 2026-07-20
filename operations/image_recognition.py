"""
图像识别模块 — 基于 OpenCV 的屏幕截图和图像匹配
"""
import cv2
import numpy as np
import mss
import pyautogui
from typing import Tuple, Optional, List
import os

class ImageRecognition:
    """图像识别器，支持模板匹配和 AKAZE 特征匹配两种算法"""

    def __init__(self):
        self.screen = mss.mss()            # MSS 屏幕截图工具
        self.monitor = self.screen.monitors[1]  # 主显示器区域

    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """截取屏幕指定区域，返回 numpy 数组"""
        if region:
            monitor = {"top": region[1], "left": region[0], "width": region[2] - region[0], "height": region[3] - region[1]}
        else:
            monitor = self.monitor
        screenshot = self.screen.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

    def find_image(self, template_path: str, region: Optional[Tuple[int, int, int, int]] = None,
                   threshold: float = 0.8, method: str = "template", direction: str = "default") -> Optional[Tuple[int, int]]:
        """查找图片位置，返回中心坐标"""
        if not os.path.exists(template_path):
            return None

        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            return None

        screen_img = self.capture_screen(region)
        if screen_img is None:
            return None

        if method == "akaze":
            return self._find_image_akaze(screen_img, template, threshold)
        else:
            return self._find_image_template(screen_img, template, threshold, direction)

    def _find_image_template(self, screen_img: np.ndarray, template: np.ndarray,
                             threshold: float, direction: str = "default") -> Optional[Tuple[int, int]]:
        """模板匹配算法，支持方向控制"""
        screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        w, h = template_gray.shape[::-1]
        if w > screen_gray.shape[1] or h > screen_gray.shape[0]:
            return None

        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        if direction == "default":
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val >= threshold:
                return (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return None

        h_result, w_result = result.shape

        if direction == "top_to_bottom":
            for y in range(h_result):
                for x in range(w_result):
                    if result[y, x] >= threshold:
                        return (x + w // 2, y + h // 2)
        elif direction == "bottom_to_top":
            for y in range(h_result - 1, -1, -1):
                for x in range(w_result):
                    if result[y, x] >= threshold:
                        return (x + w // 2, y + h // 2)
        elif direction == "left_to_right":
            for x in range(w_result):
                for y in range(h_result):
                    if result[y, x] >= threshold:
                        return (x + w // 2, y + h // 2)
        elif direction == "right_to_left":
            for x in range(w_result - 1, -1, -1):
                for y in range(h_result):
                    if result[y, x] >= threshold:
                        return (x + w // 2, y + h // 2)
        else:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val >= threshold:
                return (max_loc[0] + w // 2, max_loc[1] + h // 2)

        return None

    def _find_image_akaze(self, screen_img: np.ndarray, template: np.ndarray,
                          threshold: float) -> Optional[Tuple[int, int]]:
        """AKAZE 特征匹配算法，适合旋转/缩放场景"""
        try:
            akaze = cv2.AKAZE_create()
            kp1, des1 = akaze.detectAndCompute(cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY), None)
            kp2, des2 = akaze.detectAndCompute(cv2.cvtColor(template, cv2.COLOR_BGR2GRAY), None)

            if des1 is None or des2 is None:
                return None

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)

            if len(matches) < 10:
                return None

            matches = sorted(matches, key=lambda x: x.distance)
            good_matches = matches[:10]

            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
            if M is None:
                return None

            h, w = template.shape[:2]
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            center_x = int((dst[0][0][0] + dst[2][0][0]) / 2)
            center_y = int((dst[0][0][1] + dst[2][0][1]) / 2)
            return (center_x, center_y)
        except Exception:
            return None

    def find_all_images(self, template_path: str, region: Optional[Tuple[int, int, int, int]] = None,
                        threshold: float = 0.8) -> List[Tuple[int, int]]:
        """查找屏幕上所有匹配的图片位置"""
        if not os.path.exists(template_path):
            return []

        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            return []

        screen_img = self.capture_screen(region)
        screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        w, h = template_gray.shape[::-1]
        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        locations = np.where(result >= threshold)
        matches = []

        for pt in zip(*locations[::-1]):
            matches.append((pt[0] + w // 2, pt[1] + h // 2))

        return matches

    def image_exists(self, template_path: str, region: Optional[Tuple[int, int, int, int]] = None,
                     threshold: float = 0.8, method: str = "template", direction: str = "default") -> bool:
        """判断图片是否存在"""
        return self.find_image(template_path, region=region, threshold=threshold, method=method, direction=direction) is not None

    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕分辨率"""
        return (self.monitor["width"], self.monitor["height"])

    def save_screenshot(self, file_path: str, region: Optional[Tuple[int, int, int, int]] = None):
        """保存截图到文件"""
        img = self.capture_screen(region)
        cv2.imwrite(file_path, img)