
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

    def create_single_label(self, text="明信片", qr_data=None):
        """创建单个标签
        :param text: 标签文字内容
        :param qr_data: 二维码数据(为空则不生成)
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
        
        # 添加二维码
        if qr_data:
            qr = qrcode.QRCode(
                version=1,
                box_size=3,
                border=2
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.resize((self.mm_to_pixels(15), self.mm_to_pixels(15)))
            img.paste(qr_img, (self.mm_to_pixels(self.width)-self.mm_to_pixels(18), 10))
        
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
    
    # 生成带二维码的单标签
    label_with_qr = generator.create_single_label(
        text="明信片",
        qr_data="TRACK123456789"
    )
    label_with_qr.save("label_with_qr.png")
    
    # 生成带二维码的A4标签页
    a4_sheet_with_qr = generator.create_a4_sheet(
        cols=4, 
        rows=8, 
        text="明信片"
    )
    a4_sheet_with_qr.save("a4_sheet_with_qr.png")
