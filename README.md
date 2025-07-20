# Tracking Number Maker | 跟踪号生成器

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

A flexible label generator for creating tracking labels for postcards and other items. The generator supports:

- Single label generation with customizable size
- Full sheet label generation with dynamic layout calculation
- Support for any paper size (A4, B5, custom sizes, etc.)
- QR code generation
- Configurable DPI for output images
- CJK text support

### Features

- Dynamically calculates the number of labels that can fit on a sheet based on paper size
- Configurable paper size, label size, margins, and spacing
- Supports both single label and full sheet generation
- Configurable DPI for output images
- Supports QR codes and text on labels

### Configuration

All configuration is done through JSON files using dot notation. Example configurations are provided:

- `config.json` - A4 paper configuration
- `config_b5.json` - B5 paper configuration
- `config_small.json` - Small 4cm x 6cm sheet configuration

You can create your own configuration files for different paper sizes and label layouts.

### Usage

```python
from label_generator import LabelGenerator

# Initialize with a configuration file
generator = LabelGenerator("config.json")

# Generate a single label
label = generator.create_label("明信片", "TRACK-001")
label.save("single_label.png")

# Generate a full sheet of labels
sheet = generator.generate_sheet(text="明信片", qr_prefix="TRACK")
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

---

<a name="chinese"></a>
## 中文

一个灵活的标签生成器，用于为明信片和其他物品创建跟踪标签。生成器支持：

- 可自定义尺寸的单个标签生成
- 动态计算布局的整页标签生成
- 支持任何纸张尺寸（A4、B5、自定义尺寸等）
- 二维码生成
- 可配置的输出图像DPI
- 支持中日韩文字

### 功能特点

- 根据纸张尺寸动态计算一张纸上可以放置的标签数量
- 可配置的纸张尺寸、标签尺寸、边距和间距
- 支持单个标签和整页标签生成
- 可配置的输出图像DPI
- 支持二维码和文本标签

### 配置

所有配置通过使用点表示法的JSON文件完成。提供了示例配置：

- `config.json` - A4纸张配置
- `config_b5.json` - B5纸张配置
- `config_small.json` - 小尺寸4cm x 6cm纸张配置

您可以为不同的纸张尺寸和标签布局创建自己的配置文件。

### 使用方法

```python
from label_generator import LabelGenerator

# 使用配置文件初始化
generator = LabelGenerator("config.json")

# 生成单个标签
label = generator.create_label("明信片", "TRACK-001")
label.save("single_label.png")

# 生成整页标签
sheet = generator.generate_sheet(text="明信片", qr_prefix="TRACK")
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
