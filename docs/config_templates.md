# Configuration Templates | 配置模板

This document provides configuration templates for different paper sizes.

本文档提供了不同纸张尺寸的配置模板。

## A4 Paper | A4纸张 (210mm × 297mm)

```json
{
    "label.width": 50,
    "label.height": 30,
    "label.corner_radius": 3,
    "label.bleed": 2,
    "label.padding": 5,
    
    "paper.width": 210,
    "paper.height": 297,
    "paper.margin": 5,
    "paper.gap": 2,
    
    "font.size": 4,
    "font.path": "NotoSansCJK-Regular.ttc",
    
    "qr.size": 15,
    "qr.padding": 3,
    
    "dpi": 300,
    "unit": "mm"
}
```

## B5 Paper | B5纸张 (176mm × 250mm)

```json
{
    "label.width": 50,
    "label.height": 30,
    "label.corner_radius": 3,
    "label.bleed": 2,
    "label.padding": 5,
    
    "paper.width": 176,
    "paper.height": 250,
    "paper.margin": 5,
    "paper.gap": 2,
    
    "font.size": 4,
    "font.path": "NotoSansCJK-Regular.ttc",
    
    "qr.size": 15,
    "qr.padding": 3,
    
    "dpi": 300,
    "unit": "mm"
}
```

## Small Card | 小卡片 (40mm × 60mm)

For printing a single label on a small card.

用于在小卡片上打印单个标签。

```json
{
    "label.width": 30,
    "label.height": 20,
    "label.corner_radius": 2,
    "label.bleed": 1,
    "label.padding": 3,
    
    "paper.width": 40,
    "paper.height": 60,
    "paper.margin": 3,
    "paper.gap": 1,
    
    "font.size": 3,
    "font.path": "NotoSansCJK-Regular.ttc",
    
    "qr.size": 10,
    "qr.padding": 2,
    
    "dpi": 300,
    "unit": "mm"
}
```

## Configuration Parameters | 配置参数

| Parameter | Description | 描述 |
|-----------|-------------|------|
| `label.width` | Width of the label in mm | 标签宽度（毫米） |
| `label.height` | Height of the label in mm | 标签高度（毫米） |
| `label.corner_radius` | Radius of the label corners in mm | 标签圆角半径（毫米） |
| `label.bleed` | Bleed area width in mm | 出血区域宽度（毫米） |
| `label.padding` | Inner padding of the label in mm | 标签内边距（毫米） |
| `paper.width` | Width of the paper in mm | 纸张宽度（毫米） |
| `paper.height` | Height of the paper in mm | 纸张高度（毫米） |
| `paper.margin` | Margin around the paper in mm | 纸张边距（毫米） |
| `paper.gap` | Gap between labels in mm | 标签之间的间距（毫米） |
| `font.size` | Font size in mm | 字体大小（毫米） |
| `font.path` | Path to the font file | 字体文件路径 |
| `qr.size` | Size of the QR code in mm | 二维码尺寸（毫米） |
| `qr.padding` | Padding around the QR code in mm | 二维码周围的边距（毫米） |
| `dpi` | Output resolution in dots per inch | 输出分辨率（每英寸点数） |
| `unit` | Unit of measurement (mm or cm) | 测量单位（毫米或厘米） |