"""
OCR 识别模块 — 基于 EasyOCR 的文本识别与定位
"""
import easyocr
import numpy as np
from typing import List, Tuple, Optional
import os

class OCROperations:
    """OCR 文本识别器，支持中英文识别、文本查找和提取"""

    def __init__(self, lang_list: List[str] = None):
        if lang_list is None:
            lang_list = ['ch_sim', 'en']
        self.reader = easyocr.Reader(lang_list, gpu=False)

    def read_text(self, image_path: str) -> List[Tuple[Tuple[int, int, int, int], str, float]]:
        """从图片文件读取所有文本，返回 (边界框, 文本, 置信度) 列表"""
        if not os.path.exists(image_path):
            return []
        try:
            results = self.reader.readtext(image_path)
            return results
        except Exception:
            return []

    def read_text_from_image(self, image: np.ndarray) -> List[Tuple[Tuple[int, int, int, int], str, float]]:
        """从 numpy 数组图像读取所有文本"""
        try:
            results = self.reader.readtext(image)
            return results
        except Exception:
            return []

    def find_text(self, image_path: str, target_text: str, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        """在图片中查找指定文本，返回中心坐标"""
        results = self.read_text(image_path)
        for result in results:
            bbox, text, conf = result
            if target_text in text and conf >= threshold:
                center_x = (bbox[0][0] + bbox[2][0]) // 2
                center_y = (bbox[0][1] + bbox[2][1]) // 2
                return (center_x, center_y)
        return None

    def extract_all_text(self, image_path: str) -> str:
        """提取图片中所有文本，换行拼接"""
        results = self.read_text(image_path)
        return "\n".join([result[1] for result in results])

    def text_exists(self, image_path: str, target_text: str, threshold: float = 0.8) -> bool:
        """判断图片中是否存在指定文本"""
        return self.find_text(image_path, target_text, threshold) is not None