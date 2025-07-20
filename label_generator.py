
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
        """创建单个标签
        :param text: 标签文字内容
        :return: PIL.Image对象
        """
        img = Image.new('L', (self.mm_to_pixels(self.width), 
                            self.mm_to_pixels(self.height)), 255)
        draw = ImageDraw.Draw(img)
        
        # 添加文字
        try:
            font = ImageFont.truetype("NotoSansCJK-Regular.ttc", 20)
        except:
            font = ImageFont.load_default()
        draw.text((10, 10), text, font=font, fill=0)
        
        return img

    def create_a4_sheet(self, cols=4, rows=8, text="明信片"):
        """创建A4纸大小的标签页
        :param cols: 每行标签数
        :param rows: 每列标签数
        :return: PIL.Image对象
        """
        a4_width = 210  # A4宽度(mm)
        a4_height = 297  # A4高度(mm)
        sheet = Image.new('L', (self.mm_to_pixels(a4_width),
                              self.mm_to_pixels(a4_height)), 255)
        
        for row in range(rows):
            for col in range(cols):
                label = self.create_single_label(text)
                x = col * self.mm_to_pixels(self.width)
                y = row * self.mm_to_pixels(self.height)
                sheet.paste(label, (x, y))
        
        return sheet

if __name__ == "__main__":
    generator = LabelGenerator(width=50, height=30, dpi=300)
    
    # 生成单标签
    label = generator.create_single_label("明信片")
    label.save("single_label.png")
    
    # 生成A4标签页
    a4_sheet = generator.create_a4_sheet(cols=4, rows=8, text="明信片")
    a4_sheet.save("a4_sheet.png")
