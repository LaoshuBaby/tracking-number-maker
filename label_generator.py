import qrcode
from PIL import Image, ImageDraw, ImageFont
import json
import os
import math

class LabelGenerator:
    def __init__(self, config_file="config.json"):
        with open(config_file) as f:
            self.cfg = json.load(f)
        
        # 单位转换
        self.mm_to_px = self.cfg["dpi"] / 25.4
        self.scale = 10 if self.cfg["unit"] == "cm" else 1
        
        # 创建输出目录
        os.makedirs("dist", exist_ok=True)

    def mm_to_pixels(self, mm):
        return int(mm * self.scale * self.mm_to_px)

    def create_label(self, text="明信片", qr_data=None):
        """生成单个标签"""
        # 计算画布尺寸（含出血）
        width = self.mm_to_pixels(
            self.cfg["label"]["width"] + 2*self.cfg["label"]["bleed"]
        )
        height = self.mm_to_pixels(
            self.cfg["label"]["height"] + 2*self.cfg["label"]["bleed"]
        )
        
        img = Image.new("L", (width, height), 255)
        draw = ImageDraw.Draw(img)
        
        # 绘制标签框（含圆角）
        bleed_px = self.mm_to_pixels(self.cfg["label"]["bleed"])
        box = [
            bleed_px, bleed_px,
            width - bleed_px,
            height - bleed_px
        ]
        self._draw_rounded_rect(draw, box, self.cfg["label"]["corner_radius"])
        
        # 添加文字
        font = self._load_font()
        text_x = bleed_px + self.mm_to_pixels(self.cfg["label"]["padding"])
        text_y = bleed_px + self.mm_to_pixels(self.cfg["label"]["padding"])
        draw.text((text_x, text_y), text, font=font, fill=0)
        
        # 添加二维码（如有）
        if qr_data:
            self._add_qr_code(img, qr_data)
        
        return img

    def generate_sheet(self, labels):
        """生成整张标签页"""
        # 计算标签排列
        label_w = self.mm_to_pixels(self.cfg["label"]["width"] + 2*self.cfg["paper"]["gap"])
        label_h = self.mm_to_pixels(self.cfg["label"]["height"] + 2*self.cfg["paper"]["gap"])
        
        cols = math.floor(
            (self.cfg["paper"]["width"] - 2*self.cfg["paper"]["margin"]) / 
            (self.cfg["label"]["width"] + self.cfg["paper"]["gap"])
        )
        rows = math.floor(
            (self.cfg["paper"]["height"] - 2*self.cfg["paper"]["margin"]) /
            (self.cfg["label"]["height"] + self.cfg["paper"]["gap"])
        )
        
        # 创建画布
        sheet = Image.new(
            "L",
            (
                self.mm_to_pixels(self.cfg["paper"]["width"]),
                self.mm_to_pixels(self.cfg["paper"]["height"])
            ),
            255
        )
        
        # 排列标签
        for i, label in enumerate(labels):
            x = i % cols
            y = i // cols
            if y >= rows:
                break
                
            pos_x = self.mm_to_pixels(self.cfg["paper"]["margin"] + x*(label_w + self.cfg["paper"]["gap"]))
            pos_y = self.mm_to_pixels(self.cfg["paper"]["margin"] + y*(label_h + self.cfg["paper"]["gap"]))
            
            sheet.paste(label, (pos_x, pos_y))
        
        return sheet

    def _add_qr_code(self, img, data):
        """添加二维码到标签"""
        qr_size = self.mm_to_pixels(self.cfg["qr"]["size"])
        qr = qrcode.QRCode(version=1, box_size=3, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((qr_size, qr_size))
        
        # 定位二维码
        x = img.width - self.mm_to_pixels(self.cfg["label"]["bleed"] + self.cfg["qr"]["padding"] + self.cfg["qr"]["size"])
        y = self.mm_to_pixels(self.cfg["label"]["bleed"] + self.cfg["qr"]["padding"])
        img.paste(qr_img, (x, y))

    def _draw_rounded_rect(self, draw, box, radius_mm):
        """绘制圆角矩形"""
        radius = self.mm_to_pixels(radius_mm)
        # 实现细节...
        
    def _load_font(self):
        """加载字体"""
        try:
            return ImageFont.truetype(
                self.cfg["font"]["path"],
                self.mm_to_pixels(self.cfg["font"]["size"])
            )
        except:
            return ImageFont.load_default()

if __name__ == "__main__":
    generator = LabelGenerator()
    
    # 生成测试标签
    label = generator.create_label("测试标签", "https://example.com")
    label.save("dist/single_label.png")
    
    # 生成测试标签页
    labels = [generator.create_label(f"标签{i}") for i in range(1, 9)]
    sheet = generator.generate_sheet(labels)
    sheet.save("dist/label_sheet.png")
