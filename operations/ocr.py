import easyocr
import numpy as np
from typing import List, Tuple, Optional
import os

class OCROperations:
    def __init__(self, lang_list: List[str] = None):
        if lang_list is None:
            lang_list = ['ch_sim', 'en']
        self.reader = easyocr.Reader(lang_list, gpu=False)
    
    def read_text(self, image_path: str) -> List[Tuple[Tuple[int, int, int, int], str, float]]:
        if not os.path.exists(image_path):
            return []
        try:
            results = self.reader.readtext(image_path)
            return results
        except Exception:
            return []
    
    def read_text_from_image(self, image: np.ndarray) -> List[Tuple[Tuple[int, int, int, int], str, float]]:
        try:
            results = self.reader.readtext(image)
            return results
        except Exception:
            return []
    
    def find_text(self, image_path: str, target_text: str, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        results = self.read_text(image_path)
        for result in results:
            bbox, text, conf = result
            if target_text in text and conf >= threshold:
                center_x = (bbox[0][0] + bbox[2][0]) // 2
                center_y = (bbox[0][1] + bbox[2][1]) // 2
                return (center_x, center_y)
        return None
    
    def extract_all_text(self, image_path: str) -> str:
        results = self.read_text(image_path)
        return "\n".join([result[1] for result in results])
    
    def text_exists(self, image_path: str, target_text: str, threshold: float = 0.8) -> bool:
        return self.find_text(image_path, target_text, threshold) is not None