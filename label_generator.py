import qrcode
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import json
import os
import math
import random
import io

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

    def create_label(self, text="明信片条码", qr_data=None, tracking_number=None):
        """生成单个标签
        
        Args:
            text: 标签上显示的文字
            qr_data: 二维码数据，如果为None则不生成二维码
            tracking_number: 跟踪号，如果为None则随机生成
            
        Returns:
            PIL.Image: 生成的标签图像
        """
        # 如果没有提供跟踪号，则生成一个随机跟踪号
        if tracking_number is None:
            tracking_number = f"TN{random.randint(10000000, 99999999)}"
        
        # 如果没有提供二维码数据，则使用跟踪号
        if qr_data is None:
            qr_data = tracking_number
            
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
        padding_px = self.mm_to_pixels(self.cfg["label.padding"])
        
        box = [
            bleed_px, bleed_px,
            width - bleed_px,
            height - bleed_px
        ]
        self._draw_rounded_rect(draw, box, self.cfg["label.corner_radius"])
        
        # 计算内容区域
        content_left = bleed_px + padding_px
        content_top = bleed_px + padding_px
        content_right = width - bleed_px - padding_px
        content_bottom = height - bleed_px - padding_px
        content_width = content_right - content_left
        content_height = content_bottom - content_top
        
        # 加载字体
        font = self._load_font()
        small_font = self._load_font(size_factor=0.7)
        
        # 计算二维码尺寸和位置（右侧）
        qr_size = min(self.mm_to_pixels(self.cfg["qr.size"]), content_height // 2)
        qr_x = content_right - qr_size
        qr_y = content_top
        
        # 计算分隔线位置
        separator_x = qr_x - self.mm_to_pixels(2)
        
        # 左上角：标题文字
        draw.text((content_left, content_top), text, font=font, fill=0)
        
        # 左下角：编号（在条形码上方）
        barcode_height = self.mm_to_pixels(10)  # 条形码高度
        number_y = content_bottom - barcode_height - self.mm_to_pixels(1)
        draw.text((content_left, number_y), tracking_number, font=small_font, fill=0)
        
        # 绘制分隔线
        line_top = content_top + self.mm_to_pixels(self.cfg["font.size"]) + self.mm_to_pixels(1)
        line_bottom = content_bottom - barcode_height - self.mm_to_pixels(1)
        draw.line([(separator_x, line_top), (separator_x, line_bottom)], fill=0, width=1)
        
        # 添加二维码（右侧）
        self._add_qr_code_at_position(img, qr_data, qr_x, qr_y, qr_size)
        
        # 添加条形码（底部，横跨整个宽度）
        self._add_barcode_bottom(img, tracking_number)
        
        return img
        
    def _add_barcode(self, img, data):
        """添加条形码到标签"""
        # 确保数据符合条形码要求（只包含数字）
        if not isinstance(data, str):
            data = str(data)
        
        # 如果数据包含非数字字符，则只保留数字
        numeric_data = ''.join(filter(str.isdigit, data))
        if len(numeric_data) < 8:  # 确保至少有8位数字
            numeric_data = numeric_data.zfill(8)
        
        # 生成条形码
        barcode_class = barcode.get_barcode_class('code128')
        barcode_writer = ImageWriter()
        barcode_writer.dpi = self.cfg["dpi"]
        
        # 设置条形码尺寸
        barcode_width = self.mm_to_pixels(self.cfg["label.width"] * 0.8)
        barcode_height = self.mm_to_pixels(10)  # 10mm高度
        
        # 生成条形码图像
        barcode_obj = barcode_class(data, writer=barcode_writer)
        barcode_bytes = io.BytesIO()
        barcode_obj.write(barcode_bytes)
        barcode_img = Image.open(barcode_bytes)
        
        # 调整条形码尺寸
        barcode_img = barcode_img.resize((barcode_width, barcode_height))
        
        # 定位条形码（放在标签底部）
        bleed_px = self.mm_to_pixels(self.cfg["label.bleed"])
        padding_px = self.mm_to_pixels(self.cfg["label.padding"])
        x = bleed_px + padding_px
        y = img.height - bleed_px - padding_px - barcode_height
        
        # 粘贴条形码
        img.paste(barcode_img, (x, y))
        
    def _add_qr_code_at_position(self, img, data, x, y, size):
        """在指定位置添加二维码"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((size, size))
        
        # 粘贴二维码
        img.paste(qr_img, (x, y))
        
    def _add_barcode_bottom(self, img, data):
        """在标签底部添加条形码"""
        # 确保数据符合条形码要求
        if not isinstance(data, str):
            data = str(data)
        
        # 生成条形码
        try:
            barcode_class = barcode.get_barcode_class('code128')
            barcode_writer = ImageWriter()
            
            # 生成条形码图像
            barcode_obj = barcode_class(data, writer=barcode_writer)
            barcode_bytes = io.BytesIO()
            barcode_obj.write(barcode_bytes, options={
                'module_height': 8.0,  # 条形码高度（mm）
                'module_width': 0.2,   # 条形码宽度（mm）
                'quiet_zone': 1.0,     # 静默区（mm）
                'font_size': 8,        # 字体大小
                'text_distance': 1.0,  # 文字距离（mm）
                'background': 'white',
                'foreground': 'black',
                'write_text': True,
                'text': data
            })
            barcode_img = Image.open(barcode_bytes)
            
            # 计算条形码位置（底部居中）
            bleed_px = self.mm_to_pixels(self.cfg["label.bleed"])
            padding_px = self.mm_to_pixels(self.cfg["label.padding"])
            
            # 调整条形码尺寸以适应标签宽度
            available_width = img.width - 2 * (bleed_px + padding_px)
            barcode_height = self.mm_to_pixels(8)
            
            # 保持宽高比调整尺寸
            original_ratio = barcode_img.width / barcode_img.height
            if barcode_img.width > available_width:
                new_width = available_width
                new_height = int(new_width / original_ratio)
            else:
                new_width = barcode_img.width
                new_height = barcode_img.height
            
            # 确保高度不超过限制
            if new_height > barcode_height:
                new_height = barcode_height
                new_width = int(new_height * original_ratio)
            
            barcode_img = barcode_img.resize((new_width, new_height))
            
            # 计算居中位置
            x = (img.width - new_width) // 2
            y = img.height - bleed_px - padding_px - new_height
            
            # 粘贴条形码
            img.paste(barcode_img, (x, y))
            
        except Exception as e:
            print(f"条形码生成失败: {e}")
            # 如果条形码生成失败，至少显示文字
            draw = ImageDraw.Draw(img)
            font = self._load_font(size_factor=0.6)
            bleed_px = self.mm_to_pixels(self.cfg["label.bleed"])
            padding_px = self.mm_to_pixels(self.cfg["label.padding"])
            x = bleed_px + padding_px
            y = img.height - bleed_px - padding_px - self.mm_to_pixels(4)
            draw.text((x, y), data, font=font, fill=0)

    def calculate_layout(self):
        """计算纸张上可以放置的标签数量和排列
        
        Returns:
            tuple: (列数, 行数) - 纸张上可以放置的标签列数和行数
        """
        # 计算标签实际尺寸（含出血和间隙）
        label_width = self.cfg["label.width"] + 2 * self.cfg["label.bleed"] + self.cfg["paper.gap"]
        label_height = self.cfg["label.height"] + 2 * self.cfg["label.bleed"] + self.cfg["paper.gap"]
        
        # 计算可用区域
        available_width = self.cfg["paper.width"] - 2 * self.cfg["paper.margin"]
        available_height = self.cfg["paper.height"] - 2 * self.cfg["paper.margin"]
        
        # 计算可以放置的标签数量
        cols = math.floor(available_width / label_width)
        rows = math.floor(available_height / label_height)
        
        return (cols, rows)

    def generate_sheet(self, labels=None, text="明信片条码", qr_data=None, qr_prefix=None):
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
                # 生成跟踪号
                tracking_number = f"TN{random.randint(10000000, 99999999)}"
                
                # 如果提供了二维码前缀，则为每个标签生成序号化的二维码
                current_qr = None
                if qr_prefix:
                    current_qr = f"{qr_prefix}-{i+1}"
                elif qr_data:
                    current_qr = qr_data
                else:
                    current_qr = tracking_number
                
                labels.append(self.create_label(text, current_qr, tracking_number))
        
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
            
            # 计算标签位置（考虑出血和间隙）
            label_width_with_bleed = self.cfg["label.width"] + 2 * self.cfg["label.bleed"]
            label_height_with_bleed = self.cfg["label.height"] + 2 * self.cfg["label.bleed"]
            
            pos_x = self.mm_to_pixels(self.cfg["paper.margin"] + x * (label_width_with_bleed + self.cfg["paper.gap"]))
            pos_y = self.mm_to_pixels(self.cfg["paper.margin"] + y * (label_height_with_bleed + self.cfg["paper.gap"]))
            
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
        
    def _load_font(self, size_factor=1.0):
        """加载字体
        
        Args:
            size_factor: 字体大小的缩放因子
            
        Returns:
            PIL.ImageFont: 字体对象
        """
        font_size = int(self.mm_to_pixels(self.cfg["font.size"]) * size_factor)
        
        # 尝试加载配置中指定的字体
        try:
            return ImageFont.truetype(self.cfg["font.path"], font_size)
        except:
            pass
        
        # 尝试加载系统中的CJK字体
        cjk_fonts = [
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/unifont/unifont.otf",
            "/System/Library/Fonts/PingFang.ttc",  # macOS
            "/Windows/Fonts/msyh.ttc",  # Windows
            "DejaVu Sans"
        ]
        
        for font_path in cjk_fonts:
            try:
                return ImageFont.truetype(font_path, font_size)
            except:
                continue
        
        # 最后使用默认字体
        return ImageFont.load_default()

if __name__ == "__main__":
    print("请运行 demo.py 来查看示例 | Please run demo.py to see examples")
    print("python demo.py")
