
from PIL import Image, ImageDraw, ImageFont
import qrcode

class LabelGenerator:
    def __init__(self, width=100, height=50, dpi=300):
        """初始化标签生成器
        :param width: 标签宽度(mm)
        :param height: 标签高度(mm) 
        :param dpi: 输出分辨率
        """
        self.width = width
        self.height = height
        self.dpi = dpi
        self.mm_to_px = dpi / 25.4  # 毫米转像素系数

    def mm_to_pixels(self, mm):
        """毫米转像素"""
        return int(mm * self.mm_to_px)

    def create_single_label(self, text="明信片"):
        """创建单个标签"""
        img = Image.new('L', (self.mm_to_pixels(self.width), 
                            self.mm_to_pixels(self.height)), 255)
        draw = ImageDraw.Draw(img)
        
        # 添加文字
        font = ImageFont.load_default()
        draw.text((10, 10), text, font=font, fill=0)
        
        return img

if __name__ == "__main__":
    generator = LabelGenerator()
    label = generator.create_single_label()
    label.save("single_label.png")
