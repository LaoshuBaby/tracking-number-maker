#!/usr/bin/env python3
"""
清理脚本 - 清空dist目录中的所有文件
Cleanup script - Clear all files in the dist directory
"""

import os
import shutil

def clean_dist():
    """
    清空dist目录中的所有文件，但保留目录本身
    Clear all files in the dist directory while keeping the directory itself
    """
    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
    
    # 检查dist目录是否存在
    # Check if dist directory exists
    if not os.path.exists(dist_dir):
        print("dist目录不存在，创建新目录")
        print("dist directory does not exist, creating a new one")
        os.makedirs(dist_dir)
        return
    
    # 删除dist目录中的所有文件
    # Delete all files in the dist directory
    for filename in os.listdir(dist_dir):
        file_path = os.path.join(dist_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"删除文件时出错: {e}")
            print(f"Error deleting file: {e}")
    
    print("dist目录已清空")
    print("dist directory has been cleared")

if __name__ == "__main__":
    clean_dist()