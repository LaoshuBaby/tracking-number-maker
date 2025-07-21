import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json
import os

class LabelGenerator:
    def __init__(self, config_file="config.json"):
        """初始化标签生成器
        :param config_file: 配置文件路径
        """
        with open(config_file) as f:
            self.config = json.load(f)
        
        # 使用配置中的DPI
        self.dpi = self.config["output_dpi"]
        self.mm_to_px = self.dpi / 25.4
        
        # 确保dist目录存在
        os.makedirs("dist", exist_ok=True)
        
        # 单位转换系数
        self.unit_scale = 1 if self.config["unit"] == "mm" else 10

    def mm_to_pixels(self, value):
        """将配置值转换为像素
        :param value: 配置值(毫米或厘米)
        :return: 像素值
        """
        return int(value * self.unit_scale * self.mm_to_px)

    def create_single_label(self, text="明信片", qr_data=None):
        """创建带框线和出血线的标签
        :param text: 标签文字内容
        :param qr_data: 二维码数据
        :return: PIL.Image对象
        """
        bleed_px = self.mm_to_pixels(self.config["bleed_width"])
        width_px = self.mm_to_pixels(
            self.config["label_width"] + self.config["bleed_width"]*2
        )
        height_px = self.mm_to_pixels(
            self.config["label_height"] + self.config["bleed_width"]*2
        )
        
        # 创建带出血的画布
        img = Image.new('L', (width_px, height_px), 255)
        draw = ImageDraw.Draw(img)
        
        # 绘制标签框线(带圆角)
        box = [
            bleed_px, bleed_px,
            width_px - bleed_px,
            height_px - bleed_px
        ]
        radius = self.mm_to_pixels(self.config["corner_radius"])
        self._draw_rounded_rectangle(draw, box, radius)
        
        # 添加文字
        font = self.load_font()
        text_x = bleed_px + self.mm_to_pixels(self.config["text_padding"])
        text_y = bleed_px + self.mm_to_pixels(self.config["text_padding"])
        draw.text((text_x, text_y), text, font=font, fill=0)
        
        # 添加二维码
        if qr_data:
            qr_size = self.mm_to_pixels(self.config["qr_size"])
            qr_padding = self.mm_to_pixels(self.config["qr_padding"])
            
            qr = qrcode.QRCode(
                version=1,
                box_size=3,
                border=2
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.resize((qr_size, qr_size))
            
            qr_x = width_px - bleed_px - qr_size - qr_padding
            qr_y = bleed_px + qr_padding
            img.paste(qr_img, (qr_x, qr_y))
        
        return img

    def _draw_rounded_rectangle(self, draw, box, radius):
        """绘制圆角矩形"""
        # 实现细节保持不变
        pass

    def load_font(self):
        """加载字体"""
        try:
            return ImageFont.truetype(
                self.config["font_path"],
                self.mm_to_pixels(self.config["font_size"])
            )
        except:
            return ImageFont.load_default()

    def create_a4_sheet(self, count=8, prefix="LABEL"):
        """创建A4标签页"""
        # 实现细节保持不变
        pass
