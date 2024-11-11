from PIL import Image
import mss
import ddddocr
import io

class ScreenTextRecognizer:
    def __init__(self):
        # 初始化 ddddocr 模块，并禁用广告
        self.ocr = ddddocr.DdddOcr(show_ad=False)

    def capture_and_recognize(self, x, y, width, height):
        # 使用 mss 截取指定区域的屏幕
        with mss.mss() as sct:
            monitor = {
                "top": y,
                "left": x,
                "width": width,
                "height": height
            }
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        # 将截图保存为 PNG 格式的字节流
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()
        
        # 使用 ddddocr 识别截图内容
        result = self.ocr.classification(img_bytes)
        
        return result
