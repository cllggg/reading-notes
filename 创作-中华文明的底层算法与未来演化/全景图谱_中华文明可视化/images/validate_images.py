#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证已下载图片的质量
"""

from pathlib import Path
from PIL import Image
import os

IMAGE_DIR = Path(__file__).parent

def validate_all_images():
    """验证所有已下载的图片"""
    print("=" * 60)
    print("验证已下载图片质量")
    print("=" * 60)
    print()
    
    image_files = list(IMAGE_DIR.glob("*.jpg"))
    print(f"找到 {len(image_files)} 个图片文件")
    print()
    
    valid_count = 0
    invalid_count = 0
    
    for image_file in sorted(image_files):
        try:
            img = Image.open(image_file)
            img.verify()
            
            # 重新打开图片
            img = Image.open(image_file)
            width, height = img.size
            file_size = image_file.stat().st_size
            
            print(f"✓ {image_file.name}")
            print(f"  尺寸: {width}x{height}, 大小: {file_size/1024:.1f}KB")
            
            valid_count += 1
            
        except Exception as e:
            print(f"✗ {image_file.name}")
            print(f"  错误: {str(e)}")
            invalid_count += 1
    
    print()
    print("=" * 60)
    print(f"验证完成！")
    print(f"有效: {valid_count} 个")
    print(f"无效: {invalid_count} 个")
    print("=" * 60)

if __name__ == "__main__":
    validate_all_images()
