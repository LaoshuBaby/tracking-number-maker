# Tracking Number Maker | 跟踪号生成器

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

A flexible label generator for creating tracking labels for postcards and other items. The generator supports:

- Single label generation with customizable size
- Full sheet label generation with dynamic layout calculation
- Support for any paper size (A4, B5, custom sizes, etc.)
- QR code and barcode generation
- Automatic tracking number generation
- Configurable DPI for output images
- CJK text support with proper font handling

### Features

- Dynamically calculates the number of labels that can fit on a sheet based on paper size
- Configurable paper size, label size, margins, and spacing
- Supports both single label and full sheet generation
- Configurable DPI for output images
- Supports QR codes, barcodes, and CJK text on labels
- Professional label layout with proper spacing and alignment
- Automatic tracking number generation with random numbers
- Robust font handling for Chinese, Japanese, and Korean text

### Configuration

All configuration is done through JSON files using dot notation. Example configurations are provided:

- `config.json` - A4 paper configuration
- `config_b5.json` - B5 paper configuration
- `config_small.json` - Small 4cm x 6cm sheet configuration

You can create your own configuration files for different paper sizes and label layouts.

### Label Layout

Each label features a professional layout with:

- **Top-left**: Description text (e.g., "明信片条码")
- **Bottom-left**: Tracking number (e.g., "TN12345678")
- **Right side**: QR code containing the tracking number
- **Center**: Vertical separator line
- **Bottom**: Barcode spanning the full width

### Usage

```python
from label_generator import LabelGenerator

# Initialize with a configuration file
generator = LabelGenerator("config.json")

# Generate a single label with custom tracking number
label = generator.create_label("明信片条码", tracking_number="TN12345678")
label.save("single_label.png")

# Generate a full sheet of labels with automatic tracking numbers
sheet = generator.generate_sheet(text="明信片条码", qr_prefix="TRACK")
sheet.save("label_sheet.png")
```

Run the demo script to see examples with different paper sizes:

```bash
python demo.py
```

To clean the output directory:

```bash
python clean.py
```

### Requirements

- Python 3.6+
- Pillow
- qrcode
- python-barcode

---

<a name="chinese"></a>
## 中文

一个灵活的标签生成器，用于为明信片和其他物品创建跟踪标签。生成器支持：

- 可自定义尺寸的单个标签生成
- 动态计算布局的整页标签生成
- 支持任何纸张尺寸（A4、B5、自定义尺寸等）
- 二维码和条形码生成
- 自动跟踪号生成
- 可配置的输出图像DPI
- 支持中日韩文字并正确处理字体

### 功能特点

- 根据纸张尺寸动态计算一张纸上可以放置的标签数量
- 可配置的纸张尺寸、标签尺寸、边距和间距
- 支持单个标签和整页标签生成
- 可配置的输出图像DPI
- 支持二维码、条形码和中日韩文字标签
- 专业的标签布局，具有适当的间距和对齐
- 自动生成随机跟踪号
- 强大的中文、日文和韩文字体处理

### 配置

所有配置通过使用点表示法的JSON文件完成。提供了示例配置：

- `config.json` - A4纸张配置
- `config_b5.json` - B5纸张配置
- `config_small.json` - 小尺寸4cm x 6cm纸张配置

您可以为不同的纸张尺寸和标签布局创建自己的配置文件。

### 标签布局

每个标签都具有专业的布局设计：

- **左上角**：说明文字（如"明信片条码"）
- **左下角**：跟踪号（如"TN12345678"）
- **右侧**：包含跟踪号的二维码
- **中间**：垂直分隔线
- **底部**：横跨整个宽度的条形码

### 使用方法

```python
from label_generator import LabelGenerator

# 使用配置文件初始化
generator = LabelGenerator("config.json")

# 生成带自定义跟踪号的单个标签
label = generator.create_label("明信片条码", tracking_number="TN12345678")
label.save("single_label.png")

# 生成带自动跟踪号的整页标签
sheet = generator.generate_sheet(text="明信片条码", qr_prefix="TRACK")
sheet.save("label_sheet.png")
```

运行演示脚本查看不同纸张尺寸的示例：

```bash
python demo.py
```

清理输出目录：

```bash
python clean.py
```

### 依赖要求

- Python 3.6+
- Pillow
- qrcode
- python-barcode
