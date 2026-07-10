import pyperclip
import base64
from io import BytesIO
from PIL import Image

class ClipboardOperations:
    def __init__(self):
        pass
    
    def copy_text(self, text: str):
        pyperclip.copy(text)
    
    def paste_text(self) -> str:
        return pyperclip.paste()
    
    def copy_image(self, image_path: str):
        image = Image.open(image_path)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        pyperclip.copy(img_str)
    
    def clear(self):
        pyperclip.copy("")
    
    def has_text(self) -> bool:
        text = pyperclip.paste()
        return text is not None and len(text) > 0