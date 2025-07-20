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
        """将毫米转换为像素"""
        return int(mm * self.scale * self.mm_to_px)

    def create_label(self, text="明信片", qr_data=None):
        """生成单个标签
        
        Args:
            text: 标签上显示的文字
            qr_data: 二维码数据，如果为None则不生成二维码
            
        Returns:
            PIL.Image: 生成的标签图像
        """
        # 计算画布尺寸（含出血）
        width = self.mm_to_pixels(
            self.cfg["label.width"] + 2*self.cfg["label.bleed"]
        )
        height = self.mm_to_pixels(
            self.cfg["label.height"] + 2*self.cfg["label.bleed"]
        )
        
        img = Image.new("L", (width, height), 255)
        draw = ImageDraw.Draw(img)
        
        # 绘制标签框（含圆角）
        bleed_px = self.mm_to_pixels(self.cfg["label.bleed"])
        box = [
            bleed_px, bleed_px,
            width - bleed_px,
            height - bleed_px
        ]
        self._draw_rounded_rect(draw, box, self.cfg["label.corner_radius"])
        
        # 添加文字
        font = self._load_font()
        text_x = bleed_px + self.mm_to_pixels(self.cfg["label.padding"])
        text_y = bleed_px + self.mm_to_pixels(self.cfg["label.padding"])
        draw.text((text_x, text_y), text, font=font, fill=0)
        
        # 添加二维码（如有）
        if qr_data:
            self._add_qr_code(img, qr_data)
        
        return img

    def calculate_layout(self):
        """计算纸张上可以放置的标签数量和排列
        
        Returns:
            tuple: (列数, 行数) - 纸张上可以放置的标签列数和行数
        """
        # 计算标签实际尺寸（含间隙）
        label_width = self.cfg["label.width"] + self.cfg["paper.gap"]
        label_height = self.cfg["label.height"] + self.cfg["paper.gap"]
        
        # 计算可用区域
        available_width = self.cfg["paper.width"] - 2 * self.cfg["paper.margin"]
        available_height = self.cfg["paper.height"] - 2 * self.cfg["paper.margin"]
        
        # 计算可以放置的标签数量
        cols = math.floor(available_width / label_width)
        rows = math.floor(available_height / label_height)
        
        return (cols, rows)

    def generate_sheet(self, labels=None, text="明信片", qr_data=None, qr_prefix=None):
        """生成整张标签页
        
        Args:
            labels: 预先生成的标签列表，如果为None则自动生成
            text: 标签上显示的文字，仅当labels为None时使用
            qr_data: 二维码数据，如果为None则不生成二维码
            qr_prefix: 二维码前缀，如果提供则会为每个标签生成序号化的二维码
            
        Returns:
            PIL.Image: 生成的标签页图像
        """
        # 计算标签排列
        cols, rows = self.calculate_layout()
        total_labels = cols * rows
        
        # 如果没有提供标签，则自动生成
        if labels is None:
            labels = []
            for i in range(total_labels):
                # 如果提供了二维码前缀，则为每个标签生成序号化的二维码
                current_qr = None
                if qr_prefix:
                    current_qr = f"{qr_prefix}-{i+1}"
                elif qr_data:
                    current_qr = qr_data
                
                labels.append(self.create_label(text, current_qr))
        
        # 创建画布
        sheet = Image.new(
            "L",
            (
                self.mm_to_pixels(self.cfg["paper.width"]),
                self.mm_to_pixels(self.cfg["paper.height"])
            ),
            255
        )
        
        # 排列标签
        for i, label in enumerate(labels):
            if i >= total_labels:
                break
                
            x = i % cols
            y = i // cols
            
            # 计算标签位置
            pos_x = self.mm_to_pixels(self.cfg["paper.margin"] + x * (self.cfg["label.width"] + self.cfg["paper.gap"]))
            pos_y = self.mm_to_pixels(self.cfg["paper.margin"] + y * (self.cfg["label.height"] + self.cfg["paper.gap"]))
            
            sheet.paste(label, (pos_x, pos_y))
        
        return sheet

    def _add_qr_code(self, img, data):
        """添加二维码到标签"""
        qr_size = self.mm_to_pixels(self.cfg["qr.size"])
        qr = qrcode.QRCode(version=1, box_size=3, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((qr_size, qr_size))
        
        # 定位二维码
        x = img.width - self.mm_to_pixels(self.cfg["label.bleed"] + self.cfg["qr.padding"] + self.cfg["qr.size"])
        y = self.mm_to_pixels(self.cfg["label.bleed"] + self.cfg["qr.padding"])
        img.paste(qr_img, (x, y))

    def _draw_rounded_rect(self, draw, box, radius_mm):
        """绘制圆角矩形"""
        radius = self.mm_to_pixels(radius_mm)
        
        # 绘制四个角的圆弧
        draw.arc([box[0], box[1], box[0]+radius*2, box[1]+radius*2], 180, 270, 0)
        draw.arc([box[2]-radius*2, box[1], box[2], box[1]+radius*2], 270, 360, 0)
        draw.arc([box[2]-radius*2, box[3]-radius*2, box[2], box[3]], 0, 90, 0)
        draw.arc([box[0], box[3]-radius*2, box[0]+radius*2, box[3]], 90, 180, 0)
        
        # 绘制四条边
        draw.line([(box[0]+radius, box[1]), (box[2]-radius, box[1])], 0)
        draw.line([(box[2], box[1]+radius), (box[2], box[3]-radius)], 0)
        draw.line([(box[0]+radius, box[3]), (box[2]-radius, box[3])], 0)
        draw.line([(box[0], box[1]+radius), (box[0], box[3]-radius)], 0)
        
    def _load_font(self):
        """加载字体"""
        try:
            return ImageFont.truetype(
                self.cfg["font.path"],
                self.mm_to_pixels(self.cfg["font.size"])
            )
        except:
            return ImageFont.load_default()

if __name__ == "__main__":
    print("请运行 demo.py 来查看示例 | Please run demo.py to see examples")
    print("python demo.py")
