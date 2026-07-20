"""
剪贴板操作模块 — 封装 pyperclip 的剪贴板读写
"""
import pyperclip
import base64
from io import BytesIO
from PIL import Image

class ClipboardOperations:
    """剪贴板操作器，支持文本和图片的复制粘贴"""

    def __init__(self):
        pass

    def copy_text(self, text: str):
        """复制文本到剪贴板"""
        pyperclip.copy(text)

    def paste_text(self) -> str:
        """从剪贴板获取文本"""
        return pyperclip.paste()

    def copy_image(self, image_path: str):
        """将图片以 Base64 编码复制到剪贴板"""
        image = Image.open(image_path)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        pyperclip.copy(img_str)

    def clear(self):
        """清空剪贴板"""
        pyperclip.copy("")

    def has_text(self) -> bool:
        """判断剪贴板是否包含文本"""
        text = pyperclip.paste()
        return text is not None and len(text) > 0