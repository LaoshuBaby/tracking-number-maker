#!/usr/bin/env python3
"""
演示如何使用标签生成器生成不同尺寸的标签和标签页
Demo of how to use the label generator to create labels of different sizes
"""

from label_generator import LabelGenerator
import os

def main():
    # 确保输出目录存在
    # Ensure output directory exists
    os.makedirs("dist", exist_ok=True)
    
    # 演示A4纸张 - 生成整页标签
    # Demo A4 paper - Generate full sheet of labels
    print("=== 使用A4纸张生成整页标签 | Using A4 paper for full sheet ===")
    generator_a4 = LabelGenerator("config.json")
    cols, rows = generator_a4.calculate_layout()
    print(f"纸张尺寸 | Paper size: {generator_a4.cfg['paper.width']}mm x {generator_a4.cfg['paper.height']}mm")
    print(f"标签尺寸 | Label size: {generator_a4.cfg['label.width']}mm x {generator_a4.cfg['label.height']}mm")
    print(f"每页可放置标签 | Labels per sheet: {cols} 列 x {rows} 行 = {cols * rows} 个")
    
    # 生成标签页
    # Generate label sheet
    sheet_a4 = generator_a4.generate_sheet(text="明信片", qr_prefix="TRACK-A4")
    sheet_a4.save("dist/a4_sheet.png")
    print(f"A4标签页已保存到 | A4 sheet saved to: dist/a4_sheet.png")
    
    # 演示B5纸张 - 生成整页标签
    # Demo B5 paper - Generate full sheet of labels
    print("\n=== 使用B5纸张生成整页标签 | Using B5 paper for full sheet ===")
    generator_b5 = LabelGenerator("config_b5.json")
    cols, rows = generator_b5.calculate_layout()
    print(f"纸张尺寸 | Paper size: {generator_b5.cfg['paper.width']}mm x {generator_b5.cfg['paper.height']}mm")
    print(f"标签尺寸 | Label size: {generator_b5.cfg['label.width']}mm x {generator_b5.cfg['label.height']}mm")
    print(f"每页可放置标签 | Labels per sheet: {cols} 列 x {rows} 行 = {cols * rows} 个")
    
    # 生成标签页
    # Generate label sheet
    sheet_b5 = generator_b5.generate_sheet(text="明信片", qr_prefix="TRACK-B5")
    sheet_b5.save("dist/b5_sheet.png")
    print(f"B5标签页已保存到 | B5 sheet saved to: dist/b5_sheet.png")
    
    # 演示小尺寸纸张 - 生成单个标签
    # Demo small paper - Generate single label
    print("\n=== 使用小尺寸纸张生成单个标签 | Using small paper for single label ===")
    generator_small = LabelGenerator("config_small.json")
    print(f"纸张尺寸 | Paper size: {generator_small.cfg['paper.width']}mm x {generator_small.cfg['paper.height']}mm")
    print(f"标签尺寸 | Label size: {generator_small.cfg['label.width']}mm x {generator_small.cfg['label.height']}mm")
    
    # 生成单个标签
    # Generate single label
    label_small = generator_small.create_label("明信片", "TRACK-S-001")
    label_small.save("dist/single_label.png")
    print(f"单个标签已保存到 | Single label saved to: dist/single_label.png")
    
    print("\n所有标签和标签页已生成到dist目录 | All labels and sheets have been generated to the dist directory")

if __name__ == "__main__":
    main()