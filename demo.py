#!/usr/bin/env python3
"""
演示如何使用标签生成器生成不同尺寸的标签和标签页
"""

from label_generator import LabelGenerator
import os

def main():
    # 确保输出目录存在
    os.makedirs("dist", exist_ok=True)
    
    # 演示A4纸张
    print("=== 使用A4纸张 ===")
    generator_a4 = LabelGenerator("config.json")
    cols, rows = generator_a4.calculate_layout()
    print(f"纸张尺寸: {generator_a4.cfg['paper.width']}mm x {generator_a4.cfg['paper.height']}mm")
    print(f"标签尺寸: {generator_a4.cfg['label.width']}mm x {generator_a4.cfg['label.height']}mm")
    print(f"每页可放置标签: {cols} 列 x {rows} 行 = {cols * rows} 个")
    
    # 生成单个标签
    label_a4 = generator_a4.create_label("明信片", "TRACK-A4-001")
    label_a4.save("dist/a4_single_label.png")
    
    # 生成标签页
    sheet_a4 = generator_a4.generate_sheet(text="明信片", qr_prefix="TRACK-A4")
    sheet_a4.save("dist/a4_sheet.png")
    
    # 演示B5纸张
    print("\n=== 使用B5纸张 ===")
    generator_b5 = LabelGenerator("config_b5.json")
    cols, rows = generator_b5.calculate_layout()
    print(f"纸张尺寸: {generator_b5.cfg['paper.width']}mm x {generator_b5.cfg['paper.height']}mm")
    print(f"标签尺寸: {generator_b5.cfg['label.width']}mm x {generator_b5.cfg['label.height']}mm")
    print(f"每页可放置标签: {cols} 列 x {rows} 行 = {cols * rows} 个")
    
    # 生成单个标签
    label_b5 = generator_b5.create_label("明信片", "TRACK-B5-001")
    label_b5.save("dist/b5_single_label.png")
    
    # 生成标签页
    sheet_b5 = generator_b5.generate_sheet(text="明信片", qr_prefix="TRACK-B5")
    sheet_b5.save("dist/b5_sheet.png")
    
    # 演示小尺寸纸张
    print("\n=== 使用小尺寸纸张 ===")
    generator_small = LabelGenerator("config_small.json")
    cols, rows = generator_small.calculate_layout()
    print(f"纸张尺寸: {generator_small.cfg['paper.width']}mm x {generator_small.cfg['paper.height']}mm")
    print(f"标签尺寸: {generator_small.cfg['label.width']}mm x {generator_small.cfg['label.height']}mm")
    print(f"每页可放置标签: {cols} 列 x {rows} 行 = {cols * rows} 个")
    
    # 生成单个标签
    label_small = generator_small.create_label("明信片", "TRACK-S-001")
    label_small.save("dist/small_single_label.png")
    
    # 生成标签页
    sheet_small = generator_small.generate_sheet(text="明信片", qr_prefix="TRACK-S")
    sheet_small.save("dist/small_sheet.png")
    
    print("\n所有标签和标签页已生成到dist目录")

if __name__ == "__main__":
    main()